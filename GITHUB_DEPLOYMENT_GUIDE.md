# GitHub Push & Deployment Instructions for Neudebri HMIS

## ✅ Current Status
- ✅ Project: Fully functional Django HMIS application
- ✅ Database: SQLite with 9 users, 5 patients, 6 appointments, 8 departments
- ✅ Code: Committed to local Git repository
- ⏳ Next: Push to GitHub and deploy

---

## Step 1: Create GitHub Repository

1. **Go to GitHub**: https://github.com/new
2. **Fill in details**:
   - Repository name: `neudebri-hmis`
   - Description: `Hospital Management Information System (HMIS) for Neudebri Woundcare Hospital`
   - Public/Private: Choose based on preference
   - ❌ **DO NOT** check "Initialize this repository with..."
   - ✅ Click "Create repository"

3. **You will see a page with:**
   ```
   push an existing repository from the command line
   ```

---

## Step 2: Push to GitHub

Run these commands in your terminal:

```bash
# Navigate to project directory
cd /workspaces/codespaces-django

# Add your GitHub repository (replace YOUR_USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/neudebri-hmis.git

# Rename branch to main (if not already)
git branch -M main

# Push all commits to GitHub
git push -u origin main
```

**Example:**
```bash
git remote add origin https://github.com/MalabiBarasa/neudebri-hmis.git
git push -u origin main
```

✅ **After this, your code will be on GitHub!**

---

## Step 3: Choose Your Deployment Option

### 🎯 RECOMMENDED: Start with Option A or D (Easiest & Free)

---

## Option A: Heroku (Easiest for Beginners)

**Pros**: Free tier available, one-command deploy, automatic SSL
**Cons**: Free tier limits (dyno sleeps after 30 min), slower cold starts
**Cost**: Free tier or $7+/month

### A1. Create Heroku Account
1. Go to https://www.heroku.com
2. Sign up with email
3. Verify email
4. Create account

### A2. Install Heroku CLI
**macOS:**
```bash
brew tap heroku/brew && brew install heroku
```

**Windows/Linux:**
Visit https://devcenter.heroku.com/articles/heroku-cli

### A3. Login to Heroku
```bash
heroku login
# Opens browser for authentication
```

### A4. Create Heroku App
```bash
cd /workspaces/codespaces-django

# Create app (replace neudebri-hmis with your desired app name)
heroku create neudebri-hmis

# If name is taken, try:
heroku create neudebri-hmis-hospital
```

### A5. Set Environment Variables
```bash
# Generate a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set it in Heroku (replace YOUR_SECRET_KEY with the generated key)
heroku config:set SECRET_KEY="YOUR_SECRET_KEY"
heroku config:set DEBUG=False
```

### A6. Deploy
```bash
git push heroku main
```

**The app will deploy automatically!**

### A7. Run Migrations
```bash
heroku run python manage.py migrate
```

### A8. Create Admin User
```bash
heroku run python manage.py createsuperuser
```

### A9. Access Your App
```bash
heroku open
# Or visit: https://neudebri-hmis.herokuapp.com
```

**Login with admin credentials you just created**

---

## Option B: Render.com (Modern, Free Tier Available)

**Pros**: GitHub-native, free tier, automatic deploys on push
**Cons**: Cold starts on free tier
**Cost**: Free or $7+/month

### B1. Sign Up
1. Go to https://render.com
2. Click "Get started for free"
3. Sign in with GitHub

### B2. Connect Repository
1. Click "New +" → "Web Service"
2. Select your GitHub repository: `neudebri-hmis`
3. Grant access to your repositories

### B3. Configure Service
- **Name**: `neudebri-hmis`
- **Runtime**: Python 3
- **Build Command**: 
  ```
  pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
  ```
- **Start Command**: 
  ```
  gunicorn hello_world.wsgi:application
  ```

### B4. Add Environment Variables
- **SECRET_KEY**: Generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- **DEBUG**: `False`
- **ALLOWED_HOSTS**: Your Render domain (e.g., `neudebri-hmis.onrender.com`)

### B5. Deploy
Click "Create Web Service"

**Automatic deployment happens on every `git push`!**

---

## Option C: PythonAnywhere (Pure Python Hosting)

**Pros**: Python-specific, easy dashboard, free tier
**Cons**: Limited free tier, less flexible
**Cost**: Free or $5+/month

