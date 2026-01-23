#!/usr/bin/env python3
"""
Migration script to transfer data from SQLite to PostgreSQL.

This script:
1. Reads all data from SQLite database
2. Connects to PostgreSQL database
3. Transfers all users, expenses, and budget limits
4. Preserves all relationships and data integrity

Usage:
    python migrate_sqlite_to_postgres.py
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def migrate_data():
    """Migrate data from SQLite to PostgreSQL"""
    
    # Get database URLs
    sqlite_path = 'instance/expenses.db'
    postgres_url = os.environ.get('DATABASE_URL')
    
    if not postgres_url:
        print("❌ ERROR: DATABASE_URL not set in environment variables")
        print("   Set DATABASE_URL to your PostgreSQL connection string")
        print("   Example: postgresql://user:password@host:port/dbname")
        return False
    
    # Fix postgres:// to postgresql://
    if postgres_url.startswith('postgres://'):
        postgres_url = postgres_url.replace('postgres://', 'postgresql://', 1)
    
    # Check if SQLite database exists
    if not os.path.exists(sqlite_path):
        print(f"❌ ERROR: SQLite database not found at {sqlite_path}")
        print("   Make sure you're running this from the project root directory")
        return False
    
    print("=" * 60)
    print("📦 SQLite to PostgreSQL Migration Tool")
    print("=" * 60)
    print()
    
    # Connect to SQLite
    print(f"📂 Connecting to SQLite: {sqlite_path}")
    sqlite_engine = create_engine(f'sqlite:///{sqlite_path}')
    sqlite_session = sessionmaker(bind=sqlite_engine)()
    
    # Connect to PostgreSQL
    print(f"📂 Connecting to PostgreSQL...")
    try:
        postgres_engine = create_engine(postgres_url)
        # Test connection
        with postgres_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Connected to PostgreSQL")
    except Exception as e:
        print(f"❌ ERROR: Failed to connect to PostgreSQL: {e}")
        print("   Check your DATABASE_URL and database credentials")
        return False
    
    postgres_session = sessionmaker(bind=postgres_engine)()
    
    try:
        # Step 1: Migrate Users
        print()
        print("👥 Migrating Users...")
        sqlite_users = sqlite_session.execute(text("SELECT * FROM user")).fetchall()
        
        if not sqlite_users:
            print("   No users found in SQLite database")
        else:
            # Get column names
            user_columns = [col[0] for col in sqlite_session.execute(text("PRAGMA table_info(user)")).fetchall()]
            
            migrated_users = 0
            skipped_users = 0
            
            for user_row in sqlite_users:
                user_dict = dict(zip(user_columns, user_row))
                
                # Check if user already exists in PostgreSQL
                existing = postgres_session.execute(
                    text("SELECT id FROM \"user\" WHERE username = :username OR email = :email"),
                    {"username": user_dict.get('username'), "email": user_dict.get('email')}
                ).fetchone()
                
                if existing:
                    print(f"   ⏭️  Skipping user '{user_dict.get('username')}' (already exists)")
                    skipped_users += 1
                    continue
                
                # Insert user
                try:
                    # Handle boolean conversion for email_notifications_enabled
                    email_enabled = user_dict.get('email_notifications_enabled', 0)
                    if isinstance(email_enabled, bool):
                        email_enabled = 1 if email_enabled else 0
                    else:
                        email_enabled = int(email_enabled) if email_enabled else 0
                    
                    postgres_session.execute(
                        text("""
                            INSERT INTO "user" (id, username, email, password_hash, email_notifications_enabled, notification_email, created_at)
                            VALUES (:id, :username, :email, :password_hash, :email_notifications_enabled, :notification_email, :created_at)
                        """),
                        {
                            "id": user_dict.get('id'),
                            "username": user_dict.get('username'),
                            "email": user_dict.get('email'),
                            "password_hash": user_dict.get('password_hash'),
                            "email_notifications_enabled": email_enabled,
                            "notification_email": user_dict.get('notification_email'),
                            "created_at": user_dict.get('created_at') or datetime.utcnow()
                        }
                    )
                    migrated_users += 1
                    print(f"   ✅ Migrated user: {user_dict.get('username')}")
                except Exception as e:
                    print(f"   ❌ Error migrating user {user_dict.get('username')}: {e}")
            
            postgres_session.commit()
            print(f"   📊 Users: {migrated_users} migrated, {skipped_users} skipped")
        
        # Step 2: Migrate Expenses
        print()
        print("💰 Migrating Expenses...")
        sqlite_expenses = sqlite_session.execute(text("SELECT * FROM expense")).fetchall()
        
        if not sqlite_expenses:
            print("   No expenses found in SQLite database")
        else:
            expense_columns = [col[0] for col in sqlite_session.execute(text("PRAGMA table_info(expense)")).fetchall()]
            
            migrated_expenses = 0
            skipped_expenses = 0
            
            for exp_row in sqlite_expenses:
                exp_dict = dict(zip(expense_columns, exp_row))
                
                # Check if expense already exists
                existing = postgres_session.execute(
                    text("SELECT id FROM expense WHERE id = :id"),
                    {"id": exp_dict.get('id')}
                ).fetchone()
                
                if existing:
                    skipped_expenses += 1
                    continue
                
                # Insert expense
                try:
                    # Handle boolean conversions
                    is_recurring = exp_dict.get('is_recurring', 0)
                    is_active = exp_dict.get('is_active', 1)
                    is_bill = exp_dict.get('is_bill', 0)
                    
                    if isinstance(is_recurring, bool):
                        is_recurring = 1 if is_recurring else 0
                    else:
                        is_recurring = int(is_recurring) if is_recurring else 0
                    
                    if isinstance(is_active, bool):
                        is_active = 1 if is_active else 0
                    else:
                        is_active = int(is_active) if is_active else 1
                    
                    if isinstance(is_bill, bool):
                        is_bill = 1 if is_bill else 0
                    else:
                        is_bill = int(is_bill) if is_bill else 0
                    
                    postgres_session.execute(
                        text("""
                            INSERT INTO expense (id, user_id, date, category, subcategory, description, amount, 
                                                is_recurring, is_active, is_bill, created_at)
                            VALUES (:id, :user_id, :date, :category, :subcategory, :description, :amount,
                                    :is_recurring, :is_active, :is_bill, :created_at)
                        """),
                        {
                            "id": exp_dict.get('id'),
                            "user_id": exp_dict.get('user_id'),
                            "date": exp_dict.get('date'),
                            "category": exp_dict.get('category'),
                            "subcategory": exp_dict.get('subcategory'),
                            "description": exp_dict.get('description'),
                            "amount": exp_dict.get('amount'),
                            "is_recurring": is_recurring,
                            "is_active": is_active,
                            "is_bill": is_bill,
                            "created_at": exp_dict.get('created_at') or datetime.utcnow()
                        }
                    )
                    migrated_expenses += 1
                except Exception as e:
                    print(f"   ❌ Error migrating expense {exp_dict.get('id')}: {e}")
            
            postgres_session.commit()
            print(f"   📊 Expenses: {migrated_expenses} migrated, {skipped_expenses} skipped")
        
        # Step 3: Migrate Budget Limits
        print()
        print("📊 Migrating Budget Limits...")
        sqlite_budgets = sqlite_session.execute(text("SELECT * FROM budget_limit")).fetchall()
        
        if not sqlite_budgets:
            print("   No budget limits found in SQLite database")
        else:
            budget_columns = [col[0] for col in sqlite_session.execute(text("PRAGMA table_info(budget_limit)")).fetchall()]
            
            migrated_budgets = 0
            skipped_budgets = 0
            
            for budget_row in sqlite_budgets:
                budget_dict = dict(zip(budget_columns, budget_row))
                
                # Check if budget limit already exists
                existing = postgres_session.execute(
                    text("SELECT id FROM budget_limit WHERE id = :id"),
                    {"id": budget_dict.get('id')}
                ).fetchone()
                
                if existing:
                    skipped_budgets += 1
                    continue
                
                # Insert budget limit
                try:
                    postgres_session.execute(
                        text("""
                            INSERT INTO budget_limit (id, month, fixed_bills_loans, variable_spending, 
                                                     investing_min, investing_max, user_id, created_at, updated_at)
                            VALUES (:id, :month, :fixed_bills_loans, :variable_spending,
                                    :investing_min, :investing_max, :user_id, :created_at, :updated_at)
                        """),
                        {
                            "id": budget_dict.get('id'),
                            "month": budget_dict.get('month'),
                            "fixed_bills_loans": budget_dict.get('fixed_bills_loans', 600),
                            "variable_spending": budget_dict.get('variable_spending', 800),
                            "investing_min": budget_dict.get('investing_min', 1500),
                            "investing_max": budget_dict.get('investing_max', 1800),
                            "user_id": budget_dict.get('user_id'),
                            "created_at": budget_dict.get('created_at') or datetime.utcnow(),
                            "updated_at": budget_dict.get('updated_at') or datetime.utcnow()
                        }
                    )
                    migrated_budgets += 1
                except Exception as e:
                    print(f"   ❌ Error migrating budget limit {budget_dict.get('id')}: {e}")
            
            postgres_session.commit()
            print(f"   📊 Budget Limits: {migrated_budgets} migrated, {skipped_budgets} skipped")
        
        print()
        print("=" * 60)
        print("✅ Migration Complete!")
        print("=" * 60)
        print()
        print("📝 Summary:")
        print(f"   - Users: {migrated_users if 'migrated_users' in locals() else 0} migrated")
        print(f"   - Expenses: {migrated_expenses if 'migrated_expenses' in locals() else 0} migrated")
        print(f"   - Budget Limits: {migrated_budgets if 'migrated_budgets' in locals() else 0} migrated")
        print()
        print("🎉 Your data has been successfully migrated to PostgreSQL!")
        print("   You can now use your app with the PostgreSQL database.")
        return True
        
    except Exception as e:
        print(f"❌ ERROR during migration: {e}")
        import traceback
        traceback.print_exc()
        postgres_session.rollback()
        return False
    
    finally:
        sqlite_session.close()
        postgres_session.close()


if __name__ == '__main__':
    print()
    print("⚠️  IMPORTANT: Make sure your PostgreSQL database is set up and DATABASE_URL is configured!")
    print()
    response = input("Do you want to proceed with migration? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        success = migrate_data()
        sys.exit(0 if success else 1)
    else:
        print("Migration cancelled.")
        sys.exit(0)

