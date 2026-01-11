# Deployment Guide for Budget App

This guide will help you deploy your budget app to a hosting platform so you can receive weekly emails.

## Prerequisites

1. GitHub account
2. Account on a hosting platform (Render, Railway, or Fly.io recommended)

## Step 1: Prepare for GitHub

### 1.1 Create .gitignore (if not exists)

Make sure `.gitignore` includes:
```
instance/
venv/
.env
__pycache__/
*.pyc
*.db
*.sqlite
scheduler.log
.DS_Store
```

### 1.2 Initialize Git and Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Budget tracking app with multi-user support and email features"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/budget-app.git
git branch -M main
git push -u origin main
```

## Step 2: Choose a Hosting Platform

### Option A: Render (Recommended - Free Tier Available)

**Pros:**
- Free tier available
- Easy PostgreSQL setup
- Built-in cron jobs for scheduled tasks
- Simple deployment from GitHub

**Steps:**

1. **Sign up at [render.com](https://render.com)**

2. **Create a PostgreSQL Database:**
   - New → PostgreSQL
   - Name: `budget-app-db`
   - Copy the "Internal Database URL"

3. **Create a Web Service:**
   - New → Web Service
   - Connect your GitHub repository
   - Settings:
     - **Name:** `budget-app`
     - **Environment:** `Python 3`
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`
     - **Plan:** Free (or paid for better performance)

4. **Set Environment Variables:**
   Go to Environment tab and add:
   ```
   DATABASE_URL=<your-postgresql-url-from-step-2>
   SECRET_KEY=<generate-a-random-secret-key>
   EMAIL_SERVICE=sendgrid
   SENDER_EMAIL=your-email@gmail.com
   EMAIL_API_KEY=your-sendgrid-api-key
   RECIPIENT_EMAIL=your-email@gmail.com
   ```

5. **Set up Scheduled Email (Cron Job):**
   - New → Cron Job
   - Name: `weekly-budget-email`
   - Schedule: `0 9 * * 3` (Every Wednesday at 9 AM UTC)
   - Command: `cd /opt/render/project/src && python email_scheduler.py`
   - Environment Variables: Same as web service

### Option B: Railway (Easy Setup)

**Pros:**
- Very easy deployment
- Free tier with $5 credit/month
- Automatic HTTPS

**Steps:**

1. **Sign up at [railway.app](https://railway.app)**

2. **Deploy from GitHub:**
   - New Project → Deploy from GitHub repo
   - Select your budget-app repository

3. **Add PostgreSQL:**
   - New → Database → PostgreSQL
   - Railway automatically sets `DATABASE_URL`

4. **Set Environment Variables:**
   - Go to Variables tab
   - Add all the same variables as Render

5. **For Scheduled Emails:**
   Railway doesn't have built-in cron, so you have two options:
   
   **Option 1: Use a separate scheduler service**
   - Deploy `email_scheduler.py` as a separate service
   - Keep it running 24/7 (uses resources)
   
   **Option 2: Use external cron service (Recommended)**
   - Use [cron-job.org](https://cron-job.org) (free)
   - Set up a cron job that calls your app's API endpoint
   - Or use [EasyCron](https://www.easycron.com)

### Option C: Fly.io (Good for Scheduled Tasks)

**Pros:**
- Free tier available
- Can run multiple processes (web + scheduler)
- Good documentation

**Steps:**

1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Sign up and login:**
   ```bash
   fly auth signup
   fly auth login
   ```

3. **Initialize Fly app:**
   ```bash
   fly launch
   ```

4. **Create fly.toml:**
   ```toml
   app = "your-budget-app"
   primary_region = "iad"
   
   [build]
   
   [http_service]
     internal_port = 5000
     force_https = true
     auto_stop_machines = true
     auto_start_machines = true
     min_machines_running = 0
   
   [[services]]
     processes = ["app"]
     http_checks = []
     internal_port = 5000
     protocol = "tcp"
   
   [[processes]]
     name = "app"
     command = "gunicorn app:app"
   
   [[processes]]
     name = "scheduler"
     command = "python email_scheduler.py"
   ```

5. **Set secrets:**
   ```bash
   fly secrets set DATABASE_URL=...
   fly secrets set SECRET_KEY=...
   fly secrets set EMAIL_SERVICE=sendgrid
   fly secrets set SENDER_EMAIL=...
   fly secrets set EMAIL_API_KEY=...
   fly secrets set RECIPIENT_EMAIL=...
   ```

## Step 3: Database Migration

After deployment, your app will automatically:
- Create the database tables on first run
- Run migrations for new columns

**Important:** If you have existing data in SQLite, you'll need to export and import it to PostgreSQL.

## Step 4: Test Your Deployment

1. Visit your app URL (provided by hosting platform)
2. Create a user account
3. Test adding expenses
4. Test sending an email manually
5. Wait for the scheduled email (or trigger it manually)

## Step 5: Environment Variables Checklist

Make sure these are set in your hosting platform:

**Required:**
- `DATABASE_URL` - PostgreSQL connection string (auto-set by some platforms)
- `SECRET_KEY` - Random secret for Flask sessions
- `EMAIL_SERVICE` - `sendgrid` or `mailgun`
- `SENDER_EMAIL` - Your verified email
- `EMAIL_API_KEY` - Your SendGrid/Mailgun API key
- `RECIPIENT_EMAIL` - Email to receive weekly reports

**Optional:**
- `MAILGUN_DOMAIN` - Only if using Mailgun
- `SMTP_SERVER` - Only if using SMTP
- `SMTP_PORT` - Only if using SMTP
- `SENDER_PASSWORD` - Only if using SMTP

## Troubleshooting

### Emails not sending
- Check SendGrid activity logs
- Verify API key is correct
- Check spam folder
- Verify sender email is verified in SendGrid

### Database errors
- Make sure `DATABASE_URL` is set correctly
- Check database is accessible from your app
- Verify migrations ran successfully

### Scheduler not running
- Check cron job is set up correctly
- Verify scheduler has access to environment variables
- Check scheduler logs for errors

## Security Notes

⚠️ **Important:**
- Never commit `.env` file to GitHub
- Use environment variables in hosting platform
- Keep API keys secret
- Use strong `SECRET_KEY` for production

## Quick Start Commands

```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Test email locally before deploying
python email_scheduler.py

# Check your .gitignore before pushing
git status
```

Good luck with your deployment! 🚀

