# Automation Scripts

This directory contains scripts to fully automate the setup and configuration of the GitHub Actions workflows.

## 🚀 Quick Start (One Command!)

```bash
./scripts/complete-setup.sh
```

This single script will handle everything for you!

## 📋 Available Scripts

### 1. `complete-setup.sh` - Complete Automated Setup
**Recommended for first-time setup**

This is your all-in-one automation script that:
- ✅ Verifies all dependencies (Python, pip, GitHub CLI)
- 🔐 Guides you through GitHub Secrets setup
- ⚙️  Configures local environment (.env file)
- 🧪 Runs system tests
- 📊 Verifies automation is ready

**Usage:**
```bash
./scripts/complete-setup.sh
```

**Requirements:**
- Python 3.8+
- pip3
- GitHub CLI (optional, for secrets automation)

---

### 2. `setup-secrets.sh` - GitHub Secrets Configuration
**Use this to set up or update GitHub Secrets**

Interactive script that:
- Prompts for required Amazon Associate credentials
- Optionally configures publishing platform secrets
- Verifies existing secrets before overwriting
- Uses GitHub CLI to securely add secrets

**Usage:**
```bash
./scripts/setup-secrets.sh
```

**Requirements:**
- GitHub CLI (`gh`) installed
- Authenticated with `gh auth login`
- Write access to repository secrets

**Secrets configured:**
- `AMAZON_ASSOCIATE_ID` (required)
- `AMAZON_TRACKING_ID` (required)
- `WORDPRESS_USERNAME` (optional)
- `WORDPRESS_APP_PASSWORD` (optional)
- `MEDIUM_INTEGRATION_TOKEN` (optional)
- `GHOST_ADMIN_API_KEY` (optional)
- `WEBHOOK_URL` (optional)

---

### 3. `verify-automation.py` - Automation Verification
**Use this to check if everything is configured correctly**

Comprehensive verification script that checks:
- ✅ GitHub CLI installation and authentication
- 🔐 Required and optional secrets configuration
- 📋 Workflow files presence and validity
- 🔄 Recent workflow runs status
- ⚙️  Configuration files

**Usage:**
```bash
python3 scripts/verify-automation.py
```

**Output:**
- Detailed check results
- Summary of passed/failed checks
- Actionable recommendations for fixes

**Example output:**
```
🔍 Checking GitHub CLI
  ✅ GitHub CLI is installed
  ✅ Authenticated with GitHub

🔐 Checking GitHub Secrets
  ✅ AMAZON_ASSOCIATE_ID - Your Amazon Associate ID
  ✅ AMAZON_TRACKING_ID - Your Amazon tracking ID
  ⊘  WORDPRESS_USERNAME - WordPress username

📊 Verification Summary
  ✅ PASS: GitHub CLI
  ✅ PASS: Secrets
  ✅ PASS: Workflows
  
Results: 5/5 checks passed
🎉 All checks passed! Your automation is ready to use.
```

---

## 🔧 Installation Requirements

### GitHub CLI (for secrets automation)

**macOS:**
```bash
brew install gh
gh auth login
```

**Linux (Debian/Ubuntu):**
```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
gh auth login
```

**Windows:**
- Download from: https://github.com/cli/cli/releases
- Or use: `winget install --id GitHub.cli`

### Python Dependencies

All Python dependencies are automatically installed by the scripts, but you can install them manually:

```bash
pip3 install -r requirements.txt
```

---

## 📖 Usage Examples

### First Time Setup
```bash
# Clone the repository
git clone https://github.com/S3OPS/money.git
cd money

# Run complete setup (this does everything!)
./scripts/complete-setup.sh
```

### Update Secrets Only
```bash
# If you need to change your Amazon credentials
./scripts/setup-secrets.sh
```

### Verify Configuration
```bash
# Check if everything is working
python3 scripts/verify-automation.py
```

### Manual Secrets Setup (without GitHub CLI)
If you don't have GitHub CLI installed:

1. Go to: https://github.com/S3OPS/money/settings/secrets/actions
2. Click "New repository secret"
3. Add these required secrets:
   - `AMAZON_ASSOCIATE_ID` - Your Amazon Associate ID
   - `AMAZON_TRACKING_ID` - Your tracking ID (e.g., mystore-20)

---

## 🎯 Workflow

1. **Run `complete-setup.sh`** - Does everything automatically
2. **Add your credentials** - Script will prompt you
3. **Enable workflows on GitHub** - Visit Actions tab
4. **Test manually** - Run "Scheduled Content Generation" workflow
5. **Monitor** - Check Actions tab for daily runs

---

## 🐛 Troubleshooting

### "gh: command not found"
Install GitHub CLI (see Installation Requirements above)

### "Not authenticated with GitHub"
Run: `gh auth login`

### "Permission denied"
Make scripts executable: `chmod +x scripts/*.sh scripts/*.py`

### Secrets not showing up
- Wait a few seconds after adding secrets
- Verify you have write access to the repository
- Check: `gh secret list -R S3OPS/money`

### Workflows not running
1. Go to: https://github.com/S3OPS/money/actions
2. If prompted, click "I understand my workflows, go ahead and enable them"
3. Manually trigger "Scheduled Content Generation" to test

---

## 📚 Additional Resources

- **Complete Setup Guide:** [AUTOMATION.md](../AUTOMATION.md)
- **Implementation Summary:** [AUTOMATION-SUMMARY.md](../AUTOMATION-SUMMARY.md)
- **Workflow Details:** [.github/WORKFLOWS.md](../.github/WORKFLOWS.md)
- **General Usage:** [README.md](../README.md)

---

## 🎉 Success!

After running these scripts, your repository will be fully automated:
- ✅ Tests run on every push/PR
- 🔒 Security scanning continuously monitors for vulnerabilities
- 📅 Content generates daily at 9 AM UTC
- 📤 Auto-publishes to your configured platforms

**No manual intervention required!** Just sit back and watch your automated affiliate marketing system work. 💰
