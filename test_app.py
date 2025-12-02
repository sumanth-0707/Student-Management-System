#!/usr/bin/env python
"""
Quick test script to validate application startup and endpoints.
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 Testing Student Management System...")
print("-" * 60)

# Test 1: Import FastAPI app
print("\n✓ Test 1: Importing application modules...")
try:
    from app.main import app
    print("  ✅ FastAPI app imported successfully")
except Exception as e:
    print(f"  ❌ Failed to import app: {str(e)}")
    sys.exit(1)

# Test 2: Check routes
print("\n✓ Test 2: Validating routes...")
try:
    routes = app.routes
    print(f"  ✅ Found {len(routes)} total routes")
    
    # Check for web routes
    web_routes = [r.path for r in routes if hasattr(r, 'path') and r.path in ['/', '/login', '/dashboard', '/students']]
    print(f"  ✅ Web routes found: {web_routes}")
    
    # Check for API routes
    api_routes = [r.path for r in routes if hasattr(r, 'path') and r.path.startswith('/api/')]
    print(f"  ✅ API routes found: {len(api_routes)} routes")
except Exception as e:
    print(f"  ❌ Failed to check routes: {str(e)}")
    sys.exit(1)

# Test 3: Check database
print("\n✓ Test 3: Checking database configuration...")
try:
    from app.core.config import settings
    print(f"  ✅ Database URL configured: {settings.database_url[:50]}...")
except Exception as e:
    print(f"  ❌ Failed to load config: {str(e)}")
    sys.exit(1)

# Test 4: Check templates
print("\n✓ Test 4: Checking template files...")
try:
    from pathlib import Path
    template_dir = Path(__file__).parent / "app" / "templates"
    templates = list(template_dir.glob("*.html"))
    print(f"  ✅ Found {len(templates)} template files")
    for t in templates:
        print(f"     - {t.name}")
except Exception as e:
    print(f"  ❌ Failed to check templates: {str(e)}")
    sys.exit(1)

# Test 5: Check static files
print("\n✓ Test 5: Checking static files...")
try:
    static_dir = Path(__file__).parent / "app" / "static"
    js_files = list(static_dir.glob("js/*.js"))
    css_files = list(static_dir.glob("css/*.css"))
    print(f"  ✅ Found {len(js_files)} JavaScript files and {len(css_files)} CSS files")
except Exception as e:
    print(f"  ❌ Failed to check static files: {str(e)}")
    sys.exit(1)

# Test 6: Verify Jinja2 templates configuration
print("\n✓ Test 6: Checking Jinja2 templates configuration...")
try:
    from fastapi.templating import Jinja2Templates
    print(f"  ✅ Jinja2Templates available")
    
    # Check if templates are configured in app
    if hasattr(app.state, 'templates'):
        print(f"  ✅ Templates configured in app.state")
    else:
        print(f"  ⚠️  Templates not in app.state (will be set on startup)")
except Exception as e:
    print(f"  ❌ Failed to check templates config: {str(e)}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ All validation tests passed!")
print("=" * 60)
print("\nTo start the server, run:")
print("  python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000")
print("\nThen open http://127.0.0.1:8000 in your browser")
