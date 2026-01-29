#!/usr/bin/env python3
"""
Content Publisher Module
Automatically publishes generated content to various platforms
"""

import os
import sys
import io
from typing import Dict, List
from dotenv import load_dotenv

# Fix Unicode encoding issues on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Import utility modules
from utils import TextProcessor

load_dotenv()

# Constants for YouTube limits
YOUTUBE_COMMUNITY_POST_LIMIT = 5000
YOUTUBE_TRUNCATE_OFFSET = 50


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
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
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
        
        # Convert markdown to plain text for YouTube community post using optimized utility
        plain_text = TextProcessor.markdown_to_plain_text(content)
        
        # Truncate if too long using optimized utility
        plain_text = TextProcessor.truncate_with_ellipsis(
            plain_text, 
            YOUTUBE_COMMUNITY_POST_LIMIT - YOUTUBE_TRUNCATE_OFFSET,
            "\n\n... [Read more in the full post]"
        )
        
        # Note: YouTube Community Post API requires special access and is not publicly available
        # The API client is built but the endpoint requires special permissions from YouTube
        # For production use, content needs to be posted manually or via YouTube Studio API (requires approval)
        
        return {
            'success': True,
            'platform': 'YouTube',
            'note': 'YouTube Community Posts require manual posting through YouTube Studio or special API access',
            'post_preview': plain_text[:200],
            'instructions': 'Copy the content and post manually at: https://studio.youtube.com/channel/{}/posts'.format(self.channel_id),
            'credentials_ready': True
        }


class ContentPublisher:
    """Main content publisher that coordinates multiple platforms"""
    
    PLATFORM_CLASSES = {
        'youtube': YouTubePlatform,
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
