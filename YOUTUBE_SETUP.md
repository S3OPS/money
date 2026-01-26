# 🎥 YouTube Automated Setup

This guide walks you through the one-command YouTube setup for automated community post preparation.

## ✅ One-Command Setup

```bash
python setup_youtube.py
```

## What the Script Does

- ✅ Installs dependencies
- ✅ Guides you through YouTube credential setup
- ✅ Stores credentials securely in `.env`
- ✅ Enables YouTube auto-publishing in `config.yaml`
- ✅ Runs system tests

## Requirements

- YouTube channel ID
- OAuth credentials JSON file from Google Cloud Console

## Next Steps

1. Ensure `youtube_credentials.json` exists in the project root.
2. Run the generator:

```bash
python content_generator.py
```

3. Follow the instructions printed to post the prepared content in YouTube Studio.
