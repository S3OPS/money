"""
Input validation and sanitization utilities
Ensures all user inputs are safe and properly validated
"""

import re
from pathlib import Path
from typing import Optional


class InputValidator:
    """Validates and sanitizes user inputs for security"""
    
    # Regex patterns for validation
    _ASIN_PATTERN = re.compile(r'^[A-Z0-9]{10}$')
    _SAFE_FILENAME_PATTERN = re.compile(r'^[a-zA-Z0-9_\-\.]+$')
    _ASSOCIATE_ID_PATTERN = re.compile(r'^[a-zA-Z0-9\-]+$')
    
    # Maximum lengths for various inputs
    MAX_FILENAME_LENGTH = 255
    MAX_CATEGORY_LENGTH = 100
    MAX_TITLE_LENGTH = 500
    
    @classmethod
    def validate_asin(cls, asin: str) -> bool:
        """
        Validate Amazon ASIN format
        
        Args:
            asin: The ASIN to validate
            
        Returns:
            True if valid ASIN format, False otherwise
        """
        if not asin or not isinstance(asin, str):
            return False
        return cls._ASIN_PATTERN.match(asin) is not None
    
    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """
        Sanitize filename to prevent path traversal attacks
        
        Args:
            filename: The filename to sanitize
            
        Returns:
            Sanitized filename safe for file operations
        """
        if not filename:
            return "default"
        
        # Remove any path components
        filename = Path(filename).name
        
        # Remove potentially dangerous characters
        filename = re.sub(r'[^\w.\-]', '_', filename)
        
        # Limit length
        if len(filename) > cls.MAX_FILENAME_LENGTH:
            # Preserve extension if present
            parts = filename.rsplit('.', 1)
            if len(parts) == 2:
                name, ext = parts
                max_name_len = cls.MAX_FILENAME_LENGTH - len(ext) - 1
                filename = f"{name[:max_name_len]}.{ext}"
            else:
                filename = filename[:cls.MAX_FILENAME_LENGTH]
        
        # Prevent hidden files
        if filename.startswith('.'):
            filename = f"file_{filename}"
        
        return filename
    
    @classmethod
    def validate_associate_id(cls, associate_id: str) -> bool:
        """
        Validate Amazon Associate ID format
        
        Args:
            associate_id: The associate ID to validate
            
        Returns:
            True if valid format, False otherwise
        """
        if not associate_id or not isinstance(associate_id, str):
            return False
        
        # Check length (typical format: "yourname-20")
        if len(associate_id) < 3 or len(associate_id) > 50:
            return False
        
        return cls._ASSOCIATE_ID_PATTERN.match(associate_id) is not None
    
    @classmethod
    def sanitize_text_input(cls, text: str, max_length: Optional[int] = None) -> str:
        """
        Sanitize text input to prevent injection attacks
        
        Args:
            text: The text to sanitize
            max_length: Optional maximum length
            
        Returns:
            Sanitized text
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Remove null bytes
        text = text.replace('\0', '')
        
        # Apply max length if specified
        if max_length and len(text) > max_length:
            text = text[:max_length]
        
        return text.strip()
    
    @classmethod
    def validate_category(cls, category: str) -> bool:
        """
        Validate category name
        
        Args:
            category: Category name to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not category or not isinstance(category, str):
            return False
        
        # Check length
        if len(category) > cls.MAX_CATEGORY_LENGTH:
            return False
        
        # Category should contain only safe characters
        return bool(re.match(r'^[a-zA-Z0-9\s\-&]+$', category))
