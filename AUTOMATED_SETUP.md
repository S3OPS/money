# 🤖 Fully Automated Setup Documentation

Complete guide for the zero-input, one-command automated setup system.

## 🚀 Quick Start (TL;DR)

```bash
./automated_setup.sh --amazon-id yourname-20
```

**That's it!** Your system is fully configured and content is generated.

---

## 📖 Overview

The automated setup system allows you to configure and run the entire S3OPS/money content generation system with **zero user interaction**. Everything is configured via command-line arguments or environment variables.

### Key Features

✅ **Zero User Input** - No interactive prompts  
✅ **One-Command Setup** - Everything in a single command  
✅ **Multiple Input Methods** - Command-line args or environment variables  
✅ **Flexible Options** - Skip tests, skip generation, add API keys  
✅ **Works in CI/CD** - Perfect for automated deployments  
✅ **Python & Bash** - Two setup methods available  

---

## 🛠️ Installation Methods

### Method 1: Bash Script (Recommended)

The `automated_setup.sh` script provides the most comprehensive automated setup.

#### Basic Usage
```bash
./automated_setup.sh --amazon-id YOUR_AMAZON_ID
```

#### All Options
```bash
./automated_setup.sh \
  --amazon-id YOUR_ID \          # Required: Your Amazon Associate ID
  --tracking-id YOUR_ID-20 \     # Optional: Defaults to amazon-id
  --openai-key sk-... \          # Optional: For AI-enhanced content
  --skip-tests \                 # Optional: Skip running tests
  --skip-generation              # Optional: Skip initial content generation
```

#### Environment Variables Method
```bash
# Set via environment variables
export AMAZON_ASSOCIATE_ID=yourname-20
export AMAZON_TRACKING_ID=yourname-20
export OPENAI_API_KEY=sk-...

# Run without arguments
./automated_setup.sh
```

#### Examples

**Minimal setup:**
```bash
./automated_setup.sh --amazon-id mystore-20
```

**Fast setup (skip tests):**
```bash
./automated_setup.sh --amazon-id mystore-20 --skip-tests
```

**Setup without generating content:**
```bash
./automated_setup.sh --amazon-id mystore-20 --skip-generation
```

**Full setup with OpenAI:**
```bash
./automated_setup.sh \
  --amazon-id mystore-20 \
  --openai-key sk-proj-abc123...
```

**Using environment variables:**
```bash
AMAZON_ASSOCIATE_ID=mystore-20 ./automated_setup.sh --skip-tests
```

### Method 2: Python Script

The `quick_start.py` script also supports automated mode.

#### Basic Usage
```bash
python quick_start.py --amazon-id YOUR_ID --no-prompt
```

#### All Options
```bash
python quick_start.py \
  --amazon-id YOUR_ID \
  --tracking-id YOUR_ID-20 \
  --openai-key sk-... \
  --no-prompt \
  --skip-generation
```

#### Examples

**Automated setup:**
```bash
python quick_start.py --amazon-id mystore-20 --no-prompt
```

**Setup without content generation:**
```bash
python quick_start.py --amazon-id mystore-20 --no-prompt --skip-generation
```

**Interactive mode (default):**
```bash
python quick_start.py
```

---

## 🔧 What Gets Configured

The automated setup performs the following steps:

1. **Dependency Check**
   - Verifies Python 3.7+ is installed
   - Checks for pip

2. **Install Dependencies**
   - Installs all Python packages from requirements.txt
   - PyYAML, requests, Jinja2, schedule, python-dotenv, PyJWT

3. **Environment Configuration**
   - Creates `.env` file with your credentials
   - Sets Amazon Associate ID and Tracking ID
   - Optionally sets OpenAI API key
   - Adds placeholder values for publishing platforms

4. **Verification**
   - Checks config.yaml exists
   - Optionally runs system tests

5. **Initial Content Generation**
   - Generates your first piece of content
   - Creates output in `generated_content/` directory
   - Optionally skipped with `--skip-generation`

---

## 📋 Requirements

### System Requirements
- **Python**: 3.7 or higher
- **pip**: Python package manager
- **Git**: For cloning the repository
- **Bash**: For running shell scripts (Linux, macOS, WSL, Git Bash)

### Required Information
- **Amazon Associate ID**: Your Amazon affiliate tracking ID
  - Format: `yourname-20` or similar
  - Get it from: https://affiliate-program.amazon.com/
  - Free to sign up!

### Optional Information
- **OpenAI API Key**: For AI-enhanced content generation
  - Format: `sk-proj-...` or `sk-...`
  - Get it from: https://platform.openai.com/api-keys
  - Not required for basic functionality

---

## 🎯 Use Cases

### 1. Local Development Setup
Quick setup on your local machine:
```bash
./automated_setup.sh --amazon-id mystore-20
```

