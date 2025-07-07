# Multi-SMTP Email Marketing System

## Project Overview
A comprehensive email marketing automation system designed for Google Colab deployment with multi-SMTP support, GMass integration, and advanced content generation capabilities.

## Core Objectives
- **11-Step Workflow**: Complete email marketing automation from SMTP setup to delivery
- **Multi-SMTP Concurrency**: Handle up to 20 SMTP accounts simultaneously
- **GMass Integration**: Automated inbox testing and scoring
- **Content Variety**: 5 distinct content types including AI-generated spintax
- **Lead Management**: Automated distribution and CSV cleanup
- **Colab-Optimized**: Single-environment deployment with web interface

## Technical Architecture

### Technology Stack
- **Frontend**: Streamlit (web interface)
- **Backend**: Python (function-based architecture)
- **Database**: SQLite (logging and tracking)
- **AI Integration**: Google Gemini API
- **Web Automation**: Selenium (GMass testing)
- **Deployment**: Google Colab + LocalTunnel

### Architecture Principles
- **Simplicity First**: Function-based design over complex classes
- **MVP Focus**: 6 core files maximum for maintainability
- **Modular Design**: Clear separation of concerns
- **Error Resilience**: Comprehensive exception handling
- **Performance**: Concurrent processing with rate limiting

## Modular File Structure
```
email_marketing_system/
├── core/
│   ├── __init__.py
│   ├── app.py             # Main Streamlit interface (23 lines)
│   ├── config.py          # Configuration and session state (100 lines)
│   ├── ui_components.py   # UI workflow components (150 lines)
│   ├── file_utils.py      # CSV/JSON operations (154 lines)
│   ├── smtp_manager.py    # SMTP account management (150 lines)
│   └── email_sender.py    # Email sending logic (153 lines)
├── content/
│   ├── __init__.py
│   ├── content_types.py   # Main content interface (143 lines)
│   ├── spintax_generator.py   # Spintax content generation (142 lines)
│   ├── html_generator.py  # HTML email templates (138 lines)
│   ├── table_generator.py # Table format emails (165 lines)
│   ├── image_generator.py # HTML-to-image conversion (226 lines)
│   └── ai_enhancer.py     # AI content enhancement (210 lines)
├── testing/
│   ├── __init__.py
│   ├── gmass_automation.py    # Core GMass automation (192 lines)
│   ├── webdriver_manager.py   # Chrome WebDriver setup (176 lines)
│   ├── inbox_tester.py        # Inbox testing logic (275 lines)
│   ├── scoring_engine.py      # SMTP scoring system (211 lines)
│   └── csv_results.py         # CSV result storage (265 lines)
├── integrations/
│   ├── __init__.py
│   ├── gmail_api.py       # Gmail API integration (117 lines)
│   └── attachment_generator.py # PDF/DOCX attachments (147 lines)
├── requirements.txt       # Python dependencies
├── CLAUDE.md             # This file
└── temp/                 # Temporary files directory
```

## Development Approach

### Phase 1: Core Infrastructure
1. **Project Setup**: Directory structure, requirements, basic imports
2. **Utils Foundation**: Database setup, validation functions, file operations
3. **SMTP Manager**: Account loading, validation, connection testing

### Phase 2: Content & Testing
4. **Content Generator**: All 5 content types with AI integration
5. **GMass Tester**: Selenium automation for inbox scoring
6. **Email Sender**: Core sending logic with threading

### Phase 3: UI & Integration
7. **Streamlit Interface**: 11-step workflow implementation
8. **Integration Testing**: End-to-end workflow validation
9. **Colab Optimization**: Deployment and tunnel setup

## Key Features Implementation

### 11-Step Workflow
1. **SMTP Upload**: CSV/JSON file processing with validation
2. **Lead Upload**: CSV processing with email validation
3. **Phone Config**: Contact number integration options
4. **Content Selection**: 5 types with AI enhancement
5. **Attachment Format**: PDF, Image, DOCX with click-to-call
6. **Phone Placement**: Body vs attachment-only options
7. **Personalization**: Firstname/lastname dynamic insertion
8. **SMTP Selection**: Multi-account management with limits
9. **Email Limits**: Per-SMTP quota configuration
10. **GMass Testing**: Automated scoring and ranking
11. **Execution**: Concurrent sending with progress tracking

