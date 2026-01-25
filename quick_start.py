#!/usr/bin/env python3
"""
Quick Start Script - Run this to get started immediately!
"""

import os
import subprocess
import sys
import shutil


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


def setup_config():
    """Setup configuration files"""
    print("\n⚙️  Setting up configuration...")
    
    # Create .env if it doesn't exist
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
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
    print("=" * 60)
    print("🎯 QUICK START - Automated Content Creation System")
    print("=" * 60)
    
    check_python_version()
    install_dependencies()
    setup_config()
    
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    
    print("\n📝 Next Steps:")
    print("1. Edit .env and add your Amazon Associate ID")
    print("2. (Optional) Edit config.yaml to customize settings")
    print("3. Run: python content_generator.py")
    print("4. For scheduled generation: python content_generator.py --schedule")
    
    print("\n🤔 Want to generate content now? (y/n): ", end="")
    
    try:
        response = input().strip().lower()
        if response == 'y':
            run_content_generator()
            print("\n✅ All done! Check the 'generated_content' folder.")
    except KeyboardInterrupt:
        print("\n\n👋 Setup complete. Run the generator when you're ready!")


if __name__ == "__main__":
    main()