### C1. Sign Up
1. Go to https://www.pythonanywhere.com
2. Create account
3. Create new web app → Django → Python 3.12

### C2. Configure
1. Go to "Web" tab
2. Set WSGI configuration file path
3. Set Python virtual environment
4. Configure static files path

### C3. Clone Repository
```bash
# In PythonAnywhere bash console
git clone https://github.com/YOUR_USERNAME/neudebri-hmis.git
cd neudebri-hmis
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

### C4. Reload
Click "Reload" in web app settings

---

## Option D: DigitalOcean App Platform (Managed & Scalable)

**Pros**: Managed PostgreSQL, GitHub integration, professional infrastructure
**Cons**: $12/month minimum
**Cost**: $12+/month

### D1. Create DigitalOcean Account
1. Go to https://www.digitalocean.com
2. Sign up with GitHub (easier)

### D2. Create PostgreSQL Database
1. Click "Create" → "Databases"
2. Choose PostgreSQL 15
3. Select basic plan
4. Note credentials

### D3. Create App Platform Service
1. Click "Create" → "Apps"
2. Connect GitHub repository
3. Select `neudebri-hmis`
4. Choose branch: `main`

### D4. Configure
- **Build Command**: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
- **Run Command**: `gunicorn hello_world.wsgi:application`

### D5. Set Environment Variables
```
DATABASE_URL=postgresql://...  (from your PostgreSQL database)
SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.ondigitalocean.app
```

### D6. Deploy
Click "Deploy"

---

## 🎯 Quick Comparison

| Feature | Heroku | Render | PythonAnywhere | DigitalOcean |
|---------|--------|--------|---|---|
| **Free Tier** | ✅ (limited) | ✅ | ✅ | ❌ |
| **Setup Time** | 10 min | 10 min | 15 min | 20 min |
| **GitHub Deploy** | ✅ | ✅✅ | ✅ | ✅ |
| **Database** | PostgreSQL | PostgreSQL | MySQL/PostgreSQL | PostgreSQL |
| **Cost (Month)** | Free/$7 | Free/$7 | Free/$5 | $12+ |
| **Recommended** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

---

## 🐳 Option E: Docker Local Testing (Before Production)

Test your deployment locally with Docker:

```bash
cd /workspaces/codespaces-django

# Build image
docker build -t neudebri-hmis .

# Run container
docker run -p 8000:8000 neudebri-hmis

# Or use docker-compose
docker-compose up
```

Access at http://localhost:8000

---

## ⚠️ Production Security Checklist

Before deploying to production:

- [ ] Update `SECRET_KEY` to a secure random value
- [ ] Set `DEBUG=False` in production
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up PostgreSQL (not SQLite) for production
- [ ] Configure email backend for notifications
- [ ] Set up HTTPS/SSL certificate
- [ ] Enable CSRF protection
- [ ] Configure CORS if needed
- [ ] Set up error tracking (Sentry)
- [ ] Configure automated backups
- [ ] Enable database connection pooling
- [ ] Set up monitoring and alerts

---

## 📝 Post-Deployment

### Test Your Deployment
1. Visit your deployed app URL
2. Try logging in with admin credentials
3. Test patient creation
4. Test appointments
5. Check lab and pharmacy modules

### Set Up Custom Domain (Optional)
Each platform has domain configuration:
- **Heroku**: `heroku domains:add yourdomain.com`
- **Render**: Settings → Custom Domain
- **DigitalOcean**: App settings → Domains

### Monitor Your App
- Check logs regularly
- Set up uptime monitoring (UptimeRobot)
- Monitor database performance
- Track error rates (Sentry)

---

## 🆘 Troubleshooting

**App won't deploy?**
- Check logs: `heroku logs --tail`
- Verify requirements.txt has gunicorn
- Check that migrations run successfully

**Database errors?**
- Ensure migrations ran: `heroku run python manage.py migrate`
- Create superuser: `heroku run python manage.py createsuperuser`

**Static files not loading?**
- Run collectstatic: `heroku run python manage.py collectstatic --noinput`
- Check whitenoise is in MIDDLEWARE

**Port errors?**
- Ensure app listens on dynamic port: `0.0.0.0:$PORT`

---

## 🎉 You're Done!

Once deployed:
1. Share the live URL with stakeholders
2. Gather feedback
3. Plan Phase 2 features
4. Set up monitoring
5. Configure automated backups

**Your HMIS is now live!** 🚀
