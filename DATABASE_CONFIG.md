# Database Configuration Summary

## Current Setup

### Development (Local)
- **Database**: SQLite (`db.sqlite3`)
- **File**: `/workspaces/codespaces-django/db.sqlite3`
- **Usage**: Testing, development, migrations

### Production (Render)
- **Database**: PostgreSQL 15
- **Configuration**: Defined in `render.yaml`
- **Persistence**: ✅ Permanent (survives redeploys)
- **Connection**: Via `DATABASE_URL` environment variable

---

## Configuration Files

### 1. render.yaml (NEW)
Tells Render how to deploy:
- Creates PostgreSQL database automatically
- Sets environment variables
- Runs migrations on deploy
- **Location**: `/workspaces/codespaces-django/render.yaml`

### 2. hello_world/settings.py
Django configuration:
- Reads `DATABASE_URL` from Render
- Falls back to SQLite if not set
- **Key Change**: Now supports both databases

### 3. requirements.txt
Python dependencies:
- ✅ `psycopg2-binary` - PostgreSQL driver (already included)
- ✅ `dj-database-url` - Parse DATABASE_URL (already included)

---

## How It Works Now

```
┌─────────────────────────────────────────┐
│   Your Django App                       │
└────────────┬────────────────────────────┘
             │
      ┌──────▼────────┐
      │  Check for    │
      │ DATABASE_URL  │
      │  env var      │
      └──────┬────────┘
             │
         ____|____
        /         \
       /           \
   [SET]         [NOT SET]
     │               │
     ▼               ▼
PostgreSQL       SQLite
(Render)       (Local Dev)
```

---

## Migration Commands

### Automatic (Render)
```yaml
buildCommand: python manage.py migrate --noinput
```
- Runs on every deploy
- Creates/updates database tables
- Uses `--noinput` (no prompts on production)

### Manual (Local Development)
```bash
python manage.py makemigrations    # Create migration files
python manage.py migrate           # Apply migrations
```

---

## Database Connection Details

### PostgreSQL on Render (Automatic)
```
URL: postgresql://user:password@host:5432/database
Provided by: Render (via DATABASE_URL)
You don't need to configure it manually!
```

### SQLite Locally
```
FILE: /workspaces/codespaces-django/db.sqlite3
Created automatically on first run
```

---

## Common Commands

### Check which database is being used
```bash
python manage.py dbshell
```
- Will show PostgreSQL prompt on Render
- Will show SQLite prompt locally

### Create a superuser
```bash
# Locally
python manage.py createsuperuser

# On Render (in logs after deploy)
python manage.py createsuperuser --email admin@neudebri
```

### Check migrations status
```bash
python manage.py showmigrations
```

---

## Environment Variables

### Set by Render (from render.yaml)
- `DATABASE_URL=postgresql://...` - PostgreSQL connection
- `SECRET_KEY=xxx` - Generated randomly
- `DEBUG=False` - Production mode
- `PYTHONUNBUFFERED=1` - Real-time logging
- `ALLOWED_HOSTS=*.onrender.com` - Accept Render domains

### Optional (if you need to change)
- Go to Render Dashboard → Your Service → Environment
- Modify and redeploy

---

## Troubleshooting Database Issues

### Error: "no such table: auth_user"
✅ **FIXED** - Now uses persistent PostgreSQL

### Error: "could not connect to server"
- Wait 1-2 minutes for PostgreSQL to start
- Check DATABASE_URL is set in Render dashboard
- Try "Clear Build Cache" → "Manual Deploy"

### App starts but no data
- Migrations may not have run
- Check Render logs for migration output
- May need to recreate superuser

---

## File Locations

```
/workspaces/codespaces-django/
├── render.yaml                    ← Render config (NEW)
├── hello_world/
│   └── settings.py               ← Updated for PostgreSQL
├── requirements.txt              ← Already has psycopg2, dj-database-url
├── db.sqlite3                    ← Local development only
└── manage.py
```

---

## Next Deploy Steps

1. Changes already committed to GitHub ✅
2. Go to Render Dashboard
3. Click your service
4. Click "Clear Build Cache"
5. Click "Manual Deploy"
6. Watch logs until complete
7. Test login

That's it! PostgreSQL will handle everything else. 🎉
