from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    """
    Base page class with common methods for all page objects
    """

    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_element(self, by, locator, timeout=None):
        """
        Waits until the presence of an element is located.
        """
        try:
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            return wait.until(EC.presence_of_element_located((by, locator)))
        except TimeoutException:
            print(f"⚠️ Element not found: {locator}")
            return None

    def wait_for_element_to_be_clickable(self, by, locator, timeout=None):
        """
        Waits until the element is clickable.
        """
        try:
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            return wait.until(EC.element_to_be_clickable((by, locator)))
        except TimeoutException:
            print(f"⚠️ Element not clickable: {locator}")
            return None

    def click_element(self, by, locator):
        """
        Waits for the element to be clickable and clicks it. Falls back to JS click.
        """
        element = self.wait_for_element_to_be_clickable(by, locator)
        if element:
            try:
                element.click()
                print(f"👆 Element activated: {locator}")
            except Exception:
                print(f"⚠️ Using alternative click method for: {locator}")
                self.driver.execute_script("arguments[0].click();", element)
        else:
            print(f"⚠️ Unable to interact with element: {locator}")

    def scroll_to_element(self, by, locator):
        """
        Scrolls to the specified element on the page.
        """
        element = self.wait_for_element(by, locator)
        if element:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            print(f"📜 Viewport adjusted to: {locator}")
        else:
            print(f"⚠️ Cannot scroll to element: {locator}")

    def accept_cookies(self, cookie_xpath):
        """
        Clicks the cookie accept button if it's visible and clickable.
        """
        try:
            print("🍪 Checking for cookie consent prompt...")
            cookie_button = self.wait_for_element_to_be_clickable(By.XPATH, cookie_xpath)
            if cookie_button:
                cookie_button.click()
                print("✓ Cookie consent processed.")
            else:
                print("ℹ️ No cookie prompt detected.")
        except NoSuchElementException:
            print("ℹ️ Cookie consent not applicable.")

    def wait_for_page_to_load(self):
        """
        Waits until the page's document.readyState is 'complete'.
        """
        try:
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            print("📄 Page rendering complete.")
        except TimeoutException:
            print("⚠️ Page loading timed out.")

    def get_element_text(self, by, locator):
        """
        Returns the trimmed text content of the specified element.
        """
        element = self.wait_for_element(by, locator)
        if element:
            return element.text.strip()
        return ""

    def wait_for_element_text_to_be(self, by, locator, expected_text, timeout=10):
        """
        Waits until the element's text matches the expected value.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element((by, locator), expected_text)
            )
            print(f"✓ Text value verified: '{expected_text}'")
            return True
        except TimeoutException:
            actual_text = self.get_element_text(by, locator)
            print(f"⚠️ Text mismatch - Expected: '{expected_text}', Found: '{actual_text}'")
            return False 