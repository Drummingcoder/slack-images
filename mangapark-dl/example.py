#!/usr/bin/env python3
"""
Example usage of the MangaPark Downloader

This script demonstrates how to use the MangaParkDownloader class
to download manga chapters.
"""

import sys
import os

# Add the current directory to the path so we can import mangapark_dl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mangapark_dl import MangaParkDownloader


def example_download():
    """Example of downloading a single chapter"""
    
    # Example chapter URL (replace with actual MangaPark chapter URL)
    chapter_url = "https://mangapark.io/title/87295-en-eleceed/8945341-en-ch.1"
    
    # Create downloader instance
    downloader = MangaParkDownloader(
        download_path="/home/runner/work/slack-images/slack-images/downloads",
        headless=True,
        timeout=30
    )
    
    try:
        # Download the chapter
        print(f"Starting download of chapter from: {chapter_url}")
        success = downloader.download_chapter(chapter_url, "eleceed_chapter_1")
        
        if success:
            print("✅ Chapter downloaded successfully!")
        else:
            print("❌ Chapter download failed!")
            
    except Exception as e:
        print(f"Error during download: {e}")


def test_basic_functionality():
    """Test basic functionality without actually downloading"""
    
    print("🧪 Testing MangaParkDownloader initialization...")
    
    try:
        # Test initialization
        downloader = MangaParkDownloader(
            download_path="/tmp/test_download",
            headless=True,
            timeout=10
        )
        print("✅ Downloader initialized successfully")
        
        # Test driver creation
        print("🧪 Testing WebDriver creation...")
        driver = downloader.create_driver()
        
        if driver:
            print("✅ WebDriver created successfully")
            
            # Test a simple page load
            print("🧪 Testing page load...")
            driver.get("https://www.google.com")
            print("✅ Page loaded successfully")
            
            # Cleanup
            downloader.quit_driver()
            print("✅ WebDriver closed successfully")
        else:
            print("❌ Failed to create WebDriver")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_basic_functionality()
    else:
        print("MangaPark Downloader Example")
        print("=" * 30)
        print()
        print("To run basic functionality test:")
        print("python example.py test")
        print()
        print("To run example download (uncomment the function call below):")
        print("python example.py")
        print()
        print("Note: Make sure you have Chrome/Chromium installed and accessible.")
        print("Install dependencies with: pip install -r ../requirements.txt")
        
        # Uncomment the line below to run the actual download example
        # example_download()