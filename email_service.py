"""
Email service for sending weekly budget reports.
Supports Gmail SMTP (free) and API-based services like SendGrid, Mailgun.
"""
import smtplib
import os
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from flask import current_app


def send_budget_email(recipient_email, budget_data):
    """
    Send weekly budget report email.
    
    Args:
        recipient_email: Email address to send to
        budget_data: Dictionary containing budget information
            - month: Current month
            - fixed_bills_loans_spent: Amount spent on bills/loans
            - fixed_bills_loans_limit: Budget limit for bills/loans
            - variable_spending_spent: Amount spent on variable expenses
            - variable_spending_limit: Budget limit for variable spending
            - investment_total: Investment amount
            - investment_min: Minimum investment target
            - investment_max: Maximum investment target
            - income_total: Total income
            - remaining_buffer: Remaining buffer amount
            - top_categories: List of top spending categories
    """
    # Check if using API-based service (SendGrid, Mailgun) or SMTP
    email_service = os.environ.get('EMAIL_SERVICE', 'smtp').lower()
    
    # Debug: Print which service is being used (remove in production)
    print(f"DEBUG: Using email service: {email_service}")
    
    if email_service in ['sendgrid', 'mailgun']:
        return send_via_api(recipient_email, budget_data, email_service)
    else:
        return send_via_smtp(recipient_email, budget_data)


def send_via_smtp(recipient_email, budget_data):
    """Send email via SMTP (Gmail, etc.)"""
    # Get email configuration from environment variables
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')  # App password for Gmail
    
    if not sender_email or not sender_password:
        raise ValueError("Email configuration missing. Set SENDER_EMAIL and SENDER_PASSWORD environment variables.")
    
    # Generate email content
    html_content, text_content, subject = generate_email_content(budget_data)
    
    # Create email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    
    # Attach both versions
    msg.attach(MIMEText(text_content, 'plain'))
    msg.attach(MIMEText(html_content, 'html'))
    
    # Send email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        raise


def send_via_api(recipient_email, budget_data, service):
    """Send email via API (SendGrid, Mailgun)"""
    sender_email = os.environ.get('SENDER_EMAIL')
    api_key = os.environ.get('EMAIL_API_KEY')
    
    # Debug: Print what we found (remove in production)
    print(f"DEBUG: SENDER_EMAIL={'SET' if sender_email else 'NOT SET'}, EMAIL_API_KEY={'SET' if api_key else 'NOT SET'}")
    
    if not sender_email or not api_key:
        raise ValueError(f"Email configuration missing. Set SENDER_EMAIL and EMAIL_API_KEY environment variables for {service}.")
    
    # Generate HTML and text content
    html_content, text_content, subject = generate_email_content(budget_data)
    
    if service == 'sendgrid':
        return send_via_sendgrid(sender_email, recipient_email, subject, html_content, text_content, api_key)
    elif service == 'mailgun':
        return send_via_mailgun(sender_email, recipient_email, subject, html_content, text_content, api_key)
    else:
        raise ValueError(f"Unknown email service: {service}")


