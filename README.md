# Ai Mailer Lite

AI-powered email marketing system - A comprehensive email marketing automation system designed for Google Colab deployment with multi-SMTP support, GMass integration, and advanced content generation capabilities.

## Features

- **11-Step Workflow**: Complete email marketing automation from SMTP setup to delivery
- **Multi-SMTP Concurrency**: Handle as many SMTP accounts as provided
- **GMass Integration**: Automated inbox testing and scoring
- **Content Variety**: 5 distinct content types including AI-generated spintax
- **Lead Management**: Automated distribution and CSV cleanup
- **Colab-Optimized**: Single-environment deployment with web interface

## Quick Start

### 1. Installation

```bash
# Clone or download the project
git clone <repository-url>
cd email-marketing-system

# Install dependencies
pip install -r requirements.txt
```

### 2. Google Colab Setup

```python
# In Google Colab, run:
!git clone <repository-url>
%cd email-marketing-system
!pip install -r requirements.txt

# Run the application
!streamlit run app.py &
!npx localtunnel --port 8501
```

### 3. Configuration

#### SMTP Setup
1. Copy `data/smtp_configs/smtp_config_template.csv` to create your SMTP configuration
2. Fill in your email credentials:
   - **Gmail**: Use app-specific passwords
   - **Outlook**: Use regular password or app password
   - **Yahoo**: Use app-specific passwords

#### Lead Data
1. Prepare your CSV file with required columns:
   - `email` (required)
   - `firstname` (optional)
   - `lastname` (optional)
   - `company` (optional)
   - `phone` (optional)

### 4. Usage

1. **Launch the application**:
   ```bash
   streamlit run app.py
   ```

2. **Follow the 11-step workflow**:
   - Step 1: Upload SMTP configurations
   - Step 2: Upload lead data
   - Step 3: Configure phone number handling
   - Step 4: Select content type
   - Step 5: Choose attachment format
   - Step 6: Set phone placement options
   - Step 7: Configure personalization
   - Step 8: Select SMTP accounts
   - Step 9: Set email limits
   - Step 10: Run GMass testing (optional)
   - Step 11: Execute email campaign

## Content Types

### 1. Short Spintax
Python-based spintax with AI enhancement for brief, varied messages.

### 2. Long Spintax
Extended spintax format with comprehensive randomization.

### 3. HTML Templates
AI-generated HTML emails with inline styling and responsive design.

### 4. Table Format
Structured data presentation in clean table layouts.

### 5. HTML-to-Image
Selenium-based conversion of HTML content to image format.

## SMTP Configuration

### Supported Providers

| Provider | SMTP Server | Port | Security |
|----------|-------------|------|----------|
| Gmail | smtp.gmail.com | 587 | TLS |
| Outlook | smtp-mail.outlook.com | 587 | TLS |
| Yahoo | smtp.mail.yahoo.com | 587 | TLS |
| Custom | Your SMTP server | Custom | TLS/SSL |

### Configuration Format

**JSON Format:**
```json
[
  {
    "email": "your_email@gmail.com",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "your_email@gmail.com",
    "password": "your_app_password",
    "use_tls": true,
    "daily_limit": 100,
    "from_name": "Your Name"
  }
]
```

**CSV Format:**
```csv
email,password
your_email@gmail.com,your_app_password
```

**Note:** Gmail SMTP settings are automatically configured (smtp.gmail.com:587).

## API Keys Setup

### Google Gemini API
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set environment variable: `GEMINI_API_KEY=your_api_key`

### GMass Integration
1. Create GMass account
2. Configure login credentials in the interface

## File Structure

```
email-marketing-system/
├── app.py                 # Main Streamlit interface
├── smtp_manager.py        # SMTP account management
├── content_generator.py   # Content generation engine
├── gmass_tester.py        # GMass automation
├── email_sender.py        # Email sending engine
├── utils.py               # Utility functions
├── colab_setup.py         # Colab deployment helper
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── claude.md             # Project documentation
└── data/
    ├── smtp_configs/      # SMTP configuration files
    ├── leads/             # Lead CSV files
    ├── outputs/           # Campaign results
    └── temp/              # Temporary files
```

## Advanced Features

### Multi-SMTP Concurrency
- Automatic load distribution across SMTP accounts
- Rate limiting (4-6 seconds between emails)
- Individual account failure handling
- Real-time progress tracking

### GMass Integration
- Automated inbox testing
- Deliverability scoring
- Spam detection
- Promotional folder detection

### Content Personalization
- Dynamic firstname/lastname insertion
- Company name integration
- Phone number formatting
- Click-to-call functionality

## Troubleshooting

### Common Issues

1. **SMTP Authentication Failed**
   - Enable 2FA and use app-specific passwords
   - Check SMTP server settings
   - Verify credentials

2. **Gmail Blocked Account**
   - Use app-specific passwords
   - Enable "Less secure app access" (if available)
   - Check daily sending limits

3. **Streamlit Not Loading**
   - Check port availability (8501)
   - Verify firewall settings
   - Try different port with `--server.port 8502`

4. **GMass Testing Failed**
   - Verify Chrome browser installation
   - Check internet connectivity
   - Update ChromeDriver

### Performance Optimization

1. **Large Lead Lists**
   - Process in batches of 1000-5000
   - Monitor memory usage
   - Use CSV chunking for very large files

2. **Slow Sending**
   - Reduce concurrent SMTP accounts
   - Increase delay between emails
   - Check internet bandwidth

## Development

### Running Tests
```bash
python -m pytest tests/
python -m unittest test_smtp_manager.py
```

### Local Development
```bash
# Install in development mode
pip install -e .

# Run with hot reload
streamlit run app.py --server.runOnSave true
```

## Security Considerations

- Store SMTP credentials securely
- Use environment variables for API keys
- Implement rate limiting to prevent abuse
- Monitor sending patterns for compliance
- Regular security updates

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the sample configurations
3. Open an issue on GitHub
4. Contact support team

## Version History

- **v1.0.0**: Initial release with core functionality
- **v1.1.0**: Added GMass integration
- **v1.2.0**: Enhanced content generation
- **v1.3.0**: Improved Colab support

---

**Note**: This system is designed for legitimate email marketing purposes. Ensure compliance with anti-spam laws and email marketing regulations in your jurisdiction.
