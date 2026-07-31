#!/usr/bin/env python3
"""
Grovia Backend API Testing Suite
Tests all API endpoints for the grocery app
"""

import requests
import sys
import json
from datetime import datetime

class GroviaAPITester:
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - {details}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "details": details
        })

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'
        if headers:
            test_headers.update(headers)

        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=test_headers, timeout=10)

            success = response.status_code == expected_status
            details = f"Status: {response.status_code}"
            
            if not success:
                details += f", Expected: {expected_status}"
                try:
                    error_data = response.json()
                    details += f", Response: {error_data}"
                except:
                    details += f", Response: {response.text[:100]}"

            self.log_test(name, success, details)
            
            if success:
                try:
                    return response.json()
                except:
                    return {"status": "success"}
            return {}

        except Exception as e:
            self.log_test(name, False, f"Error: {str(e)}")
            return {}

    def test_health_check(self):
        """Test API health check"""
        response = self.run_test("Health Check", "GET", "", 200)
        return response.get("status") == "running"

    def test_categories(self):
        """Test categories endpoint"""
        response = self.run_test("Get Categories", "GET", "categories", 200)
        categories = response.get("categories", [])
        
        # Check if we have 13 categories
        if len(categories) == 13:
            self.log_test("Categories Count (13)", True)
        else:
            self.log_test("Categories Count (13)", False, f"Got {len(categories)} categories")
        
        return len(categories) > 0

    def test_products(self):
        """Test products endpoints"""
        # Test all products
        response = self.run_test("Get All Products", "GET", "products", 200)
        products = response.get("products", [])
        total = response.get("total", 0)
        
        # Check if we have 105 products
        if total == 105:
            self.log_test("Products Count (105)", True)
        else:
            self.log_test("Products Count (105)", False, f"Got {total} products")

        # Test product detail
        if products:
            product_id = products[0]["id"]
            detail_response = self.run_test("Get Product Detail", "GET", f"products/{product_id}", 200)
            
            # Check if store_availability is present
            if "store_availability" in detail_response:
                self.log_test("Product Store Availability", True)
            else:
                self.log_test("Product Store Availability", False, "Missing store_availability")

        # Test search
        search_response = self.run_test("Search Products (apple)", "GET", "products/search?q=apple", 200)
        search_products = search_response.get("products", [])
        
        if len(search_products) > 0:
            self.log_test("Product Search Works", True)
        else:
            self.log_test("Product Search Works", False, "No search results")

        return len(products) > 0

    def test_stores(self):
        """Test stores endpoints"""
        # Test all stores
        response = self.run_test("Get All Stores", "GET", "stores", 200)
        stores = response.get("stores", [])
        
        # Check if we have 8 stores
        if len(stores) == 8:
            self.log_test("Stores Count (8)", True)
        else:
            self.log_test("Stores Count (8)", False, f"Got {len(stores)} stores")

        # Test nearby stores
        nearby_response = self.run_test("Get Nearby Stores", "GET", "stores/nearby", 200)
        nearby_stores = nearby_response.get("stores", [])
        
        # Check if distance is calculated
        if nearby_stores and "distance_km" in nearby_stores[0]:
            self.log_test("Nearby Stores with Distance", True)
        else:
            self.log_test("Nearby Stores with Distance", False, "Missing distance calculation")

        return len(stores) > 0

    def test_phone_auth(self):
        """Test phone OTP authentication"""
        phone = "9876543210"
        
        # Send OTP
        otp_response = self.run_test("Send OTP", "POST", "auth/phone", 200, {"phone": phone})
        
        if "message" in otp_response:
            self.log_test("OTP Send Message", True)
        else:
            self.log_test("OTP Send Message", False, "Missing OTP send confirmation")

        # Verify OTP
        verify_response = self.run_test("Verify OTP", "POST", "auth/phone", 200, {"phone": phone, "otp": "1234"})
        
        if "token" in verify_response:
            self.token = verify_response["token"]
            self.user_id = verify_response.get("id")
            self.log_test("OTP Verification Returns Token", True)
            return True
        else:
            self.log_test("OTP Verification Returns Token", False, "Missing token in response")
            return False

    def test_authenticated_endpoints(self):
        """Test endpoints that require authentication"""
        if not self.token:
            self.log_test("Auth Required Tests", False, "No token available")
            return False

        # Test get current user
        self.run_test("Get Current User", "GET", "auth/me", 200)

        # Test cart operations
        cart_response = self.run_test("Get Cart", "GET", "cart", 200)
        
        # Add item to cart
        add_cart_response = self.run_test("Add to Cart", "POST", "cart", 200, {
            "product_id": "p1",
            "store_id": "store-1", 
            "quantity": 2,
            "weight_option": "500g"
        })
        
        if "items" in add_cart_response and len(add_cart_response["items"]) > 0:
            self.log_test("Cart Add Item Success", True)
            
            # Test cart update
            cart_item_id = add_cart_response["items"][0]["id"]
            self.run_test("Update Cart Item", "PUT", f"cart/{cart_item_id}", 200, {"quantity": 3})
            
            # Test cart remove
            self.run_test("Remove Cart Item", "DELETE", f"cart/{cart_item_id}", 200)
        else:
            self.log_test("Cart Add Item Success", False, "No items in cart response")

        # Test orders (need cart items first)
        self.run_test("Add to Cart for Order", "POST", "cart", 200, {
            "product_id": "p2",
            "store_id": "store-1",
            "quantity": 1,
            "weight_option": "6 pcs"
        })

        # Add address first
        address_response = self.run_test("Add Address", "POST", "user/addresses", 200, {
            "label": "Home",
            "full_address": "123 Test Street, Bangalore",
            "city": "Bangalore",
            "pincode": "560001"
        })

        if "id" in address_response:
            address_id = address_response["id"]
            
            # Create order
            order_response = self.run_test("Create Order", "POST", "orders", 200, {
                "address_id": address_id,
                "payment_method": "COD",
                "store_id": "store-1"
            })
            
            if "id" in order_response:
                order_id = order_response["id"]
                self.run_test("Get Order Details", "GET", f"orders/{order_id}", 200)
                self.run_test("Get All Orders", "GET", "orders", 200)

        # Test profile endpoints
        self.run_test("Get Profile", "GET", "user/profile", 200)
        self.run_test("Get Addresses", "GET", "user/addresses", 200)
        self.run_test("Get Wishlist", "GET", "user/wishlist", 200)

        return True

    def test_recommendations(self):
        """Test recommendations endpoint"""
        # Test without auth
        self.run_test("Get Recommendations (No Auth)", "GET", "recommendations", 200)
        
        # Test with auth if available
        if self.token:
            self.run_test("Get Recommendations (With Auth)", "GET", "recommendations", 200)

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Grovia API Tests...")
        print(f"📍 Testing API: {self.base_url}")
        print("=" * 60)

        # Basic endpoints
        self.test_health_check()
        self.test_categories()
        self.test_products()
        self.test_stores()
        self.test_recommendations()

        # Authentication
        auth_success = self.test_phone_auth()
        
        # Authenticated endpoints
        if auth_success:
            self.test_authenticated_endpoints()

        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return 0
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed")
            return 1

    def get_test_report(self):
        """Get detailed test report"""
        return {
            "total_tests": self.tests_run,
            "passed_tests": self.tests_passed,
            "failed_tests": self.tests_run - self.tests_passed,
            "success_rate": round((self.tests_passed / self.tests_run) * 100, 2) if self.tests_run > 0 else 0,
            "results": self.test_results
        }

def main():
    tester = GroviaAPITester()
    exit_code = tester.run_all_tests()
    
    # Save detailed report
    report = tester.get_test_report()
    with open('backend_test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: backend_test_report.json")
    return exit_code

if __name__ == "__main__":
    sys.exit(main())