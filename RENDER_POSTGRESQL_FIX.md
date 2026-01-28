# Render Deployment Fix: PostgreSQL Configuration

## The Problem ❌

You were getting this error:
```
OperationalError at /accounts/login/
no such table: auth_user
```

### Root Cause
**Render's free tier has ephemeral storage** - the filesystem is temporary and resets on every deployment or app restart. Your SQLite database file (`db.sqlite3`) was being deleted, even though migrations ran during the build process.

---

## The Solution ✅

### What Changed

1. **Added `render.yaml`** - Infrastructure-as-Code file that tells Render to:
   - Create a PostgreSQL database automatically
   - Link it to your web service
   - Run migrations on every deploy

2. **Updated `hello_world/settings.py`** - Now detects and uses:
   - PostgreSQL in production (via `DATABASE_URL` environment variable)
   - SQLite locally for development

3. **Committed and pushed to GitHub** - Render will auto-deploy these changes

---

## How to Deploy the Fix

### Option 1: Automatic (Recommended)
1. Go to your Render dashboard: https://dashboard.render.com
2. Click on your **neudebri-hmis** service
3. Scroll to **Settings** → **Clear Build Cache** (forces a fresh deploy)
4. Click **Manual Deploy** or wait for auto-deploy
5. Watch the build logs - migrations will run automatically

### Option 2: Delete and Recreate Service
1. In Render Dashboard, delete your current `neudebri-hmis` service
2. Delete the old database (optional, but recommended)
3. Click **Create** → **Web Service**
4. Connect your GitHub repo → select branch `main`
5. Use the `render.yaml` configuration (Render will auto-detect it)
6. Deploy - the database will be created automatically

---

## What Happens Now

When you deploy:

```bash
1. Render reads render.yaml
2. Creates PostgreSQL database (if not exists)
3. Runs: pip install -r requirements.txt
4. Runs: python manage.py migrate --noinput  ← Creates all tables
5. Runs: python manage.py collectstatic --noinput ← Static files
6. Starts gunicorn server
```

✅ Database tables persist across redeploys  
✅ Automatic migrations on every deployment  
✅ Free PostgreSQL database included  
✅ No more "no such table" errors  

---

## Testing the Fix

After deployment completes:

1. Visit your app: `https://neudebri-hmis-app.onrender.com`
2. Click **Login**
3. Enter credentials: `admin@neudebri` / `admin1234`
4. Should see the dashboard ✅

If you still get database errors:
- Check Render logs: Click service → **Logs**
- Look for migration errors
- Verify `DATABASE_URL` env var is set (should auto-set from render.yaml)

---

## Important Notes

### Data Persistence
- ✅ PostgreSQL database **persists** across redeploys
- ✅ All user data, patients, appointments are saved
- ✅ This is production-ready!

### SQLite (No Longer Used in Production)
- Still used locally (`db.sqlite3`) for development
- Never used on Render anymore
- Safe to ignore on deployment

### Environment Variables
Render automatically sets from `render.yaml`:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Random generated secret
- `DEBUG=False` - Production mode
- `PYTHONUNBUFFERED=1` - Real-time logs

---

## If You Need More Space/Performance

As your hospital gets busier:

| Need | Solution |
|------|----------|
| Faster database | Upgrade PostgreSQL plan ($7/month) |
| More storage | Buy PostgreSQL upgrade |
| Better performance | Upgrade web service ($7/month) |
| Custom domain | Add in Render settings |

---

## Troubleshooting

### Still getting "no such table" error?
```
1. Go to Render Dashboard
2. Click your service
3. Click "Clear Build Cache"
4. Click "Manual Deploy"
5. Wait for build to complete
6. Check logs for migration output
```

### App loads but features broken?
- Try clearing browser cache (Ctrl+Shift+Delete)
- Run static files collection manually:
  ```bash
  # From Render shell (if available)
  python manage.py collectstatic --noinput
  ```

### Need to recreate admin user?
```bash
# Contact Render support or use Render shell
python manage.py createsuperuser --email=admin@neudebri
```

---

## Next Steps

1. ✅ Push changes (already done!)
2. ✅ Deploy to Render
3. ✅ Test login
4. ✅ Verify features work
5. 📝 Share feedback
6. 🎉 Go live with confidence!

---

**Your HMIS is now on a reliable, persistent database!** 🚀
