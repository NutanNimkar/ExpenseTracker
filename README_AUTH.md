# Authentication Setup

## 🔒 Password Protection Added

Your expense tracker now has password protection! All routes are secured.

## Quick Setup

### 1. Set Your Password

Run the setup script:
```bash
python setup_password.py
```

This will:
- Prompt you for a password
- Generate a secure password hash
- Show you what to add to your environment variables

### 2. Set Environment Variable

#### For Local Development:

Create a `.env` file in the project root:
```bash
APP_PASSWORD_HASH=pbkdf2:sha256:...your-generated-hash...
SECRET_KEY=your-secret-key-here
```

Then install python-dotenv and load it:
```bash
pip install python-dotenv
```

Add to `app.py` (already done):
```python
from dotenv import load_dotenv
load_dotenv()
```

#### For Production/Deployment:

Set these environment variables in your hosting platform:
- `APP_PASSWORD_HASH` - Your password hash
- `SECRET_KEY` - A random secret key (for session security)
- `DATABASE_URL` - Database connection (auto-provided by most platforms)

## Default Password (CHANGE THIS!)

The app comes with a default password: `changeme123`

**⚠️ IMPORTANT: Change this immediately!**

## How It Works

1. **Login Page**: Users are redirected to `/login` if not authenticated
2. **Session Management**: Once logged in, session persists
3. **Protected Routes**: All API endpoints require authentication
4. **Logout**: Click "Logout" button in header to sign out

## Security Features

- ✅ Password hashing (Werkzeug PBKDF2)
- ✅ Session-based authentication
- ✅ Protected API routes
- ✅ Secure session cookies
- ✅ Environment variable configuration

## Generate Secret Key

For production, generate a secure secret key:
```python
import secrets
print(secrets.token_hex(32))
```

## Resetting Your Password

### If You Forgot Your Password

**Option 1: Use the reset script (Recommended)**
```bash
python reset_password.py
```

This will:
- Generate a new password hash
- Optionally update your `.env` file automatically
- Show you what to do next

**Option 2: Manual reset**

1. Generate new password hash:
   ```bash
   python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('your-new-password'))"
   ```

2. Update your `.env` file:
   ```bash
   APP_PASSWORD_HASH=pbkdf2:sha256:...new-hash...
   ```

3. Or set environment variable:
   ```bash
   export APP_PASSWORD_HASH="pbkdf2:sha256:...new-hash..."
   ```

4. **Restart your Flask app** (important!)

### Steps to Reset:

1. **Stop your Flask app** (Ctrl+C if running)
2. **Run reset script**: `python reset_password.py`
3. **Enter your new password** (twice for confirmation)
4. **Update .env file** (script can do this automatically)
5. **Restart Flask app**: `python app.py`
6. **Login with new password**

## Troubleshooting

**Can't login?**
- Check that `APP_PASSWORD_HASH` is set correctly
- Make sure you're using the password you set (not the hash itself)
- **Restart the app** after changing the password hash
- Clear browser cookies/cache if still having issues

**Session expires?**
- Sessions are permanent by default
- Clear browser cookies if having issues

**Want to change password?**
- Run `reset_password.py` (easier) or `setup_password.py`
- Update `APP_PASSWORD_HASH` environment variable
- **Restart the app** (this is critical!)

**Password reset not working?**
- Make sure you restarted the Flask app after updating the hash
- Check that the `.env` file is in the same directory as `app.py`
- Verify the hash format is correct (starts with `pbkdf2:sha256:`)

