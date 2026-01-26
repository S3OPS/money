# 🚀 Quick Setup Guide: YouTube & Instagram

This guide will help you quickly set up YouTube and Instagram posting for your automated content system.

## ✅ What's Changed

The system now posts to **YouTube** and **Instagram** instead of WordPress, Medium, and Ghost CMS:
- ✅ YouTube Community Posts enabled by default
- ✅ Instagram posts enabled by default
- ✅ Other platforms (WordPress, Medium, Ghost) disabled by default

## 🎯 Quick Start (5 minutes)

### Step 1: Choose Your Setup Method

**Option A: YouTube Setup** (Recommended to start with)
- Best for text-based content
- Requires Google Cloud project setup (one-time)
- Posts appear as YouTube Community posts

**Option B: Instagram Setup**
- Best for visual content
- Requires images (not included yet)
- Currently prepares captions for manual posting

### Step 2: YouTube Setup

1. **Create Google Cloud Project** (one-time setup):
   - Go to https://console.cloud.google.com/
   - Create a new project
   - Enable "YouTube Data API v3"
   - Create OAuth 2.0 credentials (Desktop app)
   - Download the credentials JSON file

2. **Get Your YouTube Channel ID**:
   - Go to https://studio.youtube.com/
   - Click Settings → Channel → Advanced settings
   - Copy your Channel ID

3. **Configure Environment**:
   ```bash
   # Edit .env file
   YOUTUBE_CHANNEL_ID=UCxxxxxxxxxxxxxxxxxxxxx
   YOUTUBE_CREDENTIALS_FILE=youtube_credentials.json
   ```

4. **Place Credentials File**:
   - Save the downloaded OAuth JSON as `youtube_credentials.json` in the project root

### Step 3: Instagram Setup

1. **For Personal Accounts**:
   ```bash
   # Edit .env file
   INSTAGRAM_USERNAME=your_username
   INSTAGRAM_PASSWORD=your_password
   ```

2. **Enable in config.yaml**:
   ```yaml
   publishing:
     auto_publish: true
     platforms:
       - type: "instagram"
         enabled: true
         use_graph_api: false  # Use false for personal accounts
   ```

## 📝 How It Works

### Current Behavior

Since both platforms have specific requirements:

**YouTube**: 
- ✅ Authenticates via OAuth 2.0
- ✅ Prepares content for community posts
- ⚠️ Requires manual posting through YouTube Studio (Community Post API requires special access)
- 📋 Provides formatted content and instructions

**Instagram**:
- ✅ Prepares captions with emojis and formatting
- ⚠️ Requires images (Instagram doesn't support text-only posts)
- 📋 Provides ready-to-use captions for manual posting

### Running the System

```bash
# Generate content (will show YouTube and Instagram ready content)
python content_generator.py

# The system will:
# 1. Generate Amazon affiliate content
# 2. Prepare it for YouTube (plain text format)
# 3. Prepare it for Instagram (emoji-formatted captions)
# 4. Provide instructions for manual posting
```

### Example Output

```
🚀 Starting content generation...
📝 Generating content for category: Tech Gadgets
✅ Content saved to: generated_content/content_20260126_120000.md

============================================================
📢 AUTO-PUBLISHING ENABLED
============================================================
🎯 Publishing to: YouTubePlatform, InstagramPlatform

📤 Publishing to YouTubePlatform...
   ✅ Content prepared for YouTube Community Post
   📋 Copy content and post at: https://studio.youtube.com/channel/UCxxx/posts
   
📤 Publishing to InstagramPlatform...
   ✅ Caption prepared for Instagram
   📋 Post manually with an image at: https://www.instagram.com/

============================================================
📊 PUBLISHING SUMMARY: 2/2 prepared successfully
============================================================
```

## 🎨 Future Enhancements

To fully automate posting, you can:

1. **For YouTube**:
   - Apply for YouTube Community Post API access (requires Google approval)
   - OR: Use YouTube Studio API when available

2. **For Instagram**:
   - Integrate with a text-to-image service (e.g., Pillow, Canva API)
   - Generate product images automatically
   - Store pre-made templates

## 📚 Detailed Documentation

For comprehensive setup guides, see:
- Full documentation: [PUBLISHING.md](PUBLISHING.md)
- Configuration options: [config.yaml](config.yaml)
- Environment variables: [.env.example](.env.example)

## 🆘 Troubleshooting

**"YouTube credentials file not found"**
- Make sure `youtube_credentials.json` is in the project root
- Check that YOUTUBE_CREDENTIALS_FILE in .env points to the correct file

**"Instagram posts require images"**
- This is expected behavior - Instagram doesn't support text-only posts
- Use the prepared caption with your own images
- Future: Integrate automatic image generation

**"No platforms enabled"**
- Check that config.yaml has `auto_publish: true`
- Verify at least one platform has `enabled: true`

## ✨ You're All Set!

Run `python content_generator.py` to start generating content for YouTube and Instagram!

For questions or issues, refer to:
- Main README: [README.md](README.md)
- Full publishing guide: [PUBLISHING.md](PUBLISHING.md)
