#!/usr/bin/env python3
"""
Simple server startup script
"""

import sys
import os
from pathlib import Path

# Add Django project to Python path
django_project_path = Path('..')
sys.path.append(str(django_project_path))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deelflow.settings')

try:
    import django
    django.setup()
    print("✅ Django setup successful")
    
    import main
    print("✅ Main module imported successfully")
    
    import uvicorn
    print("🚀 Starting server on port 8140...")
    print("📝 If port 8140 is busy, try port 8141 or 8142")
    print("🔗 Server will be available at: http://localhost:8140")
    print("📚 API docs will be available at: http://localhost:8140/docs")
    print("=" * 50)
    
    # Try port 8140 first, then 8141, then 8142
    for port in [8140, 8141, 8142]:
        try:
            print(f"🔄 Trying port {port}...")
            uvicorn.run(main.app, host='0.0.0.0', port=port, log_level='info')
            break
        except OSError as e:
            if "Address already in use" in str(e) or "only one usage of each socket address" in str(e):
                print(f"❌ Port {port} is already in use, trying next port...")
                continue
            else:
                print(f"❌ Error on port {port}: {e}")
                break
        except Exception as e:
            print(f"❌ Unexpected error on port {port}: {e}")
            break
    else:
        print("❌ All ports (8140, 8141, 8142) are busy. Please free up a port or try a different one.")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    print(traceback.format_exc())
    sys.exit(1)
