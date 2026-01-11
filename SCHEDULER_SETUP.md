# Weekly Email Scheduler Setup

This guide shows you how to set up automatic weekly budget report emails that send every Wednesday.

## Quick Setup

### Step 1: Add Recipient Email to `.env`

Add this line to your `.env` file:

```bash
RECIPIENT_EMAIL=your-email@example.com
```

This is the email address that will receive the weekly budget reports.

### Step 2: Run the Scheduler

You have two options:

#### Option A: Run Scheduler in Separate Terminal (Recommended)

1. Open a new terminal window
2. Navigate to your project directory:
   ```bash
   cd /Users/nutan/Desktop/dev/budget-app
   ```
3. Activate your virtual environment:
   ```bash
   source venv/bin/activate
   ```
4. Run the scheduler:
   ```bash
   python email_scheduler.py
   ```

The scheduler will:
- Send emails every **Wednesday at 9:00 AM**
- Send reports for the **current month**
- Keep running until you stop it (Ctrl+C)

#### Option B: Run Scheduler in Background

Run it in the background so it keeps running:

```bash
nohup python email_scheduler.py > scheduler.log 2>&1 &
```

To stop it later:
```bash
pkill -f email_scheduler.py
```

### Step 3: Verify It's Working

1. The scheduler will print a confirmation message when it starts
2. You can test it immediately by uncommenting the test line in `email_scheduler.py`:
   ```python
   # Optional: Send a test email immediately (uncomment to test)
   print("Sending test email...")
   send_weekly_budget_report()
   ```

## Customizing the Schedule

To change when emails are sent, edit `email_scheduler.py`:

```python
# Every Wednesday at 9:00 AM (default)
schedule.every().wednesday.at("09:00").do(send_weekly_budget_report)

# Examples:
# Every Wednesday at 8:30 AM
schedule.every().wednesday.at("08:30").do(send_weekly_budget_report)

# Every Monday at 10:00 AM
schedule.every().monday.at("10:00").do(send_weekly_budget_report)

# Every day at 9:00 AM
schedule.every().day.at("09:00").do(send_weekly_budget_report)
```

## Running on a Server (Production)

### Using systemd (Linux)

Create `/etc/systemd/system/budget-scheduler.service`:

```ini
[Unit]
Description=Budget App Email Scheduler
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/budget-app
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python email_scheduler.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable budget-scheduler
sudo systemctl start budget-scheduler
```

### Using cron (Mac/Linux)

Add to crontab (`crontab -e`):

```bash
# Send budget report every Wednesday at 9:00 AM
0 9 * * 3 cd /path/to/budget-app && /path/to/venv/bin/python email_scheduler.py --once
```

Note: You'll need to modify the script to accept a `--once` flag for cron.

## Troubleshooting

### Scheduler not sending emails
- Check that `RECIPIENT_EMAIL` is set in `.env`
- Check that your Flask app database is accessible
- Check the scheduler output for error messages

### Emails going to spam
- Mark emails as "Not Spam" in your email client
- Add sender email to contacts
- See EMAIL_SETUP.md for more tips

### Scheduler stops running
- Make sure the terminal stays open (or use background process)
- Check for Python errors in the output
- On servers, use systemd or cron for reliability

## Testing

To test the scheduler without waiting for Wednesday:

1. Edit `email_scheduler.py`
2. Uncomment the test line:
   ```python
   # Optional: Send a test email immediately (uncomment to test)
   print("Sending test email...")
   send_weekly_budget_report()
   ```
3. Run the scheduler - it will send immediately
4. Comment it back out after testing

## Notes

- The scheduler sends reports for the **current month** (the month you're in when it runs)
- It uses the same email configuration as manual sends (SendGrid API key, etc.)
- The scheduler needs to run continuously to check the schedule
- Make sure your Flask app database is accessible from where the scheduler runs

