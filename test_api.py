#!/usr/bin/env python3
"""
Simple test script for the Personal Blog Platform API
Run this after starting the Flask application to test basic functionality
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

class BlogAPITester:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.admin_token = None
        self.user_token = None
        self.test_user_id = None
        self.test_post_id = None
        self.test_comment_id = None
        
    def print_response(self, response, description=""):
        """Pretty print API response"""
        print(f"\n{'='*50}")
        if description:
            print(f"TEST: {description}")
        print(f"Status: {response.status_code}")
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response: {response.text}")
        print(f"{'='*50}")
    
    def test_health_check(self):
        """Test health check endpoint"""
        print("\n🏥 Testing Health Check...")
        response = self.session.get(f"{self.base_url}/health")
        self.print_response(response, "Health Check")
        return response.status_code == 200
    
    def test_admin_login(self):
        """Test admin login with default credentials"""
        print("\n👑 Testing Admin Login...")
        data = {
            "username": "admin",
            "password": "admin123"
        }
        response = self.session.post(f"{self.base_url}/login", json=data)
        self.print_response(response, "Admin Login")
        
        if response.status_code == 200:
            self.admin_token = response.json()["access_token"]
            return True
        return False
    
    def test_user_registration(self):
        """Test user registration"""
        print("\n📝 Testing User Registration...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data = {
            "username": f"testuser_{timestamp}",
            "email": f"test_{timestamp}@example.com",
            "password": "testpass123"
        }
        response = self.session.post(f"{self.base_url}/register", json=data)
        self.print_response(response, "User Registration")
        
        if response.status_code == 201:
            self.user_token = response.json()["access_token"]
            self.test_user_id = response.json()["user"]["id"]
            return True
        return False
    
    def test_get_categories(self):
        """Test getting categories"""
        print("\n📂 Testing Get Categories...")
        response = self.session.get(f"{self.base_url}/categories")
        self.print_response(response, "Get Categories")
        return response.status_code == 200
    
    def test_create_category(self):
        """Test creating a category (admin only)"""
        print("\n➕ Testing Create Category (Admin)...")
        if not self.admin_token:
            print("❌ No admin token available")
            return False
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data = {
            "name": f"Test Category {timestamp}",
            "description": "A test category created by the test script"
        }
        response = self.session.post(f"{self.base_url}/categories", json=data, headers=headers)
        self.print_response(response, "Create Category")
        return response.status_code == 201
    
    def test_create_post(self):
        """Test creating a blog post"""
        print("\n📄 Testing Create Post...")
        if not self.user_token:
            print("❌ No user token available")
            return False
            
        headers = {"Authorization": f"Bearer {self.user_token}"}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data = {
            "title": f"Test Post {timestamp}",
            "content": f"This is a test blog post created at {timestamp}. It contains some sample content to demonstrate the blog platform functionality.",
            "category_id": 1  # Assuming Technology category exists
        }
        response = self.session.post(f"{self.base_url}/posts", json=data, headers=headers)
        self.print_response(response, "Create Post")
        
        if response.status_code == 201:
            self.test_post_id = response.json()["post"]["id"]
            return True
        return False
    
    def test_get_posts(self):
        """Test getting posts with pagination"""
        print("\n📚 Testing Get Posts with Pagination...")
        params = {"page": 1, "per_page": 5}
        response = self.session.get(f"{self.base_url}/posts", params=params)
        self.print_response(response, "Get Posts")
        return response.status_code == 200
    
    def test_search_posts(self):
        """Test searching posts"""
        print("\n🔍 Testing Search Posts...")
        params = {"search": "test", "page": 1, "per_page": 10}
        response = self.session.get(f"{self.base_url}/posts", params=params)
        self.print_response(response, "Search Posts")
        return response.status_code == 200
    
    def test_get_single_post(self):
        """Test getting a single post"""
        print("\n📖 Testing Get Single Post...")
        if not self.test_post_id:
            print("❌ No test post ID available")
            return False
            
        response = self.session.get(f"{self.base_url}/posts/{self.test_post_id}")
        self.print_response(response, "Get Single Post")
        return response.status_code == 200
    
    def test_create_comment(self):
        """Test creating a comment"""
        print("\n💬 Testing Create Comment...")
        if not self.user_token or not self.test_post_id:
            print("❌ Missing user token or post ID")
            return False
            
        headers = {"Authorization": f"Bearer {self.user_token}"}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data = {
            "content": f"This is a test comment created at {timestamp}. Great post!"
        }
        response = self.session.post(
            f"{self.base_url}/posts/{self.test_post_id}/comments", 
            json=data, 
            headers=headers
        )
        self.print_response(response, "Create Comment")
        
        if response.status_code == 201:
            self.test_comment_id = response.json()["comment"]["id"]
            return True
        return False
    
    def test_get_comments(self):
        """Test getting comments for a post"""
        print("\n💭 Testing Get Comments...")
        if not self.test_post_id:
            print("❌ No test post ID available")
            return False
            
        response = self.session.get(f"{self.base_url}/posts/{self.test_post_id}/comments")
        self.print_response(response, "Get Comments")
        return response.status_code == 200
    
    def test_update_post(self):
        """Test updating a post"""
        print("\n✏️ Testing Update Post...")
        if not self.user_token or not self.test_post_id:
            print("❌ Missing user token or post ID")
            return False
            
        headers = {"Authorization": f"Bearer {self.user_token}"}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data = {
            "title": f"Updated Test Post {timestamp}",
            "content": f"This post was updated at {timestamp}. The content has been modified to test the update functionality."
        }
        response = self.session.put(
            f"{self.base_url}/posts/{self.test_post_id}", 
            json=data, 
            headers=headers
        )
        self.print_response(response, "Update Post")
        return response.status_code == 200
    
    def test_update_comment(self):
        """Test updating a comment"""
        print("\n✏️ Testing Update Comment...")
        if not self.user_token or not self.test_comment_id:
            print("❌ Missing user token or comment ID")
            return False
            
        headers = {"Authorization": f"Bearer {self.user_token}"}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data = {
            "content": f"This comment was updated at {timestamp}. Now it has different content!"
        }
        response = self.session.put(
            f"{self.base_url}/comments/{self.test_comment_id}", 
            json=data, 
            headers=headers
        )
        self.print_response(response, "Update Comment")
        return response.status_code == 200
    
    def test_admin_get_users(self):
        """Test admin endpoint to get users"""
        print("\n👥 Testing Admin Get Users...")
        if not self.admin_token:
            print("❌ No admin token available")
            return False
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = self.session.get(f"{self.base_url}/admin/users", headers=headers)
        self.print_response(response, "Admin Get Users")
        return response.status_code == 200
    
    def test_user_profile(self):
        """Test getting user profile"""
        print("\n👤 Testing Get User Profile...")
        if not self.user_token:
            print("❌ No user token available")
            return False
            
        headers = {"Authorization": f"Bearer {self.user_token}"}
        response = self.session.get(f"{self.base_url}/profile", headers=headers)
        self.print_response(response, "Get User Profile")
        return response.status_code == 200
    
    def test_error_cases(self):
        """Test various error cases"""
        print("\n❌ Testing Error Cases...")
        
        # Test invalid login
        print("\n🔐 Testing Invalid Login...")
        data = {"username": "nonexistent", "password": "wrongpass"}
        response = self.session.post(f"{self.base_url}/login", json=data)
        self.print_response(response, "Invalid Login")
        
        # Test unauthorized access
        print("\n🚫 Testing Unauthorized Access...")
        response = self.session.get(f"{self.base_url}/profile")
        self.print_response(response, "Unauthorized Profile Access")
        
        # Test non-existent post
        print("\n🔍 Testing Non-existent Post...")
        response = self.session.get(f"{self.base_url}/posts/99999")
        self.print_response(response, "Non-existent Post")
        
        return True
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting API Tests for Personal Blog Platform")
        print("=" * 60)
        
        results = {}
        
        # Basic functionality tests
        results["health_check"] = self.test_health_check()
        results["admin_login"] = self.test_admin_login()
        results["user_registration"] = self.test_user_registration()
        results["get_categories"] = self.test_get_categories()
        results["create_category"] = self.test_create_category()
        results["create_post"] = self.test_create_post()
        results["get_posts"] = self.test_get_posts()
        results["search_posts"] = self.test_search_posts()
        results["get_single_post"] = self.test_get_single_post()
        results["create_comment"] = self.test_create_comment()
        results["get_comments"] = self.test_get_comments()
        results["update_post"] = self.test_update_post()
        results["update_comment"] = self.test_update_comment()
        results["user_profile"] = self.test_user_profile()
        results["admin_get_users"] = self.test_admin_get_users()
        results["error_cases"] = self.test_error_cases()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name:<20} {status}")
        
        print(f"\n📈 Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Your API is working correctly.")
        else:
            print("⚠️ Some tests failed. Check the output above for details.")
        
        return passed == total

def main():
    """Main function to run the tests"""
    print("Personal Blog Platform API Tester")
    print("Make sure your Flask application is running on http://localhost:5000")
    
    try:
        tester = BlogAPITester()
        success = tester.run_all_tests()
        
        if success:
            print("\n🎊 Congratulations! Your Personal Blog Platform API is fully functional!")
        else:
            print("\n🔧 Some issues were found. Please check the API implementation.")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API server.")
        print("Please make sure your Flask application is running on http://localhost:5000")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()