# Deployment Guide

## ⚠️ SECURITY WARNING

**Before deploying, you MUST add authentication!** The current app has no password protection.

## Quick Deployment Options

### Option 1: Render (Recommended - Free Tier Available)

1. **Create account** at [render.com](https://render.com)

2. **Create a new Web Service:**
   - Connect your GitHub repo
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`

3. **Add Environment Variables:**
   - `SECRET_KEY`: Generate with `python -c "import secrets; print(secrets.token_hex(32))"`
   - `APP_PASSWORD_HASH`: Generate password hash (see below)
   - `DATABASE_URL`: Render will auto-create PostgreSQL (free tier)

4. **Generate Password Hash:**
   ```python
   from werkzeug.security import generate_password_hash
   print(generate_password_hash('your-secure-password'))
   ```

5. **Deploy!**

### Option 2: Railway

1. Go to [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Add environment variables (same as Render)
4. Railway auto-detects Flask apps

### Option 3: Fly.io

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Run: `fly launch`
3. Follow prompts
4. Add secrets: `fly secrets set SECRET_KEY=... APP_PASSWORD_HASH=...`

## Before Deploying Checklist

- [ ] Add authentication (use `app_secure.py` as template)
- [ ] Set strong SECRET_KEY
- [ ] Set secure password
- [ ] Update database to PostgreSQL (for production)
- [ ] Test locally with production settings
- [ ] Backup your local database
- [ ] Review .gitignore (don't commit secrets!)

## Environment Variables Needed

```bash
SECRET_KEY=your-secret-key-here
APP_PASSWORD_HASH=pbkdf2:sha256:... (generated hash)
DATABASE_URL=postgresql://... (auto-provided by platform)
```

## Local Testing with Production Settings

```bash
export SECRET_KEY="test-key"
export APP_PASSWORD_HASH="pbkdf2:sha256:..."
export DATABASE_URL="sqlite:///test.db"
python app_secure.py
```

## Migration from SQLite to PostgreSQL

1. Export data from SQLite
2. Import to PostgreSQL on your platform
3. Update DATABASE_URL environment variable

## Security Best Practices

1. **Never commit passwords or secrets to Git**
2. **Use environment variables for all secrets**
3. **Enable HTTPS (most platforms do this automatically)**
4. **Use strong passwords**
5. **Regular backups of database**
6. **Monitor access logs**

## Cost Estimates

- **Render**: Free tier (limited hours), then ~$7/month
- **Railway**: Free tier (limited), then ~$5-20/month
- **Fly.io**: Free tier available, pay-as-you-go
- **Heroku**: No free tier, ~$7-25/month

## Alternative: Keep It Local

If you don't want to deploy:
- Use it locally only
- Access via localhost
- Regular backups of `instance/expenses.db`
- Use cloud storage (Dropbox, iCloud) to sync database file

