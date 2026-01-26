#!/usr/bin/env python3
"""
Content Publisher Module
Automatically publishes generated content to various platforms
"""

import os
import requests
import json
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class PublishingPlatform:
    """Base class for publishing platforms"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.enabled = config.get('enabled', False)
    
    def publish(self, title: str, content: str, metadata: Dict) -> Dict:
        """Publish content to the platform. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement publish()")
    
    def is_enabled(self) -> bool:
        """Check if this platform is enabled"""
        return self.enabled


class WordPressPlatform(PublishingPlatform):
    """WordPress publishing via REST API"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.site_url = os.getenv('WP_SITE_URL') or config.get('site_url')
        self.username = os.getenv('WP_USERNAME') or config.get('username')
        self.app_password = os.getenv('WP_APP_PASSWORD') or config.get('app_password')
        self.status = config.get('status', 'draft')  # publish, draft, private
        
    def publish(self, title: str, content: str, metadata: Dict) -> Dict:
        """Publish to WordPress using REST API"""
        if not all([self.site_url, self.username, self.app_password]):
            raise ValueError("WordPress credentials not configured")
        
        # Convert markdown to HTML for WordPress
        html_content = self._markdown_to_html(content)
        
        # Prepare the post
        url = f"{self.site_url.rstrip('/')}/wp-json/wp/v2/posts"
        
        post_data = {
            'title': title,
            'content': html_content,
            'status': self.status,
            'categories': [self._get_default_category_id()],
        }
        
        # Add featured image if available
        if 'featured_image_id' in metadata:
            post_data['featured_media'] = metadata['featured_image_id']
        
        # Publish the post
        response = requests.post(
            url,
            auth=(self.username, self.app_password),
            json=post_data,
            headers={'Content-Type': 'application/json'}
        )
        
        response.raise_for_status()
        result = response.json()
        
        return {
            'success': True,
            'platform': 'WordPress',
            'post_id': result.get('id'),
            'url': result.get('link'),
            'status': result.get('status')
        }
    
    def _markdown_to_html(self, markdown_text: str) -> str:
        """Convert markdown to HTML (basic conversion)"""
        # For basic conversion - in production, use a proper markdown library
        html = markdown_text
        
        # Convert headers
        import re
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # Convert bold
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        
        # Convert links
        html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
        
        # Convert line breaks to paragraphs
        paragraphs = html.split('\n\n')
        html = ''.join([f'<p>{p}</p>' for p in paragraphs if p.strip()])
        
        return html
    
    def _get_default_category_id(self) -> int:
        """Get default category ID for WordPress posts
        
        Returns the default 'Uncategorized' category (ID: 1).
        For production use, implement category lookup/creation via WordPress API.
        """
        # Return default category ID (Uncategorized)
        return 1


class MediumPlatform(PublishingPlatform):
    """Medium publishing via API"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.integration_token = os.getenv('MEDIUM_TOKEN') or config.get('integration_token')
        self.publish_status = config.get('publish_status', 'draft')  # draft, public, unlisted
        
    def publish(self, title: str, content: str, metadata: Dict) -> Dict:
        """Publish to Medium using API"""
        if not self.integration_token:
            raise ValueError("Medium integration token not configured")
        
        # Get user ID
        user_response = requests.get(
            'https://api.medium.com/v1/me',
            headers={'Authorization': f'Bearer {self.integration_token}'}
        )
        user_response.raise_for_status()
        user_id = user_response.json()['data']['id']
        
        # Publish post
        post_data = {
            'title': title,
            'contentFormat': 'markdown',
            'content': content,
            'publishStatus': self.publish_status,
            'tags': metadata.get('tags', [])[:5]  # Medium allows max 5 tags
        }
        
        response = requests.post(
            f'https://api.medium.com/v1/users/{user_id}/posts',
            headers={
                'Authorization': f'Bearer {self.integration_token}',
                'Content-Type': 'application/json'
            },
            json=post_data
        )
        
        response.raise_for_status()
        result = response.json()['data']
        
        return {
            'success': True,
            'platform': 'Medium',
            'post_id': result.get('id'),
            'url': result.get('url'),
            'status': result.get('publishStatus')
        }


