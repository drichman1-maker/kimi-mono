"""
Pre-deployment verification script
Checks all components before deploying
"""

import sys
import os
from pathlib import Path

def check_file_exists(filepath, required=True):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else ("❌" if required else "⚠️")
    req_text = "(required)" if required else "(optional)"
    print(f"{status} {filepath} {req_text}")
    return exists or not required

def check_python_syntax(filepath):
    """Check Python file for syntax errors"""
    try:
        with open(filepath, 'r') as f:
            compile(f.read(), filepath, 'exec')
        return True
    except SyntaxError as e:
        print(f"   ❌ Syntax error in {filepath}: {e}")
        return False

def verify_structure():
    """Verify project structure"""
    print("\n📁 Checking project structure...")

    required_files = [
        "app/main.py",
        "app/models.py",
        "app/schemas.py",
        "app/database.py",
        "app/routers/products.py",
        "app/routers/alerts.py",
        "app/routers/retailers.py",
        "app/services/scraper_service.py",
        "scrapers/base.py",
        "scrapers/tier1_2_scrapers.py",
        "scrapers/mac_scraper.py",
        "scrapers/pokemon_scraper.py",
        "scrapers/runner.py",
        "requirements.txt",
        "Dockerfile",
        "render.yaml",
        "README.md",
    ]

    optional_files = [
        "docker-compose.yml",
        "API.md",
        "TIER_1_2_GUIDE.md",
        "DEPLOYMENT.md",
        "seed_data.py",
        "verify.py",
        "alembic.ini",
        "alembic/env.py",
    ]

    all_good = True
    for f in required_files:
        if not check_file_exists(f, required=True):
            all_good = False

    for f in optional_files:
        check_file_exists(f, required=False)

    return all_good

def verify_python_files():
    """Check Python syntax"""
    print("\n🐍 Checking Python syntax...")

    py_files = [
        "app/main.py",
        "app/models.py",
        "app/schemas.py",
        "app/database.py",
        "app/routers/products.py",
        "app/routers/alerts.py",
        "app/routers/retailers.py",
        "scrapers/base.py",
        "scrapers/tier1_2_scrapers.py",
    ]

    all_good = True
    for f in py_files:
        if os.path.exists(f):
            if not check_python_syntax(f):
                all_good = False
            else:
                print(f"   ✅ {f}")

    return all_good

def verify_imports():
    """Try importing key modules"""
    print("\n📦 Checking imports...")

    try:
        print("   Checking FastAPI...")
        import fastapi
        print("   ✅ FastAPI")
    except ImportError:
        print("   ❌ FastAPI not installed")
        return False

    try:
        print("   Checking SQLAlchemy...")
        import sqlalchemy
        print("   ✅ SQLAlchemy")
    except ImportError:
        print("   ❌ SQLAlchemy not installed")
        return False

    try:
        print("   Checking app modules...")
        sys.path.insert(0, '.')
        from app import models, schemas, database
        print("   ✅ App modules")
    except Exception as e:
        print(f"   ❌ App modules error: {e}")
        return False

    return True

def verify_config():
    """Check configuration files"""
    print("\n⚙️  Checking configuration...")

    # Check requirements.txt
    if os.path.exists("requirements.txt"):
        with open("requirements.txt") as f:
            content = f.read()
            required = ["fastapi", "uvicorn", "sqlalchemy", "psycopg2"]
            missing = [r for r in required if r not in content.lower()]
            if missing:
                print(f"   ⚠️  Missing in requirements.txt: {', '.join(missing)}")
            else:
                print("   ✅ requirements.txt looks good")

    # Check Dockerfile
    if os.path.exists("Dockerfile"):
        with open("Dockerfile") as f:
            content = f.read()
            if "uvicorn" in content and "8000" in content:
                print("   ✅ Dockerfile looks good")
            else:
                print("   ⚠️  Dockerfile might be missing uvicorn or port config")

    # Check render.yaml
    if os.path.exists("render.yaml"):
        with open("render.yaml") as f:
            content = f.read()
            if "price-aggregator" in content and "database" in content:
                print("   ✅ render.yaml looks good")
            else:
                print("   ⚠️  render.yaml might be incomplete")

    return True

def count_files():
    """Count total files"""
    print("\n📊 File count...")

    total = 0
    for root, dirs, files in os.walk("."):
        # Skip hidden and cache directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        total += len(files)

    print(f"   Total files: {total}")

    # Count by type
    py_files = list(Path('.').rglob('*.py'))
    md_files = list(Path('.').rglob('*.md'))
    yml_files = list(Path('.').rglob('*.yml')) + list(Path('.').rglob('*.yaml'))

    print(f"   Python files: {len(py_files)}")
    print(f"   Markdown files: {len(md_files)}")
    print(f"   YAML files: {len(yml_files)}")

    return total

def main():
    """Run all verification checks"""
    print("🔍 Price Aggregator API - Pre-deployment Verification")
    print("=" * 60)

    checks = [
        ("Structure", verify_structure),
        ("Python Syntax", verify_python_files),
        ("Imports", verify_imports),
        ("Configuration", verify_config),
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} check failed: {e}")
            results.append((name, False))

    # Count files
    count_files()

    # Summary
    print("\n" + "=" * 60)
    print("📋 Verification Summary")
    print("=" * 60)

    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
        if not result:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n🎉 All checks passed! Ready for deployment.")
        print("\nNext steps:")
        print("  1. Run: python seed_data.py")
        print("  2. Test locally: uvicorn app.main:app --reload")
        print("  3. Deploy to Render: git push")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
