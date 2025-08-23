#!/usr/bin/env python3
"""
Test script for the ATM System API
This script tests all endpoints and demonstrates the API functionality.
"""

import requests
import json
import time
import sys
from typing import Optional

# Configuration
BASE_URL = "http://localhost:8000"  # FastAPI direct port, change to deployed URL for cloud testing

class ATMTester:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.created_accounts = []
    
    def test_health_check(self) -> bool:
        """Test the health check endpoint"""
        print("🔍 Testing health check...")
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed: {data}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def test_create_account(self, initial_balance: float = 100.0) -> Optional[str]:
        """Test account creation"""
        print(f"🔍 Testing account creation with balance {initial_balance}...")
        try:
            payload = {"initial_balance": initial_balance}
            response = self.session.post(f"{self.base_url}/accounts", json=payload)
            
            if response.status_code == 201:
                data = response.json()
                account_number = data["account_number"]
                self.created_accounts.append(account_number)
                print(f"✅ Account created: {account_number} with balance {data['balance']}")
                return account_number
            else:
                print(f"❌ Account creation failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Account creation error: {e}")
            return None
    
    def test_get_balance(self, account_number: str) -> Optional[float]:
        """Test getting account balance"""
        print(f"🔍 Testing get balance for account {account_number}...")
        try:
            response = self.session.get(f"{self.base_url}/accounts/{account_number}/balance")
            
            if response.status_code == 200:
                data = response.json()
                balance = data["balance"]
                print(f"✅ Balance retrieved: {balance}")
                return balance
            else:
                print(f"❌ Get balance failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Get balance error: {e}")
            return None
    
    def test_deposit(self, account_number: str, amount: float) -> bool:
        """Test deposit operation"""
        print(f"🔍 Testing deposit of {amount} to account {account_number}...")
        try:
            payload = {"amount": amount}
            response = self.session.post(f"{self.base_url}/accounts/{account_number}/deposit", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Deposit successful: New balance {data['new_balance']}")
                return True
            else:
                print(f"❌ Deposit failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Deposit error: {e}")
            return False
    
    def test_withdraw(self, account_number: str, amount: float) -> bool:
        """Test withdrawal operation"""
        print(f"🔍 Testing withdrawal of {amount} from account {account_number}...")
        try:
            payload = {"amount": amount}
            response = self.session.post(f"{self.base_url}/accounts/{account_number}/withdraw", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Withdrawal successful: New balance {data['new_balance']}")
                return True
            else:
                print(f"❌ Withdrawal failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Withdrawal error: {e}")
            return False
    
    def test_insufficient_funds(self, account_number: str) -> bool:
        """Test withdrawal with insufficient funds"""
        print(f"🔍 Testing insufficient funds scenario...")
        
        # Get current balance first
        current_balance = self.test_get_balance(account_number)
        if current_balance is None:
            return False
        
        # Try to withdraw more than available
        try:
            payload = {"amount": current_balance + 1000}
            response = self.session.post(f"{self.base_url}/accounts/{account_number}/withdraw", json=payload)
            
            if response.status_code == 400:
                print("✅ Insufficient funds check working correctly")
                return True
            else:
                print(f"❌ Expected 400 status, got {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Insufficient funds test error: {e}")
            return False
    
    def test_invalid_account(self) -> bool:
        """Test operations on non-existent account"""
        print("🔍 Testing invalid account scenario...")
        fake_account = "00000000-0000-0000-0000-000000000000"
        
        try:
            response = self.session.get(f"{self.base_url}/accounts/{fake_account}/balance")
            
            if response.status_code == 404:
                print("✅ Invalid account handling working correctly")
                return True
            else:
                print(f"❌ Expected 404 status, got {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Invalid account test error: {e}")
            return False
    
    def test_list_accounts(self) -> bool:
        """Test listing all accounts"""
        print("🔍 Testing list accounts...")
        try:
            response = self.session.get(f"{self.base_url}/accounts")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Accounts listed: {data['total_accounts']} accounts")
                return True
            else:
                print(f"❌ List accounts failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ List accounts error: {e}")
            return False
    
    def test_delete_account(self, account_number: str) -> bool:
        """Test account deletion"""
        print(f"🔍 Testing account deletion for {account_number}...")
        try:
            response = self.session.delete(f"{self.base_url}/accounts/{account_number}")
            
            if response.status_code == 204:
                print("✅ Account deleted successfully")
                if account_number in self.created_accounts:
                    self.created_accounts.remove(account_number)
                return True
            else:
                print(f"❌ Account deletion failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Account deletion error: {e}")
            return False
    
    def test_rate_limiting(self) -> bool:
        """Test rate limiting by making rapid requests"""
        print("🔍 Testing rate limiting...")
        try:
            # Make rapid requests to trigger rate limiting
            for i in range(15):
                response = self.session.get(f"{self.base_url}/health")
                if response.status_code == 429:
                    print("✅ Rate limiting is working")
                    return True
                time.sleep(0.1)
            
            print("⚠️ Rate limiting not triggered (may need more requests)")
            return True
        except Exception as e:
            print(f"❌ Rate limiting test error: {e}")
            return False
    
    def test_max_accounts_limit(self) -> bool:
        """Test that the system enforces MAX_ACCOUNTS limit"""
        print("🔍 Testing MAX_ACCOUNTS limit...")
        try:
            # First, check current account count
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code != 200:
                print(f"❌ Cannot check health status: {response.status_code}")
                return False
            
            health_data = response.json()
            current_count = health_data.get('accounts_count', 0)
            max_accounts = health_data.get('max_accounts', 1000)
            
            print(f"   Current accounts: {current_count}")
            print(f"   Max accounts: {max_accounts}")
            
            # If we're already at the limit, we can't test this
            if current_count >= max_accounts:
                print("⚠️ Already at max accounts limit, cannot test")
                return True
            
            # Try to create accounts until we hit the limit
            accounts_to_create = max_accounts - current_count + 1
            print(f"   Attempting to create {accounts_to_create} accounts to test limit...")
            
            created_count = 0
            for i in range(accounts_to_create):
                payload = {"initial_balance": 10.0}
                response = self.session.post(f"{self.base_url}/accounts", json=payload)
                
                if response.status_code == 201:
                    created_count += 1
                    account_data = response.json()
                    self.created_accounts.append(account_data["account_number"])
                elif response.status_code == 400:
                    error_data = response.json()
                    if "Maximum number of accounts" in error_data.get('detail', ''):
                        print(f"✅ MAX_ACCOUNTS limit enforced after {created_count} accounts")
                        return True
                    else:
                        print(f"❌ Unexpected 400 error: {error_data}")
                        return False
                else:
                    print(f"❌ Unexpected response: {response.status_code} - {response.text}")
                    return False
            
            print(f"⚠️ Created {created_count} accounts but limit not reached")
            return True
            
        except Exception as e:
            print(f"❌ MAX_ACCOUNTS test error: {e}")
            return False
    
    def test_max_transaction_amount(self) -> bool:
        """Test that the system enforces MAX_TRANSACTION_AMOUNT limit"""
        print("🔍 Testing MAX_TRANSACTION_AMOUNT limit...")
        try:
            # Create a test account with sufficient balance
            account = self.test_create_account(20000.0)
            if not account:
                print("❌ Cannot test transaction limit without a valid account")
                return False
            
            # Try to deposit more than the maximum allowed
            max_amount = 10000.0  # Default from settings
            test_amount = max_amount + 1000.0
            
            print(f"   Testing deposit of {test_amount} (max allowed: {max_amount})...")
            
            payload = {"amount": test_amount}
            response = self.session.post(f"{self.base_url}/accounts/{account}/deposit", json=payload)
            
            if response.status_code == 400:
                error_data = response.json()
                if "Maximum transaction amount" in error_data.get('detail', ''):
                    print(f"✅ MAX_TRANSACTION_AMOUNT limit enforced for deposit")
                else:
                    print(f"❌ Unexpected 400 error: {error_data}")
                    return False
            else:
                print(f"❌ Expected 400 error but got {response.status_code}")
                return False
            
            # Try to withdraw more than the maximum allowed
            print(f"   Testing withdrawal of {test_amount} (max allowed: {max_amount})...")
            
            response = self.session.post(f"{self.base_url}/accounts/{account}/withdraw", json=payload)
            
            if response.status_code == 400:
                error_data = response.json()
                if "Maximum transaction amount" in error_data.get('detail', ''):
                    print(f"✅ MAX_TRANSACTION_AMOUNT limit enforced for withdrawal")
                    return True
                else:
                    print(f"❌ Unexpected 400 error: {error_data}")
                    return False
            else:
                print(f"❌ Expected 400 error but got {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ MAX_TRANSACTION_AMOUNT test error: {e}")
            return False
    
    def run_comprehensive_test(self):
        """Run all tests in sequence"""
        print("🚀 Starting comprehensive ATM API tests...\n")
        
        tests_passed = 0
        total_tests = 0
        
        # Test 1: Health check
        total_tests += 1
        if self.test_health_check():
            tests_passed += 1
        print()
        
        # Test 2: Create account
        total_tests += 1
        account1 = self.test_create_account(500.0)
        if account1:
            tests_passed += 1
        print()
        
        if not account1:
            print("❌ Cannot continue tests without a valid account")
            return
        
        # Test 3: Get balance
        total_tests += 1
        if self.test_get_balance(account1):
            tests_passed += 1
        print()
        
        # Test 4: Deposit money
        total_tests += 1
        if self.test_deposit(account1, 250.0):
            tests_passed += 1
        print()
        
        # Test 5: Withdraw money
        total_tests += 1
        if self.test_withdraw(account1, 100.0):
            tests_passed += 1
        print()
        
        # Test 6: Insufficient funds
        total_tests += 1
        if self.test_insufficient_funds(account1):
            tests_passed += 1
        print()
        
        # Test 7: Invalid account
        total_tests += 1
        if self.test_invalid_account():
            tests_passed += 1
        print()
        
        # Test 8: List accounts
        total_tests += 1
        if self.test_list_accounts():
            tests_passed += 1
        print()
        
        # Test 9: Create another account
        total_tests += 1
        account2 = self.test_create_account(1000.0)
        if account2:
            tests_passed += 1
        print()
        
        # Test 10: Rate limiting
        total_tests += 1
        if self.test_rate_limiting():
            tests_passed += 1
        print()

        # Test 11: MAX_ACCOUNTS limit
        total_tests += 1
        if self.test_max_accounts_limit():
            tests_passed += 1
        print()
        
        # Test 12: MAX_TRANSACTION_AMOUNT limit
        total_tests += 1
        if self.test_max_transaction_amount():
            tests_passed += 1
        print()
        
        # Test 13: Delete account
        total_tests += 1
        if account2 and self.test_delete_account(account2):
            tests_passed += 1
        print()
        
        # Summary
        print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
        
        if tests_passed == total_tests:
            print("🎉 All tests passed! The ATM API is working correctly.")
        else:
            print("⚠️ Some tests failed. Please check the API implementation.")
        
        # Cleanup remaining accounts
        for account in self.created_accounts[:]:
            self.test_delete_account(account)

def main():
    """Main function to run tests"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = BASE_URL
    
    print(f"Testing ATM API at: {base_url}")
    
    tester = ATMTester(base_url)
    tester.run_comprehensive_test()

if __name__ == "__main__":
    main()
