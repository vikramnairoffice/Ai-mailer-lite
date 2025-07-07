"""
Short and long spintax content generation for Email Marketing System
"""

import random
import re
from typing import Dict, Any, Optional
import logging

def generate_short_spintax_content(lead_data: Dict[str, Any], phone_config: Dict[str, Any], 
                                  ai_enhance: bool = False, gemini_model=None) -> str:
    """Generate short spintax content"""
    templates = [
        "Hi {firstname|there}, {I hope this finds you well|Hope you're doing great}. {I wanted to reach out|Just wanted to connect} about {your business|your company|your work}. {Would love to chat|Let's connect} {soon|when you have time}. {Best regards|Thanks}!",
        
        "{Hey|Hi} {firstname|there}! {Quick question|Just wondering} - {are you looking for|do you need} {better solutions|new opportunities|improvements} for {your business|your company}? {Let's talk|Give me a call} {when convenient|at your convenience}. {Thanks|Best}!",
        
        "{Good morning|Good afternoon} {firstname|there}, {I came across|I found} your {company|business} and {was impressed|thought you might be interested} in {what we offer|our solutions}. {Can we schedule|Would you like} a {quick call|brief chat}? {Looking forward to hearing from you|Hope to connect soon}!",
        
        "{firstname|Hi there}, {I specialize in|We help with} {business growth|improving operations|solving problems} for {companies like yours|businesses in your industry}. {Would you be interested|Are you open} to {learning more|a quick conversation}? {Let me know|Please reach out}!",
        
        "{Hello|Hi} {firstname|there}! {I noticed|I saw} {your company|your business} {online|in my research} and {thought you might benefit|believe you could use} from {our services|what we offer}. {Free to chat|Available for a call} {this week|soon}? {Thanks for your time|Best regards}!"
    ]
    
    template = random.choice(templates)
    
    # AI enhancement
    if ai_enhance and gemini_model:
        template = enhance_spintax_with_ai(template, lead_data, "short", gemini_model)
    
    return process_spintax(template, lead_data, phone_config)

