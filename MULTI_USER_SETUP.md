# Multi-User Setup Guide

Your budget app now supports multiple users! Each user has their own separate expenses and budget data.

## How It Works

- **User Registration**: New users can create accounts with username, email, and password
- **User Login**: Users log in with their username/email and password
- **Data Isolation**: Each user only sees their own expenses and budget limits
- **Secure**: Passwords are hashed and stored securely

## First Time Setup

### Step 1: Run Database Migration

The database needs to be updated to support users. Run your Flask app once to automatically migrate:

```bash
python app.py
```

This will:
- Create the `user` table
- Add `user_id` columns to `expense` and `budget_limit` tables
- Migrate existing data (if any) to a default user

### Step 2: Create Your First User

1. Go to your app: `http://localhost:5000`
2. You'll be redirected to the login page
3. Click "Register" link
4. Fill in:
   - Username (unique)
   - Email (unique)
   - Password (at least 6 characters)
   - Confirm Password
5. Click "Create Account"

You'll be automatically logged in after registration!

## Using Multiple Users

### Registering Additional Users

1. Logout from current account
2. Click "Register" on the login page
3. Create a new account with different username/email
4. Each user will have their own separate data

### Logging In

Users can log in with either:
- Their username, OR
- Their email address

Both work the same way!

## Data Migration

If you had existing expenses before adding multi-user support:

- Existing expenses will be assigned to a default user (user_id = 1)
- You may want to create a user account and manually update the user_id if needed
- Or create a new account and start fresh

## Security Notes

- Passwords are hashed using Werkzeug's secure password hashing
- Users can only access their own data
- Session-based authentication keeps users logged in
- Logout clears the session

## Troubleshooting

### "User already exists"
- Username or email is already taken
- Try a different username or email

### "Password too short"
- Password must be at least 6 characters
- Use a longer password

### Can't see my expenses
- Make sure you're logged in with the correct account
- Each user only sees their own expenses

### Want to delete a user?
- Currently, user deletion is not implemented in the UI
- You can manually delete from the database if needed (advanced)

## Features

✅ User registration and login  
✅ Separate expenses per user  
✅ Separate budget limits per user  
✅ Secure password hashing  
✅ Session management  
✅ Auto-login after registration  

Enjoy your multi-user budget app! 🎉

