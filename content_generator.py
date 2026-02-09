#!/usr/bin/env python3
"""
Automated Content Creation System with Amazon Associates
Generates product review content with embedded affiliate links
"""

import os
import sys
import yaml
import json
import random
import schedule
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv
import io

# Fix Unicode encoding issues on Windows
try:
    if hasattr(sys.stdout, 'buffer') and sys.stdout.encoding:
        encoding = sys.stdout.encoding.lower().replace('_', '-')
        if encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except (AttributeError, ValueError, LookupError):
    pass  # If encoding setup fails, continue with default encoding

# Import content publisher
from content_publisher import ContentPublisher

# Import utility modules
from utils import URLValidator, InputValidator, ConfigValidator, TextProcessor

# Load environment variables
load_dotenv()

# Constants
DEFAULT_TRACKING_SUFFIX = "-20"


class AmazonAssociateLinker:
    """Handles Amazon Associate link generation"""
    
    # Region-to-domain mapping (extracted as constant for optimization)
    REGION_URLS = {
        "US": "https://www.amazon.com",
        "UK": "https://www.amazon.co.uk",
        "CA": "https://www.amazon.ca",
        "DE": "https://www.amazon.de",
        "FR": "https://www.amazon.fr",
        "JP": "https://www.amazon.co.jp"
    }
    
    def __init__(self, associate_id: str, tracking_id: str = None):
        # Validate associate ID for security
        if not InputValidator.validate_associate_id(associate_id):
            raise ValueError("Invalid Amazon Associate ID format")
        
        self.associate_id = associate_id
        self.tracking_id = tracking_id or f"{associate_id}{DEFAULT_TRACKING_SUFFIX}"
    
    def generate_link(self, asin: str, region: str = "US") -> str:
        """Generate an Amazon affiliate link for a product ASIN"""
        # Validate ASIN for security
        if not InputValidator.validate_asin(asin):
            raise ValueError(f"Invalid ASIN format: {asin}")
        
        base_url = self.REGION_URLS.get(region, self.REGION_URLS["US"])
        return f"{base_url}/dp/{asin}?tag={self.tracking_id}"
    
    def add_affiliate_tag(self, product_url: str) -> str:
        """Add affiliate tag to existing Amazon URL"""
        # Use centralized URL validator for security
        if URLValidator.is_valid_amazon_url(product_url):
            separator = "&" if "?" in product_url else "?"
            return f"{product_url}{separator}tag={self.tracking_id}"
        
        return product_url