class GhostPlatform(PublishingPlatform):
    """Ghost CMS publishing via Admin API"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.api_url = os.getenv('GHOST_API_URL') or config.get('api_url')
        self.admin_api_key = os.getenv('GHOST_ADMIN_KEY') or config.get('admin_api_key')
        self.status = config.get('status', 'draft')  # draft, published
        
    def publish(self, title: str, content: str, metadata: Dict) -> Dict:
        """Publish to Ghost CMS using Admin API"""
        if not all([self.api_url, self.admin_api_key]):
            raise ValueError("Ghost CMS credentials not configured")
        
        # Generate JWT token for Ghost
        import jwt
        import time
        
        # Split the key into ID and SECRET with validation
        if ':' not in self.admin_api_key:
            raise ValueError("Ghost Admin API key must be in format 'id:secret'")
        
        parts = self.admin_api_key.split(':', 1)  # Split on first colon only
        if len(parts) != 2 or not parts[0] or not parts[1]:
            raise ValueError("Invalid Ghost Admin API key format. Expected 'id:secret'")
        
        id, secret = parts
        
        # Validate hex secret
        try:
            secret_bytes = bytes.fromhex(secret)
        except ValueError as e:
            raise ValueError(f"Ghost Admin API secret must be a valid hexadecimal string: {e}")
        
        # Prepare header and payload
        iat = int(time.time())
        header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
        payload = {
            'iat': iat,
            'exp': iat + 5 * 60,
            'aud': '/admin/'
        }
        
        token = jwt.encode(payload, secret_bytes, algorithm='HS256', headers=header)
        
        # Prepare post data
        post_data = {
            'posts': [{
                'title': title,
                'markdown': content,
                'status': self.status,
                'tags': [{'name': metadata.get('category', 'General')}]
            }]
        }
        
        # Publish
        url = f"{self.api_url.rstrip('/')}/ghost/api/admin/posts/"
        response = requests.post(
            url,
            headers={
                'Authorization': f'Ghost {token}',
                'Content-Type': 'application/json'
            },
            json=post_data
        )
        
        response.raise_for_status()
        result = response.json()['posts'][0]
        
        return {
            'success': True,
            'platform': 'Ghost',
            'post_id': result.get('id'),
            'url': result.get('url'),
            'status': result.get('status')
        }


class WebhookPlatform(PublishingPlatform):
    """Generic webhook for custom integrations"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.webhook_url = os.getenv('WEBHOOK_URL') or config.get('webhook_url')
        self.headers = config.get('headers', {})
        self.method = config.get('method', 'POST').upper()
        
    def publish(self, title: str, content: str, metadata: Dict) -> Dict:
        """Send content to webhook"""
        if not self.webhook_url:
            raise ValueError("Webhook URL not configured")
        
        payload = {
            'title': title,
            'content': content,
            'metadata': metadata,
            'timestamp': datetime.now().isoformat()
        }
        
        if self.method == 'POST':
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers=self.headers
            )
        elif self.method == 'PUT':
            response = requests.put(
                self.webhook_url,
                json=payload,
                headers=self.headers
            )
        else:
            raise ValueError(f"Unsupported HTTP method: {self.method}")
        
        response.raise_for_status()
        
        return {
            'success': True,
            'platform': 'Webhook',
            'status_code': response.status_code,
            'response': response.text[:200]  # First 200 chars of response
        }


