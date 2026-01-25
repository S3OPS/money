# 💰 Automated Content Creation System with Amazon Associates

**The world's fastest automated content generation system for Amazon affiliate marketing!**

Generate high-quality product review content with embedded Amazon Associate affiliate links - fully automated with minimal setup required.

## 🚀 Quick Start (60 seconds!)

```bash
# 1. Clone and navigate
cd money

# 2. Run quick start script
python quick_start.py

# 3. Add your Amazon Associate ID to .env file
# Edit .env and replace YOUR_AMAZON_ASSOCIATE_ID with your actual ID

# 4. Generate content!
python content_generator.py
```

That's it! Your content will be in the `generated_content/` folder.

## ✨ Features

- 🤖 **Fully Automated**: Generate content with a single command
- 💵 **Amazon Associates Ready**: Automatic affiliate link insertion
- 📅 **Scheduled Generation**: Set it and forget it with automated scheduling
- 📝 **Multiple Formats**: Markdown, HTML, or JSON output
- 🎯 **Multi-Category**: Tech, Home, Books, Electronics, and more
- 🔒 **Secure**: Environment variables for sensitive data
- 📊 **Analytics**: Automatic metadata tracking

## 📋 Requirements

- Python 3.7 or higher
- Amazon Associate ID (free to sign up at [Amazon Associates](https://affiliate-program.amazon.com/))

## 🛠️ Installation

### Option 1: Quick Start (Recommended)
```bash
python quick_start.py
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your Amazon Associate ID
nano .env  # or use your preferred editor

# Generate content
python content_generator.py
```

## ⚙️ Configuration

### Amazon Associate Setup

1. Sign up for [Amazon Associates](https://affiliate-program.amazon.com/) (free)
2. Get your Associate ID (format: `yourname-20`)
3. Add it to `.env`:

```bash
AMAZON_ASSOCIATE_ID=your-associate-id
AMAZON_TRACKING_ID=your-tracking-id-20
```

### Customize Content Settings

Edit `config.yaml` to customize:

- **Categories**: Choose product categories to focus on
- **Products per post**: How many products in each article
- **Generation interval**: How often to create new content
- **Output format**: Markdown, HTML, or JSON
- **Scheduling**: Enable automated daily generation

## 🎯 Usage

### Generate Content Once
```bash
python content_generator.py
```

### Run on Automated Schedule
```bash
python content_generator.py --schedule
```

This will:
1. Generate content immediately
2. Schedule daily content generation (default: 9 AM UTC)
3. Keep running until you stop it (Ctrl+C)

### Output

Content is saved to `generated_content/` directory:
- `content_YYYYMMDD_HHMMSS.md` - The generated content
- `content_YYYYMMDD_HHMMSS.json` - Metadata (stats, timestamp, etc.)

## 📝 Sample Output

```markdown
# Top 5 Tech Gadgets Products - January 25, 2026

## #1 - Premium Wireless Headphones

Looking for a great Tech Gadgets option? The **Premium Wireless Headphones** 
is an excellent choice that delivers outstanding value.

### Key Features:
- Premium quality construction
- Excellent customer reviews
- Great value at $79.99
- Fast shipping available

[**Check Current Price on Amazon**](https://www.amazon.com/dp/B08N5WRWNW?tag=yoursite-20)

---
```

## 🔄 How It Works

1. **Content Generation**: Creates product review articles
2. **Affiliate Link Injection**: Automatically adds your Amazon Associate ID
3. **Multiple Products**: Features multiple products per article
4. **Professional Format**: Clean, readable markdown/HTML output
5. **Metadata Tracking**: Tracks generated content for analytics

## 🎨 Customization

### Add Your Own Products

Edit `content_generator.py` and update the `sample_products` list:

```python
sample_products = [
    {
        'asin': 'B08N5WRWNW',  # Product ASIN from Amazon
        'title': 'Your Product Name',
        'category': 'Category',
        'price': '$XX.XX'
    },
    # Add more...
]
```

### Change Content Templates

Modify the `review_templates` in the `generate_product_review()` method to customize the writing style.

### Add New Categories

Edit `config.yaml`:

```yaml
content:
  categories:
    - "Your New Category"
    - "Another Category"
```

## 📊 Advanced Features

### Integration with Publishing Platforms

The system is designed to integrate with:
- WordPress blogs (via API)
- Static site generators (Jekyll, Hugo, etc.)
- Social media platforms
- Email newsletters

### API Integration

Extend the system to use:
- Amazon Product Advertising API for real product data
- OpenAI API for enhanced content generation
- Analytics APIs for performance tracking

## 🔐 Security Best Practices

- ✅ Store credentials in `.env` (never commit to git)
- ✅ `.env` is in `.gitignore` by default
- ✅ Use environment variables for sensitive data
- ✅ Regularly rotate your API keys

## 🐛 Troubleshooting

### "config.yaml not found"
- Make sure you're in the project directory
- Check that config.yaml exists

### "No module named 'yaml'"
- Run: `pip install -r requirements.txt`

### Affiliate links not working
- Verify your Amazon Associate ID in `.env`
- Check that the ID format is correct (e.g., `yourname-20`)
- Ensure you're approved in the Amazon Associates program

## 🤝 Contributing

This is a personal project, but feel free to fork and customize for your needs!

## 📄 License

This project is provided as-is for educational and commercial use.

## ⚠️ Disclaimer

- This tool generates content templates. Review and customize before publishing.
- Ensure compliance with Amazon Associates Program Operating Agreement
- Follow FTC guidelines for affiliate link disclosure
- Product information should be verified before publishing

## 🎯 What's Next?

1. ✅ Set up your Amazon Associate ID
2. ✅ Generate your first content
3. 📝 Customize templates to match your style
4. 🚀 Set up automated scheduling
5. 📊 Track your earnings in Amazon Associates dashboard
6. 🎨 Integrate with your blog/website
7. 💰 Start earning commissions!

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review Amazon Associates documentation
- Ensure all dependencies are installed

---

**Made with ❤️ for affiliate marketers who want to work smarter, not harder!**

🎉 **Now go make some money with Amazon Associates!** 💰