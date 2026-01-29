# 🔐 GitHub Secrets Setup Guide

This guide explains how to automatically set up and manage the credentials required for this system to work with GitHub Actions.

## 🎯 Overview

This repository requires certain credentials (GitHub Secrets) to function properly:
- **AMAZON_ASSOCIATE_ID** (Required) - Your Amazon Associates tracking ID
- **AMAZON_TRACKING_ID** (Required) - Usually the same as your Associate ID
- **YOUTUBE_CHANNEL_ID** (Optional) - For YouTube publishing
- **YOUTUBE_CREDENTIALS_FILE** (Optional) - OAuth credentials path
- **YOUTUBE_API_KEY** (Optional) - YouTube API key

## ✨ NEW: Automated Secret Validation & Setup

We've added automated workflows to make secret setup easier!

### Quick Check: Are Your Secrets Configured?

**Method 1: Use the Setup Wizard (No Installation Required)**

1. Go to the **Actions** tab in your GitHub repository
2. Click on **Setup Wizard** in the left sidebar
3. Click **Run workflow** button (top right)
4. Select "Check current configuration" from the dropdown
5. Click the green **Run workflow** button
6. Wait a few seconds and click on the workflow run
7. View the summary to see which secrets are configured ✅ or missing ❌

**Method 2: Check Validation on Every Push**

The **Validate Secrets** workflow automatically runs on every push and PR:
1. Make any commit and push to your repository
2. Go to **Actions** tab
3. Click on the latest **Validate Secrets** workflow run
4. View the summary for your secret status

### Generate Ready-to-Run Setup Commands

1. Go to **Actions** tab
2. Click on **Setup Wizard**
3. Click **Run workflow**
4. Select "Generate setup commands"
5. Click **Run workflow**
6. View the workflow run summary
7. Copy the generated commands and run them in your terminal

Example output:
```bash
gh secret set AMAZON_ASSOCIATE_ID --body "yourname-20" --repo S3OPS/money
gh secret set AMAZON_TRACKING_ID --body "yourname-20" --repo S3OPS/money
```

### View Complete Setup Instructions

1. Go to **Actions** tab
2. Click on **Setup Wizard**
3. Click **Run workflow**
4. Select "View setup instructions"
5. Click **Run workflow**
6. View comprehensive step-by-step instructions in the workflow summary

## 🚀 Setup Methods

Choose the method that works best for you:

### Method 1: Automated Setup Script (Recommended for Local Setup)

**Best for:** First-time setup with GitHub CLI

```bash
# Clone the repository
git clone https://github.com/S3OPS/money.git
cd money

# Run the automated secret setup script
./scripts/setup-secrets.sh
```

This script will:
- ✅ Check if GitHub CLI is installed
- ✅ Verify you're authenticated
- ✅ Guide you through adding each secret
- ✅ Warn before overwriting existing secrets
- ✅ Show a summary when complete

**Requirements:**
- GitHub CLI (`gh`) installed: `brew install gh` (macOS)
- Authenticated: `gh auth login`
- Write access to repository secrets

### Method 2: GitHub Actions Setup Wizard (Recommended for Quick Checks)

**Best for:** Checking status without cloning the repository

1. Navigate to your repository on GitHub
2. Click the **Actions** tab
3. Select **Setup Wizard** from the workflows list
4. Click **Run workflow**
5. Choose your desired action:
   - **Check current configuration** - See what's configured
   - **View setup instructions** - Get detailed guides
   - **Generate setup commands** - Get ready-to-use commands
6. View the workflow run summary for results

**Benefits:**
- No local setup required
- Visual feedback in GitHub UI
- Multiple options in one place
- Always up-to-date instructions

### Method 3: GitHub CLI (Quick and Direct)

**Best for:** Advanced users who know their credentials

```bash
# Install and authenticate GitHub CLI
brew install gh  # macOS
gh auth login

# Set required secrets
gh secret set AMAZON_ASSOCIATE_ID --body "yourname-20" --repo S3OPS/money
gh secret set AMAZON_TRACKING_ID --body "yourname-20" --repo S3OPS/money

# Optional: Set YouTube secrets
gh secret set YOUTUBE_CHANNEL_ID --body "UCxxxxxxxxxxxxx" --repo S3OPS/money
gh secret set YOUTUBE_CREDENTIALS_FILE --body "youtube_credentials.json" --repo S3OPS/money

# Verify secrets were set
gh secret list --repo S3OPS/money
```

### Method 4: Manual Setup via GitHub UI

**Best for:** Users without GitHub CLI

1. Go to your repository on GitHub
2. Click **Settings** (top menu)
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Add each required secret:

   **AMAZON_ASSOCIATE_ID**
   - Name: `AMAZON_ASSOCIATE_ID`
   - Value: Your Amazon Associate ID (e.g., `yourname-20`)
   
   **AMAZON_TRACKING_ID**
   - Name: `AMAZON_TRACKING_ID`
   - Value: Your tracking ID (usually same as Associate ID)

6. Click **Add secret** for each one
7. Optionally add YouTube secrets if you want to use publishing features

