@echo off
REM Daily Reflection Tree - GitHub Push Script (Windows)

echo 🚀 Pushing Daily Reflection Tree to GitHub...
echo.

REM Check if git is initialized
if not exist ".git" (
    echo 📦 Initializing Git repository...
    git init
)

REM Add all files
echo 📝 Adding all files...
git add .

REM Show what will be committed
echo.
echo 📋 Files to be committed:
git status --short

REM Commit
echo.
set /p commit_msg="Enter commit message (or press Enter for default): "
if "%commit_msg%"=="" set commit_msg=Enhanced: Professional web UI, Docker support, and deployment guides

echo 💾 Committing changes...
git commit -m "%commit_msg%"

REM Check if remote exists
git remote | findstr "origin" >nul
if errorlevel 1 (
    echo.
    echo 🔗 No remote repository found.
    set /p repo_url="Enter your GitHub repository URL: "
    git remote add origin %repo_url%
)

REM Push to GitHub
echo.
echo ⬆️  Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo ✅ Successfully pushed to GitHub!
echo.
echo 🌐 Next steps:
echo 1. Visit your GitHub repository
echo 2. Add a description and topics
echo 3. Enable GitHub Pages (Settings → Pages)
echo 4. Deploy to Heroku/Railway/Render
echo.
pause