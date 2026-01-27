#!/usr/bin/env python3
"""
Unit tests for utility modules
"""

import sys
from utils import URLValidator, TextProcessor, InputValidator, ConfigValidator


def test_url_validator():
    """Test URL validation utility"""
    print("🧪 Testing URLValidator...")
    
    # Valid Amazon URLs
    valid_urls = [
        "https://www.amazon.com/dp/B08N5WRWNW",
        "https://amazon.com/product/xyz",
        "https://www.amazon.co.uk/item/abc",
        "https://amazon.ca/test",
    ]
    
    # Invalid URLs
    invalid_urls = [
        "https://www.amazin.com/fake",  # Typo
        "https://amazon.phishing.com/product",  # Phishing
        "https://www.google.com",
        "not-a-url",
    ]
    
    try:
        # Test valid URLs
        for url in valid_urls:
            if not URLValidator.is_valid_amazon_url(url):
                print(f"   ❌ Failed to validate valid URL: {url}")
                return False
        
        # Test invalid URLs
        for url in invalid_urls:
            if URLValidator.is_valid_amazon_url(url):
                print(f"   ❌ Incorrectly validated invalid URL: {url}")
                return False
        
        # Test domain extraction
        domain = URLValidator.get_domain("https://www.amazon.com/test")
        if domain != "www.amazon.com":
            print(f"   ❌ Domain extraction failed: got {domain}")
            return False
        
        print("   ✅ URLValidator working correctly")
        return True
        
    except Exception as e:
        print(f"   ❌ URLValidator error: {e}")
        return False


