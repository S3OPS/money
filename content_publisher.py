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
            'categories': [self._get_or_create_category(metadata.get('category', 'Uncategorized'))],
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
    
    def _get_or_create_category(self, category_name: str) -> int:
        """Get or create a category by name"""
        # For simplicity, return 1 (Uncategorized). 
        # In production, implement category lookup/creation
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
        
        # Split the key into ID and SECRET
        id, secret = self.admin_api_key.split(':')
        
        # Prepare header and payload
        iat = int(time.time())
        header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
        payload = {
            'iat': iat,
            'exp': iat + 5 * 60,
            'aud': '/admin/'
        }
        
        token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)
        
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


class ContentPublisher:
    """Main content publisher that coordinates multiple platforms"""
    
    PLATFORM_CLASSES = {
        'wordpress': WordPressPlatform,
        'medium': MediumPlatform,
        'ghost': GhostPlatform,
        'webhook': WebhookPlatform,
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
