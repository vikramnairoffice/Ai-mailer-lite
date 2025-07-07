"""
Configuration management and session state for Email Marketing System
"""

import streamlit as st
from typing import Dict, Any, List

# Initialize session state variables
def init_session_state():
    """Initialize all session state variables"""
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'smtp_accounts' not in st.session_state:
        st.session_state.smtp_accounts = []
    if 'leads' not in st.session_state:
        st.session_state.leads = []
    if 'config' not in st.session_state:
        st.session_state.config = {}
    if 'selected_smtps' not in st.session_state:
        st.session_state.selected_smtps = []
    if 'gmass_scores' not in st.session_state:
        st.session_state.gmass_scores = {}

# Sender name and subject randomization arrays
SENDER_NAMES = [
    'Alert Notification', 'Alert Update', 'Thanks', 'Renewal', 'Subscription', 
    'Activation', 'Notice', 'Confirmation', 'Alert Release', 'New Update Purchase',
    'New Update Confirmation', 'Maintenance Invoice', 'Purchase Notification',
    'Maintenance Confirmation', 'Purchase Confirmation', 'Purchase Invoice',
    'Immediately notify', 'Hello', 'Thank You', 'Thanks Again', 'Notify',
    'Notification', 'Support', 'Customer Service'
]

SUBJECT_LINES = [
    'Notice', 'Confirmation', 'Alert Release', 'New Update Purchase',
    'New Update Confirmation', 'Thank you for contribution', 'Thanks for your interest',
    'Maintenance Invoice', 'Purchase Notification', 'Maintenance Confirmation',
    'Purchase Confirmation', 'Purchase Invoice', 'Immediately notify', 'Alert',
    'Important Update', 'Action Required', 'Urgent Notice'
]

def get_smtp_config(email: str) -> Dict[str, Any]:
    """Auto-detect SMTP configuration based on email provider"""
    domain = email.split('@')[1].lower()
    
    smtp_configs = {
        'gmail.com': {'server': 'smtp.gmail.com', 'port': 587},
        'yahoo.com': {'server': 'smtp.mail.yahoo.com', 'port': 587},
        'hotmail.com': {'server': 'smtp.live.com', 'port': 587},
        'outlook.com': {'server': 'smtp.live.com', 'port': 587},
        'live.com': {'server': 'smtp.live.com', 'port': 587},
        'aol.com': {'server': 'smtp.aol.com', 'port': 587},
    }
    
    return smtp_configs.get(domain, {'server': 'smtp.gmail.com', 'port': 587})

def update_config(key: str, value: Any):
    """Update configuration in session state"""
    st.session_state.config[key] = value

def get_config(key: str, default: Any = None) -> Any:
    """Get configuration value from session state"""
    return st.session_state.config.get(key, default)

def reset_session_state():
    """Reset all session state variables"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_session_state()

def get_step() -> int:
    """Get current workflow step"""
    return st.session_state.step

def set_step(step: int):
    """Set current workflow step"""
    st.session_state.step = step

def get_smtp_accounts() -> List[Dict[str, Any]]:
    """Get SMTP accounts from session state"""
    return st.session_state.smtp_accounts

def set_smtp_accounts(accounts: List[Dict[str, Any]]):
    """Set SMTP accounts in session state"""
    st.session_state.smtp_accounts = accounts

def get_leads() -> List[Dict[str, Any]]:
    """Get leads from session state"""
    return st.session_state.leads

def set_leads(leads: List[Dict[str, Any]]):
    """Set leads in session state"""
    st.session_state.leads = leads

def get_selected_smtps() -> List[Dict[str, Any]]:
    """Get selected SMTP accounts"""
    return st.session_state.selected_smtps

def set_selected_smtps(smtps: List[Dict[str, Any]]):
    """Set selected SMTP accounts"""
    st.session_state.selected_smtps = smtps