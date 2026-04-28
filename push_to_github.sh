#!/bin/bash

# Daily Reflection Tree - GitHub Push Script
# This script will push all files to GitHub

echo "🚀 Pushing Daily Reflection Tree to GitHub..."
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
fi

# Add all files
echo "📝 Adding all files..."
git add .

# Show what will be committed
echo ""
echo "📋 Files to be committed:"
git status --short

# Commit
echo ""
read -p "Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Enhanced: Professional web UI, Docker support, and deployment guides"
fi

echo "💾 Committing changes..."
git commit -m "$commit_msg"

# Check if remote exists
if ! git remote | grep -q "origin"; then
    echo ""
    echo "🔗 No remote repository found."
    read -p "Enter your GitHub repository URL (e.g., https://github.com/username/reflection-tree.git): " repo_url
    git remote add origin "$repo_url"
fi

# Push to GitHub
echo ""
echo "⬆️  Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""
echo "🌐 Next steps:"
echo "1. Visit your GitHub repository"
echo "2. Add a description and topics"
echo "3. Enable GitHub Pages (Settings → Pages)"
echo "4. Deploy to Heroku/Railway/Render"
echo ""