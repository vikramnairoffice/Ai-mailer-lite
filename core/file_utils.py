"""
CSV/JSON file operations, validation, and logging utilities
"""

import os
import json
import csv
import pandas as pd
import streamlit as st
from typing import Dict, Any, List, Optional, Union
import re
from datetime import datetime

def validate_email(email: str) -> bool:
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def load_smtp_from_json(uploaded_file) -> List[Dict[str, Any]]:
    """Load SMTP accounts from JSON file"""
    try:
        content = uploaded_file.read()
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        
        data = json.loads(content)
        
        if isinstance(data, list):
            smtp_accounts = data
        elif isinstance(data, dict):
            smtp_accounts = [data]
        else:
            return []
        
        # Validate SMTP accounts
        valid_accounts = []
        for account in smtp_accounts:
            if validate_smtp_account(account):
                valid_accounts.append(account)
        
        return valid_accounts
    except Exception as e:
        st.error(f"Error loading SMTP accounts: {str(e)}")
        return []

def load_smtp_from_csv(uploaded_file) -> List[Dict[str, Any]]:
    """Load SMTP accounts from CSV file"""
    try:
        df = pd.read_csv(uploaded_file)
        smtp_accounts = []
        
        for _, row in df.iterrows():
            account = {
                'email': str(row.get('email', '')),
                'smtp_server': 'smtp.gmail.com',  # Always Gmail
                'smtp_port': 587,  # Standard Gmail port
                'username': str(row.get('email', '')),  # Username same as email
                'password': str(row.get('password', ''))
            }
            
            if validate_smtp_account(account):
                smtp_accounts.append(account)
        
        return smtp_accounts
    except Exception as e:
        st.error(f"Error loading SMTP accounts: {str(e)}")
        return []

def validate_smtp_account(account: Dict[str, Any]) -> bool:
    """Validate SMTP account data"""
    required_fields = ['email', 'password']
    
    for field in required_fields:
        if field not in account or not account[field]:
            return False
    
    if not validate_email(account['email']):
        return False
    
    # Ensure Gmail settings are set
    account['smtp_server'] = 'smtp.gmail.com'
    account['smtp_port'] = 587
    account['username'] = account['email']
    
    return True

def load_leads_from_csv(uploaded_file) -> List[Dict[str, Any]]:
    """Load leads from CSV file"""
    try:
        df = pd.read_csv(uploaded_file)
        leads = []
        
        for _, row in df.iterrows():
            lead = {
                'email': str(row.get('email', '')),
                'firstname': str(row.get('firstname', 'there')),
                'lastname': str(row.get('lastname', '')),
                'company': str(row.get('company', 'your company')),
                'industry': str(row.get('industry', 'business'))
            }
            
            if validate_email(lead['email']):
                leads.append(lead)
        
        return leads
    except Exception as e:
        st.error(f"Error loading leads: {str(e)}")
        return []

def save_results_to_csv(results: List[Dict[str, Any]], filename: str = None) -> str:
    """Save results to CSV file"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"email_results_{timestamp}.csv"
    
    try:
        df = pd.DataFrame(results)
        df.to_csv(filename, index=False)
        return filename
    except Exception as e:
        st.error(f"Error saving results: {str(e)}")
        return ""

def log_activity(activity: str, details: Dict[str, Any] = None):
    """Log activity to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {activity}"
    
    if details:
        log_entry += f" - {json.dumps(details)}"
    
    try:
        with open("email_marketing.log", "a", encoding='utf-8') as f:
            f.write(log_entry + "\n")
    except Exception:
        pass

def validate_file_upload(uploaded_file, file_type: str) -> bool:
    """Validate uploaded file"""
    if not uploaded_file:
        return False
    
    filename = uploaded_file.name.lower()
    
    if file_type == 'csv' and not filename.endswith('.csv'):
        st.error("Please upload a CSV file")
        return False
    
    if file_type == 'json' and not filename.endswith('.json'):
        st.error("Please upload a JSON file")
        return False
    
    return True