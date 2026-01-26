#!/usr/bin/env python3
"""
Quick Start Script - Run this to get started immediately!
Supports both interactive and automated modes.

Usage:
  Interactive mode:   python quick_start.py
  Automated mode:     python quick_start.py --amazon-id YOUR_ID [--no-prompt]
"""

import os
import subprocess
import sys
import shutil
import argparse


def check_python_version():
    """Ensure Python 3.7+"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("⚠️  Some dependencies may have failed to install")


def setup_config(amazon_id=None, tracking_id=None, openai_key=None):
    """Setup configuration files"""
    print("\n⚙️  Setting up configuration...")
    
    # Create .env if it doesn't exist or update it with provided values
    if not os.path.exists('.env') or amazon_id:
        if amazon_id:
            # Create .env with provided credentials
            # Note: Tracking ID defaults to Amazon ID. Many users use the same value for both,
            # though Amazon IDs can have suffixes like '-20'. Users can customize via --tracking-id.
            tracking_id = tracking_id or amazon_id
            openai_key = openai_key or "optional-for-ai-content"
            
            with open('.env', 'w') as f:
                f.write(f"# Amazon Associate Credentials\n")
                f.write(f"AMAZON_ASSOCIATE_ID={amazon_id}\n")
                f.write(f"AMAZON_TRACKING_ID={tracking_id}\n")
                f.write(f"\n# Optional: Add API keys for advanced features\n")
                f.write(f"OPENAI_API_KEY={openai_key}\n")
                f.write(f"\n# Publishing Platform Credentials (optional - enable in config.yaml)\n")
                f.write(f"# WordPress\n")
                f.write(f"WP_SITE_URL=https://yoursite.com\n")
                f.write(f"WP_USERNAME=your-username\n")
                f.write(f"WP_APP_PASSWORD=your-app-password\n")
                f.write(f"\n# Medium\n")
                f.write(f"MEDIUM_TOKEN=your-integration-token\n")
                f.write(f"\n# Ghost CMS\n")
                f.write(f"GHOST_API_URL=https://yoursite.com\n")
                f.write(f"GHOST_ADMIN_KEY=your-admin-key-id:secret\n")
                f.write(f"\n# Generic Webhook\n")
                f.write(f"WEBHOOK_URL=https://your-webhook-endpoint.com/publish\n")
            
            print("✅ Created .env file with your Amazon credentials")
        elif os.path.exists('.env.example'):
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from template")
            print("   ⚠️  Please edit .env and add your Amazon Associate ID!")
        else:
            print("⚠️  .env.example not found")
    else:
        print("✅ .env file already exists")
    
    # Check config.yaml
    if os.path.exists('config.yaml'):
        print("✅ config.yaml found")
    else:
        print("❌ config.yaml not found!")


def run_content_generator():
    """Run the content generator"""
    print("\n🚀 Running content generator...\n")
    print("=" * 60)
    
    try:
        subprocess.check_call([sys.executable, "content_generator.py"])
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Content generation failed with error code {e.returncode}")
        sys.exit(1)


def main():
    """Main quick start flow"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Quick Start Script for Automated Content System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode:    python quick_start.py
  Automated mode:      python quick_start.py --amazon-id mystore-20 --no-prompt
  With OpenAI key:     python quick_start.py --amazon-id mystore-20 --openai-key sk-...
        """
    )
    parser.add_argument('--amazon-id', type=str, help='Amazon Associate ID')
    parser.add_argument('--tracking-id', type=str, help='Amazon Tracking ID (defaults to amazon-id)')
    parser.add_argument('--openai-key', type=str, help='OpenAI API key (optional)')
    parser.add_argument('--no-prompt', action='store_true', help='Skip all interactive prompts')
    parser.add_argument('--skip-generation', action='store_true', help='Skip initial content generation')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🎯 QUICK START - Automated Content Creation System")
    print("=" * 60)
    
    check_python_version()
    install_dependencies()
    setup_config(args.amazon_id, args.tracking_id, args.openai_key)
    
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    
    # If Amazon ID was provided, we're in automated mode
    if args.amazon_id:
        print("\n✅ Configuration complete with Amazon Associate ID:", args.amazon_id)
        
        if not args.skip_generation:
            print("\n🚀 Generating initial content...")
            run_content_generator()
            print("\n✅ All done! Check the 'generated_content' folder.")
        else:
            print("\n⏭️  Skipping initial content generation")
            print("\n📝 Next Steps:")
            print("   Run: python content_generator.py")
            print("   For scheduled generation: python content_generator.py --schedule")
    else:
        # Interactive mode
        print("\n📝 Next Steps:")
        print("1. Edit .env and add your Amazon Associate ID")
        print("2. (Optional) Edit config.yaml to customize settings")
        print("3. Run: python content_generator.py")
        print("4. For scheduled generation: python content_generator.py --schedule")
        
        if not args.no_prompt:
            print("\n🤔 Want to generate content now? (y/n): ", end="")
            
            try:
                response = input().strip().lower()
                if response == 'y':
                    run_content_generator()
                    print("\n✅ All done! Check the 'generated_content' folder.")
            except KeyboardInterrupt:
                print("\n\n👋 Setup complete. Run the generator when you're ready!")
        else:
            print("\n👋 Setup complete. Run the generator when you're ready!")


if __name__ == "__main__":
    main()
