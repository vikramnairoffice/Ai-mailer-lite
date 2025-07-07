"""
Gmail API integration and OAuth handling for Email Marketing System
"""

import os
import base64
import pickle
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import Optional, List

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    GMAIL_API_AVAILABLE = True
except ImportError:
    GMAIL_API_AVAILABLE = False

class GmailAPIMailer:
    """Gmail API mailer class"""
    
    def __init__(self, credentials_path: Optional[str] = None):
        self.credentials_path = credentials_path or "gmail_credentials"
        self.service = None
        
    def initialize_service(self) -> bool:
        """Initialize Gmail API service"""
        if not GMAIL_API_AVAILABLE:
            return False
            
        try:
            creds = None
            token_path = os.path.join(self.credentials_path, 'token.pickle')
            
            if os.path.exists(token_path):
                with open(token_path, 'rb') as token:
                    creds = pickle.load(token)
                    
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        os.path.join(self.credentials_path, 'credentials.json'),
                        ['https://www.googleapis.com/auth/gmail.send']
                    )
                    creds = flow.run_local_server(port=0)
                    
                with open(token_path, 'wb') as token:
                    pickle.dump(creds, token)
                    
            self.service = build('gmail', 'v1', credentials=creds)
            return True
        except Exception:
            return False
            
    def send_message(self, sender_email: str, recipient: str, subject: str, 
                    body: str, attachments: Optional[List[str]] = None) -> bool:
        """Send email via Gmail API"""
        try:
            message = MIMEMultipart('related')
            message['to'] = recipient
            message['from'] = sender_email
            message['subject'] = subject
            
            msg_alternative = MIMEMultipart('alternative')
            message.attach(msg_alternative)
            
            html_part = MIMEText(body, 'html')
            msg_alternative.attach(html_part)
            
            if attachments:
                for att_path in attachments:
                    if os.path.exists(att_path):
                        with open(att_path, 'rb') as f:
                            part = MIMEApplication(f.read(), Name=os.path.basename(att_path))
                            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(att_path)}"'
                            message.attach(part)
                            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            self.service.users().messages().send(
                userId='me', 
                body={'raw': raw_message}
            ).execute()
            
            return True
        except Exception:
            return False

    def test_connection(self) -> bool:
        """Test Gmail API connection"""
        try:
            if not self.service:
                if not self.initialize_service():
                    return False
            
            # Try to get profile to test connection
            self.service.users().getProfile(userId='me').execute()
            return True
        except Exception:
            return False

def is_gmail_api_available() -> bool:
    """Check if Gmail API is available"""
    return GMAIL_API_AVAILABLE

def create_gmail_mailer(credentials_path: Optional[str] = None) -> Optional[GmailAPIMailer]:
    """Create Gmail API mailer instance"""
    if not GMAIL_API_AVAILABLE:
        return None
    
    mailer = GmailAPIMailer(credentials_path)
    if mailer.initialize_service():
        return mailer
    return None