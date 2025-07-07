import time
import random
import os
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
# Removed database imports - GMass tester now shows immediate results only

@dataclass
class GmassTestResult:
    """GMass test result data."""
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

class GmassTester:
    """Automated GMass inbox testing and scoring."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.driver = None
        self.wait = None
        self.user_agent = UserAgent()
        self.gmass_credentials = {}
        self.test_results: List[GmassTestResult] = []
        
    def setup_driver(self) -> bool:
        """Setup Chrome WebDriver for GMass testing."""
        try:
            chrome_options = Options()
            
            # Add stealth options
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument(f'--user-agent={self.user_agent.random}')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-images')
            chrome_options.add_argument('--disable-javascript')
            
            # For Colab/headless environments
            if os.environ.get('COLAB_GPU') or os.environ.get('HEADLESS', False):
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--window-size=1920,1080')
            
            # Create driver
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Execute stealth script
            self.driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                })
            """)
            
            self.wait = WebDriverWait(self.driver, 30)
            
            self.logger.info("Chrome WebDriver setup successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up Chrome WebDriver: {e}")
            return False
    
    def close_driver(self) -> None:
        """Close WebDriver."""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
            self.wait = None
    
    def set_gmass_credentials(self, email: str, password: str) -> None:
        """Set GMass login credentials."""
        self.gmass_credentials = {
            'email': email,
            'password': password
        }
    
    def login_to_gmass(self) -> bool:
        """Login to GMass platform."""
        try:
            if not self.driver:
                self.logger.error("WebDriver not initialized")
                return False
            
            if not self.gmass_credentials:
                self.logger.error("GMass credentials not set")
                return False
            
            # Navigate to GMass login
            self.driver.get("https://www.gmass.co/login")
            
            # Random delay
            time.sleep(random.uniform(2, 4))
            
            # Wait for login form
            email_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            
            password_field = self.driver.find_element(By.NAME, "password")
            
            # Enter credentials with human-like typing
            self._human_type(email_field, self.gmass_credentials['email'])
            time.sleep(random.uniform(0.5, 1.5))
            
            self._human_type(password_field, self.gmass_credentials['password'])
            time.sleep(random.uniform(0.5, 1.5))
            
            # Submit form
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for successful login
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".dashboard, .inbox-test"))
            )
            
            self.logger.info("Successfully logged into GMass")
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging into GMass: {e}")
            return False
    
    def navigate_to_inbox_test(self) -> bool:
        """Navigate to GMass inbox test feature."""
        try:
            # Look for inbox test navigation
            inbox_test_links = [
                "//a[contains(text(), 'Inbox Test')]",
                "//a[contains(text(), 'Test')]",
                "//a[contains(@href, 'inbox-test')]",
                ".inbox-test-nav",
                ".test-nav"
            ]
            
            for link_selector in inbox_test_links:
                try:
                    if link_selector.startswith("//"):
                        element = self.driver.find_element(By.XPATH, link_selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, link_selector)
                    
                    element.click()
                    time.sleep(random.uniform(2, 4))
                    
                    # Check if we're on the inbox test page
                    if "inbox-test" in self.driver.current_url.lower() or \
                       "test" in self.driver.current_url.lower():
                        self.logger.info("Successfully navigated to inbox test")
                        return True
                        
                except:
                    continue
            
            # If direct navigation fails, try accessing via URL
            self.driver.get("https://www.gmass.co/inbox-test")
            time.sleep(random.uniform(3, 5))
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error navigating to inbox test: {e}")
            return False
    
    def run_inbox_test(self, smtp_email: str, test_emails: List[str]) -> List[GmassTestResult]:
        """Run inbox test for given SMTP account and test emails."""
        results = []
        
        try:
            if not self.driver:
                self.logger.error("WebDriver not initialized")
                return results
            
            # Setup test configuration
            test_config = {
                'sender_email': smtp_email,
                'test_emails': test_emails,
                'subject': f"Inbox Test - {datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'content': self._generate_test_content()
            }
            
            # Fill in test form
            if not self._fill_test_form(test_config):
                self.logger.error("Failed to fill test form")
                return results
            
            # Submit test
            if not self._submit_test():
                self.logger.error("Failed to submit test")
                return results
            
            # Wait for results
            test_results = self._wait_for_results()
            
            if test_results:
                # Parse results for each test email
                for test_email in test_emails:
                    result = self._parse_test_result(test_email, smtp_email, test_results)
                    results.append(result)
                    
                    # Save to database
                    self._save_result_to_database(result)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error running inbox test: {e}")
            return results
    
    def _fill_test_form(self, test_config: Dict[str, Any]) -> bool:
        """Fill the GMass test form."""
        try:
            # Fill sender email
            sender_fields = [
                "input[name='sender_email']",
                "input[name='from_email']",
                "#sender-email",
                ".sender-email"
            ]
            
            for field_selector in sender_fields:
                try:
                    field = self.driver.find_element(By.CSS_SELECTOR, field_selector)
                    field.clear()
                    self._human_type(field, test_config['sender_email'])
                    break
                except:
                    continue
            
            # Fill test emails
            test_email_fields = [
                "textarea[name='test_emails']",
                "textarea[name='recipients']",
                "#test-emails",
                ".test-emails"
            ]
            
            test_emails_text = '\n'.join(test_config['test_emails'])
            
            for field_selector in test_email_fields:
                try:
                    field = self.driver.find_element(By.CSS_SELECTOR, field_selector)
                    field.clear()
                    self._human_type(field, test_emails_text)
                    break
                except:
                    continue
            
            # Fill subject
            subject_fields = [
                "input[name='subject']",
                "#subject",
                ".subject"
            ]
            
            for field_selector in subject_fields:
                try:
                    field = self.driver.find_element(By.CSS_SELECTOR, field_selector)
                    field.clear()
                    self._human_type(field, test_config['subject'])
                    break
                except:
                    continue
            
            # Fill content
            content_fields = [
                "textarea[name='content']",
                "textarea[name='message']",
                "#content",
                ".content"
            ]
            
            for field_selector in content_fields:
                try:
                    field = self.driver.find_element(By.CSS_SELECTOR, field_selector)
                    field.clear()
                    self._human_type(field, test_config['content'])
                    break
                except:
                    continue
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error filling test form: {e}")
            return False
    
    def _submit_test(self) -> bool:
        """Submit the inbox test."""
        try:
            submit_buttons = [
                "button[type='submit']",
                "input[type='submit']",
                ".submit-test",
                ".send-test",
                "//button[contains(text(), 'Send Test')]",
                "//button[contains(text(), 'Start Test')]"
            ]
            
            for button_selector in submit_buttons:
                try:
                    if button_selector.startswith("//"):
                        button = self.driver.find_element(By.XPATH, button_selector)
                    else:
                        button = self.driver.find_element(By.CSS_SELECTOR, button_selector)
                    
                    button.click()
                    time.sleep(random.uniform(2, 4))
                    return True
                    
                except:
                    continue
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error submitting test: {e}")
            return False
    
    def _wait_for_results(self, timeout: int = 300) -> Optional[Dict[str, Any]]:
        """Wait for test results to be available."""
        try:
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                # Check for results indicators
                result_selectors = [
                    ".test-results",
                    ".inbox-results",
                    ".delivery-results",
                    "//div[contains(text(), 'Results')]",
                    "//div[contains(text(), 'Complete')]"
                ]
                
                for selector in result_selectors:
                    try:
                        if selector.startswith("//"):
                            element = self.driver.find_element(By.XPATH, selector)
                        else:
                            element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        
                        if element.is_displayed():
                            return self._extract_results()
                            
                    except:
                        continue
                
                # Wait before checking again
                time.sleep(10)
                
                # Check progress indicators
                progress_selectors = [
                    ".progress",
                    ".loading",
                    "//div[contains(text(), 'Testing')]",
                    "//div[contains(text(), 'Processing')]"
                ]
                
                still_processing = False
                for selector in progress_selectors:
                    try:
                        if selector.startswith("//"):
                            element = self.driver.find_element(By.XPATH, selector)
                        else:
                            element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        
                        if element.is_displayed():
                            still_processing = True
                            break
                            
                    except:
                        continue
                
                if not still_processing:
                    # Try to extract results even if no specific indicator
                    return self._extract_results()
            
            self.logger.warning("Timeout waiting for test results")
            return None
            
        except Exception as e:
            self.logger.error(f"Error waiting for results: {e}")
            return None
    
    def _extract_results(self) -> Dict[str, Any]:
        """Extract test results from the page."""
        try:
            results = {
                'inbox_score': 0,
                'spam_score': 0,
                'promotional_score': 0,
                'total_score': 0,
                'details': {},
                'raw_data': {}
            }
            
            # Extract scores using various selectors
            score_selectors = [
                (".inbox-score", "inbox_score"),
                (".spam-score", "spam_score"),
                (".promotional-score", "promotional_score"),
                (".total-score", "total_score"),
                ("//span[contains(text(), 'Inbox')]", "inbox_score"),
                ("//span[contains(text(), 'Spam')]", "spam_score"),
                ("//span[contains(text(), 'Promotional')]", "promotional_score")
            ]
            
            for selector, score_type in score_selectors:
                try:
                    if selector.startswith("//"):
                        elements = self.driver.find_elements(By.XPATH, selector)
                    else:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        text = element.text.strip()
                        # Extract number from text
                        import re
                        numbers = re.findall(r'\d+', text)
                        if numbers:
                            results[score_type] = int(numbers[0])
                            break
                            
                except:
                    continue
            
            # Calculate total score if not found
            if results['total_score'] == 0:
                results['total_score'] = results['inbox_score'] + results['spam_score'] + results['promotional_score']
            
            # Extract additional details
            results['details'] = self._extract_detailed_results()
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error extracting results: {e}")
            return {}
    
    def _extract_detailed_results(self) -> Dict[str, Any]:
        """Extract detailed test results."""
        details = {}
        
        try:
            # Extract provider-specific results
            provider_selectors = [
                ".gmail-result",
                ".outlook-result",
                ".yahoo-result",
                ".provider-results"
            ]
            
            for selector in provider_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        provider_name = element.get_attribute("data-provider") or "unknown"
                        result_text = element.text.strip()
                        details[provider_name] = result_text
                except:
                    continue
            
            # Extract timestamp
            details['tested_at'] = datetime.now().isoformat()
            
            # Extract raw HTML for debugging
            try:
                results_container = self.driver.find_element(By.CSS_SELECTOR, ".results, .test-results")
                details['raw_html'] = results_container.get_attribute("innerHTML")
            except:
                pass
            
        except Exception as e:
            self.logger.error(f"Error extracting detailed results: {e}")
        
        return details
    
    def _parse_test_result(self, test_email: str, smtp_account: str, test_results: Dict[str, Any]) -> GmassTestResult:
        """Parse test results into GmassTestResult object."""
        
        result = GmassTestResult(
            email_address=test_email,
            smtp_account=smtp_account,
            inbox_score=test_results.get('inbox_score', 0),
            spam_score=test_results.get('spam_score', 0),
            promotional_score=test_results.get('promotional_score', 0),
            total_score=test_results.get('total_score', 0),
            test_details=test_results.get('details', {}),
            tested_at=datetime.now(),
            success=True
        )
        
        return result
    
    def _save_result_to_database(self, result: GmassTestResult) -> None:
        """Save test result to database."""
        try:
            result_data = {
                'email_address': result.email_address,
                'smtp_account': result.smtp_account,
                'inbox_score': result.inbox_score,
                'spam_score': result.spam_score,
                'promotional_score': result.promotional_score,
                'tested_at': result.tested_at.isoformat(),
                'test_details': json.dumps(result.test_details)
            }
            
            save_to_database('gmass_scores', result_data)
            
        except Exception as e:
            self.logger.error(f"Error saving result to database: {e}")
    
    def _generate_test_content(self) -> str:
        """Generate test email content."""
        templates = [
            "This is a test email to check deliverability. Please ignore this message.",
            "Hello, this is a deliverability test. Thank you for your time.",
            "Testing email delivery. This message can be safely ignored.",
            "Inbox test in progress. No action required.",
            "Email deliverability check. Please disregard this message."
        ]
        
        return random.choice(templates)
    
    def _human_type(self, element, text: str) -> None:
        """Type text with human-like delays."""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
    
    def get_smtp_account_scores(self, smtp_account: str) -> List[Dict[str, Any]]:
        """Get historical scores for an SMTP account."""
        try:
            results = get_from_database('gmass_scores', {'smtp_account': smtp_account})
            
            # Sort by test date (most recent first)
            results.sort(key=lambda x: x.get('tested_at', ''), reverse=True)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error getting SMTP account scores: {e}")
            return []
    
    def get_best_smtp_accounts(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get SMTP accounts with best inbox scores."""
        try:
            all_results = get_from_database('gmass_scores')
            
            # Group by SMTP account and get latest score
            account_scores = {}
            
            for result in all_results:
                smtp_account = result['smtp_account']
                tested_at = result.get('tested_at', '')
                
                if smtp_account not in account_scores or tested_at > account_scores[smtp_account]['tested_at']:
                    account_scores[smtp_account] = result
            
            # Sort by inbox score (descending)
            sorted_accounts = sorted(
                account_scores.values(),
                key=lambda x: x.get('inbox_score', 0),
                reverse=True
            )
            
            return sorted_accounts[:limit]
            
        except Exception as e:
            self.logger.error(f"Error getting best SMTP accounts: {e}")
            return []
    
    def simulate_gmass_test(self, smtp_email: str, test_emails: List[str]) -> List[GmassTestResult]:
        """Simulate GMass test results (for testing/demo purposes)."""
        results = []
        
        for test_email in test_emails:
            # Generate realistic but randomized scores
            inbox_score = random.randint(60, 95)
            spam_score = random.randint(0, 20)
            promotional_score = random.randint(0, 30)
            
            # Ensure scores don't exceed 100%
            total = inbox_score + spam_score + promotional_score
            if total > 100:
                inbox_score = max(50, 100 - spam_score - promotional_score)
            
            result = GmassTestResult(
                email_address=test_email,
                smtp_account=smtp_email,
                inbox_score=inbox_score,
                spam_score=spam_score,
                promotional_score=promotional_score,
                total_score=inbox_score + spam_score + promotional_score,
                test_details={
                    'gmail_result': 'Inbox' if inbox_score > 70 else 'Spam',
                    'outlook_result': 'Inbox' if inbox_score > 65 else 'Spam',
                    'yahoo_result': 'Inbox' if inbox_score > 75 else 'Spam',
                    'simulated': True
                },
                tested_at=datetime.now(),
                success=True
            )
            
            results.append(result)
            self._save_result_to_database(result)
        
        return results
    
    def run_comprehensive_test(self, smtp_accounts: List[str], test_emails: List[str], 
                             use_simulation: bool = False) -> Dict[str, List[GmassTestResult]]:
        """Run comprehensive inbox tests for multiple SMTP accounts."""
        all_results = {}
        
        try:
            if use_simulation:
                # Use simulation for testing
                for smtp_account in smtp_accounts:
                    results = self.simulate_gmass_test(smtp_account, test_emails)
                    all_results[smtp_account] = results
                    
                    # Add delay to simulate real testing
                    time.sleep(random.uniform(5, 10))
                
            else:
                # Setup driver for real testing
                if not self.setup_driver():
                    self.logger.error("Failed to setup WebDriver")
                    return all_results
                
                # Login to GMass
                if not self.login_to_gmass():
                    self.logger.error("Failed to login to GMass")
                    return all_results
                
                # Navigate to inbox test
                if not self.navigate_to_inbox_test():
                    self.logger.error("Failed to navigate to inbox test")
                    return all_results
                
                # Run tests for each SMTP account
                for smtp_account in smtp_accounts:
                    try:
                        self.logger.info(f"Testing SMTP account: {smtp_account}")
                        results = self.run_inbox_test(smtp_account, test_emails)
                        all_results[smtp_account] = results
                        
                        # Add delay between tests
                        time.sleep(random.uniform(30, 60))
                        
                    except Exception as e:
                        self.logger.error(f"Error testing SMTP account {smtp_account}: {e}")
                        continue
                
                # Close driver
                self.close_driver()
            
            return all_results
            
        except Exception as e:
            self.logger.error(f"Error in comprehensive test: {e}")
            return all_results
        
        finally:
            if self.driver:
                self.close_driver()

def create_gmass_tester() -> GmassTester:
    """Create and return a GMass tester instance."""
    return GmassTester()

def test_gmass_functionality() -> bool:
    """Test GMass functionality with simulation."""
    try:
        tester = create_gmass_tester()
        
        # Test with sample data
        smtp_accounts = ["test@gmail.com", "test@outlook.com"]
        test_emails = ["inbox@gmail.com", "inbox@outlook.com"]
        
        # Run simulated test
        results = tester.run_comprehensive_test(smtp_accounts, test_emails, use_simulation=True)
        
        # Verify results
        if results and len(results) > 0:
            for smtp_account, test_results in results.items():
                if test_results and len(test_results) > 0:
                    logger.info(f"Test successful for {smtp_account}: {len(test_results)} results")
                    return True
        
        return False
        
    except Exception as e:
        logger.error(f"Error testing GMass functionality: {e}")
        return False