## 📋 Required Information

Before you start, gather this information:

### Amazon Associates (Required)

**What you need:**
- Amazon Associate ID (format: `yourname-20`)

**How to get it:**
1. Sign up at https://affiliate-program.amazon.com/ (free!)
2. Once approved, go to **Tools** → **Product Linking**
3. Your tracking ID is displayed (format: `yourname-20`)

**Don't have an Amazon Associates account?**
1. Visit https://affiliate-program.amazon.com/
2. Click "Join Now for Free"
3. Fill out the application
4. Get approved (usually within 24 hours)

### YouTube Publishing (Optional)

**What you need:**
- YouTube Channel ID
- OAuth 2.0 credentials (JSON file)
- YouTube Data API v3 enabled

**How to get it:**
See the detailed guide in [YOUTUBE_SETUP.md](YOUTUBE_SETUP.md)

## ✅ Verification

### Verify Secrets Are Configured

**Method 1: Use Validate Secrets Workflow**
1. Go to **Actions** tab
2. Click **Validate Secrets** workflow
3. Click **Run workflow**
4. View the summary to see which secrets are present

**Method 2: Use Setup Wizard**
1. Go to **Actions** tab
2. Click **Setup Wizard** workflow
3. Select "Check current configuration"
4. View results in workflow summary

**Method 3: Use GitHub CLI**
```bash
gh secret list --repo S3OPS/money
```

**Method 4: Manual Check in GitHub UI**
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. You should see your secrets listed (values are hidden for security)

### Test the Configuration

After setting up secrets, test that everything works:

1. Go to **Actions** tab
2. Click **Scheduled Content Generation** workflow
3. Click **Run workflow** → **Run workflow**
4. Wait for the workflow to complete (~2-3 minutes)
5. Check that it completes successfully
6. Download the artifacts to verify content was generated
   - Scroll to the bottom of the workflow run page
   - Look for the **Artifacts** section
   - Click on the artifact (e.g., `generated-content-123`)
   - The ZIP file contains the generated markdown files with affiliate links

## 🔒 Security Best Practices

### Do's ✅
- ✅ Use the automated scripts or GitHub UI to set secrets
- ✅ Keep your Amazon Associate ID private
- ✅ Rotate credentials periodically
- ✅ Use different tracking IDs for different sites if needed
- ✅ Review who has access to repository secrets
- ✅ Enable 2FA on your GitHub account

### Don'ts ❌
- ❌ Never commit secrets to Git
- ❌ Never share secrets in issues or pull requests
- ❌ Never log secrets in your code
- ❌ Never hardcode secrets in configuration files
- ❌ Don't use production secrets for testing

### Rotating Secrets

To update a secret:
```bash
# Using GitHub CLI
gh secret set AMAZON_ASSOCIATE_ID --body "new-value" --repo S3OPS/money

# Or re-run the setup script
./scripts/setup-secrets.sh
```

## 🐛 Troubleshooting

### "gh: command not found"

**Problem:** GitHub CLI is not installed

**Solution:**
```bash
# macOS
brew install gh

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Windows
winget install GitHub.CLI
```

Then authenticate:
```bash
gh auth login
```

### "Not authenticated with GitHub"

**Problem:** GitHub CLI needs authentication

**Solution:**
```bash
gh auth login
```
Follow the prompts to authenticate.

### Secrets not showing up in workflow

**Problem:** Secrets take a moment to propagate

**Solution:**
- Wait 30-60 seconds after setting secrets
- Trigger a new workflow run
- Verify secrets are visible in Settings → Secrets

### Workflow still says secrets are missing

**Problem:** Secret names might be incorrect

**Solution:**
- Secret names are case-sensitive
- Required names:
  - `AMAZON_ASSOCIATE_ID` (exactly this, all caps)
  - `AMAZON_TRACKING_ID` (exactly this, all caps)
- Delete and recreate the secret with the correct name

### Permission denied when running scripts

**Problem:** Script is not executable

**Solution:**
```bash
chmod +x scripts/setup-secrets.sh
chmod +x scripts/complete-setup.sh
```

### Can't access repository secrets

**Problem:** You don't have write access

**Solution:**
- You need to be a repository admin or have write access
- Ask the repository owner to grant you access
- Or ask them to set up the secrets

## 📚 Additional Resources

- **[AUTOMATION.md](AUTOMATION.md)** - Complete automation guide
- **[COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md)** - Full setup instructions
- **[scripts/README.md](scripts/README.md)** - Scripts documentation
- **[.github/WORKFLOWS.md](.github/WORKFLOWS.md)** - Workflow details
- **GitHub Docs:** [Encrypted secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

## 🎉 Success!

Once your secrets are configured:
- ✅ The **Validate Secrets** workflow will show all green checkmarks
- ✅ The **Scheduled Content Generation** workflow will run successfully
- ✅ Content will be generated automatically every day at 9 AM UTC
- ✅ You can manually trigger workflows anytime from the Actions tab

Your automated affiliate marketing system is now fully configured! 💰

---

**Need help?** Check the workflow summaries for detailed instructions, or review the documentation links above.
