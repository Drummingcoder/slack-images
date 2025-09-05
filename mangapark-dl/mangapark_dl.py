#!/usr/bin/env python3
"""
MangaPark Downloader - A stable manga chapter download tool

This script downloads manga chapters from MangaPark using Selenium WebDriver
with Chrome in headless mode. It includes proper error handling, retry logic,
and stability improvements.
"""

import os
import sys
import time
import logging
import requests
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    WebDriverException, TimeoutException, NoSuchElementException
)


class MangaParkDownloader:
    """Main class for downloading manga chapters from MangaPark"""
    
    def __init__(self, download_path=None, headless=True, timeout=30):
        """
        Initialize the downloader
        
        Args:
            download_path (str): Directory to save downloaded chapters
            headless (bool): Whether to run Chrome in headless mode
            timeout (int): Timeout for web operations in seconds
        """
        self.download_path = download_path or "/home/runner/work/slack-images/slack-images/downloads"
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        
        # Setup logging
        self.setup_logging()
        
        # Ensure download directory exists
        os.makedirs(self.download_path, exist_ok=True)
        self.logger.info(f"Download path set to: {self.download_path}")
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(os.path.join(
                    os.path.dirname(self.download_path), 
                    'mangapark_dl.log'
                ))
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def create_driver(self):
        """Create and configure Chrome WebDriver"""
        options = Options()
        
        if self.headless:
            options.add_argument('--headless=new')
        
        # Chrome stability options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')  # Speed up loading
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Memory and crash prevention
        options.add_argument('--memory-pressure-off')
        options.add_argument('--max_old_space_size=4096')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-renderer-backgrounding')
        
        try:
            # Use system Chrome driver directly
            service = Service()  # Uses system PATH chromedriver
            driver = webdriver.Chrome(service=service, options=options)
            
            driver.set_page_load_timeout(self.timeout)
            driver.implicitly_wait(10)
            
            self.logger.info("Chrome WebDriver created successfully")
            return driver
            
        except Exception as e:
            self.logger.error(f"Failed to create Chrome WebDriver: {e}")
            raise
    
    def quit_driver(self):
        """Safely quit the WebDriver"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("WebDriver closed successfully")
            except Exception as e:
                self.logger.warning(f"Error closing WebDriver: {e}")
            finally:
                self.driver = None
    
    def download_image(self, image_url, save_path, retries=3):
        """
        Download an image from URL
        
        Args:
            image_url (str): URL of the image
            save_path (str): Path to save the image
            retries (int): Number of retry attempts
            
        Returns:
            bool: True if successful, False otherwise
        """
        for attempt in range(retries):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Referer': 'https://mangapark.io/'
                }
                
                response = requests.get(image_url, headers=headers, timeout=30, stream=True)
                response.raise_for_status()
                
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                self.logger.info(f"Downloaded: {os.path.basename(save_path)}")
                return True
                
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1} failed for {image_url}: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                
        self.logger.error(f"Failed to download {image_url} after {retries} attempts")
        return False
    
    def get_chapter_images(self, chapter_url):
        """
        Extract image URLs from a chapter page
        
        Args:
            chapter_url (str): URL of the chapter page
            
        Returns:
            list: List of image URLs
        """
        try:
            self.logger.info(f"Loading chapter: {chapter_url}")
            self.driver.get(chapter_url)
            
            # Wait for images to load
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "img"))
            )
            
            # Give extra time for all images to load
            time.sleep(3)
            
            # Find all manga page images
            # This selector may need adjustment based on MangaPark's current structure
            image_elements = self.driver.find_elements(By.CSS_SELECTOR, "img[src*='mangapark']")
            
            if not image_elements:
                # Try alternative selectors
                image_elements = self.driver.find_elements(By.CSS_SELECTOR, ".reader-main img")
                
            if not image_elements:
                image_elements = self.driver.find_elements(By.CSS_SELECTOR, "img[data-src]")
            
            image_urls = []
            for img in image_elements:
                src = img.get_attribute('src') or img.get_attribute('data-src')
                if src and 'mangapark' in src:
                    image_urls.append(src)
            
            self.logger.info(f"Found {len(image_urls)} images in chapter")
            return image_urls
            
        except TimeoutException:
            self.logger.error(f"Timeout loading chapter: {chapter_url}")
            return []
        except Exception as e:
            self.logger.error(f"Error extracting images from {chapter_url}: {e}")
            return []
    
    def download_chapter(self, chapter_url, chapter_name=None):
        """
        Download a complete chapter
        
        Args:
            chapter_url (str): URL of the chapter
            chapter_name (str): Custom name for the chapter folder
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create driver for this chapter
            self.driver = self.create_driver()
            
            # Extract chapter name from URL if not provided
            if not chapter_name:
                chapter_name = f"chapter_{int(time.time())}"
            
            # Create chapter directory
            chapter_dir = os.path.join(self.download_path, chapter_name)
            os.makedirs(chapter_dir, exist_ok=True)
            
            self.logger.info(f"Starting download for: {chapter_name}")
            
            # Get image URLs
            image_urls = self.get_chapter_images(chapter_url)
            
            if not image_urls:
                self.logger.error(f"No images found for chapter: {chapter_name}")
                return False
            
            # Download each image
            success_count = 0
            for i, image_url in enumerate(image_urls, 1):
                # Create filename with zero-padded page number
                filename = f"page_{i:03d}.jpg"
                save_path = os.path.join(chapter_dir, filename)
                
                if self.download_image(image_url, save_path):
                    success_count += 1
                
                # Small delay between downloads
                time.sleep(1)
            
            self.logger.info(f"Chapter '{chapter_name}' completed: {success_count}/{len(image_urls)} images downloaded")
            return success_count > 0
            
        except Exception as e:
            self.logger.error(f"Error downloading chapter {chapter_name}: {e}")
            return False
        finally:
            # Always cleanup driver
            self.quit_driver()
            # Add delay before next chapter
            time.sleep(5)
    
    def download_manga(self, manga_url, start_chapter=1, end_chapter=None):
        """
        Download multiple chapters from a manga
        
        Args:
            manga_url (str): URL of the manga main page
            start_chapter (int): First chapter to download
            end_chapter (int): Last chapter to download (None for all)
            
        Returns:
            bool: True if at least one chapter was downloaded successfully
        """
        try:
            self.logger.info(f"Starting manga download from: {manga_url}")
            
            # This is a simplified implementation
            # In a real implementation, you would need to:
            # 1. Parse the manga page to get chapter links
            # 2. Filter chapters based on start_chapter and end_chapter
            # 3. Download each chapter
            
            # For now, this is a placeholder that shows the structure
            self.logger.info("Manga download feature needs implementation based on specific MangaPark structure")
            return True
            
        except Exception as e:
            self.logger.error(f"Error downloading manga: {e}")
            return False


def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Download manga chapters from MangaPark')
    parser.add_argument('url', help='Chapter or manga URL')
    parser.add_argument('--output', '-o', default=None, help='Output directory')
    parser.add_argument('--name', '-n', default=None, help='Chapter name')
    parser.add_argument('--headless', action='store_true', default=True, help='Run in headless mode')
    parser.add_argument('--timeout', '-t', type=int, default=30, help='Timeout in seconds')
    
    args = parser.parse_args()
    
    # Create downloader
    downloader = MangaParkDownloader(
        download_path=args.output,
        headless=args.headless,
        timeout=args.timeout
    )
    
    try:
        # Download the chapter
        success = downloader.download_chapter(args.url, args.name)
        
        if success:
            print("Download completed successfully!")
            sys.exit(0)
        else:
            print("Download failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nDownload interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()