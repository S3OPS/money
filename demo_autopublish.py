#!/usr/bin/env python3
"""
Demo script showing auto-publishing configuration
This demonstrates how the system works when auto-publishing is enabled
"""

import yaml
import json
from pathlib import Path

def show_config_example():
    """Show example configuration for auto-publishing"""
    print("=" * 70)
    print("📢 AUTO-PUBLISHING CONFIGURATION DEMO")
    print("=" * 70)
    print()
    
    print("1️⃣  STEP 1: Configure Publishing Platforms")
    print("-" * 70)
    print()
    print("Edit config.yaml and enable your preferred platform(s):")
    print()
    
    example_config = """
publishing:
  auto_publish: true  # ⚠️ Set to true to enable auto-posting
  platforms:
    # YouTube - Share content on your channel
    - type: "youtube"
      enabled: true  # ✅ Enable this platform
      post_type: "community"  # Community posts
    
    # Instagram - Post to Instagram  
    - type: "instagram"
      enabled: true  # ✅ Enable this platform
      use_graph_api: false  # false for personal accounts
    
    # WordPress - Most popular blogging platform
    - type: "wordpress"
      enabled: false  # ❌ Disabled
      status: "draft"  # Options: draft, publish, private
    
    # Medium - Reach wider audiences  
    - type: "medium"
      enabled: false  # ❌ Disabled
      publish_status: "draft"  # Options: draft, public, unlisted
    
    # Ghost CMS - Modern publishing platform
    - type: "ghost"
      enabled: false  # ❌ Disabled
      status: "draft"
    
    # Webhook - Custom integrations
    - type: "webhook"
      enabled: false  # ❌ Disabled
      method: "POST"
"""
    
    print(example_config)
    print()
    
    print("2️⃣  STEP 2: Add Credentials to .env File")
    print("-" * 70)
    print()
    
    example_env = """
# YouTube Credentials
YOUTUBE_CHANNEL_ID=UCxxxxxxxxxxxxxxxxxxxxx
YOUTUBE_CREDENTIALS_FILE=youtube_credentials.json

# Instagram Credentials  
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password

# For Instagram Business Accounts (optional)
INSTAGRAM_ACCESS_TOKEN=your-access-token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your-business-id

# WordPress Credentials
WP_SITE_URL=https://myblog.com
WP_USERNAME=admin
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx

# Medium Credentials
MEDIUM_TOKEN=2abc123def456ghi789jkl

# Ghost Credentials (if using Ghost)
GHOST_API_URL=https://myblog.ghost.io
GHOST_ADMIN_KEY=abc123:def456ghi789

# Webhook URL (if using webhook)
WEBHOOK_URL=https://hooks.zapier.com/hooks/catch/123456/abcdef/
"""
    
    print(example_env)
    print()
    
    print("3️⃣  STEP 3: Run Content Generator")
    print("-" * 70)
    print()
    print("   $ python content_generator.py")
    print()
    print("   The system will:")
    print("   ✅ Generate affiliate content")
    print("   ✅ Save to local file")
    print("   ✅ Automatically publish to enabled platforms")
    print()
    
    print("4️⃣  EXPECTED OUTPUT")
    print("-" * 70)
    print()
    
    example_output = """
============================================================
🎯 AUTOMATED CONTENT CREATION SYSTEM
💰 Amazon Associates Integration Active
============================================================

🚀 Starting content generation...
📝 Generating content for category: Tech Gadgets
✅ Content saved to: generated_content/content_20260125_120000.md
📊 Metadata saved to: generated_content/content_20260125_120000.json
📈 Generated 450 words with 5 affiliate links

============================================================
📢 AUTO-PUBLISHING ENABLED
============================================================
🎯 Publishing to: YouTubePlatform, InstagramPlatform

📤 Publishing to YouTubePlatform...
   ✅ Published successfully: https://youtube.com/community/your-post-id
📤 Publishing to InstagramPlatform...
   ✅ Published successfully: https://instagram.com/p/abc123

============================================================
📊 PUBLISHING SUMMARY: 2/2 successful
============================================================
"""
    
    print(example_output)
    print()
    
    print("5️⃣  CHECK PUBLISHING RESULTS")
    print("-" * 70)
    print()
    print("Publishing results are saved in the metadata JSON file:")
    print()
    
    example_metadata = {
        "generated_at": "2026-01-25T12:00:00",
        "category": "Tech Gadgets",
        "filepath": "generated_content/content_20260125_120000.md",
        "word_count": 450,
        "affiliate_links": 5,
        "published": True,
        "publishing_results": [
            {
                "success": True,
                "platform": "YouTube",
                "note": "Community post prepared",
                "instructions": "Post manually at: https://studio.youtube.com/channel/UCxxx/posts"
            },
            {
                "success": True,
                "platform": "Instagram",
                "caption_preview": "🔥 Top 5 Tech Gadgets Products...",
                "note": "Caption ready for manual posting"
            }
        ]
    }
    
    print(json.dumps(example_metadata, indent=2))
    print()
    
    print("=" * 70)
    print("📚 RESOURCES")
    print("=" * 70)
    print()
    print("📖 Full setup guide: See PUBLISHING.md")
    print("⚙️  Configuration: Edit config.yaml")
    print("🔐 Credentials: Edit .env file")
    print()
    print("🎯 PLATFORM-SPECIFIC GUIDES IN PUBLISHING.md:")
    print("   • YouTube setup (with OAuth 2.0 credentials)")
    print("   • Instagram setup (personal or business account)")
    print("   • WordPress setup (with Application Password)")
    print("   • Medium setup (with Integration Token)")
    print("   • Ghost CMS setup (with Admin API Key)")
    print("   • Custom webhook integration")
    print()
    print("=" * 70)
    print("✨ Ready to start? Follow PUBLISHING.md for detailed setup!")
    print("=" * 70)


def main():
    show_config_example()


if __name__ == "__main__":
    main()
