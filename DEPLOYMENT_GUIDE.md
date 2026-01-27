# Neudebri HMIS - Deployment Guide

## Project Overview
- **Name**: Neudebri Woundcare Hospital HMIS
- **Type**: Django 5.2.2 Web Application
- **Database**: SQLite (dev) → PostgreSQL (prod)
- **Auth**: Django Allauth with role-based access
- **Frontend**: Bootstrap 5 + Font Awesome 6

---

## Option 1: GitHub Push (Required First Step)

### 1.1 Create GitHub Repository
```bash
# Navigate to GitHub and create new repository
# - Go to https://github.com/new
# - Repository name: neudebri-hmis
# - Description: Hospital Management Information System for Neudebri Woundcare Hospital
# - Public/Private: Choose based on preference
# - DO NOT initialize with README (we have one)
```

### 1.2 Add Remote and Push
```bash
cd /workspaces/codespaces-django

# Add your GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/neudebri-hmis.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your GitHub username**

---

## Option 2: Deployment Recommendations

### 🏢 Option A: Heroku (Easiest for Beginners)
**Cost**: Free tier available, $7+/month for production
**Setup Time**: 10-15 minutes
**Best For**: Quick deployment, free tier exploration

**Steps:**
1. Sign up at https://www.heroku.com
2. Install Heroku CLI: `brew install heroku`
3. Create `Procfile`:
   ```
   web: gunicorn hello_world.wsgi
   ```
4. Create `runtime.txt`:
   ```
   python-3.12.1
   ```
5. Update `requirements.txt` with production packages:
   ```
   gunicorn>=21.0.0
   whitenoise>=6.6.0
   python-decouple>=3.8
   psycopg2-binary>=2.9.0
   ```
6. Deploy:
   ```bash
   heroku login
   heroku create neudebri-hmis
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

---

### 🐳 Option B: Docker + AWS EC2 (Professional)
**Cost**: $5-30/month depending on instance size
**Setup Time**: 30-45 minutes
**Best For**: Production, scalability, full control

**Create `Dockerfile`:**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations and start server
CMD ["gunicorn", "hello_world.wsgi:application", "--bind", "0.0.0.0:8000"]
```

**Create `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=neudebri_hmis
      - POSTGRES_USER=hmis_user
      - POSTGRES_PASSWORD=secure_password_here

  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DEBUG=0
      - ALLOWED_HOSTS=localhost,127.0.0.1
      - DATABASE_URL=postgresql://hmis_user:secure_password_here@db:5432/neudebri_hmis

volumes:
  postgres_data:
```

**Deploy to AWS EC2:**
1. Launch Ubuntu 20.04 EC2 instance
2. SSH into server
3. Clone repository
4. Install Docker
5. Run `docker-compose up -d`
6. Configure domain via Route 53

---

### ☁️ Option C: PythonAnywhere (Simplest for Python)
**Cost**: Free tier available, $5+/month
**Setup Time**: 15-20 minutes
**Best For**: Pure Python hosting

**Steps:**
1. Sign up at https://www.pythonanywhere.com
2. Push code to GitHub
3. PythonAnywhere → New web app → Django
4. Configure virtual environment
5. Pull from GitHub
6. Configure settings.py with your domain
7. Reload web app

---

### 🚀 Option D: Render (Modern Alternative)
**Cost**: Free tier with limitations, $7+/month
**Setup Time**: 15-20 minutes
**Best For**: GitHub-native deployment

**Steps:**
1. Sign up at https://render.com
2. Connect GitHub repository
3. Create new Web Service
4. Set build command: `pip install -r requirements.txt && python manage.py migrate`
5. Set start command: `gunicorn hello_world.wsgi:application`
6. Add environment variables
7. Deploy automatically on push

---

### 💾 Option E: DigitalOcean App Platform
**Cost**: $12-30/month
**Setup Time**: 20-30 minutes
**Best For**: Managed PostgreSQL + app

**Steps:**
1. Create DigitalOcean account
2. Create PostgreSQL database
3. Create App Platform service from GitHub
4. Configure environment variables
5. Deploy

---

## Production Checklist

Before deploying to production:

```bash
# 1. Update settings.py for production
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')  # Use env variable

# 2. Update requirements.txt with production packages
pip freeze > requirements.txt

# 3. Create .env.example
DEBUG=False
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:5432/dbname

# 4. Collect static files
python manage.py collectstatic

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Test with gunicorn locally
gunicorn hello_world.wsgi:application --bind 0.0.0.0:8000
```

---

## Database Migration (SQLite → PostgreSQL)

For production deployment, migrate from SQLite to PostgreSQL:

```bash
# 1. Install PostgreSQL client
pip install psycopg2-binary

# 2. Backup current data (optional)
python manage.py dumpdata > backup.json

# 3. Update DATABASE settings to PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'neudebri_hmis',
        'USER': 'hmis_user',
        'PASSWORD': 'secure_password',
        'HOST': 'db.example.com',
        'PORT': '5432',
    }
}

# 4. Run migrations on new database
python manage.py migrate

# 5. Load backup data (if you want to restore)
python manage.py loaddata backup.json
```

---

## Recommended Deployment Path

**For Quick Launch (Week 1):**
1. Push to GitHub
2. Deploy to Heroku free tier
3. Test functionality
4. Invite stakeholders for feedback

**For Production (Week 2+):**
1. Set up PostgreSQL database
2. Update settings for security (SECRET_KEY, DEBUG=False, etc.)
3. Configure email backend for notifications
4. Set up SSL/TLS with domain
5. Deploy to Option B, D, or E (based on budget)
6. Set up monitoring and backups

---

## Quick Start Commands

```bash
# GitHub Push
git remote add origin https://github.com/YOUR_USERNAME/neudebri-hmis.git
git push -u origin main

# Heroku Deploy
heroku login
heroku create neudebri-hmis
git push heroku main

# Local Testing Before Deploy
python manage.py runserver 0.0.0.0:8000
# Test at http://localhost:8000
# Login: admin / admin123
```

---

## Support & Monitoring

Once deployed, set up:
- **Error Tracking**: Sentry (free tier available)
- **Uptime Monitoring**: UptimeRobot (free)
- **Logs**: CloudWatch, Papertrail, or service provider's logs
- **Backups**: Configure automated database backups

---

**Next Step**: Push to GitHub and choose your deployment option!
