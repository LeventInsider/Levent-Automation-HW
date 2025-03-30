"""
Configuration settings for the test automation framework
"""

# General settings
DEFAULT_TIMEOUT = 15
RETRY_ATTEMPTS = 3

# MySQL configuration
MYSQL_DB = {
    'host': 'localhost',
    'user': 'root',
    'password': '123qwe123',  # Default password when using MySQL Docker container
    'database': 'test_results',
    'table': 'ui_test_results'
}

# URLs
BASE_URL = "https://useinsider.com"
CAREERS_URL = f"{BASE_URL}/careers"

# Browser settings
BROWSER_OPTIONS = {
    'chrome': [
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--window-size=1920,1080'
    ],
    'firefox': []
} 