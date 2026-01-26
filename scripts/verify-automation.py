#!/usr/bin/env python3
"""
Automated verification script for GitHub Actions workflows
Checks if all required secrets are configured and workflows are ready
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_REPO_OWNER = "S3OPS"
DEFAULT_REPO_NAME = "money"


def resolve_repo_from_git():
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None, None

    remote_url = result.stdout.strip()
    if not remote_url:
        return None, None

    remote_url = remote_url.rstrip("/")
    if remote_url.endswith(".git"):
        remote_url = remote_url[:-4]

    if remote_url.startswith("git@"):
        path_part = remote_url.split(":", 1)[-1]
    else:
        path_part = remote_url.split("/", 3)[-1]

    parts = path_part.split("/")
    if len(parts) != 2:
        return None, None

    return parts[0], parts[1]


def resolve_repo_owner_and_name():
    repo_path = ""
    if shutil.which("gh"):
        try:
            repo_path = subprocess.run(
                ["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
        except subprocess.CalledProcessError:
            repo_path = ""
    if repo_path and "/" in repo_path:
        owner, name = repo_path.split("/", 1)
        return owner, name

    owner = os.getenv("REPO_OWNER")
    name = os.getenv("REPO_NAME")
    if owner and name:
        return owner, name

    owner, name = resolve_repo_from_git()
    if owner and name:
        return owner, name

    return DEFAULT_REPO_OWNER, DEFAULT_REPO_NAME


REPO_OWNER, REPO_NAME = resolve_repo_owner_and_name()

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_header(text):
    print(f"\n{BOLD}{BLUE}{'=' * 80}{RESET}")
    print(f"{BOLD}{BLUE}{text:^80}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 80}{RESET}\n")

def print_section(text):
    print(f"\n{BOLD}{text}{RESET}")
    print("─" * 80)

def check_gh_cli():
    """Check if GitHub CLI is installed and authenticated"""
    print_section("🔍 Checking GitHub CLI")
    
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
        print(f"{GREEN}✅ GitHub CLI is installed{RESET}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{RED}❌ GitHub CLI is not installed{RESET}")
        print("\nPlease install it:")
        print("  • macOS: brew install gh")
        print("  • Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md")
        return False
    
    try:
        subprocess.run(["gh", "auth", "status"], capture_output=True, check=True)
        print(f"{GREEN}✅ Authenticated with GitHub{RESET}")
        return True
    except subprocess.CalledProcessError:
        print(f"{RED}❌ Not authenticated with GitHub{RESET}")
        print("\nPlease authenticate:")
        print("  gh auth login")
        return False

def check_secrets():
    """Check if required secrets are configured"""
    print_section("🔐 Checking GitHub Secrets")
    
    required_secrets = {
        "AMAZON_ASSOCIATE_ID": "Your Amazon Associate ID",
        "AMAZON_TRACKING_ID": "Your Amazon tracking ID"
    }
    
    optional_secrets = {
        "YOUTUBE_CHANNEL_ID": "YouTube channel ID",
        "YOUTUBE_CREDENTIALS_FILE": "YouTube OAuth credentials file path",
        "YOUTUBE_API_KEY": "YouTube API key"
    }
    
    try:
        result = subprocess.run(
            ["gh", "secret", "list", "-R", f"{REPO_OWNER}/{REPO_NAME}"],
            capture_output=True,
            text=True,
            check=True
        )
        
        configured_secrets = set()
        for line in result.stdout.strip().split('\n'):
            if line:
                secret_name = line.split()[0]
                configured_secrets.add(secret_name)
        
        # Check required secrets
        print("\nRequired Secrets:")
        all_required_present = True
        for secret, description in required_secrets.items():
            if secret in configured_secrets:
                print(f"  {GREEN}✅{RESET} {secret:<30} - {description}")
            else:
                print(f"  {RED}❌{RESET} {secret:<30} - {description}")
                all_required_present = False
        
        # Check optional secrets
        print("\nOptional Secrets (for YouTube publishing):")
        optional_count = 0
        for secret, description in optional_secrets.items():
            if secret in configured_secrets:
                print(f"  {GREEN}✅{RESET} {secret:<30} - {description}")
                optional_count += 1
            else:
                print(f"  {YELLOW}⊘{RESET}  {secret:<30} - {description}")
        
        if optional_count > 0:
            print(f"\n{GREEN}ℹ️  {optional_count} optional secret(s) configured for publishing{RESET}")
        else:
            print(f"\n{YELLOW}ℹ️  No YouTube publishing secrets configured (content will be stored as artifacts only){RESET}")
        
        return all_required_present
        
    except subprocess.CalledProcessError as e:
        print(f"{RED}❌ Failed to list secrets{RESET}")
        print(f"Error: {e.stderr}")
        return False

def check_workflows():
    """Check if workflow files exist and are valid"""
    print_section("📋 Checking Workflow Files")
    
    workflows = {
        "ci.yml": "CI/CD Pipeline",
        "codeql.yml": "CodeQL Security Analysis",
        "scheduled-content.yml": "Scheduled Content Generation",
        "dependency-review.yml": "Dependency Review"
    }
    
    workflow_dir = Path(".github/workflows")
    all_present = True
    
    for filename, description in workflows.items():
        filepath = workflow_dir / filename
        if filepath.exists():
            print(f"  {GREEN}✅{RESET} {filename:<30} - {description}")
        else:
            print(f"  {RED}❌{RESET} {filename:<30} - {description}")
            all_present = False
    
    return all_present

def check_workflow_runs():
    """Check recent workflow runs"""
    print_section("🔄 Checking Workflow Status")
    
    try:
        result = subprocess.run(
            ["gh", "run", "list", "-R", f"{REPO_OWNER}/{REPO_NAME}", "--limit", "5"],
            capture_output=True,
            text=True,
            check=True
        )
        
        if result.stdout.strip():
            print("\nRecent workflow runs:")
            print(result.stdout)
        else:
            print(f"\n{YELLOW}ℹ️  No workflow runs yet{RESET}")
            print("   Workflows will start running after secrets are configured")
        
        return True
        
    except subprocess.CalledProcessError:
        print(f"{YELLOW}ℹ️  Unable to check workflow runs (may need repo permissions){RESET}")
        return True

def check_config_files():
    """Check if configuration files are present"""
    print_section("⚙️  Checking Configuration Files")
    
    config_files = {
        "config.yaml": "Main configuration",
        ".env.example": "Environment template",
        "requirements.txt": "Python dependencies",
        "AUTOMATION.md": "Automation guide"
    }
    
    all_present = True
    for filename, description in config_files.items():
        filepath = Path(filename)
        if filepath.exists():
            print(f"  {GREEN}✅{RESET} {filename:<30} - {description}")
        else:
            print(f"  {RED}❌{RESET} {filename:<30} - {description}")
            all_present = False
    
    return all_present

def main():
    print_header("🤖 GitHub Actions Automation Verification")
    
    print("This script verifies that your repository is properly configured for automation.")
    print(f"Repository: {BOLD}{REPO_OWNER}/{REPO_NAME}{RESET}")
    
    # Run all checks
    checks = {
        "GitHub CLI": check_gh_cli(),
        "Secrets": check_secrets(),
        "Workflows": check_workflows(),
        "Workflow Runs": check_workflow_runs(),
        "Configuration": check_config_files()
    }
    
    # Summary
    print_section("📊 Verification Summary")
    
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    
    for check, result in checks.items():
        status = f"{GREEN}✅ PASS{RESET}" if result else f"{RED}❌ FAIL{RESET}"
        print(f"  {status}: {check}")
    
    print(f"\n{BOLD}Results: {passed}/{total} checks passed{RESET}")
    
    if all(checks.values()):
        print(f"\n{GREEN}{BOLD}🎉 All checks passed! Your automation is ready to use.{RESET}")
        print("\n🎯 Next Steps:")
        print("   1. Go to: https://github.com/{}/{}/actions".format(REPO_OWNER, REPO_NAME))
        print("   2. Run 'Scheduled Content Generation' workflow manually to test")
        print("   3. Check generated content in workflow artifacts")
        print("   4. Monitor daily scheduled runs at 9 AM UTC")
        return 0
    else:
        print(f"\n{YELLOW}{BOLD}⚠️  Some checks failed. Please review the issues above.{RESET}")
        print("\n🔧 To fix issues:")
        if not checks["GitHub CLI"]:
            print("   • Install and authenticate GitHub CLI")
        if not checks["Secrets"]:
            print("   • Run: ./scripts/setup-secrets.sh")
            print("   • Or manually add secrets: https://github.com/{}/{}/settings/secrets/actions".format(REPO_OWNER, REPO_NAME))
        if not checks["Workflows"]:
            print("   • Ensure all workflow files are committed")
        if not checks["Configuration"]:
            print("   • Ensure all configuration files are present")
        return 1

if __name__ == "__main__":
    sys.exit(main())