def generate_long_spintax_content(lead_data: Dict[str, Any], phone_config: Dict[str, Any], 
                                 ai_enhance: bool = False, gemini_model=None) -> str:
    """Generate long spintax content"""
    templates = [
        """
        {Hi|Hello|Good morning|Good afternoon} {firstname|there},

        {I hope this email finds you well|Hope you're having a great day|Trust this message reaches you in good spirits}. {I'm reaching out|I wanted to connect|I'm contacting you} because {I came across|I discovered|I found} {your company|your business|{company}} {online|in my research|during my search} and {was impressed by|really liked|found interesting} {what you do|your work|your services}.

        {I specialize in|We focus on|Our company helps with} {helping businesses|supporting companies|assisting organizations} {like yours|in your industry|in the {industry} sector} {grow and succeed|achieve their goals|reach new heights|overcome challenges}. {We've helped|I've assisted|Our team has supported} {hundreds of|many|numerous} {businesses|companies|organizations} {improve their|enhance their|optimize their} {operations|processes|performance|results}.

        {I'd love to|Would love to|I'm interested in} {learn more about|understand better|discuss} {your current|your existing|the} {challenges|situation|needs|goals} and {see how|explore how|determine if} {we can help|I can assist|our solutions might benefit} {you|your business|your team}. {This could be|It might be|There's potential for} {a great fit|an excellent opportunity|a perfect match} {for both of us|for your business|for your goals}.

        {Would you be|Are you|Might you be} {interested in|open to|available for} {a quick call|a brief conversation|a short chat|a 15-minute discussion} {this week|in the coming days|when convenient|at your convenience}? {I can work around|I'm flexible with|Let me know} your schedule.

        {Looking forward to|Hope to|Excited to} {hearing from you|connecting with you|our conversation}!

        {Best regards|Thanks|Best wishes|Warm regards},
        {Your Name|[Your Name]|[Sender Name]}
        """,
        
        """
        {Dear|Hello|Hi} {firstname|there},

        {I hope you don't mind|Hope it's okay|Trust you don't mind} me reaching out {directly|like this|via email}. {I'm|We're} {currently working with|helping|supporting} {several|many|numerous} {businesses|companies} {in your area|in the {industry} industry|similar to yours} and {thought you might|believed you could|felt you would} {benefit from|be interested in|find value in} {what we offer|our services|our solutions}.

        {The reason I'm contacting you|Why I'm reaching out|The purpose of this email} is {simple|straightforward|clear}: {we've developed|I've created|our team has built} {a system|a solution|a process} that {helps|allows|enables} {businesses|companies} {like yours|in your position|facing similar challenges} to {significantly improve|dramatically enhance|substantially increase} their {results|performance|outcomes|success}.

        {Here's what makes us different|What sets us apart|Our unique approach}: {we don't just|we avoid|we never} {talk theory|give generic advice|use cookie-cutter solutions}. {Instead|Rather|Instead of that}, {we focus on|we concentrate on|we prioritize} {practical|real-world|actionable} {solutions|strategies|approaches} that {deliver|produce|generate} {real results|tangible outcomes|measurable improvements} {quickly|fast|in a short time}.

        {I'd be happy to|Would love to|I'm excited to} {share more details|explain further|provide more information} about {how this works|our approach|what we do} and {answer any questions|address any concerns|discuss your specific situation} you might have.

        {Could we|Would it be possible to|Are you available to} {schedule|arrange|set up} {a quick call|a brief phone conversation|a short discussion} {sometime this week|in the next few days|when it's convenient for you}?

        {Thank you for your time|Thanks for reading|I appreciate your attention},
        {Best|Regards|Best regards},
        {[Your Name]|Your Name}
        """
    ]
    
    template = random.choice(templates)
    
    # AI enhancement
    if ai_enhance and gemini_model:
        template = enhance_spintax_with_ai(template, lead_data, "long", gemini_model)
    
    return process_spintax(template, lead_data, phone_config)

def process_spintax(template: str, lead_data: Dict[str, Any], phone_config: Dict[str, Any]) -> str:
    """Process spintax template and personalize content"""
    
    # Process spintax variations
    def replace_spintax(match):
        options = match.group(1).split('|')
        return random.choice(options)
    
    # Replace all spintax patterns
    content = re.sub(r'\{([^}]+)\}', replace_spintax, template)
    
    # Personalization replacements
    replacements = {
        'firstname': lead_data.get('firstname', 'there'),
        'lastname': lead_data.get('lastname', ''),
        'company': lead_data.get('company', 'your company'),
        'industry': lead_data.get('industry', 'your industry'),
        'location': lead_data.get('location', 'your area')
    }
    
    for key, value in replacements.items():
        content = content.replace(f'{{{key}}}', value)
    
    # Add phone information if configured
    if phone_config.get('phone_in_body') and phone_config.get('phone_number'):
        from .content_types import format_phone_number
        phone_display = format_phone_number(phone_config['phone_number'])
        content += f"\n\nCall us at {phone_display}"
    
    return content.strip()

def enhance_spintax_with_ai(template: str, lead_data: Dict[str, Any], spintax_type: str, 
                           gemini_model) -> str:
    """Enhance spintax template using AI"""
    if not gemini_model:
        return template
    
    try:
        prompt = f"""
        Enhance this {spintax_type} spintax email template to make it more engaging:
        
        Original: {template}
        
        Lead: {lead_data.get('firstname', 'there')} from {lead_data.get('company', 'company')}
        
        Requirements:
        - Keep the spintax format with {{option1|option2|option3}}
        - Make it more personalized and compelling
        - Keep it professional
        - Include at least 3 variations for each section
        """
        
        response = gemini_model.generate_content(prompt)
        enhanced = response.text.strip()
        
        # Validate that it's still spintax format
        if '{' in enhanced and '|' in enhanced:
            return enhanced
            
    except Exception:
        pass
    
    return template