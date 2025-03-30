import pytest
from src.pages.home_page import HomePage
from src.pages.careers_page import CareersPage
from src.pages.qa_careers_page import QACareersPage
from src.config.config import BASE_URL


@pytest.mark.smoke
@pytest.mark.ui
def test_insider_career_page(driver):
    """
    End-to-end test for the Insider career page flow.
    Tests navigation, page sections, and job listings for QA positions in Istanbul.
    
    Args:
        driver: WebDriver instance provided by the fixture
    """
    # Step 1: Navigate to Insider home page
    print("🌐 Starting test sequence: Opening Insider website...")
    home_page = HomePage(driver)
    home_page.go_to_insider_home_page()
    assert home_page.is_accessible(), "⛔ Unable to access Insider homepage!"

    # Step 2: Accept cookies if present
    print("🍪 Handling cookie consent dialog...")
    home_page.accept_cookies()

    # Step 3: Navigate to Careers page
    print("🔍 Proceeding to careers section...")
    home_page.navigate_to_careers()
    careers_page = CareersPage(driver)
    assert careers_page.is_accessible(), "⛔ Cannot access the careers portal!"

    # Step 4: Verify required sections on Careers page
    print("📋 Validating careers page structure...")
    assert careers_page.verify_sections(), "⛔ Required content sections missing from careers page!"

    # Step 5: Navigate to QA Careers page
    print("🧪 Navigating to Quality Assurance positions...")
    careers_page.go_to_qa_careers()
    qa_careers_page = QACareersPage(driver)

    # Step 6: Verify QA Careers page accessibility
    print("📱 Verifying QA careers section accessibility...")
    assert qa_careers_page.is_accessible(), "⛔ QA careers section inaccessible!"

    # Step 7: Click "See all QA jobs" button
    print("👁️ Expanding to view all QA positions...")
    qa_careers_page.click_see_all_qa_jobs()

    # Step 8: Filter jobs for Istanbul location if department is Quality Assurance
    print("🗺️ Filtering for Istanbul-based QA positions...")
    qa_careers_page.select_location_if_department_is_qa()
    qa_careers_page.wait_for_job_cards_to_be_replaced()

    # Step 9: Verify job listings contain both QA and Istanbul
    qa_careers_page.wait_for_job_cards_to_load()
    print("🔎 Analyzing job listings for relevance...")
    assert qa_careers_page.verify_job_listings(), "⛔ No matching QA positions found in Istanbul!"

    # Step 10: Verify View Role button redirects correctly
    print("🔗 Testing job details link functionality...")
    assert qa_careers_page.verify_view_role_redirects(), "⛔ Job details link redirection failed!"

    # Test completed successfully
    print("✨ Test automation sequence completed successfully!")
    print("📍 Final destination:", driver.current_url) 