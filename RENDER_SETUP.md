# Quick Render.com Setup Guide

## What's Been Configured

Your application is now ready for deployment to Render.com. Here's what was set up:

### 1. Production Dependencies Added
- `dj-database-url==2.1.0` - Parses DATABASE_URL for Django
- `whitenoise==6.6.0` - Serves static files in production

### 2. Settings Updated (`caregiving_project/settings.py`)
- ✅ **ALLOWED_HOSTS**: Configured from environment variable, includes `.onrender.com`
- ✅ **DEBUG**: Reads from environment, defaults to False in production
- ✅ **DATABASES**: Uses `DATABASE_URL` environment variable in production
- ✅ **STATIC_ROOT**: Set to `staticfiles/` for collectstatic
- ✅ **WhiteNoise**: Middleware added for static file serving
- ✅ **STORAGES**: Configured for compressed static files

### 3. Database Connection (`database.py`)
- ✅ Updated to use `DATABASE_URL` environment variable when available
- ✅ Falls back to individual env vars for local development

### 4. Deployment Files Created

**`build.sh`** - Runs during deployment:
```bash
#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

**`render.yaml`** - Infrastructure as code:
- Defines web service with correct WSGI path
- Sets up PostgreSQL database
- Configures environment variables

**`.gitignore`** - Prevents committing:
- Environment files (`.env`)
- Python cache files
- Static files directory
- Database backups

## Deployment Checklist

Before deploying, make sure you have:

- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Render.com account created
- [ ] Generated a strong SECRET_KEY

## Quick Deploy Steps

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Ready for Render deployment"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Create Database on Render
1. Go to https://dashboard.render.com/
2. New + → PostgreSQL
3. Name: `caregiving-db`
4. Create Database
5. **Copy the Internal Database URL**

### 3. Create Web Service
1. New + → Web Service
2. Connect your GitHub repo
3. Configure:
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn caregiving_project.wsgi:application`
   
4. Add Environment Variables:
   ```
   DEBUG=False
   SECRET_KEY=<generate-a-random-secret-key>
   DATABASE_URL=<paste-internal-database-url>
   ALLOWED_HOSTS=.onrender.com
   ```

5. Deploy!

### 4. Load Initial Data
Once deployed, connect to your database and run:
```sql
-- Run queries/insert_data.sql
```

## Generate SECRET_KEY
Run locally:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Testing Deployment

After deployment, your app will be at:
```
https://YOUR-SERVICE-NAME.onrender.com
```

Test these pages:
- `/` - Homepage
- `/users/` - User list
- `/caregivers/` - Caregiver list
- `/jobs/` - Job list

## Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Verify all dependencies are in `requirements.txt`
- Ensure `build.sh` is executable

### App Doesn't Start
- Check `DATABASE_URL` is set correctly
- Verify `SECRET_KEY` is set
- Check logs for errors

### Static Files Missing
- Ensure `collectstatic` runs in `build.sh`
- Verify WhiteNoise is in MIDDLEWARE
- Check STATIC_ROOT is set

## Environment Variables Explained

| Variable | Purpose | Example |
|----------|---------|---------|
| `DEBUG` | Enable/disable debug mode | `False` |
| `SECRET_KEY` | Django secret for security | Random 50-char string |
| `DATABASE_URL` | PostgreSQL connection | From Render PostgreSQL |
| `ALLOWED_HOSTS` | Allowed domain names | `.onrender.com` |

## File Structure
```
db_assignment3/
├── build.sh                 # Render build script
├── render.yaml              # Render infrastructure config
├── requirements.txt         # Python dependencies (updated)
├── .gitignore              # Git ignore file
├── database.py             # SQLAlchemy config (updated)
├── caregiving_project/
│   └── settings.py         # Django settings (updated)
├── queries/
│   └── insert_data.sql     # Initial data to load
└── DEPLOYMENT.md           # Full deployment guide
```

## Next Steps After Deployment

1. **Load data**: Run `insert_data.sql` on your Render database
2. **Test CRUD operations**: Create, read, update, delete records
3. **Monitor**: Check Render logs for any errors
4. **Secure**: Review security settings

## Support

- Full Guide: See `DEPLOYMENT.md`
- Render Docs: https://render.com/docs/deploy-django
- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/

---

**Your app is production-ready! 🚀**

Just push to GitHub and deploy on Render following the steps above.
