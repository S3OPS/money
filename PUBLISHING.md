# 📢 Automated Publishing Guide

This guide explains how to set up automated content publishing to various platforms after content generation.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Supported Platforms](#supported-platforms)
3. [Platform Setup Guides](#platform-setup-guides)
   - [WordPress](#wordpress-setup)
   - [Medium](#medium-setup)
   - [Ghost CMS](#ghost-cms-setup)
   - [Custom Webhook](#custom-webhook-setup)
4. [Configuration](#configuration)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)

## Quick Start

### 1. Enable Auto-Publishing

Edit `config.yaml` and set:

```yaml
publishing:
  auto_publish: true  # Enable automatic publishing
```

### 2. Configure a Platform

Choose and configure at least one platform (see platform-specific guides below).

### 3. Run Content Generator

```bash
python content_generator.py
```

Content will be generated AND automatically published to your configured platforms!

## Supported Platforms

- ✅ **YouTube** - Post content to YouTube Community (NEW!)
- ✅ **Instagram** - Share content on Instagram (NEW!)
- ✅ **WordPress** - Most popular blogging platform
- ✅ **Medium** - Great for reaching wider audiences
- ✅ **Ghost CMS** - Modern, fast publishing platform
- ✅ **Webhook** - For custom integrations

## Platform Setup Guides

### YouTube Setup

YouTube is a great platform for sharing content with your audience through Community posts.

#### Prerequisites
- A YouTube channel
- Google Cloud project with YouTube Data API v3 enabled
- OAuth 2.0 credentials

#### Step 1: Create Google Cloud Project and Enable YouTube API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **YouTube Data API v3**:
   - Go to "APIs & Services" → "Library"
   - Search for "YouTube Data API v3"
   - Click "Enable"

#### Step 2: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Select "Desktop app" as the application type
4. Name it (e.g., "Content Publisher")
5. Click "Create"
6. Download the credentials JSON file
7. Save it as `youtube_credentials.json` in your project directory

#### Step 3: Get Your Channel ID

1. Go to [YouTube Studio](https://studio.youtube.com/)
2. Click on "Settings" → "Channel"
3. Click "Advanced settings"
4. Copy your Channel ID

#### Step 4: Configure Environment Variables

Add to your `.env` file:

```bash
YOUTUBE_CHANNEL_ID=your-channel-id-here
YOUTUBE_CREDENTIALS_FILE=youtube_credentials.json
```

#### Step 5: Enable in Config

Edit `config.yaml`:

```yaml
publishing:
  auto_publish: true
  platforms:
    - type: "youtube"
      enabled: true
      post_type: "community"
```

#### Notes

- **First-time setup**: The first time you run the script, it will open a browser window for OAuth authentication
- **Community posts**: The system prepares content for YouTube Community posts (text-based)
- **Character limits**: YouTube Community posts have a 5,000 character limit
- **Token storage**: Your authentication token is saved as `youtube_token.pickle` for future use

#### Publishing Options

- `post_type: "community"` - Text-based community posts (recommended for markdown content)

---

### Instagram Setup

Instagram is perfect for visual content and reaching a social media audience.

#### Prerequisites
- An Instagram account (personal or business)
- For personal accounts: Username and password
- For business accounts: Facebook Page connected to Instagram, access token

#### Method 1: Personal Account (Using instagrapi)

This method uses the unofficial `instagrapi` library for personal accounts.

##### Step 1: Configure Environment Variables

Add to your `.env` file:

```bash
INSTAGRAM_USERNAME=your-instagram-username
INSTAGRAM_PASSWORD=your-instagram-password
```

##### Step 2: Enable in Config

Edit `config.yaml`:

```yaml
publishing:
  auto_publish: true
  platforms:
    - type: "instagram"
      enabled: true
      use_graph_api: false
```

#### Method 2: Business Account (Using Instagram Graph API)

This method uses the official Instagram Graph API for business/creator accounts.

##### Prerequisites
- Instagram Business or Creator account
- Facebook Page connected to your Instagram account
- Facebook Developer account

##### Step 1: Set Up Facebook App

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app or use an existing one
3. Add "Instagram Graph API" product
4. Get a User Access Token with `instagram_basic` and `instagram_content_publish` permissions

##### Step 2: Get Your Business Account ID

1. Use the Graph API Explorer to call:
   ```
   GET /me/accounts
   ```
2. Find your Facebook Page ID
3. Call:
   ```
   GET /{page-id}?fields=instagram_business_account
   ```
4. Get your Instagram Business Account ID

##### Step 3: Configure Environment Variables

Add to your `.env` file:

```bash
INSTAGRAM_ACCESS_TOKEN=your-access-token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your-business-account-id
```

##### Step 4: Enable in Config

Edit `config.yaml`:

```yaml
publishing:
  auto_publish: true
  platforms:
    - type: "instagram"
      enabled: true
      use_graph_api: true
```

#### Important Notes

- **Image requirement**: Instagram posts require images. The current implementation prepares captions for manual posting
- **Caption limits**: Instagram captions are limited to 2,200 characters
- **Hashtags**: Add relevant hashtags to increase reach
- **Links**: Instagram doesn't support clickable links in captions (except for business accounts with 10k+ followers)
- **Manual posting**: Currently, the system prepares content for manual posting or requires additional image generation

#### Future Enhancement

To fully automate Instagram posting, you can:
1. Generate images with text overlays using PIL/Pillow
2. Use a text-to-image service
3. Store pre-made product images

---

### WordPress Setup

WordPress is one of the most popular blogging platforms. Here's how to set it up:

#### Prerequisites
- A WordPress site (self-hosted or WordPress.com)
- Admin access to your site
- WordPress REST API enabled (enabled by default in WordPress 4.7+)

#### Step 1: Create Application Password

1. Log into your WordPress admin panel
2. Go to **Users** → **Profile**
3. Scroll down to **Application Passwords**
4. Enter a name (e.g., "Content Generator")
5. Click **Add New Application Password**
6. Copy the generated password (it will only be shown once!)

#### Step 2: Configure Environment Variables

Add to your `.env` file:

```bash
WP_SITE_URL=https://yoursite.com
WP_USERNAME=your-admin-username
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```

#### Step 3: Enable in Config

Edit `config.yaml`:

```yaml
publishing:
  auto_publish: true
  platforms:
    - type: "wordpress"
      enabled: true
      status: "draft"  # or "publish" to auto-publish immediately
```

#### Publishing Options

- `status: "draft"` - Save as draft (recommended for review before publishing)
- `status: "publish"` - Publish immediately
- `status: "private"` - Private posts (only visible to admins)

---

### Medium Setup

Medium is great for reaching a wider audience with your content.

#### Prerequisites
- A Medium account
- Medium Integration Token

#### Step 1: Get Integration Token

1. Log into Medium
2. Go to **Settings** → **Security and apps**
3. Scroll to **Integration tokens**
4. Enter a description (e.g., "Content Generator")
5. Click **Get integration token**
6. Copy the token

#### Step 2: Configure Environment Variables

Add to your `.env` file:

```bash
MEDIUM_TOKEN=your-integration-token-here
```

#### Step 3: Enable in Config

Edit `config.yaml`:

```yaml
publishing:
  auto_publish: true
  platforms:
    - type: "medium"
      enabled: true
      publish_status: "draft"  # draft, public, or unlisted
```

#### Publishing Options

- `publish_status: "draft"` - Save as draft
- `publish_status: "public"` - Publish publicly
- `publish_status: "unlisted"` - Unlisted (accessible via link only)

#### Notes

- Medium allows maximum 5 tags per post
- Medium converts markdown automatically
- All posts appear on your Medium profile

---

### Ghost CMS Setup

Ghost is a modern, fast, and powerful publishing platform.

#### Prerequisites
- A Ghost site (self-hosted or Ghost.org)
- Admin access
- Ghost Admin API key

#### Step 1: Create Admin API Key

1. Log into Ghost admin panel
2. Go to **Settings** → **Integrations**
3. Click **Add custom integration**
4. Enter a name (e.g., "Content Generator")
5. Click **Create**
6. Copy the **Admin API Key** (format: `id:secret`)

#### Step 2: Configure Environment Variables

Add to your `.env` file:

```bash
GHOST_API_URL=https://yoursite.com
GHOST_ADMIN_KEY=your-key-id:your-secret
```

#### Step 3: Enable in Config

Edit `config.yaml`:

```yaml
publishing:
  auto_publish: true
  platforms:
    - type: "ghost"
      enabled: true
      status: "draft"  # draft or published
```

#### Publishing Options

- `status: "draft"` - Save as draft
- `status: "published"` - Publish immediately

---

### Custom Webhook Setup

Use webhooks to integrate with any custom platform or service.

#### Use Cases

- Custom CMS or platform
- Zapier/Make.com automation
- Discord/Slack notifications
- Custom processing pipeline

#### Step 1: Set Up Webhook Endpoint

Create an endpoint that accepts POST requests with this format:

```json
{
  "title": "Post Title",
  "content": "Post content in markdown",
  "metadata": {
    "category": "Tech Gadgets",
    "generated_at": "2026-01-25T10:00:00",
    "word_count": 500,
    "affiliate_links": 5
  },
  "timestamp": "2026-01-25T10:00:00"
}
```

#### Step 2: Configure Environment Variables

Add to your `.env` file:

```bash
WEBHOOK_URL=https://your-webhook-endpoint.com/publish
```

#### Step 3: Enable in Config

Edit `config.yaml`:

```yaml
publishing:
  auto_publish: true
  platforms:
    - type: "webhook"
      enabled: true
      method: "POST"  # or "PUT"
      headers:
        Content-Type: "application/json"
        # Add custom headers if needed
        # Authorization: "Bearer your-token"
```

#### Example: Zapier Integration

1. Create a Zapier Zap with **Webhooks by Zapier** trigger
2. Use **Catch Hook** to get a webhook URL
3. Add the URL to your `.env` as `WEBHOOK_URL`
4. Test by running `python content_generator.py`
5. Build your Zap to do whatever you want with the content!

---

## Configuration

### Publishing All Platforms Simultaneously

You can enable multiple platforms to publish to all of them at once:

```yaml
publishing:
  auto_publish: true
  platforms:
    - type: "wordpress"
      enabled: true
      status: "draft"
    
    - type: "medium"
      enabled: true
      publish_status: "draft"
    
    - type: "webhook"
      enabled: true
      webhook_url: "https://your-webhook.com"
```

### Selective Publishing

Enable only the platforms you want:

```yaml
publishing:
  auto_publish: true
  platforms:
    - type: "wordpress"
      enabled: true  # ✅ Will publish
    
    - type: "medium"
      enabled: false  # ❌ Won't publish
```

---

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
    
    # Test publish
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

---

## Troubleshooting

### WordPress Issues

**Error: "REST API is disabled"**
- Solution: Enable REST API in your WordPress settings
- Check: Settings → Permalinks must not be set to "Plain"

**Error: "Invalid username or password"**
- Solution: Use Application Password, not your regular password
- Generate new Application Password if needed

**Error: "Could not create post"**
- Check: User has permission to create posts
- Verify: WordPress site URL is correct (with https://)

### Medium Issues

**Error: "Invalid access token"**
- Solution: Generate a new integration token
- Check: Token is correctly copied (no extra spaces)

**Error: "Too many tags"**
- Medium limit: Maximum 5 tags
- Solution: The system automatically limits to 5 tags

### Ghost Issues

**Error: "Invalid API key"**
- Check: API key format is `id:secret` (with colon)
- Verify: Both parts are present and correct

**Error: "Could not create post"**
- Check: Ghost site URL is correct
- Verify: Admin API access is enabled

### General Issues

**Error: "No module named 'content_publisher'"**
- Solution: Make sure you're in the correct directory
- Run: `python content_generator.py` from the project root

**Content not publishing but no errors**
- Check: `auto_publish: true` in config.yaml
- Check: At least one platform has `enabled: true`
- Verify: Credentials in `.env` are correct

**Publishing works but posts are empty**
- Check: Content is being generated successfully
- Verify: No errors in the generation step
- Review: Generated files in `generated_content/`

---

## Advanced Topics

### Customize Post Formatting

Each platform handles content differently:

- **WordPress**: Converts markdown to HTML automatically
- **Medium**: Supports native markdown
- **Ghost**: Uses markdown natively

To customize formatting for specific platforms, edit `content_publisher.py`.

### Add Custom Fields

Edit the metadata in `content_generator.py` to add custom fields:

```python
metadata = {
    'generated_at': datetime.now().isoformat(),
    'category': category,
    'tags': ['amazon', 'affiliate', 'review'],  # Add tags
    'featured_image_id': 123,  # WordPress featured image
    # Add more custom fields
}
```

### Schedule Publishing Times

WordPress example - schedule for future:

```python
# In content_publisher.py, modify WordPressPlatform.publish()
post_data = {
    'title': title,
    'content': html_content,
    'status': 'future',  # Schedule for future
    'date': '2026-01-26T09:00:00',  # ISO 8601 format
}
```

---

## Best Practices

1. **Start with Drafts**: Set status to `draft` initially to review before publishing
2. **Test First**: Test with one platform before enabling multiple
3. **Monitor Results**: Check the publishing results in metadata JSON files
4. **Backup Content**: Generated content is saved locally before publishing
5. **Review Regularly**: Periodically check published content for quality
6. **Comply with TOS**: Follow each platform's terms of service
7. **Rate Limiting**: Don't publish too frequently (respect platform limits)

---

## Support

For issues specific to:

- **WordPress**: Check WordPress REST API documentation
- **Medium**: Check Medium API documentation
- **Ghost**: Check Ghost Admin API documentation
- **This tool**: Review error messages and check configuration

---

**Happy Publishing! 🚀**