### Content Types
1. **Short Spintax**: Python-based with AI enhancement
2. **Long Spintax**: Extended format with randomization
3. **HTML Templates**: AI-generated with inline styling
4. **Table Format**: Structured data presentation
5. **HTML-to-Image**: Selenium conversion for image emails

### Multi-SMTP Features
- **Concurrent Processing**: Threading per SMTP account
- **Load Distribution**: Intelligent lead partitioning
- **Rate Limiting**: 4-6 second intervals per account
- **Progress Tracking**: Real-time status per SMTP
- **Error Recovery**: Individual SMTP failure handling

## Development Rules & Guidelines

### Code Modularity Rules
- **Maximum file size**: 150 lines of code per file (flexible for complex functionality)
- **Single responsibility**: Each module handles one specific concern
- **Clear interfaces**: Well-defined function signatures and return types
- **Minimal dependencies**: Reduce inter-module coupling

### Data Storage Policy
- **CSV Only for Leads**: All lead data must be in CSV format
- **No Database**: No SQLite or database components - use CSV/JSON files only
- **No Reports**: No reporting features or analytics storage required
- **Session State**: Use Streamlit session state for temporary data

### Feature Development Process
- **No autonomous features**: Claude will not add features without explicit approval
- **Suggestion highlighting**: New feature ideas will be clearly marked as [SUGGESTION]
- **Approval required**: All feature additions require user confirmation
- **No database features**: Do not suggest or implement any database functionality

### Code Style
- **Function-Based**: Avoid complex class hierarchies
- **Clear Naming**: Descriptive function and variable names
- **Type Hints**: Use for better code documentation
- **Error Handling**: Try-catch blocks for all external operations
- **Logging**: Comprehensive activity tracking

### Testing Strategy
- **Unit Tests**: Individual function validation
- **Integration Tests**: End-to-end workflow testing
- **SMTP Tests**: Connection and sending validation
- **UI Tests**: Streamlit interface functionality

### Performance Considerations
- **Memory Management**: Process large CSV files in chunks
- **Connection Pooling**: Reuse SMTP connections where possible
- **Rate Limiting**: Respect provider limits to avoid blocking
- **Progress Feedback**: Real-time updates for user experience

## External Dependencies

### Required APIs
- **Google Gemini**: Content generation and enhancement
- **GMass**: Inbox testing and deliverability scoring

### Python Packages
```
streamlit>=1.28.0
pandas>=2.0.0
selenium>=4.15.0
requests>=2.31.0
jinja2>=3.1.0
reportlab>=4.0.0
python-docx>=0.8.11
pillow>=10.0.0
sqlite3 (built-in)
smtplib (built-in)
threading (built-in)
```

### System Requirements
- **Chrome Browser**: Required for Selenium automation
- **ChromeDriver**: Auto-managed by Selenium
- **Internet Access**: API calls and email sending

## Security Considerations
- **SMTP Credentials**: Secure handling and validation
- **API Keys**: Environment variable management
- **Data Privacy**: No persistent storage of sensitive data
- **Rate Limiting**: Prevent account blocking and abuse

## Deployment Notes
- **Colab Environment**: Optimized for notebook execution
- **LocalTunnel**: External access to Streamlit interface
- **File Persistence**: Handle Colab session limitations
- **Resource Management**: Memory and CPU optimization

## Success Criteria
- ✅ Process 10,000+ leads per session
- ✅ Support 20 concurrent SMTP accounts
- ✅ Achieve 90%+ email delivery success rate
- ✅ Complete GMass scoring within 5 minutes
- ✅ Maintain 4-6 second sending intervals
- ✅ Provide real-time progress tracking
- ✅ Handle SMTP failures gracefully

## Future Enhancement Areas
- **Advanced Analytics**: Delivery tracking and reporting
- **Template Library**: Pre-built content templates
- **CRM Integration**: Contact management features
- **A/B Testing**: Content variation testing
- **Scheduled Sending**: Time-based campaign execution

---

## Development Commands

### Setup
```bash
mkdir email_marketing_system && cd email_marketing_system
mkdir -p data/{smtp_configs,leads,outputs,temp}
```

### Testing
```bash
python -m pytest tests/
python -m unittest test_smtp_manager.py
```

### Deployment
```bash
streamlit run core/app.py
npx localtunnel --port 8501
```

This system represents a production-ready email marketing solution with enterprise-grade features while maintaining simplicity and maintainability for rapid development and deployment.