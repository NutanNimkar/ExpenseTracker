# Quick Email Setup Guide

Since you have an API key, you're likely using **SendGrid** or **Mailgun**. Here's what you need to add to your `.env` file:

## For SendGrid:

Add these lines to your `.env` file:

```bash
EMAIL_SERVICE=sendgrid
SENDER_EMAIL=your-verified-email@example.com
EMAIL_API_KEY=your-sendgrid-api-key-here
```

**That's it!** Just 3 lines:
1. `EMAIL_SERVICE=sendgrid` - tells the app to use SendGrid API
2. `SENDER_EMAIL` - your verified email address in SendGrid
3. `EMAIL_API_KEY` - your SendGrid API key

## For Mailgun:

Add these lines to your `.env` file:

```bash
EMAIL_SERVICE=mailgun
SENDER_EMAIL=your-email@your-domain.com
EMAIL_API_KEY=your-mailgun-api-key-here
MAILGUN_DOMAIN=your-domain.com
```

**4 lines needed:**
1. `EMAIL_SERVICE=mailgun` - tells the app to use Mailgun API
2. `SENDER_EMAIL` - your sender email
3. `EMAIL_API_KEY` - your Mailgun API key
4. `MAILGUN_DOMAIN` - your Mailgun domain (e.g., `mg.yourdomain.com` or sandbox domain)

## Quick Test:

1. Make sure your `.env` file has the correct values
2. Restart your Flask app
3. Click "📧 Email Report" button in the app
4. Enter your email address
5. Click "Test" to send a test email
6. Check your inbox!

## Troubleshooting:

- **"Email configuration missing"** → Check that all required variables are in `.env`
- **"Authentication failed"** → Double-check your API key is correct
- **Email not received** → Check spam folder, verify sender email is correct

That's all you need! 🎉

