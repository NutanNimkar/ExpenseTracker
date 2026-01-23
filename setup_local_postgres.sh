#!/bin/bash
# Quick script to start PostgreSQL and create database for budget app

echo "🚀 Setting up local PostgreSQL for budget app"
echo "=============================================="
echo ""

# Detect PostgreSQL version
if [ -d "/opt/homebrew/var/postgresql@14" ]; then
    PG_VERSION="14"
    PG_DIR="/opt/homebrew/var/postgresql@14"
elif [ -d "/opt/homebrew/var/postgresql@15" ]; then
    PG_VERSION="15"
    PG_DIR="/opt/homebrew/var/postgresql@15"
else
    echo "❌ PostgreSQL data directory not found"
    echo "   Please install PostgreSQL first: brew install postgresql@14"
    exit 1
fi

echo "📦 Found PostgreSQL $PG_VERSION"
echo ""

# Check if PostgreSQL is running
if pg_isready > /dev/null 2>&1; then
    echo "✅ PostgreSQL is already running"
else
    echo "🔄 Starting PostgreSQL..."
    
    # Try to start PostgreSQL
    if pg_ctl -D "$PG_DIR" start > /dev/null 2>&1; then
        echo "✅ PostgreSQL started successfully"
        sleep 2
    else
        echo "⚠️  Could not start PostgreSQL automatically"
        echo "   Trying to initialize database..."
        
        # Check if database is initialized
        if [ ! -d "$PG_DIR" ] || [ -z "$(ls -A $PG_DIR 2>/dev/null)" ]; then
            echo "📦 Initializing PostgreSQL database..."
            initdb "$PG_DIR"
        fi
        
        # Try starting again
        if pg_ctl -D "$PG_DIR" start > /dev/null 2>&1; then
            echo "✅ PostgreSQL started successfully"
            sleep 2
        else
            echo "❌ Failed to start PostgreSQL"
            echo ""
            echo "Please try manually:"
            echo "  pg_ctl -D $PG_DIR start"
            exit 1
        fi
    fi
fi

# Check if database exists
if psql -lqt | cut -d \| -f 1 | grep -qw budgetapp; then
    echo "✅ Database 'budgetapp' already exists"
else
    echo "📦 Creating database 'budgetapp'..."
    if createdb budgetapp 2>/dev/null; then
        echo "✅ Database created successfully"
    else
        echo "⚠️  Could not create database with 'createdb'"
        echo "   Trying with psql..."
        psql postgres -c "CREATE DATABASE budgetapp;" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "✅ Database created successfully"
        else
            echo "❌ Failed to create database"
            exit 1
        fi
    fi
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Connection string for .env file:"
echo "   DATABASE_URL=postgresql://$(whoami)@localhost:5432/budgetapp"
echo ""
echo "🧪 Test connection:"
echo "   psql budgetapp"
echo ""

