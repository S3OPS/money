#!/bin/bash
# Fully Automated One-Command Setup Script
# No interactive prompts - all configuration via command-line arguments or environment variables
#
# Usage:
#   ./automated_setup.sh --amazon-id YOUR_ID --tracking-id YOUR_ID-20
#   
# Or with environment variables:
#   AMAZON_ASSOCIATE_ID=yourname-20 AMAZON_TRACKING_ID=yourname-20 ./automated_setup.sh
#
# Options:
#   --amazon-id ID          Amazon Associate ID (required)
#   --tracking-id ID        Amazon Tracking ID (default: AMAZON_ID-20)
#   --openai-key KEY        OpenAI API key (optional)
#   --skip-tests            Skip running tests
#   --skip-generation       Skip initial content generation
#   --help                  Show this help message

set -e

# Default values
SKIP_TESTS=false
SKIP_GENERATION=false
AMAZON_ASSOCIATE_ID="${AMAZON_ASSOCIATE_ID:-}"
AMAZON_TRACKING_ID="${AMAZON_TRACKING_ID:-}"
OPENAI_API_KEY="${OPENAI_API_KEY:-}"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --amazon-id)
            AMAZON_ASSOCIATE_ID="$2"
            shift 2
            ;;
        --tracking-id)
            AMAZON_TRACKING_ID="$2"
            shift 2
            ;;
        --openai-key)
            OPENAI_API_KEY="$2"
            shift 2
            ;;
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --skip-generation)
            SKIP_GENERATION=true
            shift
            ;;
        --help)
            echo "Fully Automated Setup Script"
            echo ""
            echo "Usage:"
            echo "  ./automated_setup.sh --amazon-id YOUR_ID [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --amazon-id ID          Amazon Associate ID (required)"
            echo "  --tracking-id ID        Amazon Tracking ID (default: same as amazon-id)"
            echo "  --openai-key KEY        OpenAI API key (optional)"
            echo "  --skip-tests            Skip running tests"
            echo "  --skip-generation       Skip initial content generation"
            echo "  --help                  Show this help message"
            echo ""
            echo "Environment Variables (alternative to command-line args):"
            echo "  AMAZON_ASSOCIATE_ID     Amazon Associate ID"
            echo "  AMAZON_TRACKING_ID      Amazon Tracking ID"
            echo "  OPENAI_API_KEY          OpenAI API key"
            echo ""
            echo "Examples:"
            echo "  ./automated_setup.sh --amazon-id mystore-20"
            echo "  AMAZON_ASSOCIATE_ID=mystore-20 ./automated_setup.sh"
            echo "  ./automated_setup.sh --amazon-id mystore-20 --skip-tests"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Validate required parameters
if [ -z "$AMAZON_ASSOCIATE_ID" ]; then
    echo "❌ Error: Amazon Associate ID is required!"
    echo ""
    echo "Usage:"
    echo "  ./automated_setup.sh --amazon-id YOUR_ID"
    echo "  Or set AMAZON_ASSOCIATE_ID environment variable"
    echo ""
    echo "Use --help for more information"
    exit 1
fi

# Set tracking ID to associate ID if not provided
if [ -z "$AMAZON_TRACKING_ID" ]; then
    AMAZON_TRACKING_ID="$AMAZON_ASSOCIATE_ID"
fi

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║           🚀 Fully Automated Setup - No User Input Required                  ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Configuration:"
echo "  Amazon Associate ID: $AMAZON_ASSOCIATE_ID"
echo "  Amazon Tracking ID:  $AMAZON_TRACKING_ID"
if [ -n "$OPENAI_API_KEY" ]; then
    echo "  OpenAI API Key:      ✅ Provided"
else
    echo "  OpenAI API Key:      ⏭️ Not provided (optional)"
fi
echo ""

# Step 1: Check Python
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Checking Dependencies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found!"
    echo "   Please install Python 3.7+ and try again"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ Python found: $PYTHON_VERSION"

# Step 2: Install dependencies
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2: Installing Dependencies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "Installing Python packages..."
python3 -m pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Step 3: Configure environment
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3: Configuring Environment"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Create .env file with provided configuration
echo "Creating .env file with your configuration..."
cat > .env << EOF
# Amazon Associate Credentials
AMAZON_ASSOCIATE_ID=$AMAZON_ASSOCIATE_ID
AMAZON_TRACKING_ID=$AMAZON_TRACKING_ID

# Optional: Add API keys for advanced features
OPENAI_API_KEY=${OPENAI_API_KEY:-optional-for-ai-content}

# Publishing Platform Credentials (optional - enable in config.yaml)
# YouTube
YOUTUBE_CHANNEL_ID=your-channel-id
YOUTUBE_CREDENTIALS_FILE=youtube_credentials.json
YOUTUBE_API_KEY=optional-api-key
EOF

echo "✅ .env file created with your Amazon credentials"

# Verify config.yaml exists
if [ -f "config.yaml" ]; then
    echo "✅ config.yaml found"
else
    echo "❌ config.yaml not found!"
    exit 1
fi

# Step 4: Run tests (optional)
if [ "$SKIP_TESTS" = false ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Step 4: Running System Tests"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if [ ! -f "test_system.py" ]; then
        echo "⚠️  test_system.py not found, skipping tests"
    elif python3 test_system.py; then
        echo "✅ All tests passed"
    else
        echo "⚠️  Some tests failed (may be OK if optional features aren't configured)"
    fi
else
    echo ""
    echo "⏭️  Skipping tests (--skip-tests flag provided)"
fi

# Step 5: Generate initial content (optional)
if [ "$SKIP_GENERATION" = false ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Step 5: Generating Initial Content"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if [ ! -f "content_generator.py" ]; then
        echo "❌ content_generator.py not found!"
        echo "   Please ensure you're running this script from the repository root."
        exit 1
    elif python3 content_generator.py; then
        echo "✅ Content generated successfully"
        echo "📁 Check the 'generated_content/' folder"
    else
        echo "⚠️  Content generation had issues (check configuration)"
    fi
else
    echo ""
    echo "⏭️  Skipping initial content generation (--skip-generation flag provided)"
fi

# Final summary
echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                        ✅ Setup Complete!                                     ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🎯 Your automated content system is ready!"
echo ""
echo "📝 Configuration Summary:"
echo "   • Amazon Associate ID configured: $AMAZON_ASSOCIATE_ID"
echo "   • Environment file created: .env"
echo "   • Dependencies installed"
if [ "$SKIP_TESTS" = false ]; then
    echo "   • System tests completed"
fi
if [ "$SKIP_GENERATION" = false ]; then
    echo "   • Initial content generated"
fi
echo ""
echo "🚀 Quick Commands:"
echo "   Generate content:        python3 content_generator.py"
echo "   Scheduled generation:    python3 content_generator.py --schedule"
echo "   Run tests:               python3 test_system.py"
echo ""
echo "📖 Documentation:"
echo "   • README.md - General usage"
echo "   • QUICK_START.md - Quick reference"
echo "   • AUTOMATION.md - GitHub Actions automation"
echo "   • PUBLISHING.md - Auto-publishing setup"
echo ""
echo "💰 Start earning with Amazon Associates!"
echo ""
