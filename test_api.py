#!/usr/bin/env python
"""Test the API endpoints to verify stats are being returned"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Test login
print("Testing login endpoint...")
login_response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"username": "student1", "password": "123456"}
)
print(f"Login status: {login_response.status_code}")
login_data = login_response.json()
print(json.dumps(login_data, indent=2, ensure_ascii=False))

if login_data.get("code") == 200 and login_data.get("data", {}).get("token"):
    token = login_data["data"]["token"]
    print(f"\n\nToken obtained: {token[:20]}...")
    
    # Test /api/auth/me endpoint
    print("\n\nTesting /api/auth/me endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    me_response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
    print(f"GET /api/auth/me status: {me_response.status_code}")
    me_data = me_response.json()
    print(json.dumps(me_data, indent=2, ensure_ascii=False))
    
    # Check if stats are present
    if me_data.get("data", {}).get("user", {}).get("stats"):
        print("\n✓ Stats field is present in response!")
        stats = me_data["data"]["user"]["stats"]
        print(f"Posts count: {stats.get('posts_count')}")
        print(f"Comments count: {stats.get('comments_count')}")
        print(f"Total submissions: {stats.get('total_submissions')}")
        print(f"Passed submissions: {stats.get('passed_submissions')}")
        print(f"Pass rate: {stats.get('pass_rate')}%")
    else:
        print("\n✗ Stats field is NOT present in response!")
else:
    print("Login failed!")
