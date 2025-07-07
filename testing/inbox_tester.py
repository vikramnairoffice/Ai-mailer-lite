"""
Inbox, spam, and promotional folder testing for Email Marketing System
"""

import time
import random
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from .gmass_automation import GmassTestResult

class InboxTester:
    """Test email delivery to inbox, spam, and promotional folders"""
    
    def __init__(self, webdriver_manager):
        self.logger = logging.getLogger(__name__)
        self.webdriver_manager = webdriver_manager
        
    def run_inbox_test(self, smtp_email: str, test_emails: List[str]) -> List[GmassTestResult]:
        """Run comprehensive inbox testing for SMTP account"""
        results = []
        
        if not self.webdriver_manager.is_driver_ready():
            self.logger.error("WebDriver not ready for inbox testing")
            return results
        
        driver = self.webdriver_manager.get_driver()
        wait = self.webdriver_manager.get_wait()
        
        try:
            # Prepare test configuration
            test_config = {
                'smtp_email': smtp_email,
                'test_emails': test_emails,
                'subject': f'Inbox Test {datetime.now().strftime("%Y%m%d_%H%M%S")}',
                'content': self._generate_test_content()
            }
            
            # Navigate to GMass inbox test if not already there
            current_url = driver.current_url
            if 'inbox-test' not in current_url:
                driver.get("https://gmass.co/inbox-test")
                wait.until(EC.presence_of_element_located((By.ID, "inbox-test-form")))
            
            # Fill and submit test form
            if self._fill_test_form(test_config):
                if self._submit_test():
                    # Wait for results
                    test_results = self._wait_for_results()
                    if test_results:
                        # Parse results for each test email
                        for test_email in test_emails:
                            result = self._parse_test_result(test_email, smtp_email, test_results)
                            results.append(result)
                    else:
                        # Create failed result
                        for test_email in test_emails:
                            result = GmassTestResult(
                                email_address=test_email,
                                smtp_account=smtp_email,
                                inbox_score=0,
                                spam_score=100,
                                promotional_score=0,
                                total_score=0,
                                test_details={},
                                tested_at=datetime.now(),
                                success=False,
                                error_message="Failed to get test results"
                            )
                            results.append(result)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error running inbox test: {e}")
            # Return failed results for all test emails
            for test_email in test_emails:
                result = GmassTestResult(
                    email_address=test_email,
                    smtp_account=smtp_email,
                    inbox_score=0,
                    spam_score=100,
                    promotional_score=0,
                    total_score=0,
                    test_details={},
                    tested_at=datetime.now(),
                    success=False,
                    error_message=str(e)
                )
                results.append(result)
            return results
    
    def _fill_test_form(self, test_config: Dict[str, Any]) -> bool:
        """Fill out the inbox test form"""
        driver = self.webdriver_manager.get_driver()
        
        try:
            # Fill sender email
            sender_email = driver.find_element(By.ID, "sender-email")
            sender_email.clear()
            self._human_type(sender_email, test_config['smtp_email'])
            
            # Fill test emails
            test_emails_field = driver.find_element(By.ID, "test-emails")
            test_emails_field.clear()
            self._human_type(test_emails_field, '\n'.join(test_config['test_emails']))
            
            # Fill subject
            subject_field = driver.find_element(By.ID, "subject")
            subject_field.clear()
            self._human_type(subject_field, test_config['subject'])
            
            # Fill content
            content_field = driver.find_element(By.ID, "email-content")
            content_field.clear()
            self._human_type(content_field, test_config['content'])
            
            time.sleep(random.uniform(2, 4))
            return True
            
        except Exception as e:
            self.logger.error(f"Error filling test form: {e}")
            return False
    
    def _submit_test(self) -> bool:
        """Submit the inbox test"""
        driver = self.webdriver_manager.get_driver()
        wait = self.webdriver_manager.get_wait()
        
        try:
            submit_button = driver.find_element(
                By.CSS_SELECTOR, "button[type='submit'], .submit-test, #submit-test"
            )
            submit_button.click()
            
            # Wait for submission confirmation
            wait.until(
                EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME, "test-submitted")),
                    EC.presence_of_element_located((By.ID, "test-progress")),
                    EC.presence_of_element_located((By.CLASS_NAME, "testing-progress"))
                )
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error submitting test: {e}")
            return False
    
    def _wait_for_results(self, timeout: int = 300) -> Optional[Dict[str, Any]]:
        """Wait for test results to be available"""
        driver = self.webdriver_manager.get_driver()
        wait = self.webdriver_manager.get_wait()
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Check for results container
                results_element = driver.find_element(By.CLASS_NAME, "test-results")
                if results_element.is_displayed():
                    return self._extract_results()
                
                # Check for completion indicators
                if driver.find_elements(By.CLASS_NAME, "test-complete"):
                    return self._extract_results()
                
                # Wait a bit before checking again
                time.sleep(10)
                
            except NoSuchElementException:
                # Results not ready yet, continue waiting
                time.sleep(10)
                continue
            except Exception as e:
                self.logger.error(f"Error waiting for results: {e}")
                break
        
        self.logger.warning("Timeout waiting for test results")
        return None
    
    def _extract_results(self) -> Dict[str, Any]:
        """Extract test results from the page"""
        driver = self.webdriver_manager.get_driver()
        
        try:
            results = {
                'inbox_score': 0,
                'spam_score': 0,
                'promotional_score': 0,
                'total_score': 0,
                'details': {}
            }
            
            # Try to find score elements
            try:
                inbox_element = driver.find_element(By.CSS_SELECTOR, ".inbox-score, #inbox-score")
                results['inbox_score'] = int(inbox_element.text.replace('%', ''))
            except:
                pass
            
            try:
                spam_element = driver.find_element(By.CSS_SELECTOR, ".spam-score, #spam-score")
                results['spam_score'] = int(spam_element.text.replace('%', ''))
            except:
                pass
            
            try:
                promo_element = driver.find_element(By.CSS_SELECTOR, ".promo-score, #promo-score")
                results['promotional_score'] = int(promo_element.text.replace('%', ''))
            except:
                pass
            
            # Calculate total score
            results['total_score'] = results['inbox_score'] - results['spam_score']
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error extracting results: {e}")
            return {}
    
    def _parse_test_result(self, test_email: str, smtp_account: str, 
                          test_results: Dict[str, Any]) -> GmassTestResult:
        """Parse test results into structured format"""
        
        return GmassTestResult(
            email_address=test_email,
            smtp_account=smtp_account,
            inbox_score=test_results.get('inbox_score', 0),
            spam_score=test_results.get('spam_score', 100),
            promotional_score=test_results.get('promotional_score', 0),
            total_score=test_results.get('total_score', 0),
            test_details=test_results.get('details', {}),
            tested_at=datetime.now(),
            success=test_results.get('total_score', 0) > 0,
            error_message=None if test_results.get('total_score', 0) > 0 else "Low deliverability score"
        )
    
    def _generate_test_content(self) -> str:
        """Generate realistic test email content"""
        test_contents = [
            """Hello,
            
            I hope this email finds you well. I wanted to reach out to discuss a potential business opportunity.
            
            Our company specializes in helping businesses improve their operations and achieve better results.
            Would you be interested in learning more?
            
            Best regards,
            Test User""",
            
            """Hi there,
            
            Thank you for your interest in our services. We would love to schedule a quick call to discuss your needs.
            
            Please let me know when you're available this week.
            
            Looking forward to hearing from you!
            
            Best,
            Test Team"""
        ]
        
        return random.choice(test_contents)
    
    def _human_type(self, element, text: str) -> None:
        """Type text with human-like delays"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))