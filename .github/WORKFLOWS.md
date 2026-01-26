# GitHub Actions Workflow Summary

## Overview
This repository has 4 automated workflows configured in `.github/workflows/`:

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

## Maintenance Notes
- CodeQL runs weekly (Sundays at midnight UTC)
- Content generation runs daily at 9 AM UTC
- Adjust schedules in respective workflow files if needed
- Review security alerts regularly in the Security tab
