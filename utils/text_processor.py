"""
Text processing utility module
Provides text transformation and formatting utilities
"""

import re
from typing import Pattern


class TextProcessor:
    """Handles text processing operations with optimized regex patterns"""
    
    # Compile regex patterns once for reuse (optimization)
    _HEADER_PATTERN: Pattern = re.compile(r'^#{1,6}\s+(.+)$', re.MULTILINE)
    _BOLD_PATTERN: Pattern = re.compile(r'\*\*(.+?)\*\*')
    _LINK_PATTERN: Pattern = re.compile(r'\[(.+?)\]\((.+?)\)')
    _HR_PATTERN: Pattern = re.compile(r'^-{3,}$', re.MULTILINE)
    _MULTIPLE_NEWLINES_PATTERN: Pattern = re.compile(r'\n{3,}')
    
    @classmethod
    def markdown_to_plain_text(cls, markdown_text: str) -> str:
        """
        Convert markdown to plain text
        
        Args:
            markdown_text: Markdown formatted text
            
        Returns:
            Plain text version
        """
        text = markdown_text
        
        # Remove markdown headers (convert to plain text)
        text = cls._HEADER_PATTERN.sub(r'\1', text)
        
        # Convert bold to plain text
        text = cls._BOLD_PATTERN.sub(r'\1', text)
        
        # Convert links to plain format
        text = cls._LINK_PATTERN.sub(r'\1: \2', text)
        
        # Remove horizontal rules
        text = cls._HR_PATTERN.sub('', text)
        
        # Clean up multiple newlines
        text = cls._MULTIPLE_NEWLINES_PATTERN.sub('\n\n', text)
        
        return text.strip()
    
    @classmethod
    def truncate_with_ellipsis(cls, text: str, max_length: int, ellipsis: str = "\n\n... [Read more]") -> str:
        """
        Truncate text to a maximum length with ellipsis
        
        Args:
            text: Text to truncate
            max_length: Maximum length
            ellipsis: Ellipsis string to append
            
        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text
        
        # Calculate truncation point
        truncate_at = max_length - len(ellipsis)
        if truncate_at < 0:
            truncate_at = max_length
            
        return text[:truncate_at] + ellipsis
