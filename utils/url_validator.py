"""
URL validation utility module
Provides secure URL validation and Amazon domain checking
"""

from urllib.parse import urlparse
from typing import Set


class URLValidator:
    """Validates and checks URLs for security and correctness"""
    
    # Whitelist of valid Amazon domains
    AMAZON_DOMAINS: Set[str] = {
        'www.amazon.com', 'amazon.com',
        'www.amazon.co.uk', 'amazon.co.uk',
        'www.amazon.ca', 'amazon.ca',
        'www.amazon.de', 'amazon.de',
        'www.amazon.fr', 'amazon.fr',
        'www.amazon.co.jp', 'amazon.co.jp'
    }
    
    @classmethod
    def is_valid_amazon_url(cls, url: str) -> bool:
        """
        Validate if a URL is from an official Amazon domain
        
        Args:
            url: The URL to validate
            
        Returns:
            True if the URL is from a valid Amazon domain, False otherwise
        """
        try:
            parsed = urlparse(url)
            return parsed.netloc in cls.AMAZON_DOMAINS
        except Exception:
            return False
    
    @classmethod
    def get_domain(cls, url: str) -> str:
        """
        Extract domain from URL
        
        Args:
            url: The URL to extract domain from
            
        Returns:
            The domain name or empty string if invalid
        """
        try:
            parsed = urlparse(url)
            return parsed.netloc
        except Exception:
            return ""
