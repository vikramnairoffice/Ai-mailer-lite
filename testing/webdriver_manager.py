"""
Chrome WebDriver setup and management for GMass testing
"""

import time
import random
from typing import Optional
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

class WebDriverManager:
    """Manage Chrome WebDriver for automated testing"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        self.user_agent = UserAgent()
        
    def setup_driver(self, headless: bool = True, window_size: str = "1920,1080") -> bool:
        """Setup Chrome WebDriver for GMass testing"""
        try:
            chrome_options = Options()
            
            # Basic options
            if headless:
                chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument(f'--window-size={window_size}')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-images')
            
            # Anti-detection options
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Random user agent
            try:
                user_agent = self.user_agent.random
                chrome_options.add_argument(f'--user-agent={user_agent}')
            except:
                # Fallback user agent if fake_useragent fails
                chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            # Additional stealth options
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--allow-running-insecure-content')
            chrome_options.add_argument('--disable-features=TranslateUI')
            chrome_options.add_argument('--disable-ipc-flooding-protection')
            
            # Create driver with automatic ChromeDriver management
            self.driver = webdriver.Chrome(
                service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Set implicit wait and create WebDriverWait instance
            self.driver.implicitly_wait(10)
            self.wait = WebDriverWait(self.driver, 30)
            
            # Random viewport size to appear more human
            if not headless:
                width = random.randint(1200, 1920)
                height = random.randint(800, 1080)
                self.driver.set_window_size(width, height)
            
            self.logger.info("Chrome WebDriver setup successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up Chrome WebDriver: {e}")
            return False
    
    def close_driver(self) -> None:
        """Close the WebDriver and clean up"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                self.wait = None
                self.logger.info("WebDriver closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing WebDriver: {e}")
    
    def get_driver(self) -> Optional[webdriver.Chrome]:
        """Get the current WebDriver instance"""
        return self.driver
    
    def get_wait(self) -> Optional[WebDriverWait]:
        """Get the current WebDriverWait instance"""
        return self.wait
    
    def is_driver_ready(self) -> bool:
        """Check if WebDriver is ready for use"""
        try:
            if self.driver is None:
                return False
            
            # Try to get current URL to test if driver is responsive
            _ = self.driver.current_url
            return True
        except:
            return False
    
    def restart_driver(self) -> bool:
        """Restart the WebDriver (useful for error recovery)"""
        self.close_driver()
        time.sleep(random.uniform(2, 5))
        return self.setup_driver()
    
    def add_random_delay(self, min_delay: float = 1.0, max_delay: float = 3.0) -> None:
        """Add random delay to simulate human behavior"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def scroll_page_randomly(self) -> None:
        """Scroll page randomly to simulate human behavior"""
        if not self.driver:
            return
            
        try:
            # Get page height
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Random scroll positions
            for _ in range(random.randint(2, 5)):
                scroll_position = random.randint(0, page_height)
                self.driver.execute_script(f"window.scrollTo(0, {scroll_position})")
                time.sleep(random.uniform(0.5, 1.5))
            
            # Scroll back to top
            self.driver.execute_script("window.scrollTo(0, 0)")
            
        except Exception as e:
            self.logger.warning(f"Error during random scrolling: {e}")
    
    def clear_browser_data(self) -> None:
        """Clear cookies and local storage"""
        if not self.driver:
            return
            
        try:
            self.driver.delete_all_cookies()
            self.driver.execute_script("window.localStorage.clear();")
            self.driver.execute_script("window.sessionStorage.clear();")
            self.logger.info("Browser data cleared")
        except Exception as e:
            self.logger.warning(f"Error clearing browser data: {e}")
    
    def take_screenshot(self, filename: str = None) -> str:
        """Take screenshot for debugging purposes"""
        if not self.driver:
            return ""
            
        try:
            if not filename:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
            
            screenshot_path = self.driver.save_screenshot(filename)
            self.logger.info(f"Screenshot saved: {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"Error taking screenshot: {e}")
            return ""