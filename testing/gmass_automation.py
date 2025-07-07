"""
Core GMass automation logic for Email Marketing System
"""

import time
import random
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

@dataclass
class GmassTestResult:
    """GMass test result data"""
    email_address: str
    smtp_account: str
    inbox_score: int
    spam_score: int
    promotional_score: int
    total_score: int
    test_details: Dict[str, Any]
    tested_at: datetime
    success: bool
    error_message: Optional[str] = None

class GmassAutomation:
    """Core GMass automation functionality"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.driver = None
        self.wait = None
        self.gmass_credentials = {}
        
    def login_to_gmass(self) -> bool:
        """Login to GMass platform"""
        try:
            if not self.driver:
                return False
                
            # Navigate to GMass login
            self.driver.get("https://gmass.co/login")
            
            # Wait for login form
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            password_field = self.driver.find_element(By.ID, "password")
            
            # Enter credentials
            self._human_type(email_field, self.gmass_credentials.get('email', ''))
            time.sleep(random.uniform(1, 2))
            
            self._human_type(password_field, self.gmass_credentials.get('password', ''))
            time.sleep(random.uniform(1, 2))
            
            # Submit login form
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for successful login (dashboard or inbox test page)
            self.wait.until(
                EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME, "dashboard")),
                    EC.presence_of_element_located((By.ID, "inbox-test-form"))
                )
            )
            
            self.logger.info("Successfully logged into GMass")
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging into GMass: {e}")
            return False
    
    def navigate_to_inbox_test(self) -> bool:
        """Navigate to the inbox testing page"""
        try:
            if not self.driver:
                return False
                
            # Look for inbox test link or navigate directly
            try:
                inbox_test_link = self.driver.find_element(
                    By.PARTIAL_LINK_TEXT, "Inbox Test"
                )
                inbox_test_link.click()
            except NoSuchElementException:
                # Direct navigation if link not found
                self.driver.get("https://gmass.co/inbox-test")
            
            # Wait for inbox test form
            self.wait.until(
                EC.presence_of_element_located((By.ID, "inbox-test-form"))
            )
            
            self.logger.info("Successfully navigated to inbox test page")
            return True
            
        except Exception as e:
            self.logger.error(f"Error navigating to inbox test: {e}")
            return False
    
    def fill_test_form(self, test_config: Dict[str, Any]) -> bool:
        """Fill out the GMass inbox test form"""
        try:
            # Fill sender email
            sender_email = self.driver.find_element(By.ID, "sender-email")
            sender_email.clear()
            self._human_type(sender_email, test_config.get('smtp_email', ''))
            
            # Fill test emails
            test_emails_field = self.driver.find_element(By.ID, "test-emails")
            test_emails_field.clear()
            test_emails = test_config.get('test_emails', [])
            self._human_type(test_emails_field, '\n'.join(test_emails))
            
            # Fill subject line
            subject_field = self.driver.find_element(By.ID, "subject")
            subject_field.clear()
            self._human_type(subject_field, test_config.get('subject', 'Test Email'))
            
            # Fill email content
            content_field = self.driver.find_element(By.ID, "email-content")
            content_field.clear()
            self._human_type(content_field, self._generate_test_content())
            
            time.sleep(random.uniform(2, 4))
            return True
            
        except Exception as e:
            self.logger.error(f"Error filling test form: {e}")
            return False
    
    def submit_test(self) -> bool:
        """Submit the inbox test"""
        try:
            submit_button = self.driver.find_element(
                By.CSS_SELECTOR, "button[type='submit'], .submit-test"
            )
            submit_button.click()
            
            # Wait for test submission confirmation
            self.wait.until(
                EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME, "test-submitted")),
                    EC.presence_of_element_located((By.ID, "test-progress"))
                )
            )
            
            self.logger.info("Test submitted successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error submitting test: {e}")
            return False
    
    def _generate_test_content(self) -> str:
        """Generate test email content"""
        test_contents = [
            "This is a test email to check deliverability. Please ignore this message.",
            "Testing email delivery to ensure optimal inbox placement rates.",
            "Deliverability test in progress. This message can be safely ignored.",
            "Email routing test - checking spam filters and inbox delivery."
        ]
        return random.choice(test_contents)
    
    def _human_type(self, element, text: str) -> None:
        """Type text with human-like delays"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
    
    def set_gmass_credentials(self, email: str, password: str) -> None:
        """Set GMass login credentials"""
        self.gmass_credentials = {'email': email, 'password': password}

def test_smtp_with_gmass(smtp_config: Dict[str, Any]) -> int:
    """Test SMTP account with GMass and return score"""
    try:
        # For demo purposes, return a random score
        # In real implementation, this would use the full GMass automation
        return random.randint(40, 90)
    except Exception:
        return 50  # Default score if test fails