#!/bin/bash
# Force restart PostgreSQL and create database

echo "🔄 Force Restarting PostgreSQL..."
echo "=================================="
echo ""

PG_DIR="/opt/homebrew/var/postgresql@14"

# Find and kill any PostgreSQL processes
echo "🔍 Finding PostgreSQL processes..."
PG_PIDS=$(ps aux | grep postgres | grep -v grep | awk '{print $2}')

if [ -n "$PG_PIDS" ]; then
    echo "⏹️  Stopping PostgreSQL processes..."
    for pid in $PG_PIDS; do
        kill -9 $pid 2>/dev/null
    done
    sleep 2
else
    echo "✅ No PostgreSQL processes found"
fi

# Try to stop gracefully first
pg_ctl -D "$PG_DIR" stop 2>/dev/null
sleep 2

# Start PostgreSQL
echo "▶️  Starting PostgreSQL..."
pg_ctl -D "$PG_DIR" start
sleep 4

# Check if running
if pg_isready > /dev/null 2>&1; then
    echo "✅ PostgreSQL is running"
else
    echo "❌ PostgreSQL failed to start"
    echo "   Check logs: tail -f $PG_DIR/log"
    exit 1
fi

echo ""
echo "📦 Creating database 'budgetapp'..."
echo ""

# Try creating database - should work with trust auth now
if createdb budgetapp 2>/dev/null; then
    echo "✅ Database 'budgetapp' created successfully!"
else
    echo "⚠️  Could not create as current user"
    echo ""
    echo "Let's try creating the user first..."
    echo ""
    echo "Please run these commands manually:"
    echo ""
    echo "  1. psql postgres"
    echo "  2. CREATE USER nutan WITH SUPERUSER;"
    echo "  3. CREATE DATABASE budgetapp;"
    echo "  4. \\q"
    echo ""
    echo "Or if that doesn't work, try:"
    echo "  1. psql -d postgres"
    echo "  2. CREATE DATABASE budgetapp;"
    echo "  3. \\q"
    exit 1
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

