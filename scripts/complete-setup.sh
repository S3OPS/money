#!/bin/bash
# Complete Automation Setup Script
# This script automates the entire setup process for the money repository

set -e

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║              🚀 Complete Automation Setup for S3OPS/money                    ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "This script will:"
echo "  1. ✅ Verify all dependencies"
echo "  2. 🔐 Setup GitHub Secrets"
echo "  3. ⚙️  Configure automation workflows"
echo "  4. 🧪 Run verification tests"
echo "  5. 🎯 Enable workflows in GitHub"
echo ""
read -p "Press Enter to start the automated setup..."
echo ""

# Change to script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$REPO_ROOT"

# Determine repository owner/name for links and child scripts
REPO_OWNER="${REPO_OWNER:-}"
REPO_NAME="${REPO_NAME:-}"
REPO_PATH="${REPO_PATH:-}"

parse_repo_from_remote() {
    local remote_url="$1"
    local path_part=""

    if [[ "$remote_url" =~ ^git@[^:]+:(.+)$ ]]; then
        path_part="${BASH_REMATCH[1]}"
    elif [[ "$remote_url" =~ ^https?://[^/]+/(.+)$ ]]; then
        path_part="${BASH_REMATCH[1]}"
    else
        return 1
    fi

    path_part="${path_part%.git}"
    path_part="${path_part%/}"

    if [[ "$path_part" != */* ]]; then
        return 1
    fi

    REPO_NAME="${path_part##*/}"
    REPO_OWNER="${path_part%/*}"

    if [ -z "$REPO_OWNER" ] || [ -z "$REPO_NAME" ]; then
        return 1
    fi

    return 0
}

if [ -z "$REPO_OWNER" ] || [ -z "$REPO_NAME" ]; then
    if [ -z "$REPO_PATH" ] && command -v gh &> /dev/null; then
        REPO_PATH=$(gh repo view --json nameWithOwner --jq .nameWithOwner 2>/dev/null || true)
    fi
    if [ -z "$REPO_PATH" ]; then
        REMOTE_URL=$(git config --get remote.origin.url 2>/dev/null || true)
        if [ -n "$REMOTE_URL" ]; then
            if parse_repo_from_remote "$REMOTE_URL"; then
                REPO_PATH="${REPO_OWNER}/${REPO_NAME}"
            fi
        fi
    fi
    if [ -n "$REPO_PATH" ]; then
        REPO_OWNER="${REPO_PATH%%/*}"
        REPO_NAME="${REPO_PATH##*/}"
    fi
fi

REPO_OWNER="${REPO_OWNER:-S3OPS}"
REPO_NAME="${REPO_NAME:-money}"
REPO_SLUG="${REPO_OWNER}/${REPO_NAME}"
REPO_PATH="${REPO_SLUG}"
export REPO_OWNER REPO_NAME REPO_PATH

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Check dependencies
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Checking Dependencies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ Python installed: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python 3 is not installed!${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✅ pip3 installed${NC}"
else
    echo -e "${RED}❌ pip3 is not installed!${NC}"
    exit 1
fi

# Check GitHub CLI
if command -v gh &> /dev/null; then
    echo -e "${GREEN}✅ GitHub CLI installed${NC}"
    GH_CLI_AVAILABLE=true
else
    echo -e "${YELLOW}⚠️  GitHub CLI not installed (optional for secrets setup)${NC}"
    GH_CLI_AVAILABLE=false
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Python dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install Python dependencies${NC}"
    exit 1
fi

# Step 2: Setup GitHub Secrets
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2: Setting Up GitHub Secrets"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$GH_CLI_AVAILABLE" = true ]; then
    if gh auth status &> /dev/null; then
        echo -e "${GREEN}✅ GitHub CLI authenticated${NC}"
        echo ""
        read -p "Do you want to setup GitHub Secrets now? (Y/n): " setup_secrets
        if [[ ! "$setup_secrets" =~ ^[Nn]$ ]]; then
            bash "$SCRIPT_DIR/setup-secrets.sh"
        else
            echo -e "${YELLOW}⏭️  Skipping secrets setup${NC}"
            echo "   You can run it later with: ./scripts/setup-secrets.sh"
        fi
    else
        echo -e "${YELLOW}⚠️  Not authenticated with GitHub CLI${NC}"
        echo "   Run 'gh auth login' to authenticate, then run:"
        echo "   ./scripts/setup-secrets.sh"
    fi
else
    echo -e "${YELLOW}ℹ️  GitHub CLI not available${NC}"
    echo ""
    echo "To setup secrets manually:"
    echo "  1. Go to: https://github.com/${REPO_SLUG}/settings/secrets/actions"
    echo "  2. Add these required secrets:"
    echo "     • AMAZON_ASSOCIATE_ID"
    echo "     • AMAZON_TRACKING_ID"
    echo ""
    echo "Or install GitHub CLI and run: ./scripts/setup-secrets.sh"
fi

# Step 3: Configure local environment
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3: Configuring Local Environment"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo -e "${GREEN}✅ .env file created${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env and add your Amazon Associate credentials${NC}"
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

# Step 4: Run tests
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 4: Running System Tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python3 test_system.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed${NC}"
else
    echo -e "${YELLOW}⚠️  Some tests failed (this may be OK if credentials aren't set yet)${NC}"
fi

# Step 5: Run verification
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 5: Verifying Automation Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$GH_CLI_AVAILABLE" = true ] && gh auth status &> /dev/null; then
    python3 "$SCRIPT_DIR/verify-automation.py"
else
    echo -e "${YELLOW}ℹ️  Skipping verification (GitHub CLI not authenticated)${NC}"
    echo "   Run later with: python3 scripts/verify-automation.py"
fi

# Final summary
echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                        ✅ Setup Complete!                                     ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🎯 Next Steps:"
echo ""
echo "1. 📝 Edit .env file with your Amazon Associate credentials:"
echo "   nano .env"
echo ""
echo "2. 🔐 Setup GitHub Secrets (if not done already):"
echo "   ./scripts/setup-secrets.sh"
echo ""
echo "3. 🌐 Enable workflows on GitHub:"
echo "   • Go to: https://github.com/${REPO_SLUG}/actions"
echo "   • Click 'I understand my workflows, go ahead and enable them'"
echo ""
echo "4. 🧪 Test the scheduled content generation:"
echo "   • Actions → Scheduled Content Generation → Run workflow"
echo ""
echo "5. 📊 Monitor automation:"
echo "   • View workflow runs in the Actions tab"
echo "   • Check generated content in artifacts"
echo ""
echo "📖 For detailed information, see:"
echo "   • AUTOMATION.md - Complete automation guide"
echo "   • AUTOMATION-SUMMARY.md - Implementation details"
echo "   • README.md - General usage"
echo ""
echo "🎉 Your automated affiliate marketing system is ready to generate income!"
echo ""
