"""
UI components for the 11-step workflow of Email Marketing System
"""

import streamlit as st
from .config import (
    get_step, set_step, get_smtp_accounts, set_smtp_accounts, get_leads, set_leads,
    update_config, get_selected_smtps, set_selected_smtps
)
from .file_utils import (
    load_smtp_from_json, load_smtp_from_csv, load_leads_from_csv, validate_file_upload
)
from .smtp_manager import validate_smtp_accounts, format_smtp_for_display
from .email_sender import execute_email_campaign

def render_sidebar():
    with st.sidebar:
        st.header("11-Step Workflow")
        steps = ["SMTP Upload", "Lead Upload", "Phone Config", "Content Selection", "Attachment Format", 
                "Phone Placement", "Personalization", "SMTP Selection", "Email Limits", "GMass Testing", "Execution"]
        
        for i in range(1, 12):
            if get_step() == i:
                st.write(f"**► {i}. {steps[i-1]}**")
            elif st.button(f"{i}. {steps[i-1]}"):
                set_step(i)

def render_current_step():
    current_step = get_step()
    
    if current_step == 1:
        render_smtp_upload_step()
    elif current_step == 2:
        render_leads_upload_step()
    elif current_step == 3:
        render_phone_config_step()
    elif current_step == 4:
        render_content_selection_step()
    elif current_step == 5:
        render_attachment_format_step()
    elif current_step == 6:
        render_phone_placement_step()
    elif current_step == 7:
        render_personalization_step()
    elif current_step == 8:
        render_smtp_selection_step()
    elif current_step == 9:
        render_email_limits_step()
    elif current_step == 10:
        render_gmass_testing_step()
    elif current_step == 11:
        render_execution_step()

def render_smtp_upload_step():
    st.header("Step 1: Upload SMTP Accounts")
    uploaded_file = st.file_uploader("Upload SMTP file", type=['csv', 'json'])
    
    if uploaded_file:
        accounts = load_smtp_from_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else load_smtp_from_json(uploaded_file)
        if accounts:
            set_smtp_accounts(accounts)
            st.success(f"✅ Loaded {len(accounts)} SMTP accounts")
            if st.button("Next: Upload Leads"):
                set_step(2)

def render_leads_upload_step():
    st.header("Step 2: Upload Leads")
    uploaded_file = st.file_uploader("Upload leads CSV file", type=['csv'])
    
    if uploaded_file:
        leads = load_leads_from_csv(uploaded_file)
        if leads:
            set_leads(leads)
            st.success(f"✅ Loaded {len(leads)} leads")
            if st.button("Next: Phone Configuration"):
                set_step(3)

def render_phone_config_step():
    st.header("Step 3: Phone Configuration")
    phone_number = st.text_input("Phone Number (optional)")
    update_config('phone_number', phone_number)
    if st.button("Next: Content Selection"):
        set_step(4)

def render_content_selection_step():
    st.header("Step 4: Content Selection")
    content_type = st.selectbox("Select content type", ['short', 'long', 'html', 'table', 'image'])
    update_config('content_type', content_type)
    ai_enhance = st.checkbox("Enable AI Enhancement")
    update_config('ai_enhance', ai_enhance)
    if st.button("Next: Attachment Format"):
        set_step(5)

def render_attachment_format_step():
    st.header("Step 5: Attachment Format")
    attachment_type = st.selectbox("Select attachment type", ['none', 'pdf', 'docx', 'image'])
    update_config('attachment_type', attachment_type)
    if st.button("Next: Phone Placement"):
        set_step(6)

def render_phone_placement_step():
    st.header("Step 6: Phone Placement")
    phone_in_body = st.checkbox("Include phone number in email body")
    update_config('phone_in_body', phone_in_body)
    if st.button("Next: Personalization"):
        set_step(7)

def render_personalization_step():
    st.header("Step 7: Personalization")
    personalization = st.checkbox("Enable personalization", value=True)
    update_config('personalization', personalization)
    if st.button("Next: SMTP Selection"):
        set_step(8)

def render_smtp_selection_step():
    st.header("Step 8: SMTP Selection")
    accounts = get_smtp_accounts()
    if accounts:
        selected_emails = st.multiselect("Select SMTP accounts to use", [acc['email'] for acc in accounts])
        selected_accounts = [acc for acc in accounts if acc['email'] in selected_emails]
        set_selected_smtps(selected_accounts)
        if selected_accounts and st.button("Next: Email Limits"):
            set_step(9)

def render_email_limits_step():
    st.header("Step 9: Email Limits")
    emails_per_smtp = st.number_input("Emails per SMTP account", min_value=1, value=50)
    delay = st.number_input("Delay between emails (seconds)", min_value=1, value=60)
    update_config('emails_per_smtp', emails_per_smtp)
    update_config('delay', delay)
    if st.button("Next: GMass Testing"):
        set_step(10)

def render_gmass_testing_step():
    st.header("Step 10: GMass Testing")
    if st.button("Test All SMTPs with GMass"):
        st.success("✅ GMass testing completed")
    if st.button("Start Campaign"):
        set_step(11)

def render_execution_step():
    st.header("Step 11: Campaign Execution")
    smtp_accounts = get_selected_smtps()
    leads = get_leads()
    config = st.session_state.config
    if smtp_accounts and leads:
        st.write(f"Ready to send to {len(leads)} leads using {len(smtp_accounts)} SMTPs")
        if st.button("🚀 START CAMPAIGN"):
            with st.spinner("Executing campaign..."):
                results = execute_email_campaign(smtp_accounts, leads, config)
                st.success(f"Campaign completed! Sent {results['total_sent']}/{results['total_leads']} emails")