# Render.com Deployment Guide

## Files Created for Deployment

1. ✅ `build.sh` - Build script for Render
2. ✅ `runtime.txt` - Specifies Python 3.12.0 (compatible with psycopg2)
3. ✅ `requirements.txt` - Updated with psycopg2-binary 2.9.10 and psycopg 3.1.18
4. ✅ `.env` - Environment variables template

## Environment Variables to Set on Render

In your Render.com dashboard, add these environment variables:

```
DATABASE_URL=<provided by Render PostgreSQL>
SECRET_KEY=<generate a secure random key>
DEBUG=False
ALLOWED_HOSTS=<your-app-name>.onrender.com
```

## Deploy Steps

### 1. Commit and Push
```bash
git add .
git commit -m "Add Render deployment configuration"
git push
```

### 2. Create Web Service on Render
1. Go to https://render.com/
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: Your app name
   - **Environment**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn caregiving_project.wsgi:application`
   - **Plan**: Free

### 3. Add PostgreSQL Database
1. In Render dashboard, click "New +" → "PostgreSQL"
2. Create database (Free tier available)
3. Copy the "Internal Database URL"
4. In your Web Service, go to "Environment"
5. Add environment variable: `DATABASE_URL` = <internal database url>

### 4. Set Other Environment Variables
Add these in the "Environment" section:

```
SECRET_KEY=your-secret-key-here-generate-new-one
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
```

To generate a SECRET_KEY:
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Deploy
Click "Manual Deploy" → "Deploy latest commit"

## Troubleshooting

### If you see "Error loading psycopg2"
- Check that `runtime.txt` specifies Python 3.12.0
- Check that both `psycopg2-binary` and `psycopg` are in requirements.txt

### If static files don't load
- Ensure `whitenoise` is in requirements.txt
- Check that `build.sh` runs `collectstatic`

### If database connection fails
- Verify `DATABASE_URL` is set in Render environment variables
- Make sure you're using the Internal Database URL (not External)

### View Logs
In Render dashboard → Your service → "Logs" tab

## Local Testing Before Deploy

```bash
# Test with production-like settings
export DEBUG=False
export SECRET_KEY=test-key
export DATABASE_URL=postgresql://user:password@localhost:5432/caregiving_db

python3 manage.py check --deploy
```

## Post-Deployment

Your app will be available at:
`https://your-app-name.onrender.com/`

### Create Superuser (if needed)
In Render dashboard → "Shell" tab:
```bash
python manage.py createsuperuser
```

## Important Notes

- Free tier sleeps after 15 minutes of inactivity
- First request after sleep may take 30-60 seconds
- Database has 90-day retention on free tier
- Static files are served via WhiteNoise (no separate storage needed)

## Support

- Render Docs: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/
