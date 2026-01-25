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
from urllib.parse import urlparse
from dotenv import load_dotenv

# Import content publisher
from content_publisher import ContentPublisher

# Load environment variables
load_dotenv()


class AmazonAssociateLinker:
    """Handles Amazon Associate link generation"""
    
    def __init__(self, associate_id: str, tracking_id: str = None):
        self.associate_id = associate_id
        self.tracking_id = tracking_id or f"{associate_id}-20"
    
    def generate_link(self, asin: str, region: str = "US") -> str:
        """Generate an Amazon affiliate link for a product ASIN"""
        base_urls = {
            "US": "https://www.amazon.com",
            "UK": "https://www.amazon.co.uk",
            "CA": "https://www.amazon.ca",
            "DE": "https://www.amazon.de",
            "FR": "https://www.amazon.fr",
            "JP": "https://www.amazon.co.jp"
        }
        
        base_url = base_urls.get(region, base_urls["US"])
        return f"{base_url}/dp/{asin}?tag={self.tracking_id}"
    
    def add_affiliate_tag(self, product_url: str) -> str:
        """Add affiliate tag to existing Amazon URL"""
        # More secure URL validation - check if URL is from Amazon domains
        try:
            parsed = urlparse(product_url)
            # Explicitly check for exact Amazon domain matches
            amazon_domains = {
                'www.amazon.com', 'amazon.com',
                'www.amazon.co.uk', 'amazon.co.uk',
                'www.amazon.ca', 'amazon.ca',
                'www.amazon.de', 'amazon.de',
                'www.amazon.fr', 'amazon.fr',
                'www.amazon.co.jp', 'amazon.co.jp'
            }
            
            if parsed.netloc in amazon_domains:
                separator = "&" if "?" in product_url else "?"
                return f"{product_url}{separator}tag={self.tracking_id}"
        except Exception:
            pass  # If URL parsing fails, return original
        
        return product_url


class ContentGenerator:
    """Generates product review content"""
    
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
        
        # Generate review content
        review_templates = [
            f"## {title}\n\n"
            f"Looking for a great {category} option? The **{title}** is an excellent choice that delivers outstanding value.\n\n"
            f"### Key Features:\n"
            f"- Premium quality construction\n"
            f"- Excellent customer reviews\n"
            f"- Great value at {price}\n"
            f"- Fast shipping available\n\n"
            f"[**Check Current Price on Amazon**]({affiliate_link})\n\n"
            f"This product has received excellent ratings from verified purchasers and is currently one of the best-selling items in its category.\n\n",
            
            f"## Product Spotlight: {title}\n\n"
            f"If you're in the market for {category}, you'll want to check out the {title}. "
            f"It's currently available at a competitive price of {price}.\n\n"
            f"### Why We Recommend It:\n"
            f"1. **Quality**: Built to last with premium materials\n"
            f"2. **Performance**: Exceeds expectations in real-world use\n"
            f"3. **Value**: Competitively priced for what you get\n\n"
            f"[**View on Amazon →**]({affiliate_link})\n\n"
        ]
        
        return random.choice(review_templates)
    
    def generate_content_post(self, category: str = None) -> str:
        """Generate a full content post with multiple products"""
        if not category:
            category = random.choice(self.config['content']['categories'])
        
        # Sample products (in real use, these would come from Amazon API or database)
        sample_products = [
            {
                'asin': 'B08N5WRWNW',
                'title': 'Premium Wireless Headphones',
                'category': category,
                'price': '$79.99'
            },
            {
                'asin': 'B08J5F3G18',
                'title': 'Smart Home Device',
                'category': category,
                'price': '$49.99'
            },
            {
                'asin': 'B07XJ8C8F5',
                'title': 'Bestselling Book',
                'category': category,
                'price': '$14.99'
            },
            {
                'asin': 'B08L5VFJ5C',
                'title': 'Portable Charger',
                'category': category,
                'price': '$29.99'
            },
            {
                'asin': 'B09JQMJHXY',
                'title': 'Kitchen Gadget',
                'category': category,
                'price': '$39.99'
            }
        ]
        
        # Select products for this post
        num_products = min(
            self.config['content']['products_per_post'],
            len(sample_products)
        )
        selected_products = random.sample(sample_products, num_products)
        
        # Generate post header
        date_str = datetime.now().strftime("%B %d, %Y")
        post = f"# Top {num_products} {category} Products - {date_str}\n\n"
        post += f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
        post += f"Discover the best {category} products available on Amazon today. "
        post += "We've curated this list to help you find exactly what you need.\n\n"
        post += "---\n\n"
        
        # Add product reviews
        for i, product in enumerate(selected_products, 1):
            post += f"### #{i} - {product['title']}\n\n"
            post += self.generate_product_review(product)
            post += "\n---\n\n"
        
        # Add footer
        post += "\n## Disclosure\n\n"
        post += "*As an Amazon Associate, we earn from qualifying purchases. "
        post += "This means if you click on an affiliate link and make a purchase, "
        post += "we may receive a small commission at no extra cost to you.*\n"
        
        return post
    
    def save_content(self, content: str, filename: str = None) -> Path:
        """Save generated content to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"content_{timestamp}.md"
        
        filepath = self.output_dir / filename
        filepath.write_text(content)
        
        return filepath


class AutomatedContentSystem:
    """Main system coordinator"""
    
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
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
        
        # Extract title from content (first line starting with #)
        title = "Generated Content"
        for line in content.split('\n'):
            stripped = line.strip()
            if stripped.startswith('#'):
                # Remove all leading # characters and whitespace
                title = stripped.lstrip('#').strip()
                if title:  # Only use if we got a non-empty title
                    break
        
        # Fallback to a descriptive title if extraction failed
        if not title or title == "Generated Content":
            title = f"{category} Products - {datetime.now().strftime('%B %d, %Y')}"
        
        # Generate metadata
        metadata = {
            'generated_at': datetime.now().isoformat(),
            'category': category,
            'filepath': str(filepath),
            'word_count': len(content.split()),
            'affiliate_links': content.count('amazon.com')
        }
        
        # Save metadata
        metadata_path = filepath.with_suffix('.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"📊 Metadata saved to: {metadata_path}")
        print(f"📈 Generated {metadata['word_count']} words with {metadata['affiliate_links']} affiliate links")
        
        # Auto-publish if enabled
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
                
                # Update metadata file
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
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
