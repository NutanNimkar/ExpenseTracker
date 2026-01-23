#!/bin/bash
# Test different ways to connect to PostgreSQL

echo "🔍 Testing PostgreSQL Connection Methods"
echo "========================================"
echo ""

echo "Method 1: Connect with your macOS username (peer auth)..."
if psql -d postgres -c "SELECT current_user, version();" 2>/dev/null; then
    echo "✅ SUCCESS! Connected with your username"
    echo ""
    echo "Creating database 'budgetapp'..."
    if psql -d postgres -c "CREATE DATABASE budgetapp;" 2>/dev/null; then
        echo "✅ Database 'budgetapp' created!"
        echo ""
        echo "📝 Add this to your .env file:"
        echo "   DATABASE_URL=postgresql://$(whoami)@localhost:5432/budgetapp"
        exit 0
    else
        echo "⚠️  Database might already exist"
        exit 0
    fi
else
    echo "❌ Could not connect with username"
fi

echo ""
echo "Method 2: Try connecting to template1 database..."
if psql -d template1 -c "SELECT current_user;" 2>/dev/null; then
    echo "✅ Connected to template1!"
    echo "Creating database 'budgetapp'..."
    psql -d template1 -c "CREATE DATABASE budgetapp;" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✅ Database created!"
        echo ""
        echo "📝 Add this to your .env file:"
        echo "   DATABASE_URL=postgresql://$(whoami)@localhost:5432/budgetapp"
        exit 0
    fi
else
    echo "❌ Could not connect to template1"
fi

echo ""
echo "❌ Could not connect using any method"
echo ""
echo "💡 Recommendation: Use Cloud PostgreSQL instead!"
echo ""
echo "For deployment, cloud PostgreSQL is much easier:"
echo "  1. Sign up for Render.com or Railway"
echo "  2. Create PostgreSQL database (one click)"
echo "  3. Copy connection string"
echo "  4. No authentication issues!"
echo ""
echo "Your app will work the same way - it automatically uses"
echo "PostgreSQL when DATABASE_URL is set!"

