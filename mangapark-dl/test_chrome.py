#!/usr/bin/env python3
"""
Simple test script to verify Chrome WebDriver functionality
"""

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def test_chrome_simple():
    """Simple Chrome test without webdriver-manager"""
    
    print("🧪 Testing Chrome WebDriver (simple)...")
    
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    try:
        # Use system chromedriver
        service = Service()  # Uses /usr/bin/chromedriver
        driver = webdriver.Chrome(service=service, options=options)
        
        print("✅ Chrome WebDriver created successfully")
        
        # Test simple page load
        print("🧪 Testing page load...")
        driver.get("https://httpbin.org/get")
        
        print("✅ Page loaded successfully")
        print(f"📄 Page title: {driver.title}")
        
        # Cleanup
        driver.quit()
        print("✅ Chrome WebDriver closed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Chrome test failed: {e}")
        return False


if __name__ == "__main__":
    if test_chrome_simple():
        print("\n🎉 Chrome WebDriver is working correctly!")
    else:
        print("\n💥 Chrome WebDriver test failed!")
        sys.exit(1)