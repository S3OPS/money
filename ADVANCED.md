# Advanced Features Guide

This guide covers advanced features and customization options for the Automated Content Creation System.

## Table of Contents

1. [Amazon Product API Integration](#amazon-product-api-integration)
2. [AI-Powered Content Generation](#ai-powered-content-generation)
3. [Multi-Platform Publishing](#multi-platform-publishing)
4. [Custom Templates](#custom-templates)
5. [Analytics and Tracking](#analytics-and-tracking)
6. [Scheduled Automation](#scheduled-automation)

## Amazon Product API Integration

To use real product data from Amazon, integrate with the Amazon Product Advertising API:

### Setup

1. Sign up for Product Advertising API access
2. Get your Access Key and Secret Key
3. Add to `.env`:

```bash
AMAZON_ACCESS_KEY=your-access-key
AMAZON_SECRET_KEY=your-secret-key
```

### Example Usage

```python
from amazon.paapi import AmazonAPI

api = AmazonAPI(
    access_key=os.getenv('AMAZON_ACCESS_KEY'),
    secret_key=os.getenv('AMAZON_SECRET_KEY'),
    region='US',
    partner_tag=os.getenv('AMAZON_TRACKING_ID')
)

# Search for products
products = api.search_items(keywords='wireless headphones')

# Get product details
product = api.get_items(asin='B08N5WRWNW')
```

## AI-Powered Content Generation

Enhance content quality with AI services:

### OpenAI Integration

```python
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_ai_review(product_title, features):
    prompt = f"""Write a compelling product review for {product_title}.
    Features: {features}
    Style: Informative, helpful, natural
    Length: 200-300 words"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content
```

### Local AI (Free Alternative)

```python
# Use transformers library for local AI
from transformers import pipeline

generator = pipeline('text-generation', model='gpt2')

def generate_local_content(prompt):
    result = generator(prompt, max_length=200)
    return result[0]['generated_text']
```

## Multi-Platform Publishing

Automatically publish content to multiple platforms:

### WordPress Integration

```python
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

def publish_to_wordpress(content, title):
    wp = Client(
        'https://yoursite.com/xmlrpc.php',
        os.getenv('WP_USERNAME'),
        os.getenv('WP_PASSWORD')
    )
    
    post = WordPressPost()
    post.title = title
    post.content = content
    post.post_status = 'publish'
    
    wp.call(NewPost(post))
```

### Medium Integration

```python
import requests

def publish_to_medium(content, title):
    headers = {
        'Authorization': f'Bearer {os.getenv("MEDIUM_TOKEN")}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'title': title,
        'content': content,
        'contentFormat': 'markdown',
        'publishStatus': 'draft'
    }
    
    response = requests.post(
        'https://api.medium.com/v1/users/me/posts',
        headers=headers,
        json=data
    )
```

## Custom Templates

Create custom Jinja2 templates:

### Template File (templates/product_review.j2)

```jinja2
# {{ product.title }}

*Last updated: {{ date }}*

## Overview

{{ product.description }}

## Key Features

{% for feature in product.features %}
- {{ feature }}
{% endfor %}

## Our Rating

⭐⭐⭐⭐⭐ ({{ product.rating }}/5)

## Price

**Current Price**: {{ product.price }}

[**Buy on Amazon**]({{ affiliate_link }})

---

## Customer Reviews

{{ customer_reviews }}

## Final Verdict

{{ conclusion }}

---

*Disclosure: As an Amazon Associate, we earn from qualifying purchases.*
```

### Using Templates

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('product_review.j2')

content = template.render(
    product=product_data,
    date=datetime.now().strftime('%B %d, %Y'),
    affiliate_link=affiliate_link,
    customer_reviews=reviews,
    conclusion=conclusion
)
```

## Analytics and Tracking

Track performance of your content:

### Click Tracking

```python
import sqlite3

def track_click(product_asin, timestamp):
    conn = sqlite3.connect('analytics.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO clicks (asin, timestamp)
        VALUES (?, ?)
    ''', (product_asin, timestamp))
    conn.commit()
    conn.close()
```

### Performance Dashboard

```python
def generate_report():
    conn = sqlite3.connect('analytics.db')
    c = conn.cursor()
    
    # Get click stats
    c.execute('''
        SELECT asin, COUNT(*) as clicks
        FROM clicks
        GROUP BY asin
        ORDER BY clicks DESC
        LIMIT 10
    ''')
    
    top_products = c.fetchall()
    
    print("Top 10 Products by Clicks:")
    for asin, clicks in top_products:
        print(f"{asin}: {clicks} clicks")
```

## Scheduled Automation

Advanced scheduling options:

### Cron-based Scheduling (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add entry to run daily at 9 AM
0 9 * * * cd /path/to/money && python3 content_generator.py >> logs/cron.log 2>&1

# Run every 6 hours
0 */6 * * * cd /path/to/money && python3 content_generator.py >> logs/cron.log 2>&1
```

### Systemd Service (Linux)

Create `/etc/systemd/system/content-generator.service`:

```ini
[Unit]
Description=Automated Content Generator
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/money
ExecStart=/usr/bin/python3 content_generator.py --schedule
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable content-generator
sudo systemctl start content-generator
```

### Windows Task Scheduler

```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute 'python' -Argument 'C:\path\to\money\content_generator.py'
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "ContentGenerator" -Description "Daily content generation"
```

## Database Integration

Store generated content in database:

```python
import sqlite3

def save_to_database(content, metadata):
    conn = sqlite3.connect('content.db')
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY,
            title TEXT,
            content TEXT,
            category TEXT,
            created_at TIMESTAMP,
            published BOOLEAN
        )
    ''')
    
    c.execute('''
        INSERT INTO content (title, content, category, created_at, published)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        metadata['title'],
        content,
        metadata['category'],
        metadata['generated_at'],
        False
    ))
    
    conn.commit()
    conn.close()
```

## Email Notifications

Get notified when content is generated:

```python
import smtplib
from email.mime.text import MIMEText

def send_notification(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = os.getenv('EMAIL_FROM')
    msg['To'] = os.getenv('EMAIL_TO')
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(
            os.getenv('EMAIL_USER'),
            os.getenv('EMAIL_PASSWORD')
        )
        server.send_message(msg)
```

## Best Practices

1. **Rate Limiting**: Don't generate too much content too quickly
2. **Quality Over Quantity**: Focus on valuable, helpful content
3. **Regular Updates**: Keep product information current
4. **Backup**: Regularly backup your generated content
5. **Testing**: Always test affiliate links before publishing
6. **Compliance**: Follow Amazon Associates terms of service
7. **Disclosure**: Always include affiliate disclosure
8. **Monitoring**: Track clicks and conversions

## Need Help?

- Check the main README.md
- Review Amazon Associates documentation
- Test with sample products first
- Start simple and add features gradually

---

*Remember: The goal is to provide value to readers while earning commissions!*
