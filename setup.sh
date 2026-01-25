#!/bin/bash
# One-Click Setup and Run Script
# This is the FASTEST way to get started!

set -e

echo "============================================================"
echo "🚀 ONE-CLICK AUTOMATED CONTENT SYSTEM SETUP"
echo "============================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found!"
    echo "   Please install Python 3.7+ and try again"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
python3 -m pip install -q -r requirements.txt
echo "✅ Dependencies installed"

# Create .env if needed
if [ ! -f .env ]; then
    echo ""
    echo "⚙️  Setting up environment..."
    
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Created .env file"
        echo ""
        echo "📝 Please edit .env and add your Amazon Associate ID"
        echo "   You can do this now or later."
        echo ""
        read -p "Do you want to edit .env now? (y/n): " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            ${EDITOR:-nano} .env
        fi
    fi
fi

# Generate content
echo ""
echo "============================================================"
echo "🎯 GENERATING YOUR FIRST CONTENT"
echo "============================================================"
echo ""

python3 content_generator.py

echo ""
echo "============================================================"
echo "✨ SUCCESS!"
echo "============================================================"
echo ""
echo "📁 Your content is in: generated_content/"
echo ""
echo "🎯 Next steps:"
echo "1. Edit .env with your Amazon Associate ID (if not done)"
echo "2. Customize config.yaml to your preferences"
echo "3. Run: python3 content_generator.py"
echo "4. For scheduled generation: python3 content_generator.py --schedule"
echo ""
echo "💰 Start earning with Amazon Associates today!"
echo ""
