#!/usr/bin/env python3
"""
Test script to validate the automated content creation system
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path


def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import yaml
        import schedule
        from dotenv import load_dotenv
        from jinja2 import Template
        print("   ✅ All required modules available")
        return True
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        print("   Run: pip install -r requirements.txt")
        return False


def test_config_file():
    """Test that config file exists and is valid"""
    print("🧪 Testing config file...")
    
    if not os.path.exists('config.yaml'):
        print("   ❌ config.yaml not found")
        return False
    
    try:
        import yaml
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Check required fields
        required_fields = ['amazon', 'content', 'schedule']
        for field in required_fields:
            if field not in config:
                print(f"   ❌ Missing required field: {field}")
                return False
        
        print("   ✅ Config file is valid")
        return True
    except Exception as e:
        print(f"   ❌ Config file error: {e}")
        return False


def test_amazon_linker():
    """Test Amazon Associate link generation"""
    print("🧪 Testing Amazon link generation...")
    
    try:
        from content_generator import AmazonAssociateLinker
        
        linker = AmazonAssociateLinker("test-id", "test-id-20")
        
        # Test link generation
        link = linker.generate_link("B08N5WRWNW", "US")
        
        if "amazon.com" in link and "test-id-20" in link:
            print(f"   ✅ Generated link: {link}")
            return True
        else:
            print(f"   ❌ Invalid link generated: {link}")
            return False
            
    except Exception as e:
        print(f"   ❌ Link generation error: {e}")
        return False


def test_content_generation():
    """Test content generation"""
    print("🧪 Testing content generation...")
    
    try:
        # Set up test environment
        os.environ['AMAZON_ASSOCIATE_ID'] = 'test-id'
        os.environ['AMAZON_TRACKING_ID'] = 'test-id-20'
        
        from content_generator import ContentGenerator
        import yaml
        
        # Load config
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Create temp directory for output
        original_output = config['content']['output_directory']
        config['content']['output_directory'] = tempfile.mkdtemp()
        
        try:
            generator = ContentGenerator(config)
            
            # Generate content
            content = generator.generate_content_post("Test Category")
            
            if len(content) > 100 and "amazon.com" in content and "test-id-20" in content:
                print("   ✅ Content generated successfully")
                print(f"   📊 Generated {len(content)} characters")
                print(f"   🔗 Contains affiliate links: {content.count('amazon.com')}")
                return True
            else:
                print(f"   ❌ Invalid content generated")
                return False
        finally:
            # Cleanup
            shutil.rmtree(config['content']['output_directory'], ignore_errors=True)
            
    except Exception as e:
        print(f"   ❌ Content generation error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_file_saving():
    """Test saving content to file"""
    print("🧪 Testing file saving...")
    
    try:
        os.environ['AMAZON_ASSOCIATE_ID'] = 'test-id'
        os.environ['AMAZON_TRACKING_ID'] = 'test-id-20'
        
        from content_generator import ContentGenerator
        import yaml
        
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        config['content']['output_directory'] = temp_dir
        
        try:
            generator = ContentGenerator(config)
            
            # Generate and save
            content = generator.generate_content_post("Test")
            filepath = generator.save_content(content, "test_output.md")
            
            if filepath.exists() and filepath.read_text() == content:
                print(f"   ✅ File saved successfully: {filepath}")
                return True
            else:
                print(f"   ❌ File save failed")
                return False
        finally:
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)
            
    except Exception as e:
        print(f"   ❌ File save error: {e}")
        return False


def test_system_integration():
    """Test the full system integration"""
    print("🧪 Testing system integration...")
    
    try:
        os.environ['AMAZON_ASSOCIATE_ID'] = 'test-id'
        os.environ['AMAZON_TRACKING_ID'] = 'test-id-20'
        
        from content_generator import AutomatedContentSystem
        import yaml
        
        # Load and modify config for testing
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Create temp config
        temp_config = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        
        # Use temp directory for output
        config['content']['output_directory'] = tempfile.mkdtemp()
        
        try:
            yaml.dump(config, temp_config)
            temp_config.close()
            
            # Create system with temp config
            system = AutomatedContentSystem(temp_config.name)
            
            # Generate content
            metadata = system.generate_and_save()
            
            if metadata['filepath'] and metadata['affiliate_links'] > 0:
                print("   ✅ System integration successful")
                print(f"   📝 Generated: {metadata['filepath']}")
                print(f"   📊 Word count: {metadata['word_count']}")
                print(f"   🔗 Affiliate links: {metadata['affiliate_links']}")
                return True
            else:
                print("   ❌ System integration failed")
                return False
        finally:
            # Cleanup
            os.unlink(temp_config.name)
            shutil.rmtree(config['content']['output_directory'], ignore_errors=True)
            
    except Exception as e:
        print(f"   ❌ System integration error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 RUNNING AUTOMATED TESTS")
    print("=" * 60)
    print()
    
    tests = [
        ("Import Dependencies", test_imports),
        ("Config File", test_config_file),
        ("Amazon Link Generator", test_amazon_linker),
        ("Content Generation", test_content_generation),
        ("File Saving", test_file_saving),
        ("System Integration", test_system_integration),
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
        print("\n🎉 ALL TESTS PASSED! System is ready to use.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
