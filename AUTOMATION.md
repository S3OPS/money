# 🤖 Automation Setup Guide

This repository is now fully automated with GitHub Actions workflows! This guide explains all the automated processes and how to configure them.

## 🚀 Quick Start - Fully Automated Setup

**The fastest way to complete the entire setup:**

```bash
./scripts/complete-setup.sh
```

**Windows users:** run `scripts\complete-setup.cmd` in Command Prompt or `.\scripts\complete-setup.ps1` in PowerShell (requires Git Bash or WSL).

This single script will:
- ✅ Verify dependencies
- 🔐 Configure GitHub Secrets automatically
- ⚙️  Set up local environment
- 🧪 Run tests
- 📊 Verify everything is ready

**See [scripts/README.md](scripts/README.md) for detailed script documentation.**

---

## 📋 Overview

The automation system includes:

1. **Continuous Integration (CI)** - Automated testing and code quality checks on every push/PR
2. **Security Scanning** - CodeQL analysis and dependency vulnerability scanning
3. **Scheduled Content Generation** - Automatic daily content creation at 9 AM UTC
4. **Dependency Review** - Automated checks for vulnerable dependencies in PRs

## 🔄 Automated Workflows

### 1. CI - Tests and Code Quality (`ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Manual trigger via GitHub UI

**What it does:**
- ✅ Runs all tests in `test_system.py` on Python 3.8, 3.9, 3.10, and 3.11
- 📊 Performs code quality checks with flake8, pylint, black, and isort
- 🔒 Runs security scans with bandit and safety
- ✔️ Validates YAML configuration files
- 📦 Checks for required files

**Status:** Always runs on code changes to ensure quality

### 2. CodeQL Security Analysis (`codeql.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Weekly on Sundays at midnight UTC
- Manual trigger via GitHub UI

**What it does:**
- 🔍 Performs deep security analysis using GitHub's CodeQL
- 🛡️ Detects security vulnerabilities and coding errors
- 📈 Creates security alerts in the Security tab
- 📊 Provides detailed reports on code quality

**Status:** Helps maintain secure, high-quality code

### 3. Scheduled Content Generation (`scheduled-content.yml`)

**Triggers:**
- Daily at 9 AM UTC (configurable)
- Manual trigger via GitHub UI

**What it does:**
- 🤖 Automatically generates affiliate marketing content
- 📝 Creates product review articles with Amazon affiliate links
- 📤 Prepares YouTube Community posts when configured
- 💾 Stores generated content as artifacts (30-day retention)
- 📊 Provides detailed summary of generated content

**Configuration Required:**
You need to add secrets in your repository settings for this to work:

1. Go to: **Settings** → **Secrets and variables** → **Actions**
2. Add the following secrets:

**Required:**
- `AMAZON_ASSOCIATE_ID` - Your Amazon Associate ID
- `AMAZON_TRACKING_ID` - Your Amazon tracking ID (e.g., yoursite-20)

**Optional (for YouTube publishing):**
- `YOUTUBE_CHANNEL_ID` - Your YouTube channel ID
- `YOUTUBE_CREDENTIALS_FILE` - Path to OAuth credentials JSON
- `YOUTUBE_API_KEY` - YouTube API key (optional)

### 4. Dependency Review (`dependency-review.yml`)

**Triggers:**
- Pull requests to `main` or `develop`

**What it does:**
- 🔍 Scans dependency changes in PRs
- ⚠️ Flags vulnerable or risky dependencies
- 📝 Comments on PRs with security findings
- 🚫 Fails on moderate or higher severity issues

**Status:** Protects against supply chain attacks

## ⚙️ Configuration

### Setting Up Secrets

#### Option 1: Automated Validation & Setup Wizard (NEW! ✨)

The repository now includes automated workflows to help you set up secrets:

**Check Current Configuration:**
1. Go to **Actions** tab in your repository
2. Click on **Setup Wizard** workflow
3. Click **Run workflow**
4. Select "Check current configuration"
5. Review the summary to see which secrets are configured

**Get Setup Commands:**
1. Go to **Actions** tab
2. Click on **Setup Wizard** workflow  
3. Click **Run workflow**
4. Select "Generate setup commands"
5. Copy and run the generated commands

**Automatic Validation:**
- Every push/PR automatically validates that required secrets exist
- Check the **Validate Secrets** workflow runs for immediate feedback
- Warnings (not errors) if secrets are missing with setup instructions

#### Option 2: Automated Setup Script (Recommended)

Use the provided script to configure secrets automatically:

```bash
./scripts/setup-secrets.sh
```

This interactive script will:
- ✅ Guide you through adding required secrets
- 🔐 Securely configure credentials using GitHub CLI
- ⚠️  Prompt before overwriting existing secrets
- 📋 Show summary of configured secrets