class YouTubePlatform(PublishingPlatform):
    """YouTube publishing via YouTube Data API v3"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.api_key = os.getenv('YOUTUBE_API_KEY') or config.get('api_key')
        self.channel_id = os.getenv('YOUTUBE_CHANNEL_ID') or config.get('channel_id')
        self.credentials_file = os.getenv('YOUTUBE_CREDENTIALS_FILE') or config.get('credentials_file')
        self.post_type = config.get('post_type', 'community')  # 'community' or 'video'
        
    def publish(self, title: str, content: str, metadata: Dict) -> Dict:
        """Publish to YouTube as a Community Post
        
        Note: For video uploads, the content would need to be a video file.
        Community posts are text-based and are a better fit for markdown content.
        """
        if not all([self.credentials_file, self.channel_id]):
            raise ValueError("YouTube credentials file and channel ID not configured")
        
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            import pickle
        except ImportError:
            raise ImportError("YouTube API requires: pip install google-api-python-client google-auth-oauthlib google-auth-httplib2")
        
        # OAuth 2.0 scopes for YouTube
        SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
        
        creds = None
        token_file = 'youtube_token.pickle'
        
        # Load saved credentials
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        # Build YouTube API client
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Convert markdown to plain text for YouTube community post
        plain_text = self._markdown_to_plain_text(content)
        
        # Truncate if too long (YouTube community posts have character limits)
        max_length = 5000
        if len(plain_text) > max_length:
            plain_text = plain_text[:max_length-50] + "\n\n... [Read more in the full post]"
        
        # Create community post
        # Note: As of 2024, YouTube Community Posts API requires special access
        # For now, we'll prepare the post data and provide instructions for manual posting
        post_data = {
            'snippet': {
                'channelId': self.channel_id,
                'description': plain_text
            }
        }
        
        # Since YouTube Community Post API requires special access,
        # we'll save the post for manual upload or use through YouTube Studio
        return {
            'success': True,
            'platform': 'YouTube',
            'note': 'YouTube Community Posts require manual posting through YouTube Studio',
            'post_preview': plain_text[:200],
            'instructions': 'Copy the content and post manually at: https://studio.youtube.com/channel/{}/posts'.format(self.channel_id)
        }
    
    def _markdown_to_plain_text(self, markdown_text: str) -> str:
        """Convert markdown to plain text for YouTube"""
        import re
        
        text = markdown_text
        
        # Remove markdown headers (convert to bold text)
        text = re.sub(r'^#{1,6}\s+(.+)$', r'\1', text, flags=re.MULTILINE)
        
        # Convert bold to uppercase (YouTube doesn't support bold in community posts)
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        
        # Convert links to plain format
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'\1: \2', text)
        
        # Remove horizontal rules
        text = re.sub(r'^-{3,}$', '', text, flags=re.MULTILINE)
        
        # Clean up multiple newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()


class InstagramPlatform(PublishingPlatform):
    """Instagram publishing via Instagram Graph API or unofficial API"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.username = os.getenv('INSTAGRAM_USERNAME') or config.get('username')
        self.password = os.getenv('INSTAGRAM_PASSWORD') or config.get('password')
        self.access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN') or config.get('access_token')
        self.business_account_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID') or config.get('business_account_id')
        self.use_graph_api = config.get('use_graph_api', False)
        
    def publish(self, title: str, content: str, metadata: Dict) -> Dict:
        """Publish to Instagram
        
        This uses the unofficial instagrapi library for personal accounts.
        For business accounts, use Instagram Graph API with access_token.
        """
        if self.use_graph_api:
            return self._publish_via_graph_api(title, content, metadata)
        else:
            return self._publish_via_instagrapi(title, content, metadata)
    
    def _publish_via_graph_api(self, title: str, content: str, metadata: Dict) -> Dict:
        """Publish using Instagram Graph API (for business accounts)"""
        if not all([self.access_token, self.business_account_id]):
            raise ValueError("Instagram Graph API requires access_token and business_account_id")
        
        # Convert markdown to caption
        caption = self._markdown_to_caption(content)
        
        # Truncate to Instagram's caption limit (2,200 characters)
        if len(caption) > 2200:
            caption = caption[:2190] + "...[more]"
        
        # Note: Instagram Graph API requires an image URL for posts
        # Since we're generating text content, we need to create a text image
        return {
            'success': False,
            'platform': 'Instagram',
            'error': 'Instagram posts require images. Please provide an image URL or use a text-to-image service.',
            'caption_preview': caption[:200],
            'note': 'You can manually post this caption with an image at: https://www.instagram.com/'
        }
    
    def _publish_via_instagrapi(self, title: str, content: str, metadata: Dict) -> Dict:
        """Publish using instagrapi library (for personal accounts)"""
        if not all([self.username, self.password]):
            raise ValueError("Instagram credentials (username/password) not configured")
        
        try:
            from instagrapi import Client
        except ImportError:
            raise ImportError("Instagram posting requires: pip install instagrapi")
        
        # Convert markdown to caption
        caption = self._markdown_to_caption(content)
        
        # Truncate to Instagram's caption limit
        if len(caption) > 2200:
            caption = caption[:2190] + "...[more]"
        
        # Initialize client
        cl = Client()
        
        try:
            # Login
            cl.login(self.username, self.password)
            
            # Note: Instagram requires images for posts
            # For now, we'll create a simple text-based image or require the user to provide one
            # This is a placeholder - in production, you'd want to generate an image with the text
            
            return {
                'success': False,
                'platform': 'Instagram',
                'error': 'Instagram posts require images. Please provide an image or use a text-to-image service.',
                'caption_preview': caption[:200],
                'note': 'Caption ready for manual posting'
            }
            
        except Exception as e:
            return {
                'success': False,
                'platform': 'Instagram',
                'error': f'Instagram login/posting failed: {str(e)}',
                'note': 'Check your username and password in .env file'
            }
    
    def _markdown_to_caption(self, markdown_text: str) -> str:
        """Convert markdown to Instagram caption format"""
        import re
        
        text = markdown_text
        
        # Convert headers to emoji headers
        text = re.sub(r'^# (.+)$', r'🔥 \1 🔥', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.+)$', r'✨ \1', text, flags=re.MULTILINE)
        text = re.sub(r'^### (.+)$', r'📌 \1', text, flags=re.MULTILINE)
        
        # Keep bold as-is (Instagram doesn't support markdown bold)
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        
        # Convert links to "Link in bio" style
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'\1 (Link in bio)', text)
        
        # Convert bullet points to emojis
        text = re.sub(r'^- (.+)$', r'• \1', text, flags=re.MULTILINE)
        
        # Remove horizontal rules
        text = re.sub(r'^-{3,}$', '', text, flags=re.MULTILINE)
        
        # Clean up multiple newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()


