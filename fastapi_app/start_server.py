#!/usr/bin/env python3
"""
Start server script with proper error handling
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
    print("🚀 Starting server...")
    uvicorn.run(main.app, host='0.0.0.0', port=8140, log_level='info')
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    print(traceback.format_exc())
    sys.exit(1)
