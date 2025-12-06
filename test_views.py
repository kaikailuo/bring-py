#!/usr/bin/env python
"""Test views counter increment"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Test login
print("Testing login endpoint...")
login_response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"username": "student1", "password": "123456"}
)

if login_response.status_code == 200:
    login_data = login_response.json()
    if login_data.get("code") == 200:
        token = login_data["data"]["token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        print("\n✓ Login successful!")
        print(f"Token: {token[:30]}...")
        
        # Get list of posts
        print("\n\nFetching list of posts...")
        posts_response = requests.get(f"{BASE_URL}/api/posts/", headers=headers)
        if posts_response.status_code == 200:
            posts_data = posts_response.json()
            if posts_data.get("code") == 200 and posts_data.get("data"):
                posts = posts_data["data"]
                print(f"✓ Got {len(posts)} posts")
                
                if len(posts) > 0:
                    post = posts[0]
                    post_id = post.get("id")
                    initial_views = post.get("views", 0)
                    print(f"\nTesting post ID {post_id}:")
                    print(f"  - Title: {post.get('title')}")
                    print(f"  - Initial views: {initial_views}")
                    
                    # Fetch the post details multiple times to increment views
                    print(f"\n  - Fetching post details (should increment views)...")
                    for i in range(3):
                        detail_response = requests.get(
                            f"{BASE_URL}/api/posts/{post_id}",
                            headers=headers
                        )
                        if detail_response.status_code == 200:
                            detail_data = detail_response.json()
                            if detail_data.get("code") == 200:
                                current_post = detail_data.get("data", {})
                                current_views = current_post.get("views", 0)
                                print(f"    - Fetch {i+1}: views = {current_views}")
                    
                    # Fetch post list again to check views
                    print(f"\n  - Fetching post list again to verify views were updated...")
                    posts_response2 = requests.get(f"{BASE_URL}/api/posts/", headers=headers)
                    if posts_response2.status_code == 200:
                        posts_data2 = posts_response2.json()
                        if posts_data2.get("code") == 200 and posts_data2.get("data"):
                            updated_posts = posts_data2["data"]
                            updated_post = next((p for p in updated_posts if p.get("id") == post_id), None)
                            if updated_post:
                                final_views = updated_post.get("views", 0)
                                print(f"  - Final views in list: {final_views}")
                                
                                if final_views > initial_views:
                                    print(f"\n✓ Views counter is working! Incremented from {initial_views} to {final_views}")
                                else:
                                    print(f"\n✗ Views counter might not be updating (still {final_views})")
