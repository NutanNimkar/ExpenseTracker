#!/bin/bash
# Set password for postgres user or create your own user

echo "🔐 PostgreSQL User Setup"
echo "======================="
echo ""

PG_DIR="/opt/homebrew/var/postgresql@14"

echo "The 'postgres' user is the default superuser in PostgreSQL."
echo "On Homebrew installations, it often doesn't have a password set."
echo ""
echo "Let's set it up..."
echo ""

# Check if we can connect without password (trust auth)
if psql -U postgres -d postgres -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ Can connect to postgres user (no password needed)"
    echo ""
    echo "Setting password for postgres user..."
    read -sp "Enter a password for 'postgres' user (or press Enter to skip): " POSTGRES_PASSWORD
    echo ""
    
    if [ -n "$POSTGRES_PASSWORD" ]; then
        psql -U postgres -d postgres -c "ALTER USER postgres WITH PASSWORD '$POSTGRES_PASSWORD';" 2>/dev/null
        echo "✅ Password set for postgres user"
    else
        echo "⏭️  Skipping password setup"
    fi
    
    echo ""
    echo "Creating database 'budgetapp'..."
    if psql -U postgres -d postgres -c "CREATE DATABASE budgetapp;" 2>/dev/null; then
        echo "✅ Database 'budgetapp' created!"
    else
        echo "⚠️  Database might already exist"
    fi
    
    echo ""
    echo "Creating user 'nutan'..."
    if psql -U postgres -d postgres -c "CREATE USER nutan WITH SUPERUSER;" 2>/dev/null; then
        echo "✅ User 'nutan' created!"
    else
        echo "⚠️  User might already exist"
    fi
    
    echo ""
    echo "✅ Setup complete!"
    echo ""
    echo "📝 Connection strings for .env file:"
    if [ -n "$POSTGRES_PASSWORD" ]; then
        echo "   DATABASE_URL=postgresql://postgres:$POSTGRES_PASSWORD@localhost:5432/budgetapp"
    fi
    echo "   DATABASE_URL=postgresql://nutan@localhost:5432/budgetapp"
    
else
    echo "❌ Cannot connect to postgres user"
    echo ""
    echo "The postgres user might need a password, or authentication is misconfigured."
    echo ""
    echo "Try these options:"
    echo ""
    echo "Option 1: Try connecting with your macOS username:"
    echo "   psql -d postgres"
    echo ""
    echo "Option 2: Reset postgres password (requires stopping PostgreSQL):"
    echo "   1. Stop PostgreSQL: pg_ctl -D $PG_DIR stop"
    echo "   2. Start in single-user mode: postgres --single -D $PG_DIR postgres"
    echo "   3. Run: ALTER USER postgres WITH PASSWORD 'newpassword';"
    echo "   4. Restart normally"
    echo ""
    echo "Option 3: Use cloud PostgreSQL instead (much easier!):"
    echo "   - Sign up for Render.com or Railway"
    echo "   - Create PostgreSQL database"
    echo "   - Copy connection string"
    exit 1
fi

