#!/usr/bin/env python3
"""
Simple test script to verify the Me-API Playground application
"""

import requests
import json
import time
import subprocess
import sys
import os

def test_application():
    """Test the Me-API Playground application"""
    
    print("🚀 Testing Me-API Playground Application")
    print("=" * 50)
    
    # Start the server
    print("Starting server...")
    try:
        process = subprocess.Popen([
            sys.executable, "main_profile.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(3)
        
        base_url = "http://localhost:8000"
        
        # Test 1: Health Check
        print("\n1. Testing Health Check...")
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                print(f"✅ Health Check: {health_data['status']}")
                print(f"   Database: {health_data['database']}")
            else:
                print(f"❌ Health Check failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Health Check error: {e}")
        
        # Test 2: Get All Profiles
        print("\n2. Testing Get All Profiles...")
        try:
            response = requests.get(f"{base_url}/profiles", timeout=5)
            if response.status_code == 200:
                profiles = response.json()
                print(f"✅ Found {len(profiles)} profiles")
                for profile in profiles[:2]:  # Show first 2
                    print(f"   - {profile['name']} ({profile['email']})")
            else:
                print(f"❌ Get Profiles failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Get Profiles error: {e}")
        
        # Test 3: Search Projects by Skill
        print("\n3. Testing Search Projects by Skill...")
        try:
            response = requests.get(f"{base_url}/projects?skill=python", timeout=5)
            if response.status_code == 200:
                projects_data = response.json()
                print(f"✅ Found {projects_data['total']} projects with Python")
                for project in projects_data['projects'][:2]:  # Show first 2
                    print(f"   - {project['title']}")
            else:
                print(f"❌ Search Projects failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Search Projects error: {e}")
        
        # Test 4: Get Top Skills
        print("\n4. Testing Get Top Skills...")
        try:
            response = requests.get(f"{base_url}/skills/top?limit=5", timeout=5)
            if response.status_code == 200:
                skills_data = response.json()
                print(f"✅ Found {skills_data['total']} top skills")
                for skill in skills_data['skills'][:3]:  # Show first 3
                    print(f"   - {skill['name']} ({skill['count']})")
            else:
                print(f"❌ Get Top Skills failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Get Top Skills error: {e}")
        
        # Test 5: Global Search
        print("\n5. Testing Global Search...")
        try:
            response = requests.get(f"{base_url}/search?q=machine%20learning&limit=5", timeout=5)
            if response.status_code == 200:
                search_data = response.json()
                print(f"✅ Found {search_data['total']} results for 'machine learning'")
                for result in search_data['results'][:2]:  # Show first 2
                    print(f"   - {result['type']}: {result.get('name', result.get('title', 'Unknown'))}")
            else:
                print(f"❌ Global Search failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Global Search error: {e}")
        
        # Test 6: Frontend
        print("\n6. Testing Frontend...")
        try:
            response = requests.get(f"{base_url}/", timeout=5)
            if response.status_code == 200:
                content = response.text
                if "Me-API Playground" in content:
                    print("✅ Frontend loaded successfully")
                else:
                    print("⚠️  Frontend loaded but content may be incorrect")
            else:
                print(f"❌ Frontend failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Frontend error: {e}")
        
        # Test 7: API Documentation
        print("\n7. Testing API Documentation...")
        try:
            response = requests.get(f"{base_url}/docs", timeout=5)
            if response.status_code == 200:
                print("✅ API Documentation accessible")
            else:
                print(f"❌ API Documentation failed: {response.status_code}")
        except Exception as e:
            print(f"❌ API Documentation error: {e}")
        
        print("\n" + "=" * 50)
        print("🎉 Testing completed!")
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
    finally:
        # Clean up
        try:
            process.terminate()
        except:
            pass

if __name__ == "__main__":
    test_application()