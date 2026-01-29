# 🚀 Quick Reference: Automated Secrets Setup

## Check Your Configuration Status (No Installation Required!)

### Option 1: Use Setup Wizard
1. Go to **Actions** tab → Click **Setup Wizard**
2. Click **Run workflow** button
3. Select "Check current configuration"
4. Click **Run workflow**
5. View summary: ✅ = configured, ❌ = missing

### Option 2: Automatic Validation
- Every push/PR automatically validates secrets
- Check **Actions** tab → **Validate Secrets** workflow runs
- View summary for current status

## Get Setup Commands

1. **Actions** tab → **Setup Wizard**
2. **Run workflow** → "Generate setup commands"
3. Copy the commands shown in summary
4. Run them in your terminal

Example:
```bash
gh secret set AMAZON_ASSOCIATE_ID --body "yourname-20" --repo S3OPS/money
gh secret set AMAZON_TRACKING_ID --body "yourname-20" --repo S3OPS/money
```

## Setup Methods (Choose One)

### 🎯 Fastest: Automated Script
```bash
git clone https://github.com/S3OPS/money.git
cd money
./scripts/setup-secrets.sh
```

### 💻 Quick: GitHub CLI
```bash
gh secret set AMAZON_ASSOCIATE_ID --body "yourname-20"
gh secret set AMAZON_TRACKING_ID --body "yourname-20"
```

### 🖱️ Manual: GitHub UI
Settings → Secrets and variables → Actions → New repository secret

## Required Information

**Amazon Associate ID**
- Sign up: https://affiliate-program.amazon.com/
- Format: `yourname-20`
- Used for: Affiliate link tracking

## Verify Setup Works

1. **Actions** tab → **Scheduled Content Generation**
2. Click **Run workflow** → **Run workflow**
3. Wait ~2-3 minutes
4. Check it completes successfully ✅

## Need Help?

📖 **Full Guide:** [SECRETS_SETUP.md](SECRETS_SETUP.md)
🤖 **Automation:** [AUTOMATION.md](AUTOMATION.md)
📚 **Complete Setup:** [COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md)

## Troubleshooting

**"gh: command not found"**
```bash
brew install gh  # macOS
gh auth login
```

**Secrets not showing?**
- Wait 30-60 seconds after setting
- Check: Settings → Secrets and variables → Actions

**Still having issues?**
- Run Setup Wizard for detailed instructions
- Check workflow summaries for specific error messages