class ContentGenerator:
    """Generates product review content"""
    
    # Sample products as class constant (optimization - avoid recreation each call)
    SAMPLE_PRODUCTS = [
        {
            'asin': 'B08N5WRWNW',
            'title': 'Premium Wireless Headphones',
            'price': '$79.99'
        },
        {
            'asin': 'B08J5F3G18',
            'title': 'Smart Home Device',
            'price': '$49.99'
        },
        {
            'asin': 'B07XJ8C8F5',
            'title': 'Bestselling Book',
            'price': '$14.99'
        },
        {
            'asin': 'B08L5VFJ5C',
            'title': 'Portable Charger',
            'price': '$29.99'
        },
        {
            'asin': 'B09JQMJHXY',
            'title': 'Kitchen Gadget',
            'price': '$39.99'
        }
    ]
    
    def __init__(self, config: Dict):
        self.config = config
        amazon_config = config.get('amazon', {})
        
        # Get Amazon Associate ID from env or config
        associate_id = os.getenv('AMAZON_ASSOCIATE_ID') or amazon_config.get('associate_id')
        tracking_id = os.getenv('AMAZON_TRACKING_ID') or amazon_config.get('tracking_id')
        
        self.linker = AmazonAssociateLinker(associate_id, tracking_id)
        self.output_dir = Path(config['content']['output_directory'])
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_product_review(self, product: Dict) -> str:
        """Generate a product review with affiliate link"""
        asin = product.get('asin')
        if not asin:
            raise ValueError("Product ASIN is required for generating affiliate links")
        
        title = product.get('title', 'Amazing Product')
        category = product.get('category', 'General')
        price = product.get('price', 'Check Amazon')
        
        affiliate_link = self.linker.generate_link(asin, self.config['amazon']['api_region'])
        
        # Generate review content using efficient string building
        # Templates are lists of strings to avoid repeated string concatenation overhead
        # random.choice selects a template, then ''.join() builds the final string efficiently
        review_templates = [
            [
                f"## {title}\n\n",
                f"Looking for a great {category} option? The **{title}** is an excellent choice that delivers outstanding value.\n\n",
                "### Key Features:\n",
                "- Premium quality construction\n",
                "- Excellent customer reviews\n",
                f"- Great value at {price}\n",
                "- Fast shipping available\n\n",
                f"[**Check Current Price on Amazon**]({affiliate_link})\n\n",
                "This product has received excellent ratings from verified purchasers and is currently one of the best-selling items in its category.\n\n"
            ],
            [
                f"## Product Spotlight: {title}\n\n",
                f"If you're in the market for {category}, you'll want to check out the {title}. ",
                f"It's currently available at a competitive price of {price}.\n\n",
                "### Why We Recommend It:\n",
                "1. **Quality**: Built to last with premium materials\n",
                "2. **Performance**: Exceeds expectations in real-world use\n",
                "3. **Value**: Competitively priced for what you get\n\n",
                f"[**View on Amazon →**]({affiliate_link})\n\n"
            ]
        ]
        
        return ''.join(random.choice(review_templates))
    
    def _prepare_products_for_category(self, category: str) -> List[Dict]:
        """Prepare products by adding category field to each product
        
        This helper method makes the intent clear and keeps product preparation logic separate.
        """
        return [
            {**product, 'category': category}
            for product in self.SAMPLE_PRODUCTS
        ]
    
    def generate_content_post(self, category: str = None) -> str:
        """Generate a full content post with multiple products"""
        if not category:
            category = random.choice(self.config['content']['categories'])
        
        # Prepare products with category information
        sample_products = self._prepare_products_for_category(category)
        
        # Select products for this post
        num_products = min(
            self.config['content']['products_per_post'],
            len(sample_products)
        )
        selected_products = random.sample(sample_products, num_products)
        
        # Build post using list for efficient string concatenation
        date_str = datetime.now().strftime("%B %d, %Y")
        timestamp_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        post_parts = [
            f"# Top {num_products} {category} Products - {date_str}\n\n",
            f"*Last updated: {timestamp_str}*\n\n",
            f"Discover the best {category} products available on Amazon today. ",
            "We've curated this list to help you find exactly what you need.\n\n",
            "---\n\n"
        ]
        
        # Add product reviews
        for i, product in enumerate(selected_products, 1):
            post_parts.append(f"### #{i} - {product['title']}\n\n")
            post_parts.append(self.generate_product_review(product))
            post_parts.append("\n---\n\n")
        
        # Add footer
        post_parts.extend([
            "\n## Disclosure\n\n",
            "*As an Amazon Associate, we earn from qualifying purchases. ",
            "This means if you click on an affiliate link and make a purchase, ",
            "we may receive a small commission at no extra cost to you.*\n"
        ])
        
        return ''.join(post_parts)
    
    def save_content(self, content: str, filename: str = None) -> Path:
        """Save generated content to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"content_{timestamp}.md"
        
        # Sanitize filename to prevent path traversal attacks
        filename = InputValidator.sanitize_filename(filename)
        
        filepath = self.output_dir / filename
        filepath.write_text(content, encoding='utf-8')
        
        return filepath


class AutomatedContentSystem:
    """Main system coordinator"""
    
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Validate configuration for security and correctness
        config_errors = ConfigValidator.validate_config(self.config)
        if config_errors:
            error_msg = "Configuration validation errors:\n" + "\n".join(f"  - {err}" for err in config_errors)
            raise ValueError(error_msg)
        
        self.generator = ContentGenerator(self.config)
        self.publisher = ContentPublisher(self.config)
    
    def generate_and_save(self) -> Dict:
        """Generate content and save to file"""
        print("🚀 Starting content generation...")
        
        # Generate content for a random category
        category = random.choice(self.config['content']['categories'])
        print(f"📝 Generating content for category: {category}")
        
        content = self.generator.generate_content_post(category)
        
        # Save content
        filepath = self.generator.save_content(content)
        print(f"✅ Content saved to: {filepath}")
        
        # Extract title from content using utility method
        title = TextProcessor.extract_heading(content, f"{category} Products - {datetime.now().strftime('%B %d, %Y')}")
        
        # Generate metadata
        metadata = {
            'generated_at': datetime.now().isoformat(),
            'category': category,
            'filepath': str(filepath),
            'word_count': len(content.split()),
            'affiliate_links': content.count('amazon.com')
        }
        
        # Auto-publish if enabled (collect results before writing metadata)
        if self.config.get('publishing', {}).get('auto_publish', False):
            print("\n" + "=" * 60)
            print("📢 AUTO-PUBLISHING ENABLED")
            print("=" * 60)
            
            if self.publisher.has_enabled_platforms():
                print(f"🎯 Publishing to: {', '.join(self.publisher.get_enabled_platform_names())}")
                print()
                
                publish_results = self.publisher.publish_content(title, content, metadata)
                
                # Add publishing results to metadata
                metadata['published'] = True
                metadata['publishing_results'] = publish_results
                
                # Summary
                successful = sum(1 for r in publish_results if r.get('success', False))
                total = len(publish_results)
                print()
                print("=" * 60)
                print(f"📊 PUBLISHING SUMMARY: {successful}/{total} successful")
                print("=" * 60)
            else:
                print("⚠️  No publishing platforms enabled in config.yaml")
                print("   Enable platforms to auto-publish content")
        else:
            print("\n💡 Tip: Enable auto_publish in config.yaml to automatically post content")
        
        # Save metadata once with all information (optimization - single write)
        metadata_path = filepath.with_suffix('.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"📊 Metadata saved to: {metadata_path}")
        print(f"📈 Generated {metadata['word_count']} words with {metadata['affiliate_links']} affiliate links")
        
        return metadata
    
    def run_automated_schedule(self):
        """Run on automated schedule"""
        schedule_config = self.config.get('schedule', {})
        
        if not schedule_config.get('enabled', False):
            print("⚠️  Scheduling is disabled in config.yaml")
            return
        
        schedule_time = schedule_config.get('time', '09:00')
        
        print(f"⏰ Scheduling content generation daily at {schedule_time}")
        
        schedule.every().day.at(schedule_time).do(self.generate_and_save)
        
        # Run once immediately
        print("🎯 Running initial content generation...")
        self.generate_and_save()
        
        print("\n✨ System is now running! Press Ctrl+C to stop.")
        
        while True:
            schedule.run_pending()
            time.sleep(60)


def main():
    """Main entry point"""
    print("=" * 60)
    print("🎯 AUTOMATED CONTENT CREATION SYSTEM")
    print("💰 Amazon Associates Integration Active")
    print("=" * 60)
    print()
    
    # Check for config file
    if not os.path.exists('config.yaml'):
        print("❌ Error: config.yaml not found!")
        print("Please copy config.yaml and update with your settings.")
        return
    
    # Check for environment variables
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found. Using config.yaml values.")
        print("   Consider creating .env from .env.example for better security.")
    
    # Initialize system
    system = AutomatedContentSystem()
    
    # Run once or schedule
    if '--schedule' in sys.argv:
        system.run_automated_schedule()
    else:
        print("Running one-time content generation...")
        print("(Use --schedule flag to run on automated schedule)")
        print()
        system.generate_and_save()
        print()
        print("✨ Done! Check the generated_content/ directory for output.")


if __name__ == "__main__":
    main()
