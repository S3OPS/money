# 💰 Automated Content Creation System for Amazon Associates

[![CI](https://github.com/S3OPS/money/actions/workflows/ci.yml/badge.svg)](https://github.com/S3OPS/money/actions/workflows/ci.yml)
[![CodeQL](https://github.com/S3OPS/money/actions/workflows/codeql.yml/badge.svg)](https://github.com/S3OPS/money/actions/workflows/codeql.yml)
[![Scheduled Content](https://github.com/S3OPS/money/actions/workflows/scheduled-content.yml/badge.svg)](https://github.com/S3OPS/money/actions/workflows/scheduled-content.yml)

Automated product review content generator with Amazon Associates affiliate links. Generate content in seconds with minimal setup.

## 📖 Complete Setup Guide

**NEW!** → **[COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md)** - The consolidated guide for 100% automation setup

This single comprehensive guide combines all setup, configuration, and installation instructions with the correct sequence order to take you from zero to fully automated operation.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/S3OPS/money.git
cd money

# Run setup (installs dependencies and configures environment)
python quick_start.py

# Generate content
python content_generator.py
```

Your generated content will be in the `generated_content/` folder.

**For detailed step-by-step instructions, see [COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md)**

## ✨ Features

- 🤖 **Automated Content Generation** - Create product reviews with a single command
- 💵 **Amazon Associates Integration** - Automatic affiliate link insertion
- 📤 **YouTube Publishing** - Auto-post to YouTube Community (optional)
- 📅 **Scheduled Generation** - GitHub Actions workflow for daily content creation
- 🔒 **Secure** - Environment variables for credentials
- 📝 **Multiple Formats** - Output to Markdown, HTML, or JSON

## 📋 Requirements

- Python 3.7+
- Amazon Associate ID ([sign up free](https://affiliate-program.amazon.com/))

## ⚙️ Configuration

### 1. Amazon Associates Setup

Add your credentials to `.env`:

```bash
AMAZON_ASSOCIATE_ID=yourname-20
AMAZON_TRACKING_ID=yourname-20
```

### 2. Customize Settings (Optional)

Edit `config.yaml` to change:
- Product categories
- Number of products per post
- Output format
- Publishing settings

See [QUICK_START.md](QUICK_START.md) for detailed setup options.

## 🎯 Usage

```bash
# Generate content once
python content_generator.py

# Run with scheduling (generates content at 9 AM UTC daily)
python content_generator.py --schedule
```

## 📚 Documentation

**Start Here:**
- **[COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md)** - ⭐ **Complete setup guide with everything in sequence order for 100% automation**

**Additional Guides:**
- **[QUICK_START.md](QUICK_START.md)** - Quick reference for common tasks
- **[AUTOMATION.md](AUTOMATION.md)** - GitHub Actions automation setup
- **[PUBLISHING.md](PUBLISHING.md)** - YouTube publishing configuration
- **[scripts/README.md](scripts/README.md)** - Setup scripts documentation
- **[THE_ONE_RING.md](THE_ONE_RING.md)** - Master documentation hub

## 🤖 Automation

This repository includes GitHub Actions workflows for:
- ✅ Continuous Integration (tests on Python 3.8-3.11)
- 🔒 Security scanning (CodeQL, dependency checks)
- 📅 Scheduled content generation (daily at 9 AM UTC)
- 🔐 **NEW:** Automated secrets validation and setup wizard

**Quick Setup:**
1. Go to **Actions** tab → **Setup Wizard**
2. Click **Run workflow** to check your configuration
3. Follow the automated instructions to configure credentials

See [AUTOMATION.md](AUTOMATION.md) or [SECRETS_SETUP.md](SECRETS_SETUP.md) for detailed setup instructions.

## 🔐 Security

- Store credentials in `.env` (never commit to git)
- `.env` is in `.gitignore` by default
- Regularly rotate API keys
- Automated security scanning via CodeQL

## ⚠️ Disclaimer

- Review and customize generated content before publishing
- Comply with Amazon Associates Program Operating Agreement
- Follow FTC guidelines for affiliate link disclosure
- Verify product information before publishing

## 📄 License

Provided as-is for educational and commercial use.

---

**Made for affiliate marketers who want to automate their content creation.** 💰
