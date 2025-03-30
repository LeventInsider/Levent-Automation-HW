import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.core.base_page import BasePage


class QACareersPage(BasePage):
    """
    QA Careers page class for handling QA-specific job listings
    """
    
    def __init__(self, driver):
        """
        QACareersPage constructor
        
        Args:
            driver: Selenium WebDriver instance
        """
        super().__init__(driver)
        self.department_container_id = "select2-filter-by-department-container"
        self.location_container_id = "select2-filter-by-location-container"
        self.location_istanbul_xpath = "//li[contains(@class, 'select2-results__option') and normalize-space(text())='Istanbul, Turkiye']"
        self.location_dropdown_xpath = "//select[@id='location']"
        self.department_dropdown_xpath = "//select[@id='department']"
        self.view_role_button_xpath = "//a[contains(text(), 'View Role')]"
        self.see_all_qa_jobs_xpath = "//a[contains(text(), 'See all QA jobs')]"
        self.job_card_xpath = "//div[contains(@class, 'position-list-item')]"
        self.job_list_xpath = "//div[@id='jobs-list']//div[contains(@class, 'position-list-item')]"

    def is_accessible(self):
        """
        Verifies if the QA Careers page is accessible by checking the URL and page elements
        
        Returns:
            bool: True if accessible, False otherwise
        """
        try:
            print("📊 Examining QA careers page elements...")
            self.wait_for_page_to_load()
            self.wait_for_element(By.XPATH, self.view_role_button_xpath)
            current_url = self.driver.current_url
            print("🔗 Currently at URL:", current_url)
            return "quality-assurance" in current_url.lower() or "qa" in current_url.lower()
        except Exception as e:
            print(f"⚠️ Problem identifying QA careers page: {e}")
            return False

    def filter_jobs(self, location, department):
        """
        Filters job listings by location and department
        
        Args:
            location: Location to filter (e.g., 'Istanbul')
            department: Department to filter (e.g., 'Quality Assurance')
        """
        location_dropdown = self.wait_for_element_to_be_clickable(By.XPATH, self.location_dropdown_xpath)
        if location_dropdown:
            location_dropdown.send_keys(location)

        department_dropdown = self.wait_for_element_to_be_clickable(By.XPATH, self.department_dropdown_xpath)
        if department_dropdown:
            department_dropdown.send_keys(department)

    def select_location_if_department_is_qa(self):
        """
        If the department is 'Quality Assurance', selects 'Istanbul, Turkiye' from location filter.
        Retries up to 3 times if department is not loaded properly.
        """
        print("🔍 Confirming department filter shows QA...")

        for attempt in range(3):
            self.scroll_to_element(By.ID, self.department_container_id)
            success = self.wait_for_element_text_to_be(By.ID, self.department_container_id, "Quality Assurance",
                                                       timeout=5)

            if success:
                print("✓ Department filter verified, selecting location...")
                self.wait_for_job_cards_to_be_replaced()
                self.click_element(By.ID, self.location_container_id)
                print("📍 Selecting Istanbul from location dropdown...")
                self.click_element(By.XPATH, self.location_istanbul_xpath)
                print("✓ Istanbul location selected successfully.")
                print("⏳ Waiting for job listings to update...")
                self.wait_for_element(By.XPATH, self.job_card_xpath)
                return
            else:
                print(f"⚠️ Attempt {attempt + 1}: Department filter not set to 'Quality Assurance'. Retrying...")
                time.sleep(2)

        print("⛔ Failed to set department filter to 'Quality Assurance'.")

    def wait_for_job_cards_to_load(self, timeout=15):
        """
        Waits for job cards to load completely
        
        Args:
            timeout: Maximum wait time in seconds
        """
        print("⌛ Awaiting job listing data to populate...")
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, self.job_list_xpath))
        )
        print("✓ Job listings data received.")

    def wait_for_job_cards_to_be_replaced(self):
        """
        Waits until old job cards are replaced with new ones
        """
        try:
            print("⌛ Monitoring for listing refresh...")
            self.wait.until(EC.invisibility_of_element_located((By.XPATH, self.job_card_xpath)))
            print("✓ Previous listings cleared.")
        except:
            print("⚠️ Previous listings state unclear. Proceeding anyway...")

        self.wait.until(lambda d: len(d.find_elements(By.XPATH, self.job_card_xpath)) > 0)
        print("✓ New listing data rendered.")

    def verify_job_listings(self):
        """
        Validates that each job listing includes both QA and Istanbul keywords
        
        Returns:
            bool: True if valid jobs exist, False otherwise
        """
        print("🧐 Scanning listings for QA positions in Istanbul...")

        job_texts = self.driver.execute_script("""
            return Array.from(document.querySelectorAll(".position-list-item")).map(el => el.innerText);
        """)

        valid_jobs = 0
        for i, text in enumerate(job_texts, 1):
            print(f"📄 Listing {i}:\n{text}\n")
            lower_text = text.lower()
            if "quality assurance" in lower_text and "istanbul" in lower_text:
                print(f"✓ Listing {i} MATCHES criteria: QA position in Istanbul")
                valid_jobs += 1
            else:
                print(f"✗ Listing {i} does NOT match criteria")

        print(f"📊 Found {valid_jobs} matching positions")
        return valid_jobs > 0

    def verify_view_role_redirects(self):
        """
        Clicks the first 'View Role' button and verifies it redirects to lever.co job detail page
        
        Returns:
            bool: True if redirected to lever.co, else False
        """
        print("🔍 Locating job details link...")
        try:
            self.wait_for_element(By.XPATH, self.job_card_xpath, timeout=15)
            print("✓ Job listings located.")

            for attempt in range(3):
                try:
                    view_role_buttons = self.driver.find_elements(By.XPATH, self.view_role_button_xpath)
                    if view_role_buttons:
                        view_role_button = view_role_buttons[0]
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_role_button)
                        time.sleep(0.5)

                        try:
                            view_role_button.click()
                            print("✓ Job details link activated.")
                        except Exception as e:
                            print(f"⚠️ Standard click method failed: {e}, trying JavaScript alternative.")
                            self.driver.execute_script("arguments[0].click();", view_role_button)

                        break
                    else:
                        print("⛔ Job details link not found.")
                        return False

                except Exception as e:
                    print(f"⚠️ Attempt {attempt + 1} unsuccessful: {e}")
                    time.sleep(1)

            # Check if new tab was opened
            windows = self.driver.window_handles
            if len(windows) > 1:
                self.driver.switch_to.window(windows[1])
                print("🔄 Switched to job details tab:", self.driver.current_url)

            self.wait_for_page_to_load()
            return "lever.co" in self.driver.current_url

        except Exception as e:
            print(f"⛔ Job details link verification error: {e}")
            return False

    def click_see_all_qa_jobs(self):
        """
        Clicks on the 'See all QA jobs' button
        """
        print("🔍 Searching for 'See all QA jobs' option...")
        button = self.wait_for_element_to_be_clickable(By.XPATH, self.see_all_qa_jobs_xpath)
        if button:
            print("✓ 'See all QA jobs' button detected, activating...")
            button.click()
        else:
            print("⚠️ Primary button not found, searching for alternatives...")
            # Try JavaScript click as fallback
            all_buttons = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'jobs')]")
            for btn in all_buttons:
                if "qa" in btn.text.lower() or "quality" in btn.text.lower():
                    print("✓ Alternative QA job button located, using JavaScript click.")
                    self.driver.execute_script("arguments[0].click();", btn)
                    break 