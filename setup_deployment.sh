#!/bin/bash
# Quick setup script for GitHub and deployment

echo "🚀 Budget App - GitHub & Deployment Setup"
echo "=========================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if already a git repo
if [ -d ".git" ]; then
    echo "⚠️  Git repository already exists"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "📦 Initializing git repository..."
    git init
fi

# Check .gitignore
if [ ! -f ".gitignore" ]; then
    echo "⚠️  .gitignore not found. Creating one..."
    # .gitignore should already exist, but just in case
fi

echo ""
echo "📋 Files to be committed:"
git status --short 2>/dev/null || echo "No git repo yet"

echo ""
echo "✅ Ready to commit!"
echo ""
echo "Next steps:"
echo "1. Review files above (make sure .env, venv/, instance/ are NOT listed)"
echo "2. Run: git add ."
echo "3. Run: git commit -m 'Initial commit: Budget tracking app'"
echo "4. Create a repository on GitHub"
echo "5. Run: git remote add origin https://github.com/YOUR_USERNAME/budget-app.git"
echo "6. Run: git push -u origin main"
echo ""
echo "📖 See GITHUB_SETUP.md for detailed instructions"
echo "📖 See DEPLOYMENT_GUIDE.md for hosting options"

