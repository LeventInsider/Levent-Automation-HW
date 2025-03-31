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
        try:
            firefox_options = FirefoxOptions()
            driver = webdriver.Firefox(options=firefox_options)
            driver.implicitly_wait(5)
            print("Firefox driver initialized successfully")
        except Exception as e:
            print(f"Failed to initialize Firefox: {e}")
            raise

    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to handle test result reporting:
    - Inserts test result to MySQL database
    - Captures screenshot on test failure
    
    Args:
        item: pytest test item
        call: pytest call object
    """
    # Get the test result
    outcome = yield
    report = outcome.get_result()

    # Only record results during the test execution phase
    if report.when == "call":
        test_name = item.name
        status = "passed" if report.passed else "failed"
        duration = report.duration

        # Write results to MySQL database
        try:
            insert_test_result_to_mysql(
                test_name=test_name,
                status=status,
                duration=duration
            )
            print(f"📊 Test result saved to mysql-qa database: {test_name} | {status} | {duration:.2f}s")
        except Exception as e:
            print(f"Failed to save test result to database: {e}")

        # If the test fails, take a screenshot
        if report.failed:
            try:
                screenshot_dir = "screenshots"
                if not os.path.exists(screenshot_dir):
                    os.makedirs(screenshot_dir)
                screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")
                item.funcargs["driver"].save_screenshot(screenshot_path)
                print(f"🖼 Screenshot captured: {screenshot_path}")
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")


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