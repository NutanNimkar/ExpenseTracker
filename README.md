# 💰 Budget & Expense Tracker

A full-featured budget tracking application with multi-user support, automated email reports, and detailed expense categorization.

## Features

- 📝 **Expense Tracking**: Track expenses with categories, subcategories, and descriptions
- 👥 **Multi-User Support**: Each user has their own separate budget and expenses
- 📊 **Budget Management**: Set monthly budget limits for bills, variable spending, and investments
- 📈 **Visualizations**: Interactive charts showing spending trends and category breakdowns
- 📧 **Email Reports**: Automated weekly budget reports sent via email
- 🔄 **Recurring Expenses**: Automatically generate recurring monthly expenses
- 📤 **Export**: Export expenses to CSV or Excel
- 🔍 **Search & Filter**: Quickly find expenses by category or search term
- 💡 **Insights**: Spending insights, projections, and budget alerts

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Alpine.js + Tailwind CSS
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Charts**: Chart.js
- **Email**: SendGrid API / Mailgun API / SMTP
- **Authentication**: Session-based with password hashing

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/budget-app.git
cd budget-app
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
# Authentication
SECRET_KEY=your-secret-key-here

# Email Configuration (for SendGrid)
EMAIL_SERVICE=sendgrid
SENDER_EMAIL=your-email@gmail.com
EMAIL_API_KEY=your-sendgrid-api-key

# Optional: For weekly email scheduler
RECIPIENT_EMAIL=your-email@gmail.com
```

### 5. Run the Application

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

### 6. Create Your First User

1. Click "Register" on the login page
2. Create an account with username, email, and password
3. Start tracking your expenses!

## Email Setup

See [EMAIL_SETUP.md](EMAIL_SETUP.md) for detailed email configuration instructions.

## Weekly Email Scheduler

To set up automated weekly emails:

1. Add `RECIPIENT_EMAIL` to your `.env` file
2. Run the scheduler:
   ```bash
   python email_scheduler.py
   ```

See [SCHEDULER_SETUP.md](SCHEDULER_SETUP.md) for more details.

## Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for deployment instructions to:
- Render
- Railway
- Fly.io
- Other platforms

## Project Structure

```
budget-app/
├── app.py                 # Main Flask application
├── email_service.py       # Email sending service
├── email_scheduler.py     # Weekly email scheduler
├── requirements.txt       # Python dependencies
├── Procfile              # For deployment (Heroku/Render)
├── templates/
│   ├── index.html        # Main application UI
│   ├── login.html        # Login page
│   └── register.html     # Registration page
├── instance/
│   └── expenses.db       # SQLite database (created automatically)
└── .env                  # Environment variables (not in git)
```

## Features in Detail

### Expense Categories
- Groceries, Fast Food, Restaurant, Coffee
- Transportation, Shopping, Entertainment
- Healthcare, Education, Travel
- Personal Care, Pet
- Subscription, Bills, Loans
- Payment, Income, Investment

### Subcategories
- Add explicit subcategories (e.g., "Veggies", "Meat" for Groceries)
- Or use descriptions automatically as subcategories
- Subscriptions automatically grouped by service name

### Budget Tracking
- Fixed Bills + Loans budget
- Variable Spending budget
- Investment target range
- Visual progress indicators
- Budget alerts and warnings

### Data Export
- Export to CSV
- Export to Excel with formatting
- Filter by month/year

## Contributing

Feel free to submit issues or pull requests!

## License

MIT License
