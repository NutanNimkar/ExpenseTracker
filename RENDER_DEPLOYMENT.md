# Render.com Deployment Guide (Recommended)

Render is the easiest platform for deploying your budget app with scheduled emails.

## Why Render?

✅ Free tier available  
✅ Built-in PostgreSQL database  
✅ Built-in cron jobs (perfect for weekly emails)  
✅ Automatic HTTPS  
✅ Easy GitHub integration  

## Step-by-Step Deployment

### Step 1: Push to GitHub

First, make sure your code is on GitHub (see GITHUB_SETUP.md).

### Step 2: Sign Up for Render

1. Go to [render.com](https://render.com)
2. Sign up with GitHub (easiest option)
3. Connect your GitHub account

### Step 3: Create PostgreSQL Database

1. In Render dashboard, click **New +**
2. Select **PostgreSQL**
3. Name: `budget-app-db`
4. Database: `budgetapp` (or leave default)
5. Region: Choose closest to you
6. Plan: **Free** (or paid for better performance)
7. Click **Create Database**
8. **Important:** Copy the **Internal Database URL** (you'll need this)

### Step 4: Create Web Service

1. Click **New +** → **Web Service**
2. Connect your GitHub repository (`budget-app`)
3. Configure:
   - **Name:** `budget-app` (or any name)
   - **Region:** Same as database
   - **Branch:** `main`
   - **Root Directory:** (leave empty)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** **Free** (or paid)

4. Click **Advanced** and add Environment Variables:
   ```
   DATABASE_URL=<paste-internal-database-url-from-step-3>
   SECRET_KEY=<generate-random-key-see-below>
   EMAIL_SERVICE=sendgrid
   SENDER_EMAIL=your-email@gmail.com
   EMAIL_API_KEY=your-sendgrid-api-key-here
   RECIPIENT_EMAIL=your-email@gmail.com
   ```

5. Click **Create Web Service**

### Step 5: Generate Secret Key

Run this command to generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and use it as `SECRET_KEY` in Render.

### Step 6: Set Up Weekly Email Scheduler (Cron Job)

1. In Render dashboard, click **New +**
2. Select **Cron Job**
3. Configure:
   - **Name:** `weekly-budget-email`
   - **Schedule:** `0 9 * * 3` (Every Wednesday at 9:00 AM UTC)
   - **Command:** `cd /opt/render/project/src && python email_scheduler.py`
   - **Environment Variables:** Click **Add Environment Variable** and add the same ones as web service:
     - `DATABASE_URL`
     - `SECRET_KEY`
     - `EMAIL_SERVICE`
     - `SENDER_EMAIL`
     - `EMAIL_API_KEY`
     - `RECIPIENT_EMAIL`

4. Click **Create Cron Job**

### Step 7: Test Your Deployment

1. Wait for deployment to complete (2-3 minutes)
2. Visit your app URL (shown in Render dashboard)
3. Create a user account
4. Test adding expenses
5. Test sending an email manually (click "📧 Email Report")
6. Check your email!

### Step 8: Verify Scheduled Emails

- The cron job will run every Wednesday at 9:00 AM UTC
- Check Render logs to see if it's running
- You can manually trigger it by clicking "Run Now" in the cron job dashboard

## Timezone Adjustment

The cron job runs at 9:00 AM UTC. To change the time:

1. Go to your Cron Job in Render
2. Click **Settings**
3. Update the schedule:
   - `0 9 * * 3` = 9 AM UTC (Wednesday)
   - `0 14 * * 3` = 2 PM UTC (Wednesday) = 9 AM EST
   - `0 17 * * 3` = 5 PM UTC (Wednesday) = 12 PM EST

Use [crontab.guru](https://crontab.guru) to calculate your desired time.

## Environment Variables Summary

Make sure these are set in BOTH Web Service and Cron Job:

| Variable | Value | Notes |
|----------|-------|-------|
| `DATABASE_URL` | `postgresql://...` | From PostgreSQL service |
| `SECRET_KEY` | Random 64-char string | Generate with Python |
| `EMAIL_SERVICE` | `sendgrid` | Your email service |
| `SENDER_EMAIL` | `nutannimkar69@gmail.com` | Your verified email |
| `EMAIL_API_KEY` | `SG.xxx...` | Your SendGrid API key |
| `RECIPIENT_EMAIL` | `nutannimkar69@gmail.com` | Where to send reports |

## Troubleshooting

### App won't start
- Check build logs in Render
- Verify all environment variables are set
- Check that `requirements.txt` is correct

### Database connection errors
- Verify `DATABASE_URL` is correct
- Make sure database is in same region as web service
- Check database is running

### Emails not sending
- Check SendGrid activity logs
- Verify API key is correct
- Check cron job logs in Render

### Cron job not running
- Check cron job logs
- Verify environment variables are set in cron job
- Check schedule syntax is correct

## Cost

**Free Tier:**
- Web Service: Free (spins down after 15 min inactivity)
- PostgreSQL: Free (90 days, then $7/month)
- Cron Job: Free

**Paid Tier (Recommended for Production):**
- Web Service: $7/month (always on)
- PostgreSQL: $7/month
- Cron Job: Free

## Next Steps

1. ✅ Deploy to Render
2. ✅ Set up cron job
3. ✅ Test email sending
4. ✅ Wait for first weekly email!

Your app is now live! 🎉

