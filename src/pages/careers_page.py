import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.core.base_page import BasePage


class CareersPage(BasePage):
    """
    Careers page class for useinsider.com/careers
    """
    
    def __init__(self, driver):
        """
        CareersPage constructor
        
        Args:
            driver: Selenium WebDriver instance
        """
        super().__init__(driver)
        self.locations_xpath = "//*[@id='career-our-location']/div/div/div/div[1]"
        self.teams_xpath = "//*[@id='career-find-our-calling']/div/div/a"
        self.life_at_insider_xpath = "//h2[contains(text(), 'Life at Insider')]"
        self.see_all_teams_xpath = "//a[contains(text(), 'See all teams')]"
        self.qa_careers_xpath = "//h3[contains(text(), 'Quality Assurance')]"
        self.cookie_accept_xpath = "//*[@id='wt-cli-accept-all-btn']"
        self.qa_open_positions_xpath = "//h3[contains(text(), 'Quality Assurance')]/following-sibling::a[contains(text(), 'Open Positions')]"

    def is_accessible(self):
        """
        Verifies if the Careers page is accessible
        
        Returns:
            bool: True if title or URL contains career-related keywords, else False
        """
        try:
            print("Assessing careers portal accessibility...")
            self.wait_for_page_to_load()
            title = self.driver.title.lower()
            url = self.driver.current_url.lower()
            print(f"Page title: {title}")
            print(f"Current address: {url}")
            return "careers" in title or "quality assurance" in title or "/careers" in url
        except Exception as e:
            print(f"Careers portal access verification issue: {e}")
            return False

    def verify_sections(self):
        """
        Verifies the presence of key sections: Locations, Teams, and Life at Insider
        
        Returns:
            bool: True if all sections are found, else False
        """
        try:
            print("Searching for Locations section...")
            self.wait_for_element(By.XPATH, self.locations_xpath)
            print("Locations section identified.")

            print("Searching for Teams section...")
            self.wait_for_element(By.XPATH, self.teams_xpath)
            print("Teams section identified.")

            print("Searching for Company Culture section...")
            self.wait_for_element(By.XPATH, self.life_at_insider_xpath)
            print("Company Culture section identified.")

            return True
        except Exception as e:
            print(f"Section verification issue: {e}")
            return False

    def go_to_qa_careers(self):
        """
        Navigates to the QA Careers page, using fallback methods if necessary
        """
        try:
            print("Locating the teams overview option...")
            see_all_teams_button = self.wait_for_element_to_be_clickable(By.XPATH, self.see_all_teams_xpath)

            # Scroll twice with pause to ensure visibility
            self.scroll_to_element(By.XPATH, self.see_all_teams_xpath)
            time.sleep(1)
            self.scroll_to_element(By.XPATH, self.see_all_teams_xpath)
            time.sleep(1)

            see_all_teams_button.click()
            print("Teams overview selected.")

            print("Allowing page content to load...")
            self.wait_for_page_to_load()
            time.sleep(2)

            print("Finding Quality Assurance department...")
            self.scroll_to_element(By.XPATH, self.qa_careers_xpath)
            time.sleep(1)

            qa_careers_section = self.wait_for_element(By.XPATH, self.qa_careers_xpath)

            # Try using the "Open Positions" link first
            qa_open_link = self.wait_for_element_to_be_clickable(By.XPATH, self.qa_open_positions_xpath)

            if qa_open_link:
                print("Selecting 'Open Positions' for QA team...")
                self.scroll_to_element(By.XPATH, self.qa_open_positions_xpath)
                time.sleep(1)
                qa_open_link.click()
                print("QA career opportunities page loaded.")
            else:
                # Fallback to clicking on the QA section title
                print("Alternative navigation method required, attempting direct selection...")
                self.driver.execute_script("arguments[0].click();", qa_careers_section)
                print("QA section selected (alternative method).")

            # Verify we're on the right page by waiting for a QA jobs button
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'See all QA jobs')]"))
            )
        except Exception as e:
            print(f"Navigation to QA department failed: {e}") 