#!/bin/bash
# Restart PostgreSQL and create database

echo "🔄 Restarting PostgreSQL..."
echo "============================"
echo ""

PG_DIR="/opt/homebrew/var/postgresql@14"

# Stop PostgreSQL
echo "⏹️  Stopping PostgreSQL..."
pg_ctl -D "$PG_DIR" stop 2>/dev/null
sleep 2

# Start PostgreSQL
echo "▶️  Starting PostgreSQL..."
pg_ctl -D "$PG_DIR" start
sleep 3

# Check if running
if pg_isready > /dev/null 2>&1; then
    echo "✅ PostgreSQL is running"
else
    echo "❌ PostgreSQL failed to start"
    exit 1
fi

echo ""
echo "📦 Creating database 'budgetapp'..."
echo ""

# Try to create database as current user (should work with trust auth now)
if createdb budgetapp 2>/dev/null; then
    echo "✅ Database 'budgetapp' created successfully!"
else
    echo "⚠️  Could not create as current user, trying as postgres..."
    
    # Try connecting as postgres user (might need password, but try)
    if psql -U postgres -d postgres -c "CREATE DATABASE budgetapp;" 2>/dev/null; then
        echo "✅ Database 'budgetapp' created successfully!"
    else
        echo ""
        echo "❌ Still having issues. Let's try a different approach..."
        echo ""
        echo "Try this manually:"
        echo "  1. psql postgres"
        echo "  2. CREATE DATABASE budgetapp;"
        echo "  3. \\q"
        echo ""
        echo "Or create a user first:"
        echo "  1. psql postgres"
        echo "  2. CREATE USER nutan WITH SUPERUSER;"
        echo "  3. CREATE DATABASE budgetapp;"
        echo "  4. \\q"
        exit 1
    fi
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Connection string for .env file:"
echo "   DATABASE_URL=postgresql://nutan@localhost:5432/budgetapp"
echo ""
echo "🧪 Test connection:"
echo "   psql budgetapp"
echo ""

