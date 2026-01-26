#!/bin/bash
# Automated GitHub Secrets Configuration Script
# This script helps automate the setup of GitHub Secrets for the automation workflows

set -e

REPO_OWNER="${REPO_OWNER:-S3OPS}"
REPO_NAME="${REPO_NAME:-money}"
REPO_PATH="${REPO_PATH:-${REPO_OWNER}/${REPO_NAME}}"

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║         🔐 GitHub Secrets Automation Setup for $REPO_OWNER/$REPO_NAME          ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed!"
    echo ""
    echo "Please install it first:"
    echo "  • macOS: brew install gh"
    echo "  • Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md"
    echo "  • Windows: https://github.com/cli/cli/releases"
    echo ""
    exit 1
fi

# Check if user is authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub CLI"
    echo ""
    echo "Please authenticate first:"
    echo "  gh auth login"
    echo ""
    exit 1
fi

echo "✅ GitHub CLI is installed and authenticated"
echo ""

# Function to add or update a secret
add_secret() {
    local secret_name=$1
    local secret_description=$2
    local is_required=$3
    local example_value=$4
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📝 Setting up: $secret_name"
    echo "   Description: $secret_description"
    if [ "$is_required" = "true" ]; then
        echo "   Status: ⚠️  REQUIRED"
    else
        echo "   Status: ℹ️  Optional"
    fi
    if [ -n "$example_value" ]; then
        echo "   Example: $example_value"
    fi
    echo ""
    
    # Check if secret already exists
    if gh secret list -R "$REPO_OWNER/$REPO_NAME" | grep -q "^$secret_name"; then
        echo "   ℹ️  Secret already exists"
        read -p "   Do you want to update it? (y/N): " update_choice
        if [[ ! "$update_choice" =~ ^[Yy]$ ]]; then
            echo "   ⏭️  Skipping $secret_name"
            echo ""
            return
        fi
    fi
    
    if [ "$is_required" = "true" ]; then
        read -p "   Enter value for $secret_name: " secret_value
        while [ -z "$secret_value" ]; do
            echo "   ⚠️  This secret is required!"
            read -p "   Enter value for $secret_name: " secret_value
        done
    else
        read -p "   Enter value for $secret_name (press Enter to skip): " secret_value
        if [ -z "$secret_value" ]; then
            echo "   ⏭️  Skipping optional secret"
            echo ""
            return
        fi
    fi
    
    # Add the secret
    echo "$secret_value" | gh secret set "$secret_name" -R "$REPO_OWNER/$REPO_NAME"
    
    if [ $? -eq 0 ]; then
        echo "   ✅ Successfully set $secret_name"
    else
        echo "   ❌ Failed to set $secret_name"
    fi
    echo ""
}

echo "This script will guide you through setting up GitHub Secrets."
echo "These secrets are required for the automated workflows to function."
echo ""
read -p "Press Enter to continue..."
echo ""

# Required secrets
add_secret "AMAZON_ASSOCIATE_ID" "Your Amazon Associate ID" "true" "mystore-20"
add_secret "AMAZON_TRACKING_ID" "Your Amazon tracking ID" "true" "mystore-20"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📤 Optional: YouTube Publishing Credentials"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "The following secrets are optional but enable YouTube publishing:"
echo ""
read -p "Do you want to configure YouTube publishing credentials? (y/N): " setup_publishing

if [[ "$setup_publishing" =~ ^[Yy]$ ]]; then
    echo ""
    add_secret "YOUTUBE_CHANNEL_ID" "YouTube channel ID for community posts" "false" "UCxxxxxxxxxxxxxxxxxxxxx"
    add_secret "YOUTUBE_CREDENTIALS_FILE" "YouTube OAuth credentials file path" "false" "youtube_credentials.json"
    add_secret "YOUTUBE_API_KEY" "YouTube API key (optional)" "false" ""
else
    echo "   ⏭️  Skipping publishing platform setup"
    echo ""
fi

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                            ✅ Setup Complete!                                 ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Summary of configured secrets:"
gh secret list -R "$REPO_OWNER/$REPO_NAME"
echo ""
echo "🎯 Next Steps:"
echo "   1. Verify secrets are set correctly above"
echo "   2. Go to: https://github.com/$REPO_OWNER/$REPO_NAME/actions"
echo "   3. Enable workflows if prompted"
echo "   4. Test 'Scheduled Content Generation' workflow manually"
echo "   5. Monitor the Actions tab for workflow runs"
echo ""
echo "📖 For more information, see: AUTOMATION.md"
echo ""
