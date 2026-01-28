# 💰 Automated Content Creation System

[![CI](https://github.com/S3OPS/money/actions/workflows/ci.yml/badge.svg)](https://github.com/S3OPS/money/actions/workflows/ci.yml)
[![CodeQL](https://github.com/S3OPS/money/actions/workflows/codeql.yml/badge.svg)](https://github.com/S3OPS/money/actions/workflows/codeql.yml)
[![Scheduled Content](https://github.com/S3OPS/money/actions/workflows/scheduled-content.yml/badge.svg)](https://github.com/S3OPS/money/actions/workflows/scheduled-content.yml)

Automated product review content generator with Amazon Associates affiliate links. Generate content in seconds with minimal setup.

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

- **[QUICK_START.md](QUICK_START.md)** - Detailed setup guide with all options
- **[AUTOMATION.md](AUTOMATION.md)** - GitHub Actions automation setup
- **[PUBLISHING.md](PUBLISHING.md)** - YouTube publishing configuration
- **[scripts/README.md](scripts/README.md)** - Setup scripts documentation

## 🤖 Automation

This repository includes GitHub Actions workflows for:
- ✅ Continuous Integration (tests on Python 3.8-3.11)
- 🔒 Security scanning (CodeQL, dependency checks)
- 📅 Scheduled content generation (daily at 9 AM UTC)

See [AUTOMATION.md](AUTOMATION.md) for setup instructions.

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
