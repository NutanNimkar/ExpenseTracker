# Email Setup Guide

## Free Email Service Options

### Option 1: Gmail (Recommended - Free & Easy)

Gmail offers free SMTP service. Here's how to set it up:

#### Step 1: Enable 2-Factor Authentication
1. Go to your Google Account settings
2. Security → 2-Step Verification
3. Enable it (required for app passwords)

#### Step 2: Generate App Password
1. Go to Google Account → Security
2. Under "2-Step Verification", click "App passwords"
3. Select "Mail" and "Other (Custom name)"
4. Enter "Budget App" as the name
5. Click "Generate"
6. Copy the 16-character password (you'll use this as SENDER_PASSWORD)

#### Step 3: Set Environment Variables

Add to your `.env` file:
```bash
SENDER_EMAIL=your.email@gmail.com
SENDER_PASSWORD=your-16-char-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### Option 2: SendGrid (Free Tier: 100 emails/day)

1. Sign up at [sendgrid.com](https://sendgrid.com) (free tier)
2. Create an API key
3. Set environment variables:
```bash
SENDER_EMAIL=your-verified-email@example.com
SENDER_PASSWORD=your-sendgrid-api-key
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587
```

### Option 3: Mailgun (Free Tier: 5,000 emails/month)

1. Sign up at [mailgun.com](https://mailgun.com)
2. Verify your domain or use sandbox domain
3. Get SMTP credentials
4. Set environment variables:
```bash
SENDER_EMAIL=your-email@your-domain.com
SENDER_PASSWORD=your-mailgun-smtp-password
SMTP_SERVER=smtp.mailgun.org
SMTP_PORT=587
```

### Option 4: SMTP2GO (Free Tier: 1,000 emails/month)

1. Sign up at [smtp2go.com](https://smtp2go.com)
2. Get SMTP credentials
3. Set environment variables:
```bash
SENDER_EMAIL=your-email@example.com
SENDER_PASSWORD=your-smtp2go-password
SMTP_SERVER=mail.smtp2go.com
SMTP_PORT=587
```

## Testing Your Setup

1. Start your Flask app
2. Click "📧 Email Report" button
3. Enter your email address
4. Click "Test" to send a test email
5. Check your inbox!

## Weekly Automated Emails (Optional)

To set up automatic weekly emails, you can:

### Option A: Use a Cron Job (Linux/Mac)

Add to your crontab (`crontab -e`):
```bash
# Send budget report every Monday at 9 AM
0 9 * * 1 cd /path/to/budget-app && python -c "from app import app; from email_service import send_budget_email; ..."
```

### Option B: Use Python Schedule (Included)

Create a `scheduler.py` file:
```python
import schedule
import time
from app import app
from email_service import send_budget_email
# ... your scheduling code
```

Run it separately: `python scheduler.py`

### Option C: Use a Cloud Scheduler

- **Heroku Scheduler** (if deployed on Heroku)
- **AWS EventBridge** (if on AWS)
- **Google Cloud Scheduler** (if on GCP)

## Troubleshooting

### "Email configuration missing"
- Make sure `.env` file exists with all required variables
- Check that variables are spelled correctly

### "Authentication failed"
- For Gmail: Make sure you're using an App Password, not your regular password
- Check that 2FA is enabled
- Verify SMTP server and port are correct

### "Connection refused"
- Check your firewall/network settings
- Verify SMTP server and port are correct
- Some networks block SMTP ports

### Email not received
- Check spam/junk folder
- Verify recipient email is correct
- Check email service logs for errors

## Security Notes

⚠️ **Important:**
- Never commit your `.env` file to Git
- Use App Passwords, not your main account password
- Keep your email credentials secure
- Consider using environment variables in production

## Production Deployment

When deploying, set environment variables in your hosting platform:
- Render: Environment → Add Environment Variable
- Railway: Variables tab
- Heroku: `heroku config:set SENDER_EMAIL=...`

