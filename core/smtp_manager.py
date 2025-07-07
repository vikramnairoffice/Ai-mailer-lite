"""
SMTP account management and validation for Email Marketing System
"""

import smtplib
import streamlit as st
from typing import Dict, Any, List, Tuple
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

from .config import get_smtp_config
from .file_utils import validate_email, log_activity

def test_smtp_connection(account: Dict[str, Any]) -> Tuple[bool, str]:
    """Test SMTP connection for a single account"""
    try:
        server = smtplib.SMTP(account['smtp_server'], account['smtp_port'])
        server.starttls()
        server.login(account['username'], account['password'])
        server.quit()
        return True, "Connection successful"
    except smtplib.SMTPAuthenticationError:
        return False, "Authentication failed - check username/password"
    except smtplib.SMTPConnectError:
        return False, "Cannot connect to SMTP server"
    except smtplib.SMTPServerDisconnected:
        return False, "Server disconnected unexpectedly"
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def validate_smtp_accounts(accounts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Validate multiple SMTP accounts concurrently"""
    valid_accounts = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(test_smtp_connection, account): account 
                  for account in accounts}
        
        for future in as_completed(futures):
            account = futures[future]
            try:
                is_valid, message = future.result()
                account['status'] = 'valid' if is_valid else 'invalid'
                account['message'] = message
                
                if is_valid:
                    valid_accounts.append(account)
                    log_activity(f"SMTP validation successful: {account['email']}")
                else:
                    log_activity(f"SMTP validation failed: {account['email']} - {message}")
                    
            except Exception as e:
                account['status'] = 'error'
                account['message'] = f"Validation error: {str(e)}"
                log_activity(f"SMTP validation error: {account['email']} - {str(e)}")
    
    return valid_accounts

def auto_configure_smtp(email: str) -> Dict[str, Any]:
    """Auto-configure SMTP settings based on email domain"""
    config = get_smtp_config(email)
    return {
        'email': email,
        'smtp_server': config['server'],
        'smtp_port': config['port'],
        'username': email,
        'password': ''  # User needs to fill this
    }

def get_smtp_status_summary(accounts: List[Dict[str, Any]]) -> Dict[str, int]:
    """Get summary of SMTP account statuses"""
    summary = {'valid': 0, 'invalid': 0, 'error': 0, 'untested': 0}
    
    for account in accounts:
        status = account.get('status', 'untested')
        summary[status] = summary.get(status, 0) + 1
    
    return summary

def select_optimal_smtps(accounts: List[Dict[str, Any]], max_accounts: int = 10) -> List[Dict[str, Any]]:
    """Select optimal SMTP accounts for sending"""
    valid_accounts = [acc for acc in accounts if acc.get('status') == 'valid']
    
    if len(valid_accounts) <= max_accounts:
        return valid_accounts
    
    # Prioritize accounts with better performance (can be enhanced with scoring)
    return random.sample(valid_accounts, max_accounts)

def distribute_leads_across_smtps(leads: List[Dict[str, Any]], 
                                smtp_accounts: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Distribute leads evenly across SMTP accounts"""
    if not smtp_accounts:
        return {}
    
    distribution = {acc['email']: [] for acc in smtp_accounts}
    
    for i, lead in enumerate(leads):
        smtp_email = smtp_accounts[i % len(smtp_accounts)]['email']
        distribution[smtp_email].append(lead)
    
    return distribution

def get_smtp_limits(account: Dict[str, Any]) -> Dict[str, int]:
    """Get sending limits for SMTP account based on provider"""
    email_domain = account['email'].split('@')[1].lower()
    
    limits = {
        'gmail.com': {'hourly': 100, 'daily': 500},
        'yahoo.com': {'hourly': 50, 'daily': 300},
        'hotmail.com': {'hourly': 50, 'daily': 300},
        'outlook.com': {'hourly': 50, 'daily': 300},
        'live.com': {'hourly': 50, 'daily': 300},
    }
    
    return limits.get(email_domain, {'hourly': 50, 'daily': 300})

def check_smtp_rate_limit(account: Dict[str, Any], sent_count: int) -> bool:
    """Check if SMTP account has reached rate limit"""
    limits = get_smtp_limits(account)
    return sent_count < limits['hourly']

def format_smtp_for_display(account: Dict[str, Any]) -> str:
    """Format SMTP account for display"""
    status_emoji = {
        'valid': '✅',
        'invalid': '❌', 
        'error': '⚠️',
        'untested': '⏳'
    }
    
    status = account.get('status', 'untested')
    emoji = status_emoji.get(status, '❓')
    
    return f"{emoji} {account['email']} ({account['smtp_server']}:{account['smtp_port']})"

def prepare_smtp_for_sending(account: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare SMTP account data for sending process"""
    return {
        'email': account['email'],
        'smtp_server': account['smtp_server'],
        'smtp_port': account['smtp_port'],
        'username': account['username'],
        'password': account['password'],
        'sent_count': 0,
        'failed_count': 0,
        'last_send_time': None
    }