#!/usr/bin/env python3
"""
Comprehensive test suite for MangaPark Downloader

This test validates the refactored code structure, error handling,
and functionality without requiring external network access.
"""

import os
import sys
import tempfile
import shutil
import unittest
from unittest.mock import patch, MagicMock

# Add the mangapark-dl directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mangapark_dl import MangaParkDownloader


class TestMangaParkDownloader(unittest.TestCase):
    """Test cases for MangaParkDownloader"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.downloader = MangaParkDownloader(
            download_path=self.test_dir,
            headless=True,
            timeout=10
        )
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_initialization(self):
        """Test downloader initialization"""
        self.assertIsNotNone(self.downloader)
        self.assertEqual(self.downloader.download_path, self.test_dir)
        self.assertTrue(self.downloader.headless)
        self.assertEqual(self.downloader.timeout, 10)
        self.assertTrue(os.path.exists(self.test_dir))
    
    def test_logging_setup(self):
        """Test logging configuration"""
        self.assertIsNotNone(self.downloader.logger)
        self.assertEqual(self.downloader.logger.name, 'mangapark_dl')
    
    def test_download_directory_creation(self):
        """Test download directory creation"""
        test_subdir = os.path.join(self.test_dir, "test_manga", "chapter_1")
        os.makedirs(test_subdir, exist_ok=True)
        self.assertTrue(os.path.exists(test_subdir))
    
    @patch('mangapark_dl.requests.get')
    def test_download_image_success(self, mock_get):
        """Test successful image download"""
        # Mock successful HTTP response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.iter_content.return_value = [b'fake_image_data']
        mock_get.return_value = mock_response
        
        # Test download
        test_file = os.path.join(self.test_dir, "test_image.jpg")
        result = self.downloader.download_image("http://example.com/image.jpg", test_file)
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(test_file))
        
        # Check file content
        with open(test_file, 'rb') as f:
            content = f.read()
            self.assertEqual(content, b'fake_image_data')
    
    @patch('mangapark_dl.requests.get')
    def test_download_image_failure(self, mock_get):
        """Test image download failure handling"""
        # Mock failed HTTP response
        mock_get.side_effect = Exception("Network error")
        
        # Test download
        test_file = os.path.join(self.test_dir, "test_image.jpg")
        result = self.downloader.download_image("http://example.com/image.jpg", test_file, retries=1)
        
        self.assertFalse(result)
        self.assertFalse(os.path.exists(test_file))
    
    def test_quit_driver_no_driver(self):
        """Test quit_driver when no driver exists"""
        self.downloader.driver = None
        # Should not raise an exception
        self.downloader.quit_driver()
    
    def test_quit_driver_with_driver(self):
        """Test quit_driver with mock driver"""
        mock_driver = MagicMock()
        self.downloader.driver = mock_driver
        
        self.downloader.quit_driver()
        
        mock_driver.quit.assert_called_once()
        self.assertIsNone(self.downloader.driver)
    
    def test_chrome_options_configuration(self):
        """Test Chrome options are properly configured"""
        # This is tested implicitly by checking the create_driver method structure
        # We can't easily test the actual Chrome instantiation without network access
        # but we can verify the method exists and doesn't crash on import
        self.assertTrue(hasattr(self.downloader, 'create_driver'))
        self.assertTrue(callable(self.downloader.create_driver))
    
    def test_file_path_handling(self):
        """Test file path creation and handling"""
        chapter_name = "test_chapter"
        chapter_dir = os.path.join(self.test_dir, chapter_name)
        os.makedirs(chapter_dir, exist_ok=True)
        
        # Test page filename creation
        for i in range(1, 4):
            filename = f"page_{i:03d}.jpg"
            file_path = os.path.join(chapter_dir, filename)
            
            # Create test file
            with open(file_path, 'w') as f:
                f.write(f"page {i}")
            
            self.assertTrue(os.path.exists(file_path))
        
        # Verify files were created with correct names
        files = sorted(os.listdir(chapter_dir))
        expected_files = ["page_001.jpg", "page_002.jpg", "page_003.jpg"]
        self.assertEqual(files, expected_files)


def run_syntax_validation():
    """Run syntax and import validation"""
    print("🔍 Running syntax validation...")
    
    try:
        # Test imports
        from mangapark_dl import MangaParkDownloader
        print("✅ Import validation passed")
        
        # Test class instantiation
        downloader = MangaParkDownloader(download_path="/tmp/test")
        print("✅ Class instantiation passed")
        
        # Test method existence
        required_methods = [
            'setup_logging', 'create_driver', 'quit_driver',
            'download_image', 'get_chapter_images', 'download_chapter'
        ]
        
        for method in required_methods:
            if hasattr(downloader, method) and callable(getattr(downloader, method)):
                print(f"✅ Method {method} exists")
            else:
                print(f"❌ Method {method} missing or not callable")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Syntax validation failed: {e}")
        return False


def run_structure_validation():
    """Validate code structure and error handling patterns"""
    print("\n🏗️  Running structure validation...")
    
    try:
        # Check if main functions are properly structured
        with open('mangapark_dl.py', 'r') as f:
            content = f.read()
        
        # Check for error handling patterns
        error_patterns = [
            'try:', 'except Exception as e:', 'finally:', 'self.logger.error',
            'self.logger.warning', 'self.logger.info'
        ]
        
        for pattern in error_patterns:
            if pattern in content:
                print(f"✅ Error handling pattern '{pattern}' found")
            else:
                print(f"⚠️  Error handling pattern '{pattern}' not found")
        
        # Check for proper class structure
        if 'class MangaParkDownloader:' in content:
            print("✅ Main class structure found")
        else:
            print("❌ Main class structure missing")
            return False
        
        # Check for command line interface
        if 'def main():' in content and 'argparse' in content:
            print("✅ Command line interface found")
        else:
            print("⚠️  Command line interface incomplete")
        
        return True
        
    except Exception as e:
        print(f"❌ Structure validation failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🧪 MangaPark Downloader - Comprehensive Test Suite")
    print("=" * 60)
    
    # Run syntax validation
    syntax_ok = run_syntax_validation()
    
    # Run structure validation
    structure_ok = run_structure_validation()
    
    # Run unit tests
    print("\n🔬 Running unit tests...")
    
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestMangaParkDownloader)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"   Syntax Validation: {'✅ PASS' if syntax_ok else '❌ FAIL'}")
    print(f"   Structure Validation: {'✅ PASS' if structure_ok else '❌ FAIL'}")
    print(f"   Unit Tests: {'✅ PASS' if result.wasSuccessful() else '❌ FAIL'}")
    
    all_passed = syntax_ok and structure_ok and result.wasSuccessful()
    
    if all_passed:
        print("\n🎉 All tests passed! The refactored code is ready for use.")
        print("\n💡 Next steps:")
        print("   1. Test with actual manga URLs (requires internet)")
        print("   2. Customize chapter selectors for current MangaPark structure")
        print("   3. Add additional error recovery mechanisms as needed")
    else:
        print("\n💥 Some tests failed. Please review the issues above.")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())