"""
Base content type definitions and main content generation interface
"""

import os
from typing import Dict, Any, Optional
import logging

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class ContentGenerator:
    """Main content generator interface"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.gemini_model = None
        
        # Initialize Gemini if available
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key and GEMINI_AVAILABLE:
            try:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                self.logger.info("Gemini AI initialized successfully")
            except Exception as e:
                self.logger.error(f"Error initializing Gemini AI: {e}")
    
    def generate_content(self, lead_data: Dict[str, Any], content_type: str, 
                        phone_config: Dict[str, Any] = None, ai_enhance: bool = False) -> str:
        """Generate content based on type"""
        if phone_config is None:
            phone_config = {}
        
        if content_type == 'short':
            from .spintax_generator import generate_short_spintax_content
            return generate_short_spintax_content(lead_data, phone_config, ai_enhance, self.gemini_model)
        elif content_type == 'long':
            from .spintax_generator import generate_long_spintax_content
            return generate_long_spintax_content(lead_data, phone_config, ai_enhance, self.gemini_model)
        elif content_type == 'html':
            from .html_generator import generate_html_template_content
            return generate_html_template_content(lead_data, phone_config, ai_enhance, self.gemini_model)
        elif content_type == 'table':
            from .table_generator import generate_table_format_content
            return generate_table_format_content(lead_data, phone_config, ai_enhance, self.gemini_model)
        elif content_type == 'image':
            from .image_generator import generate_html_to_image_content
            return generate_html_to_image_content(lead_data, phone_config, ai_enhance, self.gemini_model)
        else:
            return self._generate_default_content(lead_data, phone_config)
    
    def _generate_default_content(self, lead_data: Dict[str, Any], phone_config: Dict[str, Any]) -> str:
        """Generate default content when type is not recognized"""
        firstname = lead_data.get('firstname', 'there')
        company = lead_data.get('company', 'your company')
        
        content = f"""
        <html>
        <body>
        <p>Hi {firstname},</p>
        <p>I wanted to reach out regarding {company} and discuss how we can help you achieve your goals.</p>
        <p>Would you be interested in learning more about our services?</p>
        """
        
        if phone_config.get('phone_number'):
            phone_display = format_phone_number(phone_config['phone_number'])
            content += f"<p>Feel free to call us at {phone_display}</p>"
        
        content += """
        <p>Best regards,<br>Your Name</p>
        </body>
        </html>
        """
        
        return content

def format_phone_number(phone: str, format_type: str = 'display') -> str:
    """Format phone number for display or click-to-call"""
    if not phone:
        return ""
    
    # Remove all non-digit characters
    digits = ''.join(filter(str.isdigit, phone))
    
    if format_type == 'display':
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        else:
            return phone
    elif format_type == 'click_to_call':
        return f"tel:+{digits}"
    
    return phone

def enhance_with_ai(content: str, lead_data: Dict[str, Any], content_type: str, 
                   gemini_model) -> str:
    """Enhance content using Gemini AI if available"""
    if not gemini_model:
        return content
    
    try:
        prompt = f"""
        Enhance this {content_type} email content to make it more engaging and professional:
        
        Original: {content}
        
        Lead: {lead_data.get('firstname', 'there')} from {lead_data.get('company', 'company')}
        
        Requirements:
        - Keep same format and structure
        - Make it personalized and compelling  
        - Keep it professional
        - Don't add clickable links
        - Similar length to original
        """
        
        response = gemini_model.generate_content(prompt)
        enhanced = response.text.strip()
        return enhanced if enhanced else content
        
    except Exception:
        return content

def create_content_generator() -> ContentGenerator:
    """Create and return a content generator instance"""
    return ContentGenerator()

# Main function for backward compatibility
def generate_content(lead: Dict[str, Any], content_type: str, personalization: bool = True,
                    phone_number: Optional[str] = None, phone_in_body: bool = False, 
                    ai_enhance: bool = False) -> str:
    """Main content generation function for compatibility with email sender"""
    generator = ContentGenerator()
    phone_config = {
        'phone_number': phone_number,
        'phone_in_body': phone_in_body
    }
    return generator.generate_content(lead, content_type, phone_config, ai_enhance)