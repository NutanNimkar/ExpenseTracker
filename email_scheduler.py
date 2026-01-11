#!/usr/bin/env python3
"""
Weekly email scheduler for budget reports.
Sends budget report every Wednesday for the current month.
"""
import schedule
import time
import os
from datetime import datetime
from app import app, db, Expense, BudgetLimit
from email_service import send_budget_email

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Get recipient email from environment variable
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL')


def send_weekly_budget_report():
    """Send weekly budget report for the current month"""
    if not RECIPIENT_EMAIL:
        print("❌ RECIPIENT_EMAIL not set in .env file. Skipping email.")
        return
    
    with app.app_context():
        try:
            # Get current month
            now = datetime.now()
            current_month = f"{now.year}-{now.month:02d}"
            
            print(f"📧 Sending weekly budget report for {now.strftime('%B %Y')} to {RECIPIENT_EMAIL}...")
            
            # Get expenses for the current month
            expenses = Expense.query.filter(
                Expense.date.like(f'{now.year}-{now.month:02d}%')
            ).all()
            
            # Calculate totals
            fixed_bills_loans_spent = sum(
                exp.amount for exp in expenses 
                if exp.category in ['Bills', 'Loans'] or (exp.category == 'Subscription' and exp.is_bill)
            )
            
            variable_spending_spent = sum(
                exp.amount for exp in expenses
                if exp.category not in ['Bills', 'Loans', 'Income', 'Investment', 'Payment'] 
                and not (exp.category == 'Subscription' and exp.is_bill)
            )
            
            investment_total = sum(exp.amount for exp in expenses if exp.category == 'Investment')
            income_total = sum(exp.amount for exp in expenses if exp.category == 'Income')
            
            # Get budget limits
            budget_limit = BudgetLimit.query.filter_by(month=current_month).first()
            if not budget_limit:
                # Use defaults
                fixed_bills_loans_limit = 600
                variable_spending_limit = 800
                investment_min = 1500
                investment_max = 1800
            else:
                fixed_bills_loans_limit = budget_limit.fixed_bills_loans
                variable_spending_limit = budget_limit.variable_spending
                investment_min = budget_limit.investing_min
                investment_max = budget_limit.investing_max
            
            # Calculate remaining buffer
            remaining_buffer = income_total - (fixed_bills_loans_spent + variable_spending_spent + investment_total)
            
            # Get top categories
            category_totals = {}
            for exp in expenses:
                if exp.category not in ['Income', 'Investment', 'Payment']:
                    category_totals[exp.category] = category_totals.get(exp.category, 0) + exp.amount
            
            top_categories = [
                {'category': cat, 'total': total}
                for cat, total in sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:5]
            ]
            
            # Format month display
            month_display = now.strftime('%B %Y')
            
            # Prepare budget data
            budget_data = {
                'month': month_display,
                'fixed_bills_loans_spent': fixed_bills_loans_spent,
                'fixed_bills_loans_limit': fixed_bills_loans_limit,
                'variable_spending_spent': variable_spending_spent,
                'variable_spending_limit': variable_spending_limit,
                'investment_total': investment_total,
                'investment_min': investment_min,
                'investment_max': investment_max,
                'income_total': income_total,
                'remaining_buffer': remaining_buffer,
                'top_categories': top_categories
            }
            
            # Send email
            send_budget_email(RECIPIENT_EMAIL, budget_data)
            print(f"✅ Weekly budget report sent successfully!")
            
        except Exception as e:
            print(f"❌ Error sending weekly budget report: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Main scheduler loop"""
    print("=" * 60)
    print("📅 Budget Report Email Scheduler")
    print("=" * 60)
    
    if not RECIPIENT_EMAIL:
        print("⚠️  WARNING: RECIPIENT_EMAIL not set in .env file")
        print("   Add this to your .env file: RECIPIENT_EMAIL=your-email@example.com")
        print("   The scheduler will run but won't send emails until this is set.")
        print()
    
    # Schedule email every Wednesday at 9:00 AM
    schedule.every().wednesday.at("09:00").do(send_weekly_budget_report)
    
    print(f"✅ Scheduled weekly budget reports every Wednesday at 9:00 AM")
    print(f"📧 Recipient: {RECIPIENT_EMAIL if RECIPIENT_EMAIL else 'NOT SET'}")
    print()
    print("🔄 Scheduler running... (Press Ctrl+C to stop)")
    print("=" * 60)
    print()
    
    # Show next run time
    next_run = schedule.next_run()
    if next_run:
        print(f"⏰ Next email will be sent: {next_run.strftime('%A, %B %d, %Y at %I:%M %p')}")
        print()
    
    # Optional: Send a test email immediately (uncomment to test)
    # print("Sending test email...")
    # send_weekly_budget_report()
    
    # Run scheduler
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\n👋 Scheduler stopped.")


if __name__ == '__main__':
    main()