class ContentPublisher:
    """Main content publisher that coordinates multiple platforms"""
    
    PLATFORM_CLASSES = {
        'wordpress': WordPressPlatform,
        'medium': MediumPlatform,
        'ghost': GhostPlatform,
        'webhook': WebhookPlatform,
        'youtube': YouTubePlatform,
        'instagram': InstagramPlatform,
    }
    
    def __init__(self, config: Dict):
        self.config = config
        self.platforms = []
        
        # Initialize enabled platforms
        publishing_config = config.get('publishing', {})
        
        for platform_config in publishing_config.get('platforms', []):
            platform_type = platform_config.get('type')
            
            if platform_type in self.PLATFORM_CLASSES:
                platform_class = self.PLATFORM_CLASSES[platform_type]
                platform = platform_class(platform_config)
                
                if platform.is_enabled():
                    self.platforms.append(platform)
    
    def publish_content(self, title: str, content: str, metadata: Dict = None) -> List[Dict]:
        """Publish content to all enabled platforms"""
        if metadata is None:
            metadata = {}
        
        results = []
        
        for platform in self.platforms:
            try:
                print(f"📤 Publishing to {platform.__class__.__name__}...")
                result = platform.publish(title, content, metadata)
                results.append(result)
                print(f"   ✅ Published successfully: {result.get('url', 'N/A')}")
            except Exception as e:
                error_result = {
                    'success': False,
                    'platform': platform.__class__.__name__,
                    'error': str(e)
                }
                results.append(error_result)
                print(f"   ❌ Publishing failed: {e}")
        
        return results
    
    def has_enabled_platforms(self) -> bool:
        """Check if any platforms are enabled"""
        return len(self.platforms) > 0
    
    def get_enabled_platform_names(self) -> List[str]:
        """Get list of enabled platform names"""
        return [platform.__class__.__name__ for platform in self.platforms]
