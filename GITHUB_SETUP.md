# GitHub Setup Guide

Follow these steps to add your budget app to GitHub and deploy it.

## Step 1: Initialize Git Repository

```bash
# Navigate to your project directory
cd /Users/nutan/Desktop/dev/budget-app

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Budget tracking app with multi-user support, email features, and subcategories"
```

## Step 2: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **+** icon in the top right → **New repository**
3. Repository name: `budget-app` (or any name you prefer)
4. Description: "Personal budget and expense tracking application"
5. Choose: **Public** or **Private** (your choice)
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click **Create repository**

## Step 3: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add GitHub as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/budget-app.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 4: Verify Files Are Pushed

Go to your GitHub repository and verify:
- ✅ All Python files are there
- ✅ `requirements.txt` is there
- ✅ `Procfile` is there
- ✅ Templates folder is there
- ❌ `.env` file is NOT there (should be ignored)
- ❌ `venv/` folder is NOT there (should be ignored)
- ❌ `instance/` folder is NOT there (should be ignored)

## Step 5: Deploy to Hosting Platform

Now that your code is on GitHub, you can deploy it. See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

**Recommended: Render.com** (easiest for scheduled emails)

## Quick Checklist Before Pushing

- [ ] `.env` file is in `.gitignore` ✅
- [ ] `venv/` is in `.gitignore` ✅
- [ ] `instance/` is in `.gitignore` ✅
- [ ] Database files are in `.gitignore` ✅
- [ ] All code files are ready
- [ ] `requirements.txt` is up to date
- [ ] `Procfile` exists for deployment

## Security Reminder

⚠️ **Never commit:**
- `.env` file
- API keys
- Passwords
- Database files
- Virtual environment

All sensitive data should be set as environment variables in your hosting platform!

