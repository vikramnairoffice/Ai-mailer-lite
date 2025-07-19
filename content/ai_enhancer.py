"""
AI content enhancement using Google Gemini for Email Marketing System
"""

import os
from typing import Dict, Any, Optional
import logging

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class AIContentEnhancer:
    """AI-powered content enhancement using Google Gemini"""
    
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.gemini_model = None
        self.model_name = model_name or "gemini-2.5-flash"
        
        # Initialize Gemini with provided API key or environment variable
        if not api_key:
            api_key = os.getenv('GEMINI_API_KEY')
        
        if api_key and GEMINI_AVAILABLE:
            try:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel(self.model_name)
                self.logger.info(f"Gemini AI initialized successfully with {self.model_name}")
            except Exception as e:
                self.logger.error(f"Error initializing Gemini AI: {e}")
    
    def update_api_key(self, api_key: str, model_name: Optional[str] = None) -> bool:
        """Update the API key and optionally model, then reinitialize"""
        if not api_key or not GEMINI_AVAILABLE:
            return False
        
        if model_name:
            self.model_name = model_name
        
        try:
            genai.configure(api_key=api_key)
            self.gemini_model = genai.GenerativeModel(self.model_name)
            self.logger.info(f"Gemini AI reinitialized with new API key and {self.model_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating Gemini API key: {e}")
            self.gemini_model = None
            return False
    
    def update_model(self, model_name: str) -> bool:
        """Update the model name and reinitialize if API key exists"""
        if not model_name:
            return False
        
        self.model_name = model_name
        
        # If we already have a working model, reinitialize with new model
        if self.gemini_model:
            try:
                self.gemini_model = genai.GenerativeModel(self.model_name)
                self.logger.info(f"Gemini model updated to {self.model_name}")
                return True
            except Exception as e:
                self.logger.error(f"Error updating Gemini model: {e}")
                return False
        
        return True
    
    def enhance_spintax_content(self, template: str, lead_data: Dict[str, Any], 
                               content_type: str = "email") -> str:
        """Enhance spintax template using AI"""
        if not self.gemini_model:
            return template
        
        try:
            prompt = f"""
            Enhance this spintax email template to make it more engaging and personalized:
            
            Original template: {template}
            
            Lead information:
            - Name: {lead_data.get('firstname', 'there')}
            - Company: {lead_data.get('company', 'your company')}
            - Industry: {lead_data.get('industry', 'your industry')}
            
            Requirements:
            - Keep the spintax format with {{option1|option2|option3}}
            - Make it more personalized and compelling
            - Keep it professional but engaging
            - Include at least 3-4 variations for each section
            - Make it sound natural and conversational
            - Length should be appropriate for {content_type}
            """
            
            response = self.gemini_model.generate_content(prompt)
            enhanced_template = response.text.strip()
            
            # Validate that it's still spintax format
            if '{' in enhanced_template and '|' in enhanced_template and '}' in enhanced_template:
                return enhanced_template
            else:
                self.logger.warning("AI enhanced content lost spintax format, using original")
                return template
                
        except Exception as e:
            self.logger.error(f"Error enhancing spintax with AI: {e}")
            return template
    
    def enhance_html_content(self, html_template: str, lead_data: Dict[str, Any]) -> str:
        """Enhance HTML email template using AI"""
        if not self.gemini_model:
            return html_template
        
        try:
            prompt = f"""
            Enhance this HTML email template to make it more engaging and professional:
            
            Original template: {html_template[:1000]}...
            
            Lead information:
            - Name: {lead_data.get('firstname', 'there')}
            - Company: {lead_data.get('company', 'your company')}
            - Industry: {lead_data.get('industry', 'your industry')}
            
            Requirements:
            - Keep the HTML structure and any template variables intact (like {{{{ firstname }}}})
            - Make it more personalized and compelling
            - Improve the design and styling where appropriate
            - Keep it professional but engaging
            - Don't remove any phone functionality or CTAs
            - Ensure it's mobile-friendly
            """
            
            response = self.gemini_model.generate_content(prompt)
            enhanced_html = response.text.strip()
            
            # Basic validation that key elements are preserved
            key_elements = ['firstname', 'company', '<html>', '</html>']
            if all(element in enhanced_html.lower() for element in key_elements):
                return enhanced_html
            else:
                self.logger.warning("AI enhanced HTML lost key elements, using original")
                return html_template
                
        except Exception as e:
            self.logger.error(f"Error enhancing HTML with AI: {e}")
            return html_template
    
    def enhance_table_services(self, industry: str, company: str) -> list:
        """Generate industry-specific services using AI"""
        if not self.gemini_model:
            return self._get_default_services()
        
        try:
            prompt = f"""
            Create a table of 4-5 services/benefits relevant to a company in the {industry} industry.
            
            Company: {company}
            Industry: {industry}
            
            Requirements:
            - Create 4-5 rows of relevant services
            - Each row should have: Service, Benefit, Timeline
            - Make it specific to their industry
            - Keep timelines realistic (30-90 days)
            - Format as JSON array like: [{{"Service": "...", "Benefit": "...", "Timeline": "..."}}]
            - Services should be actionable and valuable
            - Benefits should be measurable
            """
            
            response = self.gemini_model.generate_content(prompt)
            
            # Try to parse the JSON response
            import json
            try:
                enhanced_services = json.loads(response.text.strip())
                if isinstance(enhanced_services, list) and len(enhanced_services) > 0:
                    # Validate structure
                    if all('Service' in item and 'Benefit' in item and 'Timeline' in item 
                          for item in enhanced_services):
                        return enhanced_services
            except json.JSONDecodeError:
                pass
            
            self.logger.warning("AI generated services had invalid format, using defaults")
            return self._get_default_services()
                
        except Exception as e:
            self.logger.error(f"Error generating AI services: {e}")
            return self._get_default_services()
    
    def enhance_general_content(self, content: str, lead_data: Dict[str, Any], 
                               content_type: str = "email") -> str:
        """General content enhancement for any text"""
        if not self.gemini_model:
            return content
        
        try:
            prompt = f"""
            Enhance this {content_type} content to make it more engaging and professional:
            
            Original content: {content}
            
            Lead information:
            - Name: {lead_data.get('firstname', 'there')}
            - Company: {lead_data.get('company', 'your company')}
            - Industry: {lead_data.get('industry', 'your industry')}
            
            Requirements:
            - Keep the same format and structure
            - Make it more personalized and compelling
            - Keep it professional but engaging
            - Don't add clickable links unless they were already present
            - Length should be similar to original
            - Maintain the tone and purpose of the original
            """
            
            response = self.gemini_model.generate_content(prompt)
            enhanced_content = response.text.strip()
            
            return enhanced_content if enhanced_content else content
            
        except Exception as e:
            self.logger.error(f"Error enhancing general content with AI: {e}")
            return content
    
    def _get_default_services(self) -> list:
        """Get default services when AI enhancement fails"""
        return [
            {"Service": "Business Consulting", "Benefit": "Increased Revenue", "Timeline": "30 days"},
            {"Service": "Process Optimization", "Benefit": "Reduced Costs", "Timeline": "45 days"},
            {"Service": "Marketing Strategy", "Benefit": "More Leads", "Timeline": "60 days"},
            {"Service": "Team Training", "Benefit": "Better Performance", "Timeline": "90 days"}
        ]
    
    def is_available(self) -> bool:
        """Check if AI enhancement is available"""
        return self.gemini_model is not None

# Global instance for easy access
_ai_enhancer = None

def get_ai_enhancer() -> AIContentEnhancer:
    """Get global AI enhancer instance"""
    global _ai_enhancer
    if _ai_enhancer is None:
        _ai_enhancer = AIContentEnhancer()
    return _ai_enhancer