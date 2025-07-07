"""
Core email sending logic and threading for Email Marketing System
"""

import smtplib
import os
import time
import threading
import random
import streamlit as st
from typing import Dict, Any, List, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from .config import SENDER_NAMES, SUBJECT_LINES
from .file_utils import log_activity

def send_email_smtp(smtp_config: Dict[str, Any], lead: Dict[str, Any], 
                   subject: str, content: str, attachment_path: Optional[str] = None, 
                   delay: int = 60) -> bool:
    """Send email via SMTP"""
    try:
        server = smtplib.SMTP(smtp_config['smtp_server'], smtp_config['smtp_port'])
        server.starttls()
        server.login(smtp_config['username'], smtp_config['password'])
        
        msg = MIMEMultipart()
        
        # Randomize sender name
        sender_name = random.choice(SENDER_NAMES)
        msg['From'] = f"{sender_name} <{smtp_config['email']}>"
        msg['To'] = lead['email']
        
        # Randomize subject
        random_subject = random.choice(SUBJECT_LINES)
        msg['Subject'] = random_subject
        
        msg.attach(MIMEText(content, 'html'))
        
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as f:
                part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                msg.attach(part)
        
        server.send_message(msg)
        server.quit()
        
        time.sleep(delay)
        log_activity(f"Email sent successfully to {lead['email']} via {smtp_config['email']}")
        return True
        
    except Exception as e:
        log_activity(f"Email sending failed to {lead['email']} via {smtp_config['email']}: {str(e)}")
        return False

def send_emails_for_smtp(smtp_config: Dict[str, Any], leads: List[Dict[str, Any]], 
                        config: Dict[str, Any], progress_placeholder) -> int:
    """Send emails for one SMTP account with progress tracking"""
    sent_count = 0
    total_leads = len(leads)
    
    for i, lead in enumerate(leads):
        try:
            # Import content generation here to avoid circular imports
            from content.content_types import generate_content
            from integrations.attachment_generator import generate_attachment
            
            # Generate content
            content = generate_content(
                lead, 
                config['content_type'],
                config.get('personalization', True),
                config.get('phone_number'),
                config.get('phone_in_body', False),
                config.get('ai_enhance', False)
            )
            
            # Generate attachment if needed
            attachment_path = None
            if config.get('attachment_type') != 'none':
                attachment_path = generate_attachment(
                    lead, 
                    config.get('attachment_type'), 
                    config.get('phone_number')
                )
            
            # Send email
            success = send_email_smtp(
                smtp_config,
                lead,
                config.get('subject', 'Important Update'),
                content,
                attachment_path,
                config.get('delay', 60)
            )
            
            if success:
                sent_count += 1
            
            # Update progress
            progress = (i + 1) / total_leads
            progress_placeholder.progress(
                progress, 
                text=f"{smtp_config['email']}: {sent_count}/{total_leads}"
            )
            
        except Exception:
            continue
    
    return sent_count

def execute_email_campaign(smtp_accounts: List[Dict[str, Any]], 
                         leads: List[Dict[str, Any]], 
                         config: Dict[str, Any]) -> Dict[str, Any]:
    """Execute email campaign with multiple SMTP accounts"""
    emails_per_smtp = config.get('emails_per_smtp', 50)
    
    # Distribute leads across SMTP accounts
    lead_chunks = []
    for i, smtp_account in enumerate(smtp_accounts):
        start_idx = i * emails_per_smtp
        end_idx = min(start_idx + emails_per_smtp, len(leads))
        if start_idx < len(leads):
            lead_chunks.append(leads[start_idx:end_idx])
        else:
            lead_chunks.append([])
    
    # Start sending with threading
    threads = []
    for i, smtp_account in enumerate(smtp_accounts):
        placeholder = st.empty()
        thread = threading.Thread(
            target=send_emails_for_smtp,
            args=(smtp_account, lead_chunks[i], config, placeholder)
        )
        threads.append(thread)
        thread.start()
    
    # Wait for completion
    for thread in threads:
        thread.join()
    
    # Calculate results
    total_sent = sum(len(chunk) for chunk in lead_chunks)
    total_leads = len(leads)
    
    log_activity(f"Campaign completed: {total_sent}/{total_leads} emails sent")
    return {
        'total_leads': total_leads,
        'total_sent': total_sent,
        'success_rate': (total_sent / total_leads) * 100 if total_leads > 0 else 0
    }