"""
HTML-to-image email generation for Email Marketing System
"""

import os
from typing import Dict, Any, Optional
from datetime import datetime

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

def generate_html_to_image_content(lead_data: Dict[str, Any], phone_config: Dict[str, Any], 
                                  ai_enhance: bool = False, gemini_model=None) -> str:
    """Generate HTML content and convert to image"""
    
    # Generate regular HTML content first
    from .html_generator import generate_html_template_content
    html_content = generate_html_template_content(lead_data, phone_config, ai_enhance, gemini_model)
    
    # Create a simplified version optimized for image conversion
    image_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                width: 600px; 
                margin: 0; 
                padding: 40px; 
                background: white;
                line-height: 1.6;
            }}
            .container {{ 
                border: 2px solid #007bff; 
                border-radius: 10px; 
                padding: 30px; 
                background: #f8f9fa;
            }}
            .header {{ 
                text-align: center; 
                margin-bottom: 20px; 
                color: #007bff; 
            }}
            .content {{ 
                background: white; 
                padding: 20px; 
                border-radius: 8px; 
                margin: 20px 0;
            }}
            .cta {{ 
                background: #28a745; 
                color: white; 
                padding: 15px 30px; 
                text-decoration: none; 
                border-radius: 25px; 
                display: inline-block; 
                margin: 20px 0; 
                font-weight: bold;
            }}
            .footer {{ 
                text-align: center; 
                margin-top: 20px; 
                color: #666; 
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Personal Message for {lead_data.get('firstname', 'You')}</h1>
            </div>
            <div class="content">
                <p>Dear {lead_data.get('firstname', 'there')},</p>
                
                <p>I hope this message finds you well. I'm reaching out because I came across {lead_data.get('company', 'your company')} and was impressed by your work in the {lead_data.get('industry', 'business')} industry.</p>
                
                <p>We specialize in helping businesses like yours achieve remarkable results through our proven approach. Our clients typically see significant improvements within the first 30 days.</p>
                
                <p>I'd love to discuss how we can help {lead_data.get('company', 'your business')} reach new heights.</p>
                
                <center>
                    <div class="cta">Let's Connect Today!</div>
                </center>
                
                <p>Would you be available for a brief conversation this week?</p>
            </div>
            <div class="footer">
                <p><strong>Best regards,</strong><br>Your Name</p>
    """
    
    # Add phone number if available
    if phone_config.get('phone_number'):
        from .content_types import format_phone_number
        phone_display = format_phone_number(phone_config['phone_number'], 'display')
        image_html += f"<p>📞 {phone_display}</p>"
    
    image_html += """
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        # Convert HTML to image using Selenium
        image_path = html_to_image_selenium(image_html)
        
        if image_path:
            # Return image information
            return f"""
            <html>
            <body>
                <h3>Email converted to image format</h3>
                <p>Image saved at: {image_path}</p>
                <p>This email has been converted to an image to ensure consistent display across all email clients.</p>
                <p>Content preview: Personal message for {lead_data.get('firstname', 'recipient')} from {lead_data.get('company', 'their company')}</p>
            </body>
            </html>
            """
        else:
            # Fallback to regular HTML
            return html_content
            
    except Exception:
        # Fallback to regular HTML if image conversion fails
        return html_content

def html_to_image_selenium(html_content: str) -> Optional[str]:
    """Convert HTML to image using Selenium"""
    if not SELENIUM_AVAILABLE:
        return None
        
    try:
        # Setup Chrome options for headless operation
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=800,1200')
        chrome_options.add_argument('--disable-gpu')
        
        # Create driver
        driver = webdriver.Chrome(options=chrome_options)
        
        # Create temporary directory and HTML file
        temp_dir = os.path.join(os.getcwd(), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        temp_html_path = os.path.join(temp_dir, 'temp_email.html')
        
        with open(temp_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Load HTML file in browser
        driver.get(f'file://{os.path.abspath(temp_html_path)}')
        
        # Wait for page to load completely
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Generate unique filename for screenshot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(temp_dir, f'email_image_{timestamp}.png')
        
        # Take screenshot
        driver.save_screenshot(image_path)
        
        # Clean up
        driver.quit()
        
        # Remove temporary HTML file
        try:
            os.remove(temp_html_path)
        except:
            pass
        
        return image_path
        
    except Exception:
        return None

def create_image_email_template(lead_data: Dict[str, Any], phone_config: Dict[str, Any]) -> str:
    """Create a simple image-optimized email template"""
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }}
            .card {{ background: white; border-radius: 10px; padding: 30px; max-width: 500px; margin: 0 auto; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; color: #333; margin-bottom: 20px; }}
            .content {{ color: #555; line-height: 1.6; }}
            .cta {{ background: #007bff; color: white; padding: 12px 24px; border-radius: 5px; text-align: center; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 30px; color: #888; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <h2>Hello {lead_data.get('firstname', 'there')}!</h2>
            </div>
            <div class="content">
                <p>I wanted to reach out regarding {lead_data.get('company', 'your company')} and share how we can help you achieve your business goals.</p>
                <p>Our proven strategies have helped companies in the {lead_data.get('industry', 'business')} industry increase their performance significantly.</p>
                <div class="cta">
                    <strong>Ready to Learn More?</strong>
                </div>
                <p>I'd love to schedule a quick call to discuss your specific needs and how we can help.</p>
            </div>
            <div class="footer">
                <p>Best regards,<br><strong>Your Name</strong></p>
                {f'<p>📞 {phone_config.get("phone_number", "")}</p>' if phone_config.get("phone_number") else ""}
            </div>
        </div>
    </body>
    </html>
    """