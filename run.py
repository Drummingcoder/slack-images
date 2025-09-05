#!/usr/bin/env python3
"""
Main runner script for the MangaPark Downloader

This script provides a simple interface to download manga chapters
using the refactored mangapark_dl module.
"""

import os
import sys

# Add mangapark-dl directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mangapark-dl'))

from mangapark_dl import MangaParkDownloader


def main():
    """Main function to run the manga downloader"""
    
    # Setup download directory (adjust path as needed)
    download_dir = os.path.join(os.path.dirname(__file__), 'downloads')
    os.makedirs(download_dir, exist_ok=True)
    
    print("🚀 MangaPark Downloader")
    print("=" * 30)
    print(f"📁 Download directory: {download_dir}")
    print()
    
    # Example usage - replace with actual chapter URL
    example_url = "https://mangapark.io/title/87295-en-eleceed/8945341-en-ch.1"
    
    print("📖 Example usage:")
    print(f"   Chapter URL: {example_url}")
    print()
    
    # Create downloader instance
    downloader = MangaParkDownloader(
        download_path=download_dir,
        headless=True,
        timeout=30
    )
    
    try:
        print("To download a chapter, modify this script with the actual chapter URL")
        print("and uncomment the download_chapter call below.")
        print()
        print("Example:")
        print("success = downloader.download_chapter(chapter_url, 'chapter_name')")
        
        # Uncomment and modify the line below to actually download
        # success = downloader.download_chapter(example_url, "eleceed_ch1")
        
        print("✅ Script completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()