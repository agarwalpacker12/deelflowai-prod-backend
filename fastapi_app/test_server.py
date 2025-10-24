#!/usr/bin/env python3
"""
Test server startup script
"""

import sys
import os
import traceback

# Add Django project to Python path
django_project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(django_project_path)

try:
    print("Setting up Django...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deelflow.settings')
    import django
    django.setup()
    print("✅ Django setup successful")
    
    print("Importing main module...")
    import main
    print("✅ Main module imported successfully")
    
    print("Starting server...")
    import uvicorn
    uvicorn.run(main.app, host='0.0.0.0', port=8140, log_level='info')
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Traceback: {traceback.format_exc()}")
    sys.exit(1)
