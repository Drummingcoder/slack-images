# MangaPark Downloader

A stable and robust manga chapter downloader for MangaPark.io with proper error handling and Chrome WebDriver integration.

## Features

- ✅ **Stable Chrome WebDriver**: Configured for headless operation with crash prevention
- ✅ **Error Handling**: Comprehensive error handling and retry logic
- ✅ **Logging**: Detailed logging for debugging and monitoring
- ✅ **Memory Management**: Proper cleanup and memory management
- ✅ **Rate Limiting**: Built-in delays to prevent server overload
- ✅ **Flexible Configuration**: Customizable timeout, download path, and browser options

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure Chrome/Chromium is installed on your system.

## Usage

### Command Line Usage

```bash
# Download a single chapter
python mangapark-dl/mangapark_dl.py "https://mangapark.io/title/87295-en-eleceed/8945341-en-ch.1" --name "eleceed_ch1"

# Specify custom output directory
python mangapark-dl/mangapark_dl.py "chapter_url" --output "/path/to/downloads" --name "chapter_name"

# Run with custom timeout
python mangapark-dl/mangapark_dl.py "chapter_url" --timeout 60
```

### Programmatic Usage

```python
from mangapark_dl import MangaParkDownloader

# Create downloader instance
downloader = MangaParkDownloader(
    download_path="/path/to/downloads",
    headless=True,
    timeout=30
)

# Download a chapter
success = downloader.download_chapter(
    "https://mangapark.io/title/87295-en-eleceed/8945341-en-ch.1",
    "eleceed_chapter_1"
)
```

### Testing

Test the basic functionality:
```bash
python mangapark-dl/example.py test
```

## Configuration

The downloader uses the following Chrome options for stability:

- `--headless=new`: Run in headless mode
- `--no-sandbox`: Required for some environments
- `--disable-dev-shm-usage`: Prevent shared memory issues
- `--disable-gpu`: Disable GPU for stability
- `--disable-images`: Speed up page loading
- Memory optimization flags

## Error Handling

The script includes:

- **Retry Logic**: Automatic retries for failed downloads
- **Timeout Management**: Configurable timeouts for all operations
- **Driver Cleanup**: Proper WebDriver cleanup to prevent memory leaks
- **Exponential Backoff**: Progressive delays between retries
- **Comprehensive Logging**: Detailed logs for debugging

## Troubleshooting

1. **Chrome not found**: Ensure Chrome/Chromium is installed
2. **Permission errors**: Check write permissions for download directory
3. **Timeout errors**: Increase timeout value with `--timeout` option
4. **Memory issues**: The script automatically handles driver cleanup

## File Structure

```
mangapark-dl/
├── mangapark_dl.py    # Main downloader script
├── example.py         # Example usage and testing
└── README.md          # This file
```

## Log Files

Logs are saved to `mangapark_dl.log` in the parent directory of the download path.