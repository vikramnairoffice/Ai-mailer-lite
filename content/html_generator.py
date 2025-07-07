"""
HTML template generation for Email Marketing System
"""

import random
from typing import Dict, Any, Optional
from jinja2 import Template

def generate_html_template_content(lead_data: Dict[str, Any], phone_config: Dict[str, Any], 
                                  ai_enhance: bool = False, gemini_model=None) -> str:
    """Generate HTML email template"""
    
    templates = [
        """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
                .content { padding: 20px 0; }
                .cta { background: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; margin: 20px 0; }
                .footer { border-top: 1px solid #eee; padding-top: 20px; margin-top: 30px; color: #666; font-size: 14px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Hello {{ firstname }}!</h2>
                </div>
                <div class="content">
                    <p>I hope this email finds you well. I'm reaching out because I came across {{ company }} and was impressed by what you do in the {{ industry }} industry.</p>
                    
                    <p>We specialize in helping businesses like yours achieve their goals and overcome challenges. Our proven approach has helped hundreds of companies improve their operations and results.</p>
                    
                    <p>I'd love to learn more about your current situation and see how we might be able to help {{ company }} reach new heights.</p>
                    
                    {% if phone_display %}
                    <div class="cta">Call Us: {{ phone_display }} (Please save this number for future contact)</div>
                    {% endif %}
                    
                    <p>Would you be interested in a quick 15-minute conversation this week? I can work around your schedule.</p>
                    
                    <p>Looking forward to hearing from you!</p>
                </div>
                <div class="footer">
                    <p>Best regards,<br>Your Name</p>
                    {% if phone_display %}
                    <p>📞 {{ phone_display }}</p>
                    {% endif %}
                </div>
            </div>
        </body>
        </html>
        """,
        
        """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Georgia, serif; line-height: 1.8; color: #2c3e50; }
                .container { max-width: 600px; margin: 20px auto; background: white; border-radius: 8px; padding: 30px; }
                .header { text-align: center; margin-bottom: 30px; }
                .content { margin: 20px 0; }
                .cta-button { display: inline-block; background: #4caf50; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; margin: 20px 0; }
                .footer { text-align: center; color: #777; margin-top: 30px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Dear {{ firstname }},</h1>
                </div>
                <div class="content">
                    <p>I hope this finds you well. {{ company }} caught my attention as a leader in the {{ industry }} industry.</p>
                    <p>We help businesses like yours achieve remarkable results. Our approach has proven successful for many companies.</p>
                    {% if phone_display %}
                    <a href="tel:{{ phone_link }}" class="cta-button">📞 Call {{ phone_display }}</a>
                    {% endif %}
                    <p>Would you be available for a brief conversation this week?</p>
                </div>
                <div class="footer">
                    <p><strong>Best regards,</strong><br>Your Name</p>
                    {% if phone_display %}
                    <p>{{ phone_display }}</p>
                    {% endif %}
                </div>
            </div>
        </body>
        </html>
        """
    ]
    
    # Select random template
    template_str = random.choice(templates)
    
    # AI enhancement
    if ai_enhance and gemini_model:
        template_str = enhance_html_with_ai(template_str, lead_data, gemini_model)
    
    # Prepare phone formatting
    phone_display = ""
    phone_link = ""
    
    if phone_config.get('phone_number'):
        from .content_types import format_phone_number
        phone_display = format_phone_number(phone_config['phone_number'], 'display')
        phone_link = format_phone_number(phone_config['phone_number'], 'click_to_call')
    
    # Render template
    template = Template(template_str)
    content = template.render(
        firstname=lead_data.get('firstname', 'there'),
        company=lead_data.get('company', 'your company'),
        industry=lead_data.get('industry', 'your industry'),
        phone_display=phone_display,
        phone_link=phone_link
    )
    
    return content

def enhance_html_with_ai(template_str: str, lead_data: Dict[str, Any], gemini_model) -> str:
    """Enhance HTML template using AI"""
    if not gemini_model:
        return template_str
    
    try:
        prompt = f"Enhance this HTML email for {lead_data.get('firstname', 'there')} from {lead_data.get('company', 'company')}. Keep HTML structure and variables intact: {template_str[:500]}..."
        response = gemini_model.generate_content(prompt)
        enhanced = response.text.strip()
        
        if 'firstname' in enhanced and 'company' in enhanced and '<html>' in enhanced:
            return enhanced
    except Exception:
        pass
    
    return template_str