# 📢 YouTube Publishing Guide

This guide explains how to set up automated content publishing to YouTube Community posts after content generation.

## Quick Start

### 1. Enable Auto-Publishing

Edit `config.yaml` and set:

```yaml
publishing:
  auto_publish: true  # Enable automatic publishing
```

### 2. Configure YouTube Credentials

Add to your `.env` file:

```bash
YOUTUBE_CHANNEL_ID=your-channel-id-here
YOUTUBE_CREDENTIALS_FILE=youtube_credentials.json
```

### 3. Run Content Generator

```bash
python content_generator.py
```

Content will be generated and prepared for YouTube Community posts.

## YouTube Setup

YouTube is a great platform for sharing content with your audience through Community posts.

### Prerequisites
- A YouTube channel
- Google Cloud project with YouTube Data API v3 enabled
- OAuth 2.0 credentials

### Step 1: Create Google Cloud Project and Enable YouTube API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **YouTube Data API v3**:
   - Go to "APIs & Services" → "Library"
   - Search for "YouTube Data API v3"
   - Click "Enable"

### Step 2: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Select "Desktop app" as the application type
4. Name it (e.g., "Content Publisher")
5. Click "Create"
6. Download the credentials JSON file
7. Save it as `youtube_credentials.json` in your project directory

### Step 3: Get Your Channel ID

1. Go to [YouTube Studio](https://studio.youtube.com/)
2. Click on "Settings" → "Channel"
3. Click "Advanced settings"
4. Copy your Channel ID

### Step 4: Configure Environment Variables

Add to your `.env` file:

```bash
YOUTUBE_CHANNEL_ID=your-channel-id-here
YOUTUBE_CREDENTIALS_FILE=youtube_credentials.json
```

### Step 5: Enable in Config

Edit `config.yaml`:

```yaml
publishing:
  auto_publish: true
  platforms:
    - type: "youtube"
      enabled: true
      post_type: "community"
```

### Notes

- **First-time setup**: The first time you run the script, it will open a browser window for OAuth authentication.
- **Community posts**: The system prepares content for YouTube Community posts (text-based).
- **Character limits**: YouTube Community posts have a 5,000 character limit.
- **Token storage**: Your authentication token is saved as `youtube_token.pickle` for future use.

### Publishing Options

- `post_type: "community"` - Text-based community posts (recommended for markdown content)

## Testing

### Test Without Publishing

Before enabling auto-publish, test your content generation:

```bash
python content_generator.py
```

Check the `generated_content/` folder to review the content.

### Test Publishing Configuration

Create a test script `test_publishing.py`:

```python
import yaml
from content_publisher import ContentPublisher

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

publisher = ContentPublisher(config)

if publisher.has_enabled_platforms():
    print(f"✅ Enabled platforms: {publisher.get_enabled_platform_names()}")
    
    result = publisher.publish_content(
        title="Test Post",
        content="This is a test post from the automated system.",
        metadata={'category': 'Test'}
    )
    
    print(f"Results: {result}")
else:
    print("❌ No platforms enabled")
```

Run with:

```bash
python test_publishing.py
```

## Troubleshooting

### "No module named 'content_publisher'"
- Make sure you're in the correct directory
- Run: `python content_generator.py` from the project root

### "YouTube credentials file not configured"
- Ensure `YOUTUBE_CREDENTIALS_FILE` points to your downloaded JSON file
- Keep `youtube_credentials.json` in the project root or update the path in `.env`

### "YouTube channel ID not configured"
- Check that `YOUTUBE_CHANNEL_ID` is set in `.env`
- Verify the channel ID in YouTube Studio → Settings → Channel → Advanced settings

### Content not publishing but no errors
- Check: `auto_publish: true` in config.yaml
- Check: `type: "youtube"` platform has `enabled: true`
- Verify: Credentials in `.env` are correct

## Best Practices

1. **Review content** before posting to YouTube.
2. **Store credentials securely** and never commit `.env`.
3. **Monitor YouTube policies** for community posts and automation.
4. **Test with a single post** before relying on scheduled runs.

## Support

For issues specific to YouTube:
- Check YouTube Data API documentation
- Review OAuth credential setup in Google Cloud Console
