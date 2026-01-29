# GitHub Actions Workflow Summary

## Overview
This repository has 6 automated workflows configured in `.github/workflows/`:

## 1. CI - Tests and Code Quality (`ci.yml`)
- **Purpose**: Automated testing and code quality validation
- **Triggers**: Push/PR to main/develop, manual
- **Jobs**:
  - Test on Python 3.8, 3.9, 3.10, 3.11
  - Lint with flake8, pylint, black, isort
  - Security scan with bandit and safety
  - Configuration validation
- **Artifacts**: Test results and logs

## 2. CodeQL Security Analysis (`codeql.yml`)
- **Purpose**: Advanced security vulnerability detection
- **Triggers**: Push/PR to main/develop, weekly schedule, manual
- **Jobs**:
  - Deep code analysis
  - Security vulnerability detection
  - Creates alerts in Security tab
- **Language**: Python

## 3. Scheduled Content Generation (`scheduled-content.yml`)
- **Purpose**: Automated daily content generation
- **Triggers**: Daily at 9 AM UTC, manual
- **Jobs**:
  - Generate affiliate content
  - Auto-publish to platforms
  - Store artifacts (30 days)
- **Requires Secrets**:
  - AMAZON_ASSOCIATE_ID (required)
  - AMAZON_TRACKING_ID (required)
- YOUTUBE_CHANNEL_ID (optional)
- YOUTUBE_CREDENTIALS_FILE (optional)
- YOUTUBE_API_KEY (optional)

## 4. Dependency Review (`dependency-review.yml`)
- **Purpose**: Scan for vulnerable dependencies
- **Triggers**: Pull requests to main/develop
- **Jobs**:
  - Review dependency changes
  - Flag vulnerabilities
  - Comment on PRs
- **Fail Level**: Moderate or higher severity

## 5. Validate Secrets (`validate-secrets.yml`) 🆕
- **Purpose**: Automatically check if required GitHub secrets are configured
- **Triggers**: Push/PR to main/develop, manual
- **Jobs**:
  - Validates AMAZON_ASSOCIATE_ID exists
  - Validates AMAZON_TRACKING_ID exists
  - Checks optional YouTube secrets
  - Provides setup instructions if secrets are missing
- **Benefits**:
  - Immediate feedback on missing credentials
  - Clear instructions for fixing configuration
  - No workflow failures, just warnings

## 6. Setup Wizard (`setup-wizard.yml`) 🆕
- **Purpose**: Interactive wizard to help configure GitHub secrets
- **Triggers**: Manual only (workflow_dispatch)
- **Options**:
  - **Check current configuration**: See which secrets are configured
  - **View setup instructions**: Get detailed setup guides
  - **Generate setup commands**: Get ready-to-use CLI commands
- **Benefits**:
  - User-friendly guided setup
  - Multiple setup method options
  - No code cloning required for basic checks

## Configuration Checklist

### For Local Development
- [x] All workflows created
- [x] Python 3.8+ supported
- [x] Tests run successfully
- [x] Code quality checks configured

### For Production (Repository Secrets Required)
- [ ] AMAZON_ASSOCIATE_ID - Your Amazon Associate ID
- [ ] AMAZON_TRACKING_ID - Your tracking ID (e.g., yoursite-20)
- [ ] YOUTUBE_CHANNEL_ID - (Optional) YouTube channel ID
- [ ] YOUTUBE_CREDENTIALS_FILE - (Optional) OAuth credentials file path
- [ ] YOUTUBE_API_KEY - (Optional) YouTube API key

### Workflow Status
All workflows are configured and ready to run. To see them in action:
1. Navigate to the Actions tab in GitHub
2. Select any workflow
3. Click "Run workflow" to test manually

### Using the New Automated Secret Setup Features 🆕

#### Quick Check Your Configuration
1. Go to **Actions** tab
2. Click **Setup Wizard** workflow
3. Click **Run workflow**
4. Select "Check current configuration"
5. Review which secrets are configured

#### Get Setup Commands
1. Go to **Actions** tab
2. Click **Setup Wizard** workflow
3. Click **Run workflow**
4. Select "Generate setup commands"
5. Copy and run the commands provided

#### Automatic Validation
- The **Validate Secrets** workflow runs automatically on every push/PR
- It warns if secrets are missing but doesn't fail the build
- Check workflow run summaries for setup instructions

## Maintenance Notes
- CodeQL runs weekly (Sundays at midnight UTC)
- Content generation runs daily at 9 AM UTC
- Adjust schedules in respective workflow files if needed
- Review security alerts regularly in the Security tab