def send_via_sendgrid(sender_email, recipient_email, subject, html_content, text_content, api_key):
    """Send email via SendGrid API"""
    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "personalizations": [{
            "to": [{"email": recipient_email}]
        }],
        "from": {"email": sender_email},
        "subject": subject,
        "content": [
            {"type": "text/plain", "value": text_content},
            {"type": "text/html", "value": html_content}
        ]
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        print(f"✅ Email sent successfully via SendGrid to {recipient_email}")
        return True
    except requests.exceptions.HTTPError as e:
        error_msg = f"SendGrid API error: {e}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                error_msg += f" - {error_detail}"
            except:
                error_msg += f" - {e.response.text}"
        print(f"❌ {error_msg}")
        raise ValueError(error_msg) from e
    except Exception as e:
        print(f"❌ Error sending email via SendGrid: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        raise


def send_via_mailgun(sender_email, recipient_email, subject, html_content, text_content, api_key):
    """Send email via Mailgun API"""
    domain = os.environ.get('MAILGUN_DOMAIN')
    if not domain:
        raise ValueError("MAILGUN_DOMAIN environment variable required for Mailgun")
    
    url = f"https://api.mailgun.net/v3/{domain}/messages"
    auth = ("api", api_key)
    
    data = {
        "from": sender_email,
        "to": recipient_email,
        "subject": subject,
        "text": text_content,
        "html": html_content
    }
    
    try:
        response = requests.post(url, auth=auth, data=data)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error sending email via Mailgun: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        raise


def generate_email_content(budget_data):
    """Generate HTML and text email content from budget data"""
    # Calculate percentages and status
    bills_percent = (budget_data['fixed_bills_loans_spent'] / budget_data['fixed_bills_loans_limit'] * 100) if budget_data['fixed_bills_loans_limit'] > 0 else 0
    variable_percent = (budget_data['variable_spending_spent'] / budget_data['variable_spending_limit'] * 100) if budget_data['variable_spending_limit'] > 0 else 0
    
    bills_status = "✅" if bills_percent < 100 else "⚠️ EXCEEDED"
    variable_status = "✅" if variable_percent < 100 else "⚠️ EXCEEDED"
    
    investment_status = "✅"
    if budget_data['investment_total'] < budget_data['investment_min']:
        investment_status = "📉 Below Target"
    elif budget_data['investment_total'] > budget_data['investment_max']:
        investment_status = "📈 Above Max"
    
    buffer_status = "✅" if budget_data['remaining_buffer'] >= 0 else "⚠️ NEGATIVE"
    
    subject = f'Weekly Budget Report - {budget_data.get("month", "Current Month")}'
    
    # Create HTML email
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 20px; border-radius: 0 0 10px 10px; }}
            .budget-item {{ background: white; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #667eea; }}
            .budget-item.exceeded {{ border-left-color: #ef4444; }}
            .budget-item.warning {{ border-left-color: #f59e0b; }}
            .progress-bar {{ background: #e5e7eb; height: 20px; border-radius: 10px; overflow: hidden; margin: 10px 0; }}
            .progress-fill {{ height: 100%; background: #10b981; transition: width 0.3s; }}
            .progress-fill.warning {{ background: #f59e0b; }}
            .progress-fill.exceeded {{ background: #ef4444; }}
            .amount {{ font-size: 24px; font-weight: bold; color: #667eea; }}
            .category-list {{ list-style: none; padding: 0; }}
            .category-list li {{ padding: 8px; background: white; margin: 5px 0; border-radius: 5px; }}
            .footer {{ text-align: center; margin-top: 20px; color: #6b7280; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💰 Weekly Budget Report</h1>
                <p>{budget_data.get('month', 'Current Month')}</p>
            </div>
            <div class="content">
                <h2>Budget Summary</h2>
                
                <!-- Fixed Bills + Loans -->
                <div class="budget-item {'exceeded' if bills_percent >= 100 else 'warning' if bills_percent >= 80 else ''}">
                    <h3>Fixed Bills + Loans {bills_status}</h3>
                    <div class="amount">${budget_data['fixed_bills_loans_spent']:.2f} / ${budget_data['fixed_bills_loans_limit']:.2f}</div>
                    <div class="progress-bar">
                        <div class="progress-fill {'exceeded' if bills_percent >= 100 else 'warning' if bills_percent >= 80 else ''}" 
                             style="width: {min(100, bills_percent)}%"></div>
                    </div>
                    <p>{bills_percent:.1f}% of budget used</p>
                    <p>Remaining: ${budget_data['fixed_bills_loans_limit'] - budget_data['fixed_bills_loans_spent']:.2f}</p>
                </div>
                
                <!-- Variable Spending -->
                <div class="budget-item {'exceeded' if variable_percent >= 100 else 'warning' if variable_percent >= 80 else ''}">
                    <h3>Variable Spending {variable_status}</h3>
                    <div class="amount">${budget_data['variable_spending_spent']:.2f} / ${budget_data['variable_spending_limit']:.2f}</div>
                    <div class="progress-bar">
                        <div class="progress-fill {'exceeded' if variable_percent >= 100 else 'warning' if variable_percent >= 80 else ''}" 
                             style="width: {min(100, variable_percent)}%"></div>
                    </div>
                    <p>{variable_percent:.1f}% of budget used</p>
                    <p>Remaining: ${budget_data['variable_spending_limit'] - budget_data['variable_spending_spent']:.2f}</p>
                </div>
                
                <!-- Investment -->
                <div class="budget-item">
                    <h3>Investment {investment_status}</h3>
                    <div class="amount">${budget_data['investment_total']:.2f}</div>
                    <p>Target Range: ${budget_data['investment_min']:.2f} - ${budget_data['investment_max']:.2f}</p>
                </div>
                
                <!-- Remaining Buffer -->
                <div class="budget-item {'exceeded' if budget_data['remaining_buffer'] < 0 else ''}">
                    <h3>Remaining Buffer {buffer_status}</h3>
                    <div class="amount" style="color: {'#ef4444' if budget_data['remaining_buffer'] < 0 else '#10b981'}">
                        ${budget_data['remaining_buffer']:.2f}
                    </div>
                    <p>Income - (Bills/Loans + Variable Spending + Investment)</p>
                </div>
                
                <!-- Top Categories -->
                {f'''
                <h3>Top Spending Categories</h3>
                <ul class="category-list">
                    {''.join([f'<li><strong>{cat["category"]}:</strong> ${cat["total"]:.2f}</li>' for cat in budget_data.get('top_categories', [])[:5]])}
                </ul>
                ''' if budget_data.get('top_categories') else ''}
                
                <div class="footer">
                    <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                    <p>This is an automated weekly budget report from your Expense Tracker app.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Create plain text version
    text_content = f"""
    Weekly Budget Report - {budget_data.get('month', 'Current Month')}
    
    Fixed Bills + Loans: ${budget_data['fixed_bills_loans_spent']:.2f} / ${budget_data['fixed_bills_loans_limit']:.2f} ({bills_percent:.1f}%)
    Variable Spending: ${budget_data['variable_spending_spent']:.2f} / ${budget_data['variable_spending_limit']:.2f} ({variable_percent:.1f}%)
    Investment: ${budget_data['investment_total']:.2f} (Target: ${budget_data['investment_min']:.2f} - ${budget_data['investment_max']:.2f})
    Remaining Buffer: ${budget_data['remaining_buffer']:.2f}
    
    Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
    """
    
    return html_content, text_content, subject


def send_test_email(recipient_email):
    """Send a test email to verify configuration."""
    test_data = {
        'month': 'Test Month',
        'fixed_bills_loans_spent': 450.00,
        'fixed_bills_loans_limit': 600.00,
        'variable_spending_spent': 650.00,
        'variable_spending_limit': 800.00,
        'investment_total': 1500.00,
        'investment_min': 1500.00,
        'investment_max': 1800.00,
        'income_total': 5000.00,
        'remaining_buffer': 1400.00,
        'top_categories': [
            {'category': 'Groceries', 'total': 200.00},
            {'category': 'Restaurants', 'total': 150.00},
            {'category': 'Coffee', 'total': 50.00}
        ]
    }
    return send_budget_email(recipient_email, test_data)

