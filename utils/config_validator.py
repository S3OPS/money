"""
Configuration validation module
Ensures configuration files are properly structured and secure
"""

from typing import Dict, List, Any


class ConfigValidator:
    """Validates configuration settings for security and correctness"""
    
    # Required top-level configuration keys
    REQUIRED_KEYS = {'amazon', 'content', 'schedule'}
    
    # Required Amazon configuration keys
    REQUIRED_AMAZON_KEYS = {'associate_id', 'tracking_id', 'api_region'}
    
    # Required content configuration keys
    REQUIRED_CONTENT_KEYS = {'categories', 'products_per_post', 'output_directory'}
    
    # Valid API regions
    VALID_REGIONS = {'US', 'UK', 'CA', 'DE', 'FR', 'JP'}
    
    @classmethod
    def validate_config(cls, config: Dict[str, Any]) -> List[str]:
        """
        Validate configuration dictionary
        
        Args:
            config: Configuration dictionary to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Type check
        if not isinstance(config, dict):
            errors.append('Configuration must be a dictionary')
            return errors
        
        # Check required top-level keys
        missing_keys = cls.REQUIRED_KEYS - set(config.keys())
        if missing_keys:
            errors.append(f"Missing required configuration keys: {', '.join(missing_keys)}")
        
        # Validate Amazon configuration
        if 'amazon' in config:
            amazon_errors = cls._validate_amazon_config(config['amazon'])
            errors.extend(amazon_errors)
        
        # Validate content configuration
        if 'content' in config:
            content_errors = cls._validate_content_config(config['content'])
            errors.extend(content_errors)
        
        # Validate publishing configuration if present
        if 'publishing' in config:
            publishing_errors = cls._validate_publishing_config(config['publishing'])
            errors.extend(publishing_errors)
        
        return errors
    
    @classmethod
    def _validate_amazon_config(cls, amazon_config: Dict[str, Any]) -> List[str]:
        """Validate Amazon configuration section"""
        errors = []
        
        # Check API region
        if 'api_region' in amazon_config:
            region = amazon_config['api_region']
            if region not in cls.VALID_REGIONS:
                errors.append(f"Invalid API region: {region}. Must be one of {cls.VALID_REGIONS}")
        
        return errors
    
    @classmethod
    def _validate_content_config(cls, content_config: Dict[str, Any]) -> List[str]:
        """Validate content configuration section"""
        errors = []
        
        # Validate categories
        if 'categories' in content_config:
            categories = content_config['categories']
            if not isinstance(categories, list) or not categories:
                errors.append("Categories must be a non-empty list")
        
        # Validate products_per_post
        if 'products_per_post' in content_config:
            products_per_post = content_config['products_per_post']
            if not isinstance(products_per_post, int) or products_per_post < 1:
                errors.append("products_per_post must be a positive integer")
            elif products_per_post > 50:
                errors.append("products_per_post should not exceed 50 for performance reasons")
        
        # Validate output format
        if 'format' in content_config:
            fmt = content_config['format']
            valid_formats = {'markdown', 'html', 'json'}
            if fmt not in valid_formats:
                errors.append(f"Invalid format: {fmt}. Must be one of {valid_formats}")
        
        return errors
    
    @classmethod
    def _validate_publishing_config(cls, publishing_config: Dict[str, Any]) -> List[str]:
        """Validate publishing configuration section"""
        errors = []
        
        # Validate auto_publish flag
        if 'auto_publish' in publishing_config:
            auto_publish = publishing_config['auto_publish']
            if not isinstance(auto_publish, bool):
                errors.append("auto_publish must be a boolean value")
        
        # Validate platforms
        if 'platforms' in publishing_config:
            platforms = publishing_config['platforms']
            if not isinstance(platforms, list):
                errors.append("platforms must be a list")
            else:
                for i, platform in enumerate(platforms):
                    if not isinstance(platform, dict):
                        errors.append(f"Platform {i} must be a dictionary")
                    elif 'type' not in platform:
                        errors.append(f"Platform {i} missing required 'type' field")
        
        return errors
    
    @classmethod
    def is_valid(cls, config: Dict[str, Any]) -> bool:
        """
        Check if configuration is valid
        
        Args:
            config: Configuration dictionary
            
        Returns:
            True if valid, False otherwise
        """
        errors = cls.validate_config(config)
        return len(errors) == 0
