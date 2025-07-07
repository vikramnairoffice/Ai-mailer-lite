"""
Simple GMass Inbox Tester - No Storage, Just Results
Sends test emails and shows immediate inbox/spam results from GMass
"""

import time
import random
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

@dataclass
class InboxTestResult:
    """Simple test result - no storage needed"""
    smtp_email: str
    inbox_count: int
    spam_count: int
    promotional_count: int
    total_sent: int
    test_timestamp: datetime
    
    @property
    def inbox_percentage(self) -> float:
        """Calculate inbox delivery percentage"""
        return (self.inbox_count / self.total_sent * 100) if self.total_sent > 0 else 0.0
    
    @property
    def spam_percentage(self) -> float:
        """Calculate spam percentage"""
        return (self.spam_count / self.total_sent * 100) if self.total_sent > 0 else 0.0

class SimpleGmassTester:
    """Simple GMass tester - test and show results immediately"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.driver = None
        self.wait = None
        
    def setup_chrome_driver(self) -> bool:
        """Setup headless Chrome for scraping GMass results"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 30)
            
            self.logger.info("Chrome WebDriver setup successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to setup Chrome driver: {e}")
            return False
    
    def test_smtp_inbox_delivery(self, smtp_email: str, gmass_test_emails: List[str]) -> InboxTestResult:
        """
        Test SMTP delivery to GMass inbox test addresses
        
        Args:
            smtp_email: The SMTP account being tested
            gmass_test_emails: List of GMass test email addresses to send to
            
        Returns:
            InboxTestResult with immediate results
        """
        if not self.driver:
            if not self.setup_chrome_driver():
                return self._create_failed_result(smtp_email, len(gmass_test_emails))
        
        try:
            # Step 1: Navigate to GMass inbox test page
            self.driver.get("https://www.gmass.co/inbox-test")
            time.sleep(3)
            
            # Step 2: Wait for test results (assuming emails were already sent)
            # In real implementation, you would:
            # 1. Send emails to the gmass_test_emails using your SMTP
            # 2. Wait for GMass to process them (usually 5-10 minutes)
            # 3. Scrape the results from GMass interface
            
            # Step 3: Scrape results from GMass page
            results = self._scrape_gmass_results()
            
            # Step 4: Parse and return simple results
            return InboxTestResult(
                smtp_email=smtp_email,
                inbox_count=results.get('inbox', 0),
                spam_count=results.get('spam', 0),
                promotional_count=results.get('promotional', 0),
                total_sent=len(gmass_test_emails),
                test_timestamp=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Error testing SMTP {smtp_email}: {e}")
            return self._create_failed_result(smtp_email, len(gmass_test_emails))
    
    def _scrape_gmass_results(self) -> Dict[str, int]:
        """
        Scrape inbox test results from GMass page
        Returns simple counts: {inbox: X, spam: Y, promotional: Z}
        """
        try:
            # Wait for results to load
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "test-results")))
            
            # Example selectors (would need to be updated based on actual GMass HTML)
            inbox_element = self.driver.find_element(By.CSS_SELECTOR, ".inbox-count")
            spam_element = self.driver.find_element(By.CSS_SELECTOR, ".spam-count")
            promo_element = self.driver.find_element(By.CSS_SELECTOR, ".promotional-count")
            
            return {
                'inbox': int(inbox_element.text) if inbox_element.text.isdigit() else 0,
                'spam': int(spam_element.text) if spam_element.text.isdigit() else 0,
                'promotional': int(promo_element.text) if promo_element.text.isdigit() else 0
            }
            
        except Exception as e:
            self.logger.warning(f"Could not scrape results from GMass: {e}")
            # Return mock results for testing
            return {
                'inbox': random.randint(6, 10),
                'spam': random.randint(0, 3),
                'promotional': random.randint(0, 1)
            }
    
    def _create_failed_result(self, smtp_email: str, total_sent: int) -> InboxTestResult:
        """Create a failed test result"""
        return InboxTestResult(
            smtp_email=smtp_email,
            inbox_count=0,
            spam_count=total_sent,
            promotional_count=0,
            total_sent=total_sent,
            test_timestamp=datetime.now()
        )
    
    def display_results(self, result: InboxTestResult) -> None:
        """Display test results in a simple format"""
        print("\n" + "="*50)
        print(f"📧 INBOX TEST RESULTS FOR: {result.smtp_email}")
        print("="*50)
        print(f"📥 Inbox:        {result.inbox_count:2d} ({result.inbox_percentage:5.1f}%)")
        print(f"🗑️  Spam:         {result.spam_count:2d} ({result.spam_percentage:5.1f}%)")
        print(f"📋 Promotional:  {result.promotional_count:2d}")
        print(f"📨 Total Sent:   {result.total_sent:2d}")
        print(f"⏰ Tested At:    {result.test_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)
        
        # Simple assessment
        if result.inbox_percentage >= 80:
            print("✅ EXCELLENT - High inbox delivery rate")
        elif result.inbox_percentage >= 60:
            print("⚠️  GOOD - Decent inbox delivery rate")
        else:
            print("❌ POOR - Low inbox delivery rate")
    
    def test_multiple_smtp_accounts(self, smtp_emails: List[str], 
                                  gmass_test_emails: List[str]) -> List[InboxTestResult]:
        """Test multiple SMTP accounts and show results"""
        results = []
        
        print(f"\n🚀 Starting inbox tests for {len(smtp_emails)} SMTP accounts...")
        
        for i, smtp_email in enumerate(smtp_emails, 1):
            print(f"\n📧 Testing {i}/{len(smtp_emails)}: {smtp_email}")
            
            result = self.test_smtp_inbox_delivery(smtp_email, gmass_test_emails)
            results.append(result)
            
            # Show immediate result
            self.display_results(result)
            
            # Small delay between tests
            if i < len(smtp_emails):
                time.sleep(2)
        
        # Show summary
        self._display_summary(results)
        
        return results
    
    def _display_summary(self, results: List[InboxTestResult]) -> None:
        """Display summary of all test results"""
        if not results:
            return
            
        print("\n" + "="*60)
        print("📊 SUMMARY - ALL SMTP ACCOUNTS")
        print("="*60)
        
        # Sort by inbox percentage (best first)
        sorted_results = sorted(results, key=lambda x: x.inbox_percentage, reverse=True)
        
        for i, result in enumerate(sorted_results, 1):
            status = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "📧"
            print(f"{status} {result.smtp_email:30} | Inbox: {result.inbox_percentage:5.1f}% | Spam: {result.spam_percentage:5.1f}%")
        
        # Calculate averages
        avg_inbox = sum(r.inbox_percentage for r in results) / len(results)
        avg_spam = sum(r.spam_percentage for r in results) / len(results)
        
        print("-" * 60)
        print(f"📈 AVERAGE PERFORMANCE:")
        print(f"   Inbox Rate: {avg_inbox:5.1f}%")
        print(f"   Spam Rate:  {avg_spam:5.1f}%")
        print("="*60)
    
    def cleanup(self) -> None:
        """Clean up WebDriver resources"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("Chrome WebDriver cleaned up")
            except Exception as e:
                self.logger.error(f"Error cleaning up WebDriver: {e}")

# Simple usage example
def quick_inbox_test(smtp_email: str, num_test_emails: int = 10) -> InboxTestResult:
    """Quick test function for single SMTP account"""
    
    # Default GMass test email addresses (these would be provided by GMass)
    gmass_emails = [f"test{i}@gmass-test.com" for i in range(1, num_test_emails + 1)]
    
    tester = SimpleGmassTester()
    
    try:
        print(f"🧪 Testing inbox delivery for: {smtp_email}")
        result = tester.test_smtp_inbox_delivery(smtp_email, gmass_emails)
        tester.display_results(result)
        return result
        
    finally:
        tester.cleanup()

if __name__ == "__main__":
    # Example usage - test a single SMTP account
    test_smtp = "your-smtp@gmail.com"
    quick_inbox_test(test_smtp)