### 2. CI/CD Pipeline
Use in GitHub Actions or other CI/CD:
```yaml
- name: Setup content system
  run: |
    ./automated_setup.sh --amazon-id ${{ secrets.AMAZON_ASSOCIATE_ID }} --skip-tests
  env:
    AMAZON_ASSOCIATE_ID: ${{ secrets.AMAZON_ASSOCIATE_ID }}
```

### 3. Docker Container
Build a Docker container with automated setup:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
ARG AMAZON_ID
RUN chmod +x automated_setup.sh && \
    ./automated_setup.sh --amazon-id ${AMAZON_ID} --skip-generation
CMD ["python3", "content_generator.py", "--schedule"]
```

### 4. Quick Demo
Fast setup for testing or demos:
```bash
./automated_setup.sh --amazon-id demo-20 --skip-tests
```

### 5. Production Deployment
Full setup with all features:
```bash
./automated_setup.sh \
  --amazon-id production-20 \
  --openai-key ${OPENAI_KEY}
```

---

## 🔐 Security Best Practices

### Never Commit Secrets
The `.env` file is in `.gitignore` - never commit it!

### Use Environment Variables in CI/CD
```bash
# Set secrets in GitHub Actions
./automated_setup.sh --amazon-id ${{ secrets.AMAZON_ID }}
```

### Separate Development and Production IDs
```bash
# Development
./automated_setup.sh --amazon-id mystore-dev-20

# Production
./automated_setup.sh --amazon-id mystore-prod-20
```

---

## 🧪 Testing

### Run with Tests (Default)
```bash
./automated_setup.sh --amazon-id mystore-20
```

### Skip Tests for Speed
```bash
./automated_setup.sh --amazon-id mystore-20 --skip-tests
```

### Run Tests Manually Later
```bash
python test_system.py
```

---

## 🐛 Troubleshooting

### Error: "Amazon Associate ID is required"
**Solution:** Provide the ID via `--amazon-id` flag or `AMAZON_ASSOCIATE_ID` environment variable.

```bash
./automated_setup.sh --amazon-id yourname-20
```

### Error: "Python 3 is required but not found"
**Solution:** Install Python 3.7 or higher.

```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip

# macOS
brew install python3

# Windows
# Download from https://www.python.org/downloads/
```

### Error: "Permission denied"
**Solution:** Make the script executable.

```bash
chmod +x automated_setup.sh
```

### Tests Failing
**Note:** Some tests may fail if optional features (OpenAI, publishing platforms) aren't configured. This is normal and expected.

**Solution:** Either configure the optional features or use `--skip-tests`:

```bash
./automated_setup.sh --amazon-id mystore-20 --skip-tests
```

---

## 📊 Comparison: Automated vs Interactive

| Feature | Automated Setup | Interactive Setup |
|---------|----------------|-------------------|
| User Input Required | ❌ None | ✅ Yes (prompts) |
| Configuration Method | CLI args/env vars | Manual editing |
| CI/CD Compatible | ✅ Yes | ❌ No |
| Setup Time | ~30 seconds | ~2-3 minutes |
| Scriptable | ✅ Yes | ❌ No |
| Reproducible | ✅ Yes | ⚠️ Manual steps |

---

## 🚀 Advanced Usage

### Scripted Setup with Error Handling
```bash
#!/bin/bash
set -e

if [ -z "$AMAZON_ID" ]; then
  echo "Error: AMAZON_ID not set"
  exit 1
fi

./automated_setup.sh \
  --amazon-id "$AMAZON_ID" \
  --skip-tests \
  --skip-generation

echo "Setup complete!"
```

### Conditional Setup Based on Environment
```bash
#!/bin/bash
if [ "$ENV" = "production" ]; then
  ./automated_setup.sh \
    --amazon-id "$PROD_AMAZON_ID" \
    --openai-key "$OPENAI_KEY"
else
  ./automated_setup.sh \
    --amazon-id "$DEV_AMAZON_ID" \
    --skip-tests
fi
```

### Parallel Setup for Multiple Configs
```bash
# Setup multiple configurations
./automated_setup.sh --amazon-id config1-20 &
./automated_setup.sh --amazon-id config2-20 &
wait
```

---

## 📚 Related Documentation

- **[README.md](README.md)** - General usage and features
- **[QUICK_START.md](QUICK_START.md)** - Quick reference guide
- **[AUTOMATION.md](AUTOMATION.md)** - GitHub Actions automation
- **[PUBLISHING.md](PUBLISHING.md)** - Auto-publishing setup

---

## 💡 Tips

1. **Save Your Command**: Save your setup command in a script for easy reuse
2. **Use Environment Variables**: Safer than command-line args (don't show in process list)
3. **Skip Tests in CI/CD**: Use `--skip-tests` for faster pipeline execution
4. **Version Control**: Document your setup method in your repository
5. **Backup .env**: Keep a secure backup of your `.env` file

---

## 🎉 Success!

After running automated setup, you should see:
```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        ✅ Setup Complete!                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

Your content system is ready! Generate content with:
```bash
python3 content_generator.py
```

---

**Happy automated affiliate marketing! 💰**
