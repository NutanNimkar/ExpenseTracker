# 🔑 Password Reset Guide

## Quick Reset Steps

### 1. Stop Your Flask App
If the app is running, stop it first (press `Ctrl+C` in the terminal).

### 2. Run the Reset Script
```bash
python reset_password.py
```

### 3. Enter Your New Password
- Enter your new password (twice for confirmation)
- The script will generate a secure hash

### 4. Update Configuration

**If you have a `.env` file:**
- The script can update it automatically (just say 'y' when prompted)
- Or manually edit `.env` and set:
  ```
  APP_PASSWORD_HASH=pbkdf2:sha256:...your-new-hash...
  ```

**If using environment variables:**
- Set the variable:
  ```bash
  export APP_PASSWORD_HASH="pbkdf2:sha256:...your-new-hash..."
  ```

### 5. Restart Your App
```bash
python app.py
```

### 6. Login with New Password
Visit your app and login with the new password.

---

## Alternative: Manual Reset

If the script doesn't work, you can reset manually:

### Step 1: Generate Password Hash
```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('your-new-password'))"
```

### Step 2: Update .env File
Create or edit `.env` file in the project root:
```
APP_PASSWORD_HASH=pbkdf2:sha256:...paste-hash-here...
SECRET_KEY=your-secret-key
```

### Step 3: Restart App
```bash
python app.py
```

---

## Common Issues

### "Password reset not working"
- ✅ **Did you restart the app?** This is the most common issue!
- ✅ Check that `.env` file is in the same directory as `app.py`
- ✅ Verify the hash starts with `pbkdf2:sha256:`
- ✅ Make sure you're using the password (not the hash) to login

### "Can't find .env file"
- Create a new `.env` file in the project root
- Add: `APP_PASSWORD_HASH=your-hash-here`

### "Still can't login after reset"
1. Stop the app completely
2. Clear browser cookies for the site
3. Restart the app
4. Try logging in again

---

## Security Notes

- ⚠️ **Never commit your `.env` file to Git** (it's in `.gitignore`)
- ⚠️ **Use a strong password** (8+ characters, mix of letters/numbers)
- ⚠️ **Keep your password hash secure**
- ⚠️ **Change default password immediately** (default is `changeme123`)

---

## Need Help?

If you're still having issues:
1. Check `README_AUTH.md` for detailed authentication info
2. Verify your `.env` file format is correct
3. Make sure `python-dotenv` is installed: `pip install python-dotenv`
4. Check that Flask app is reading environment variables correctly

