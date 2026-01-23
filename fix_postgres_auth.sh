#!/bin/bash
# Fix PostgreSQL authentication to allow local connections without password

echo "🔧 Fixing PostgreSQL Authentication"
echo "===================================="
echo ""

PG_VERSION="14"
PG_DIR="/opt/homebrew/var/postgresql@14"
PG_CONF="$PG_DIR/pg_hba.conf"

# Check if pg_hba.conf exists
if [ ! -f "$PG_CONF" ]; then
    echo "❌ PostgreSQL config file not found at $PG_CONF"
    echo "   PostgreSQL may not be initialized"
    exit 1
fi

echo "📝 Current authentication settings:"
grep -E "^local|^host.*127.0.0.1|^host.*localhost" "$PG_CONF" | head -5
echo ""

# Backup original config
if [ ! -f "$PG_CONF.backup" ]; then
    cp "$PG_CONF" "$PG_CONF.backup"
    echo "✅ Backed up original config to $PG_CONF.backup"
fi

# Check if trust is already set
if grep -q "^local.*trust" "$PG_CONF" && grep -q "^host.*127.0.0.1.*trust" "$PG_CONF"; then
    echo "✅ Authentication already configured for local trust"
else
    echo "🔧 Configuring local authentication to 'trust' (no password required)..."
    
    # Create temporary file with updated config
    cat > /tmp/pg_hba_fix.conf << 'EOF'
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     trust
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust
# IPv6 local connections:
host    all             all             ::1/128                 trust
EOF
    
    # Replace the local and host lines in pg_hba.conf
    # Keep other lines intact
    awk '
    BEGIN { 
        print "# TYPE  DATABASE        USER            ADDRESS                 METHOD"
        print ""
        print "# \"local\" is for Unix domain socket connections only"
        print "local   all             all                                     trust"
        print "# IPv4 local connections:"
        print "host    all             all             127.0.0.1/32            trust"
        print "# IPv6 local connections:"
        print "host    all             all             ::1/128                 trust"
        print ""
    }
    /^#/ { next }
    /^local/ { next }
    /^host.*127\.0\.0\.1/ { next }
    /^host.*::1/ { next }
    /^$/ { next }
    { print }
    ' "$PG_CONF" > /tmp/pg_hba_new.conf
    
    # Replace the original file
    mv /tmp/pg_hba_new.conf "$PG_CONF"
    
    echo "✅ Updated pg_hba.conf"
fi

# Reload PostgreSQL configuration
echo "🔄 Reloading PostgreSQL configuration..."
pg_ctl -D "$PG_DIR" reload 2>/dev/null || echo "⚠️  Could not reload (PostgreSQL may need restart)"

echo ""
echo "✅ Configuration updated!"
echo ""
echo "📝 Now try creating the database again:"
echo "   createdb budgetapp"
echo ""
echo "Or connect as postgres user:"
echo "   psql -U postgres -c 'CREATE DATABASE budgetapp;'"
echo ""

