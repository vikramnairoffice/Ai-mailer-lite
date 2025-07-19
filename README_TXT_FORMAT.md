# 📧 TXT Format Support for SMTP Accounts

## Overview
The Email Marketing System now supports uploading SMTP accounts in **TXT format** - a simple, comma-separated format that's easy to create and manage.

## Supported Formats

### 1. **TXT Format** (New!)
Simple comma-separated format: `email,password`
```
user1@gmail.com,password123
user2@gmail.com,password456
user3@gmail.com,password789
```

### 2. **CSV Format**
Structured format with headers:
```csv
email,password
user@gmail.com,password123
```

**Note:** Gmail SMTP settings are automatically configured (smtp.gmail.com:587).

### 3. **JSON Format**
Structured JSON array:
```json
[
  {"email": "user@gmail.com", "password": "password123"},
  {"email": "user2@gmail.com", "password": "password456"}
]
```

## TXT Format Features

### ✅ **Supported Cases:**
- **Basic format**: `email@domain.com,password`
- **Passwords with spaces**: `email@domain.com,pass word 123`
- **Passwords with commas**: `email@domain.com,pass,word,123`
- **Extra whitespace**: ` email@domain.com , password `
- **Empty lines**: Automatically skipped

### ❌ **Invalid Cases:**
- **Invalid email format**: `invalid-email,password`
- **Missing password**: `email@domain.com`
- **Empty password**: `email@domain.com,`
- **No comma separator**: `email@domain.com password`

## Example Usage

### Step 1: Create Your TXT File
Create a file named `my_smtp_accounts.txt`:
```
john@gmail.com,mypassword123
jane@outlook.com,securepass456
admin@company.com,admin password 789
marketing@business.com,marketing,pass,2024
```

### Step 2: Upload in Application
1. Open the Email Marketing System
2. Go to **Step 1: Upload SMTP Accounts**
3. Click **"Upload SMTP file"**
4. Select your `.txt` file
5. The system will automatically parse and validate all accounts

### Step 3: Review Results
The system will show:
- ✅ **Valid accounts loaded**: Number of successfully parsed accounts
- ⚠️ **Warning messages**: For any invalid lines (with line numbers)
- 📄 **Processing summary**: Total lines processed vs. valid accounts

## Advanced Features

### **Automatic SMTP Detection**
The system automatically detects SMTP settings based on email domain:
- `@gmail.com` → `smtp.gmail.com:587`
- `@outlook.com` → `smtp.outlook.com:587`
- `@yahoo.com` → `smtp.mail.yahoo.com:587`
- And many more...

### **Error Handling**
- **Line-by-line validation**: Each line is checked independently
- **Graceful failures**: Invalid lines are skipped with warnings
- **Detailed feedback**: Shows exactly what went wrong and on which line

### **Security**
- **No data storage**: TXT files are processed in memory only
- **Password protection**: Passwords are handled securely
- **Validation**: Basic email format validation prevents errors

## Migration from Other Formats

### From CSV:
```csv
email,password
user@gmail.com,password123
```
**To TXT:**
```
user@gmail.com,password123
```

### From Manual Lists:
If you have accounts in any format, just arrange them as:
```
email1,password1
email2,password2
email3,password3
```

## Best Practices

1. **File Naming**: Use descriptive names like `gmail_accounts.txt`
2. **Backup**: Keep a backup of your account files
3. **Testing**: Test with a small file first
4. **Security**: Don't share account files publicly
5. **Validation**: Check the upload results for any warnings

## Troubleshooting

### Common Issues:
- **"Invalid email format"**: Check for missing @ or domain
- **"Invalid format"**: Ensure comma separator exists
- **"No valid accounts"**: Check file encoding (should be UTF-8)

### Tips:
- Use a plain text editor (not Word)
- Ensure each line has exactly one comma
- Don't include header lines
- Save as UTF-8 encoding

## Example Files

Check the project directory for:
- `sample_smtp.txt` - Real-world example
- `test_smtp_accounts.txt` - Simple test file

---

**📧 Ready to use TXT format for your SMTP accounts!**