from selenium.webdriver.common.by import By
from src.core.base_page import BasePage
from src.config.config import BASE_URL


class HomePage(BasePage):
    """
    Home page class for useinsider.com
    """
    
    def __init__(self, driver):
        """
        HomePage constructor
        
        Args:
            driver: Selenium WebDriver instance
        """
        super().__init__(driver)
        self.url = BASE_URL
        self.company_menu_xpath = "(//*[@id='navbarDropdownMenuLink'])[5]"
        self.careers_link_xpath = "//*[@id='navbarNavDropdown']/ul[1]/li[6]/div/div[2]/a[2]"
        self.cookie_button_xpath = "//*[@id='wt-cli-accept-all-btn']"

    def go_to_insider_home_page(self):
        """
        Opens the Insider homepage
        """
        print(f"🏠 Accessing main portal: {self.url}")
        self.driver.get(self.url)
        self.wait_for_page_to_load()

    def is_accessible(self):
        """
        Checks whether the homepage is accessible by verifying the title
        
        Returns:
            bool: True if title contains 'Insider', else False
        """
        title = self.driver.title
        print(f"📝 Site identification: {title}")
        return "Insider" in title

    def accept_cookies(self):
        """
        Accepts cookies using BasePage method
        """
        super().accept_cookies(self.cookie_button_xpath)

    def navigate_to_careers(self):
        """
        Navigates to the Careers page through the Company menu
        """
        print("📂 Accessing company information...")
        self.click_element(By.XPATH, self.company_menu_xpath)
        print("💼 Selecting career opportunities...")
        self.click_element(By.XPATH, self.careers_link_xpath) 