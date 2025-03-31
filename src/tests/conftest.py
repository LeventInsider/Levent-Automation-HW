import pytest
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from src.utils.db_controller import insert_test_result_to_mysql
from src.config.config import BROWSER_OPTIONS, RETRY_ATTEMPTS


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    """
    Fixture to provide WebDriver instances for Chrome and Firefox.
    The test will run for each browser defined in the params.
    
    Args:
        request: pytest request object
        
    Returns:
        WebDriver: configured browser driver instance
    """
    if request.param == "chrome":
        try:
            driver = webdriver.Chrome()
            driver.implicitly_wait(5)
            print("Chrome driver initialized successfully")
        except Exception as e:
            print(f"Failed to initialize Chrome: {e}")
            raise

    elif request.param == "firefox":
        firefox_options = FirefoxOptions()
        for option in BROWSER_OPTIONS['firefox']:
            firefox_options.add_argument(option)
            
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)

    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Pytest hook to handle test result reporting:
    - Inserts test result to MySQL database
    - Captures screenshot on test failure
    
    Args:
        item: pytest test item
    """
    # Get the test result
    outcome = yield
    report = outcome.get_result()

    # Only record results during the test execution phase
    if report.when == "call":
        test_name = item.name
        status = "passed" if report.passed else "failed"
        duration = getattr(report, 'duration', 0)
        timestamp = datetime.utcnow()

        # Write results to MySQL database
        try:
            insert_test_result_to_mysql(
                test_name=test_name,
                status=status,
                duration=duration,
                timestamp=timestamp
            )
        except Exception as e:
            print(f"⚠️ Error saving to database: {e}")

        # If the test fails, take a screenshot
        if report.failed:
            driver = item.funcargs.get("driver", None)
            if driver:
                screenshot_dir = "screenshots"
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")
                driver.save_screenshot(screenshot_path)
                print(f"🖼 Screenshot captured: {screenshot_path}")


# Configure retry for flaky tests
def pytest_configure(config):
    """Configure pytest with retry plugin if available"""
    config.addinivalue_line(
        "markers", "flaky: mark test as flaky, will be retried"
    )


@pytest.hookimpl(trylast=True)
def pytest_runtest_setup(item):
    """Apply retry marker to all tests"""
    item.add_marker(pytest.mark.flaky(reruns=RETRY_ATTEMPTS)) 