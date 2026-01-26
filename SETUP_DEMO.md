# One-Command Setup Demo

## Running the setup script:

```bash
$ python setup_youtube_instagram.py
```

## What you'll see:

```
================================================================================
🎥 YOUTUBE & INSTAGRAM AUTOMATED SETUP
================================================================================

This script will help you configure YouTube and Instagram publishing.
Your credentials will be stored securely in the .env file.

Press Enter to start setup (or Ctrl+C to cancel)... 

────────────────────────────────────────────────────────────────────────────────
📝 Checking Dependencies
────────────────────────────────────────────────────────────────────────────────

✅ Python 3.11 detected
📦 Installing required packages...
✅ All dependencies installed successfully

────────────────────────────────────────────────────────────────────────────────
📝 YouTube Setup
────────────────────────────────────────────────────────────────────────────────

📺 YouTube requires:
   1. A YouTube Channel ID
   2. OAuth 2.0 credentials file (youtube_credentials.json)

ℹ️  To get these:
   • Go to: https://console.cloud.google.com/
   • Create a project and enable YouTube Data API v3
   • Create OAuth 2.0 credentials (Desktop app)
   • Download the JSON file and save it as 'youtube_credentials.json'

Do you want to configure YouTube now? (y/n): y

Enter your YouTube Channel ID: UCxxxxxxxxxxxxxxxxxxxxx
✅ Found credentials file: youtube_credentials.json

✅ YouTube configured:
   Channel ID: UCxxxxxxxxxxxxxxxxxxxxx
   Credentials: youtube_credentials.json

────────────────────────────────────────────────────────────────────────────────
📝 Instagram Setup
────────────────────────────────────────────────────────────────────────────────

📸 Instagram can be configured in two ways:

Option 1: Personal Account (Recommended)
   • Uses your Instagram username and password
   • Simpler setup
   • Good for most users

Option 2: Business Account
   • Uses Instagram Graph API
   • Requires Facebook Page connected to Instagram
   • More complex setup

Do you want to configure Instagram now? (y/n): y

Choose account type (1=Personal, 2=Business): 1

👤 Personal Account Setup
Enter your Instagram username: your_username
Enter your Instagram password (hidden): ********
✅ Instagram Personal Account configured

────────────────────────────────────────────────────────────────────────────────
📝 Saving Configuration
────────────────────────────────────────────────────────────────────────────────

✅ Configuration saved to .env (secure permissions set)

⚙️  Updating config.yaml to enable YouTube and Instagram...
✅ Enabled auto_publish in config.yaml

────────────────────────────────────────────────────────────────────────────────
📝 Testing Configuration
────────────────────────────────────────────────────────────────────────────────

🧪 Running system tests...
✅ All tests passed!
   ✅ PASS: Import Dependencies
   ✅ PASS: Config File
   ✅ PASS: Amazon Link Generator
   ✅ PASS: Content Generation
   ✅ PASS: File Saving
   ✅ PASS: Content Publisher
   ✅ PASS: System Integration
   🎉 ALL TESTS PASSED! System is ready to use.

================================================================================
✨ SETUP COMPLETE!
================================================================================

📋 What was configured:
   ✅ YouTube credentials added to .env
   ✅ Instagram credentials added to .env

🎯 Next Steps:

1. 🎥 YouTube:
   • Ensure 'youtube_credentials.json' is in the project directory
   • Run the generator - first time will open browser for OAuth

2. 📸 Instagram:
   • Add product images (Instagram requires images)
   • System will prepare captions for you

3. 🚀 Generate Content:
   python content_generator.py

4. 📖 Documentation:
   • Quick guide: YOUTUBE_INSTAGRAM_SETUP.md
   • Full guide: PUBLISHING.md
   • Main README: README.md

🔒 Security Note:
   Your credentials are stored in .env with restricted permissions.
   Never commit .env to version control (it's in .gitignore).

================================================================================
```

## Key Features:

✅ **Interactive prompts** - Guides you through each step
✅ **Secure input** - Passwords are hidden during typing
✅ **Automatic validation** - Tests configuration after setup
✅ **Clear next steps** - Shows exactly what to do next
✅ **Safe defaults** - Sensible choices for most users
✅ **Error handling** - Gracefully handles missing files/credentials

## Time to complete:
- **With credentials ready**: 2-3 minutes
- **First time setup**: 5-10 minutes (includes getting YouTube OAuth credentials)
