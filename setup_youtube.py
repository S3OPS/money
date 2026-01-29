#!/usr/bin/env python3
"""
YouTube Setup Script
One-command automated configuration for YouTube credentials
"""

import os
import sys
import subprocess
from pathlib import Path
import io

# Fix Unicode encoding issues on Windows
if hasattr(sys.stdout, 'buffer') and sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def print_header():
    """Print setup header"""
    print("=" * 80)
    print("🎥 YOUTUBE AUTOMATED SETUP")
    print("=" * 80)
    print()
    print("This script will help you configure YouTube publishing.")
    print("Your credentials will be stored securely in the .env file.")
    print()


def print_section(title):
    """Print section header"""
    print()
    print("─" * 80)
    print(f"📝 {title}")
    print("─" * 80)
    print()


def check_dependencies():
    """Check and install required dependencies"""
    print_section("Checking Dependencies")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    print("📦 Installing required packages...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("✅ All dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("⚠️  Some dependencies may have failed to install")


def load_env_file():
    """Load existing .env file or create from template"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("📄 Creating .env file from template...")
            with open(env_example, 'r') as f:
                content = f.read()
            with open(env_file, 'w') as f:
                f.write(content)
            print("✅ Created .env file")
        else:
            print("❌ .env.example not found!")
            sys.exit(1)
    
    # Read current .env content
    with open(env_file, 'r') as f:
        return f.read()


def update_env_value(env_content, key, value):
    """Update or add a value in .env content with proper escaping"""
    # Escape special characters in value
    # Quote value if it contains spaces or special characters
    if any(char in value for char in [' ', '"', "'", '\\', '\n', '\r', '$', '`']):
        # Escape quotes and backslashes
        value = value.replace('\\', '\\\\').replace('"', '\\"')
        value = f'"{value}"'
    
    lines = env_content.split('\n')
    updated = False
    new_lines = []
    
    for line in lines:
        if line.strip().startswith(f"{key}="):
            new_lines.append(f"{key}={value}")
            updated = True
        else:
            new_lines.append(line)
    
    # If key wasn't found, add it
    if not updated:
        new_lines.append(f"{key}={value}")
    
    return '\n'.join(new_lines)


def save_env_file(content):
    """Save .env file with proper permissions"""
    env_file = Path(".env")
    with open(env_file, 'w') as f:
        f.write(content)
    
    # Set secure permissions (owner read/write only)
    try:
        os.chmod(env_file, 0o600)
    except Exception:
        pass  # May not work on Windows


def setup_youtube():
    """Setup YouTube credentials"""
    print_section("YouTube Setup")
    
    print("📺 YouTube requires:")
    print("   1. A YouTube Channel ID")
    print("   2. OAuth 2.0 credentials file (youtube_credentials.json)")
    print()
    print("ℹ️  To get these:")
    print("   • Go to: https://console.cloud.google.com/")
    print("   • Create a project and enable YouTube Data API v3")
    print("   • Create OAuth 2.0 credentials (Desktop app)")
    print("   • Download the JSON file and save it as 'youtube_credentials.json'")
    print()
    
    setup_yt = input("Do you want to configure YouTube now? (y/n): ").strip().lower()
    if setup_yt != 'y':
        print("⏭️  Skipping YouTube setup")
        return None, None
    
    print()
    channel_id = input("Enter your YouTube Channel ID: ").strip()
    
    while not channel_id:
        print("⚠️  Channel ID is required!")
        channel_id = input("Enter your YouTube Channel ID: ").strip()
    
    # Check for credentials file
    creds_file = "youtube_credentials.json"
    if not Path(creds_file).exists():
        print()
        print(f"⚠️  Credentials file '{creds_file}' not found in current directory!")
        print("   Please download it from Google Cloud Console first.")
        print()
        creds_file = input("Enter the path to your credentials file (or press Enter to skip): ").strip()
        
        if not creds_file or not Path(creds_file).exists():
            print("⚠️  Credentials file not found. You'll need to add it later.")
            creds_file = "youtube_credentials.json"
    else:
        print(f"✅ Found credentials file: {creds_file}")
    
    print()
    print(f"✅ YouTube configured:")
    print(f"   Channel ID: {channel_id}")
    print(f"   Credentials: {creds_file}")
    
    return channel_id, creds_file


def update_config_yaml():
    """Update config.yaml to enable YouTube"""
    config_file = Path("config.yaml")
    
    if not config_file.exists():
        print("⚠️  config.yaml not found, skipping configuration update")
        return
    
    print()
    print("⚙️  Updating config.yaml to enable YouTube...")
    
    try:
        import yaml
        
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        # Enable auto_publish if not already enabled
        if 'publishing' in config:
            if config['publishing'].get('auto_publish') == False:
                config['publishing']['auto_publish'] = True
                print("✅ Enabled auto_publish in config.yaml")
        
        # Save back to file
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            
    except ImportError:
        # Fallback to simple string replacement if yaml not available
        with open(config_file, 'r') as f:
            content = f.read()
        
        # Only replace if it's the exact key-value pair in publishing section
        if 'auto_publish: false' in content:
            content = content.replace('auto_publish: false', 'auto_publish: true')
            with open(config_file, 'w') as f:
                f.write(content)
            print("✅ Enabled auto_publish in config.yaml")
    except Exception as e:
        print(f"⚠️  Could not update config.yaml: {e}")


def test_configuration():
    """Test the configuration"""
    print_section("Testing Configuration")
    
    print("🧪 Running system tests...")
    try:
        result = subprocess.run(
            [sys.executable, "test_system.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            # Show summary
            for line in result.stdout.split('\n'):
                if '✅ PASS:' in line or 'Results:' in line or '🎉' in line:
                    print(f"   {line}")
        else:
            print("⚠️  Some tests failed (this may be OK if you haven't added all credentials)")
    except subprocess.TimeoutExpired:
        print("⚠️  Tests timed out")
    except Exception as e:
        print(f"⚠️  Could not run tests: {e}")


def print_next_steps(yt_configured):
    """Print next steps"""
    print()
    print("=" * 80)
    print("✨ SETUP COMPLETE!")
    print("=" * 80)
    print()
    print("📋 What was configured:")
    if yt_configured:
        print("   ✅ YouTube credentials added to .env")
    else:
        print("   ⏭️  YouTube setup skipped")
    
    print()
    print("🎯 Next Steps:")
    print()
    
    if yt_configured:
        print("1. 🎥 YouTube:")
        print("   • Ensure 'youtube_credentials.json' is in the project directory")
        print("   • Run the generator - first time will open browser for OAuth")
        print()
    
    print("2. 🚀 Generate Content:")
    print("   python content_generator.py")
    print()
    
    print("3. 📖 Documentation:")
    print("   • Quick guide: YOUTUBE_SETUP.md")
    print("   • Full guide: PUBLISHING.md")
    print("   • Main README: README.md")
    print()
    
    print("🔒 Security Note:")
    print("   Your credentials are stored in .env with restricted permissions.")
    print("   Never commit .env to version control (it's in .gitignore).")
    print()
    print("=" * 80)


def main():
    """Main setup flow"""
    print_header()
    
    # Confirm setup (wait for user to press Enter)
    input("Press Enter to start setup (or Ctrl+C to cancel)... ")
    
    # Check dependencies
    check_dependencies()
    
    # Load .env file
    env_content = load_env_file()
    
    # Setup YouTube
    yt_channel_id, yt_creds_file = setup_youtube()
    if yt_channel_id:
        env_content = update_env_value(env_content, "YOUTUBE_CHANNEL_ID", yt_channel_id)
        env_content = update_env_value(env_content, "YOUTUBE_CREDENTIALS_FILE", yt_creds_file)
    
    # Save .env file
    print_section("Saving Configuration")
    save_env_file(env_content)
    print("✅ Configuration saved to .env (secure permissions set)")
    
    # Update config.yaml
    update_config_yaml()
    
    # Test configuration
    test_configuration()
    
    # Print next steps
    print_next_steps(yt_channel_id is not None)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
