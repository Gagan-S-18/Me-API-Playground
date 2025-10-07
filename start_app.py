#!/usr/bin/env python3
"""
Simple startup script for Me-API Playground
This script handles the proper startup sequence
"""

import subprocess
import sys
import time
import os

def start_application():
    """Start the Me-API Playground application"""
    
    print("🚀 Starting Me-API Playground...")
    print("=" * 50)
    
    # Check if database exists and seed if needed
    if not os.path.exists("meapi_playground.db"):
        print("📊 Database not found. Creating and seeding database...")
        try:
            subprocess.run([sys.executable, "seed_database.py"], check=True)
            print("✅ Database created and seeded successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating database: {e}")
            return False
    
    # Start the application with uvicorn
    print("\n🌐 Starting FastAPI server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Use uvicorn to start the application
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main_profile:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_application()