def test_text_processor():
    """Test text processing utility"""
    print("🧪 Testing TextProcessor...")
    
    try:
        # Test markdown to plain text
        markdown = """
# Heading 1
## Heading 2

This is **bold** text and this is a [link](https://example.com).

---

More content here.
"""
        
        plain = TextProcessor.markdown_to_plain_text(markdown)
        
        # Check that markdown formatting is removed
        if "#" in plain:
            print("   ❌ Markdown headers not removed")
            return False
        
        if "**" in plain:
            print("   ❌ Bold markers not removed")
            return False
        
        if "[link]" in plain:
            print("   ❌ Link format not converted")
            return False
        
        # Test truncation
        long_text = "A" * 1000
        truncated = TextProcessor.truncate_with_ellipsis(long_text, 100)
        
        if len(truncated) > 110:  # Allow some space for ellipsis
            print(f"   ❌ Truncation failed: length {len(truncated)}")
            return False
        
        if "..." not in truncated and "[Read more]" not in truncated:
            print("   ❌ Ellipsis not added")
            return False
        
        # Test truncation with short text (should not truncate)
        short_text = "Short"
        result = TextProcessor.truncate_with_ellipsis(short_text, 100)
        if result != short_text:
            print("   ❌ Short text incorrectly truncated")
            return False
        
        print("   ✅ TextProcessor working correctly")
        return True
        
    except Exception as e:
        print(f"   ❌ TextProcessor error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_input_validator():
    """Test input validation utility"""
    print("🧪 Testing InputValidator...")
    
    try:
        # Test ASIN validation
        valid_asins = ["B08N5WRWNW", "B07XJ8C8F5", "B09JQMJHXY"]
        invalid_asins = ["invalid", "B08N5", "B08N5WRWNW1", "b08n5wrwnw"]
        
        for asin in valid_asins:
            if not InputValidator.validate_asin(asin):
                print(f"   ❌ Failed to validate valid ASIN: {asin}")
                return False
        
        for asin in invalid_asins:
            if InputValidator.validate_asin(asin):
                print(f"   ❌ Incorrectly validated invalid ASIN: {asin}")
                return False
        
        # Test filename sanitization
        dangerous_filenames = [
            ("../../../etc/passwd", "passwd"),  # Path traversal
            ("test/../../secret.txt", "secret.txt"),  # Path traversal
            ("file<script>.md", "file_script_.md"),  # Dangerous chars
            (".hidden", "file_.hidden"),  # Hidden file
            ("A" * 300 + ".txt", None),  # Too long
        ]
        
        for filename, expected_prefix in dangerous_filenames:
            sanitized = InputValidator.sanitize_filename(filename)
            # Should not contain path separators
            if "/" in sanitized or "\\" in sanitized:
                print(f"   ❌ Path separator not removed from '{filename}': {sanitized}")
                return False
            # Check expected prefix if provided
            if expected_prefix and not sanitized.startswith(expected_prefix):
                print(f"   ❌ Unexpected sanitization for '{filename}': got '{sanitized}', expected prefix '{expected_prefix}'")
                return False
        
        # Test associate ID validation
        valid_ids = ["mysite-20", "test-id", "amazonuser-20"]
        invalid_ids = ["", "a", "has spaces", "has!special", None]
        
        for aid in valid_ids:
            if not InputValidator.validate_associate_id(aid):
                print(f"   ❌ Failed to validate valid associate ID: {aid}")
                return False
        
        for aid in invalid_ids:
            if InputValidator.validate_associate_id(aid):
                print(f"   ❌ Incorrectly validated invalid associate ID: {aid}")
                return False
        
        # Test text sanitization
        text_with_null = "Hello\x00World"
        sanitized = InputValidator.sanitize_text_input(text_with_null)
        if '\x00' in sanitized:
            print("   ❌ Null byte not removed")
            return False
        
        print("   ✅ InputValidator working correctly")
        return True
        
    except Exception as e:
        print(f"   ❌ InputValidator error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config_validator():
    """Test configuration validation utility"""
    print("🧪 Testing ConfigValidator...")
    
    try:
        # Test valid configuration
        valid_config = {
            'amazon': {
                'associate_id': 'test-20',
                'tracking_id': 'test-20',
                'api_region': 'US'
            },
            'content': {
                'categories': ['Tech', 'Books'],
                'products_per_post': 5,
                'output_directory': 'output',
                'format': 'markdown'
            },
            'schedule': {
                'enabled': True,
                'time': '09:00'
            }
        }
        
        if not ConfigValidator.is_valid(valid_config):
            errors = ConfigValidator.validate_config(valid_config)
            print(f"   ❌ Valid config marked as invalid: {errors}")
            return False
        
        # Test invalid region
        invalid_region_config = valid_config.copy()
        invalid_region_config['amazon'] = valid_config['amazon'].copy()
        invalid_region_config['amazon']['api_region'] = 'INVALID'
        
        errors = ConfigValidator.validate_config(invalid_region_config)
        if not errors:
            print("   ❌ Invalid region not detected")
            return False
        
        # Test missing required keys
        incomplete_config = {'amazon': {}}
        errors = ConfigValidator.validate_config(incomplete_config)
        if not errors:
            print("   ❌ Missing keys not detected")
            return False
        
        # Test invalid products_per_post
        invalid_products_config = valid_config.copy()
        invalid_products_config['content'] = valid_config['content'].copy()
        invalid_products_config['content']['products_per_post'] = 0
        
        errors = ConfigValidator.validate_config(invalid_products_config)
        if not errors:
            print("   ❌ Invalid products_per_post not detected")
            return False
        
        print("   ✅ ConfigValidator working correctly")
        return True
        
    except Exception as e:
        print(f"   ❌ ConfigValidator error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run utility tests"""
    print("=" * 60)
    print("🧪 RUNNING UTILITY MODULE TESTS")
    print("=" * 60)
    print()
    
    tests = [
        ("URLValidator", test_url_validator),
        ("TextProcessor", test_text_processor),
        ("InputValidator", test_input_validator),
        ("ConfigValidator", test_config_validator),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"   💥 Unexpected error: {e}")
            results.append((name, False))
        print()
    
    # Summary
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL UTILITY TESTS PASSED!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
