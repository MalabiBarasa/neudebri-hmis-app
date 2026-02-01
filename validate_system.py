#!/usr/bin/env python
"""
Comprehensive system validation script for Sanitas HMIS
Run this before pushing to production
"""
import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_world.settings')
django.setup()

from django.conf import settings
from django.db import connection
from django.urls import reverse
from django.apps import apps
from hello_world.core.models import *

def check_database():
    """Check database connectivity and key tables"""
    print("🔍 Checking Database...")
    try:
        with connection.cursor() as cursor:
            # Check key tables exist
            tables = ['core_userprofile', 'core_patient', 'core_woundcare', 'core_notification']
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   ✅ {table}: {count} records")
        return True
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False

def check_models():
    """Check that all models can be imported and instantiated"""
    print("🔍 Checking Models...")
    models_to_check = [
        UserProfile, Patient, WoundCare, Appointment, Prescription,
        Notification, WoundBilling, PaymentTransaction
    ]
    for model in models_to_check:
        try:
            # Try to get model metadata
            meta = model._meta
            print(f"   ✅ {model.__name__}: {meta.db_table}")
        except Exception as e:
            print(f"   ❌ {model.__name__} error: {e}")
            return False
    return True

def check_urls():
    """Check that key URLs can be reversed"""
    print("🔍 Checking URLs...")
    urls_to_check = [
        'index', 'dashboard', 'patient_list', 'global_search',
        'advanced_search', 'advanced_analytics', 'audit_trail'
    ]
    for url_name in urls_to_check:
        try:
            url = reverse(url_name)
            print(f"   ✅ {url_name}: {url}")
        except Exception as e:
            print(f"   ❌ {url_name} error: {e}")
            return False
    return True

def check_settings():
    """Check critical settings"""
    print("🔍 Checking Settings...")
    checks = [
        ('DEBUG', getattr(settings, 'DEBUG', None)),
        ('SECRET_KEY', bool(getattr(settings, 'SECRET_KEY', ''))),
        ('DATABASES', len(getattr(settings, 'DATABASES', {}))),
        ('INSTALLED_APPS', len(getattr(settings, 'INSTALLED_APPS', []))),
        ('MIDDLEWARE', len(getattr(settings, 'MIDDLEWARE', []))),
    ]
    for name, value in checks:
        if value:
            print(f"   ✅ {name}: {value}")
        else:
            print(f"   ❌ {name}: Missing or invalid")
            return False
    return True

def check_apps():
    """Check that all apps are properly configured"""
    print("🔍 Checking Apps...")
    required_apps = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'rest_framework',
        'channels',
        'guardian',
        'auditlog',
        'core'
    ]
    for app_name in required_apps:
        try:
            app_config = apps.get_app_config(app_name.split('.')[-1])
            print(f"   ✅ {app_name}")
        except Exception as e:
            print(f"   ❌ {app_name} error: {e}")
            return False
    return True

def check_templates():
    """Check that key templates exist"""
    print("🔍 Checking Templates...")
    template_dir = Path(settings.BASE_DIR) / 'hello_world' / 'templates'
    key_templates = [
        'index.html', 'dashboard.html', 'global_search.html',
        'advanced_search.html', 'advanced_analytics.html'
    ]
    for template in key_templates:
        template_path = template_dir / template
        if template_path.exists():
            print(f"   ✅ {template}")
        else:
            print(f"   ❌ {template}: Missing")
            return False
    return True

def main():
    """Run all validation checks"""
    print("🚀 Sanitas HMIS - Pre-Push Validation")
    print("=" * 50)

    checks = [
        ("Settings Configuration", check_settings),
        ("Django Apps", check_apps),
        ("Database Connectivity", check_database),
        ("Model Definitions", check_models),
        ("URL Configuration", check_urls),
        ("Template Files", check_templates),
    ]

    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        result = check_func()
        results.append(result)
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}")

    print("\n" + "=" * 50)
    if all(results):
        print("🎉 ALL CHECKS PASSED - Ready for production!")
        print("\nNext steps:")
        print("1. Run: git add .")
        print("2. Run: git commit -m 'Phase 2 enhancements complete'")
        print("3. Run: git push origin main")
        return 0
    else:
        print("❌ SOME CHECKS FAILED - Fix issues before pushing")
        return 1

if __name__ == '__main__':
    sys.exit(main())