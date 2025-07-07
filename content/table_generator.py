"""
Table format email generation for Email Marketing System
"""

import json
from typing import Dict, Any, List, Optional

def generate_table_format_content(lead_data: Dict[str, Any], phone_config: Dict[str, Any], 
                                 ai_enhance: bool = False, gemini_model=None) -> str:
    """Generate table-formatted email content"""
    
    # Default service/benefit data
    services = [
        {"Service": "Business Consulting", "Benefit": "Increased Revenue", "Timeline": "30 days"},
        {"Service": "Process Optimization", "Benefit": "Reduced Costs", "Timeline": "45 days"},
        {"Service": "Marketing Strategy", "Benefit": "More Leads", "Timeline": "60 days"},
        {"Service": "Team Training", "Benefit": "Better Performance", "Timeline": "90 days"}
    ]
    
    # AI enhancement for services
    if ai_enhance and gemini_model:
        try:
            prompt = f"""
            Create a table of services/benefits relevant to a company in the {lead_data.get('industry', 'business')} industry.
            
            Company: {lead_data.get('company', 'the company')}
            Industry: {lead_data.get('industry', 'business')}
            
            Requirements:
            - Create 4-5 rows of relevant services
            - Each row should have: Service, Benefit, Timeline
            - Make it specific to their industry
            - Keep timelines realistic (30-90 days)
            - Format as JSON array like: [{{"Service": "...", "Benefit": "...", "Timeline": "..."}}]
            """
            
            response = gemini_model.generate_content(prompt)
            try:
                enhanced_services = json.loads(response.text.strip())
                if isinstance(enhanced_services, list) and len(enhanced_services) > 0:
                    services = enhanced_services
            except:
                pass
                
        except Exception:
            pass
    
    # Build HTML table
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .header h2 {{ color: #007bff; margin-bottom: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #f8f9fa; font-weight: bold; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            .cta {{ background: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; margin: 20px 0; }}
            .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Personalized Solutions for {lead_data.get('firstname', 'You')}</h2>
                <p>Here's how we can help {lead_data.get('company', 'your business')} succeed:</p>
            </div>
            
            <table>
                <tr>
                    <th>Service</th>
                    <th>Benefit</th>
                    <th>Timeline</th>
                </tr>
    """
    
    # Add service rows
    for service in services:
        html_content += f"""
                <tr>
                    <td>{service.get('Service', '')}</td>
                    <td>{service.get('Benefit', '')}</td>
                    <td>{service.get('Timeline', '')}</td>
                </tr>
        """
    
    # Add phone info if available
    phone_section = ""
    if phone_config.get('phone_number'):
        from .content_types import format_phone_number
        phone_display = format_phone_number(phone_config['phone_number'], 'display')
        phone_link = format_phone_number(phone_config['phone_number'], 'click_to_call')
        phone_section = f"""
            <p>Ready to get started? <a href="{phone_link}">Call {phone_display}</a> (Please save this number for future contact)</p>
        """
    
    # Complete the HTML
    html_content += f"""
            </table>
            
            <p>Hi {lead_data.get('firstname', 'there')},</p>
            
            <p>I've put together this customized overview of how we can help {lead_data.get('company', 'your business')} achieve better results. Each service is designed to deliver specific, measurable benefits within the timelines shown.</p>
            
            <p>Would you be interested in discussing any of these solutions in more detail? I'd be happy to answer questions and explore how we can tailor our approach to your specific needs.</p>
            
            {phone_section}
            
            <div class="footer">
                <p>Best regards,<br>Your Name</p>
                <p>Looking forward to helping {lead_data.get('company', 'your business')} succeed!</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

def generate_industry_specific_services(industry: str, company: str) -> List[Dict[str, str]]:
    """Generate industry-specific services based on company industry"""
    
    industry_services = {
        'technology': [
            {"Service": "Cloud Migration", "Benefit": "Reduced IT Costs", "Timeline": "45 days"},
            {"Service": "Security Audit", "Benefit": "Enhanced Protection", "Timeline": "30 days"},
            {"Service": "DevOps Implementation", "Benefit": "Faster Deployment", "Timeline": "60 days"},
            {"Service": "API Development", "Benefit": "Better Integration", "Timeline": "90 days"}
        ],
        'healthcare': [
            {"Service": "Compliance Review", "Benefit": "HIPAA Compliance", "Timeline": "30 days"},
            {"Service": "EHR Optimization", "Benefit": "Improved Efficiency", "Timeline": "60 days"},
            {"Service": "Staff Training", "Benefit": "Better Patient Care", "Timeline": "45 days"},
            {"Service": "Process Automation", "Benefit": "Reduced Errors", "Timeline": "90 days"}
        ],
        'retail': [
            {"Service": "Inventory Management", "Benefit": "Reduced Waste", "Timeline": "45 days"},
            {"Service": "Customer Analytics", "Benefit": "Higher Sales", "Timeline": "30 days"},
            {"Service": "E-commerce Setup", "Benefit": "Online Revenue", "Timeline": "60 days"},
            {"Service": "Staff Training", "Benefit": "Better Service", "Timeline": "30 days"}
        ],
        'manufacturing': [
            {"Service": "Process Optimization", "Benefit": "Increased Output", "Timeline": "60 days"},
            {"Service": "Quality Control", "Benefit": "Reduced Defects", "Timeline": "45 days"},
            {"Service": "Safety Training", "Benefit": "Fewer Accidents", "Timeline": "30 days"},
            {"Service": "Equipment Audit", "Benefit": "Lower Maintenance", "Timeline": "90 days"}
        ]
    }
    
    # Return industry-specific services or default
    industry_lower = industry.lower() if industry else 'business'
    for key in industry_services:
        if key in industry_lower:
            return industry_services[key]
    
    # Default services
    return [
        {"Service": "Business Consulting", "Benefit": "Increased Revenue", "Timeline": "30 days"},
        {"Service": "Process Optimization", "Benefit": "Reduced Costs", "Timeline": "45 days"},
        {"Service": "Marketing Strategy", "Benefit": "More Leads", "Timeline": "60 days"},
        {"Service": "Team Training", "Benefit": "Better Performance", "Timeline": "90 days"}
    ]