**Requirements:** GitHub CLI (`gh`) installed and authenticated
- Install: `brew install gh` (macOS) or see [scripts/README.md](scripts/README.md)
- Authenticate: `gh auth login`

#### Option 3: Manual Setup

To enable automated content generation and publishing manually:

1. Navigate to your repository on GitHub
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret from the list above

Example:
```
Name: AMAZON_ASSOCIATE_ID
Value: mystore-20
```

### Customizing Schedule

To change the content generation schedule, edit `.github/workflows/scheduled-content.yml`:

```yaml
schedule:
  # Change this cron expression
  - cron: '0 9 * * *'  # Daily at 9 AM UTC
```

**Cron examples:**
- `0 */6 * * *` - Every 6 hours
- `0 0 * * *` - Daily at midnight UTC
- `0 9 * * 1,3,5` - Monday, Wednesday, Friday at 9 AM UTC

**Important Notes:**
- ⚠️ GitHub Actions scheduled workflows have a minimum 5-minute interval
- ⚠️ Scheduled workflows may experience delays during high load times
- ⚠️ Workflows won't run if the repository has had no activity for 60 days

### Enabling/Disabling Auto-Publishing

Edit `config.yaml` to control publishing:

```yaml
publishing:
  auto_publish: true  # Set to false to disable auto-publishing
  platforms:
    - type: "youtube"
      enabled: true  # Enable/disable YouTube publishing
```

## 📊 Monitoring Automation

### Viewing Workflow Runs

1. Go to the **Actions** tab in your repository
2. Select a workflow from the left sidebar
3. View recent runs, logs, and results

### Checking Generated Content

After scheduled content generation:
1. Go to the **Actions** tab
2. Click on a **Scheduled Content Generation** run
3. Scroll down to **Artifacts**
4. Download `generated-content-XXXXX.zip`

### Reviewing Security Alerts

1. Go to the **Security** tab
2. Click **Code scanning alerts** for CodeQL findings
3. Review and fix any identified issues

## 🎯 Best Practices

1. **Always review generated content** before publishing to production
2. **Monitor workflow runs** regularly for failures
3. **Update secrets** when credentials change
4. **Review security alerts** promptly
5. **Test changes** in a separate branch before merging to main

## 🔧 Troubleshooting

### Workflow Fails with "Secret not found"

**Solution:** Add the required secrets in repository settings (see "Setting Up Secrets" above)

### Tests Fail on Python 3.11 but Pass on 3.8

**Solution:** Check for compatibility issues in dependencies or code. Update as needed.

### CodeQL Analysis Times Out

**Solution:** This is normal for large codebases. GitHub will retry automatically.

### Scheduled Content Not Generated

**Possible causes:**
1. Secrets not configured correctly
2. Workflow disabled in Actions settings
3. Repository is private without GitHub Actions minutes

**Solution:** 
- Verify secrets are set correctly
- Check Actions tab for error messages
- Ensure you have available Actions minutes

### Content Published to Wrong Platform

**Solution:** Review `config.yaml` platform settings and verify secrets

## 📈 CI/CD Pipeline Status

To add status badges to your README:

```markdown
[![CI](https://github.com/S3OPS/money/actions/workflows/ci.yml/badge.svg)](https://github.com/S3OPS/money/actions/workflows/ci.yml)
[![CodeQL](https://github.com/S3OPS/money/actions/workflows/codeql.yml/badge.svg)](https://github.com/S3OPS/money/actions/workflows/codeql.yml)
```

## 🚀 Next Steps

1. ✅ **Configure secrets** for your Amazon Associate ID
2. ✅ **Enable auto-publishing** by adding platform credentials
3. ✅ **Test the workflow** manually via "Run workflow" button
4. ✅ **Monitor the Actions tab** to ensure everything works
5. ✅ **Customize the schedule** to match your content needs
6. ✅ **Review generated content** regularly
7. ✅ **Track your earnings** in Amazon Associates dashboard

## 🎉 Benefits of Full Automation

- 🤖 **Set it and forget it** - Content generates automatically
- ⏰ **Consistent schedule** - Never miss a publishing day
- 🔒 **Secure** - Credentials stored as encrypted secrets
- 📊 **Quality assurance** - Automated testing on every change
- 🛡️ **Security** - Continuous vulnerability scanning
- 📈 **Scalable** - Runs reliably without manual intervention

## 📞 Support

If you encounter issues:
1. Check workflow logs in the Actions tab
2. Review this guide's troubleshooting section
3. Verify all secrets are configured correctly
4. Ensure `config.yaml` settings are valid

---

**Made with ❤️ for automated affiliate marketing success!** 💰

🎉 **Your repository is now fully automated!**
