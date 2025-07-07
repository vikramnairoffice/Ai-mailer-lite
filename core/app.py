"""
Main Streamlit interface and workflow orchestration for Email Marketing System
"""

import streamlit as st
import json
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import init_session_state, get_step, set_step
from core.ui_components import render_sidebar, render_current_step

def main():
    """Main application entry point"""
    st.set_page_config(page_title="Email Marketing System", layout="wide")
    init_session_state()
    
    st.title("📧 Email Marketing System")
    
    # Sidebar navigation
    render_sidebar()
    
    # Main content based on current step
    render_current_step()

if __name__ == "__main__":
    main()