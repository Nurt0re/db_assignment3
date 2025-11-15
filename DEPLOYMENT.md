# Deployment Guide for Render.com

This guide will help you deploy your Caregiving Management System to Render.com.

## Prerequisites

1. A GitHub account
2. A Render.com account (free tier is fine)
3. Your application code pushed to a GitHub repository

## Step 1: Prepare Your Code

Your code is already prepared with the necessary files:
- `build.sh` - Build script that runs during deployment
- `render.yaml` - Infrastructure as code configuration
- `requirements.txt` - Python dependencies including production packages
- `.gitignore` - Ensures sensitive files aren't committed

## Step 2: Push to GitHub

1. Initialize git repository (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Caregiving Management System"
   ```

2. Create a new repository on GitHub (don't initialize with README)

3. Push your code:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

## Step 3: Create PostgreSQL Database on Render

1. Go to https://dashboard.render.com/
2. Click "New +" and select "PostgreSQL"
3. Configure:
   - **Name**: caregiving-db (or your choice)
   - **Database**: caregiving_db
   - **User**: postgres (or your choice)
   - **Region**: Choose closest to you
   - **PostgreSQL Version**: 15 or latest
   - **Plan**: Free (or your choice)
4. Click "Create Database"
5. Wait for the database to be created (takes ~1-2 minutes)
6. **IMPORTANT**: Copy the "Internal Database URL" - you'll need this

## Step 4: Deploy Web Service

1. From Render Dashboard, click "New +" and select "Web Service"
2. Connect your GitHub repository
3. Configure the web service:

   **Basic Settings**:
   - **Name**: caregiving-app (or your choice)
   - **Region**: Same as your database
   - **Branch**: main
   - **Root Directory**: Leave empty
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn caregiving_project.wsgi:application`

4. Click "Advanced" to add environment variables:

   **Environment Variables** (click "Add Environment Variable" for each):
   
   ```
   DEBUG=False
   
   SECRET_KEY=your-super-secret-key-change-this-to-something-random
   
   DATABASE_URL=<paste the Internal Database URL from Step 3>
   
   ALLOWED_HOSTS=.onrender.com
   
   PYTHON_VERSION=3.12.0
   ```

   **Generate a strong SECRET_KEY**:
   ```python
   # Run this locally to generate a secret key:
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. Click "Create Web Service"

## Step 5: Wait for Deployment

1. Render will:
   - Clone your repository
   - Run `build.sh` which installs dependencies, collects static files, and runs migrations
   - Start your application with gunicorn

2. Monitor the logs - you should see:
   ```
   ==> Build successful 🎉
   ==> Deploying...
   ==> Your service is live 🎉
   ```

3. Your app will be available at: `https://caregiving-app.onrender.com` (or whatever name you chose)

## Step 6: Initialize Database

Your database schema should already be created by the migrations in `build.sh`. Now you need to add initial data:

1. From Render Dashboard, go to your web service
2. Click "Shell" tab
3. Run the insert data SQL:
   ```bash
   python manage.py dbshell < queries/insert_data.sql
   ```

   Or connect directly to your database and run the SQL manually.

## Step 7: Test Your Application

Visit your application URL and test:
1. Homepage loads
2. User list shows data
3. CRUD operations work (create, edit, delete)
4. All navigation links work

## Troubleshooting

### Build Fails

Check the build logs for errors. Common issues:
- Missing dependencies in `requirements.txt`
- Python version mismatch
- Database connection issues

### App Crashes After Deploy

1. Check the logs in Render Dashboard
2. Common issues:
   - Wrong `DATABASE_URL`
   - Missing environment variables
   - Incorrect `SECRET_KEY`

### Static Files Not Loading

1. Ensure `build.sh` runs `collectstatic`:
   ```bash
   python manage.py collectstatic --no-input
   ```
2. Check `STATIC_ROOT` is set in settings.py
3. Verify WhiteNoise is in `MIDDLEWARE`

### Database Connection Errors

1. Verify `DATABASE_URL` is set correctly in environment variables
2. Make sure you're using the **Internal Database URL** (not external)
3. Check database is in the same region as your web service

## Updating Your Application

When you make changes:

1. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your commit message"
   git push
   ```

2. Render will automatically detect the push and redeploy

## Free Tier Limitations

Render's free tier has some limitations:
- Services spin down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- 750 hours/month of running time
- Database limited to 1GB storage

For production use, consider upgrading to a paid plan.

## Support

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com/

## Security Checklist

Before going to production:
- ✅ `DEBUG=False` in production
- ✅ Strong `SECRET_KEY` (not in version control)
- ✅ `ALLOWED_HOSTS` properly configured
- ✅ Database credentials secure (use Render's DATABASE_URL)
- ✅ `.env` file in `.gitignore`
- ✅ HTTPS enabled (Render does this automatically)

---

Your application is now deployed! 🚀
