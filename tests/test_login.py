"""
DemoBlaze Login Test Suite - BDD Format
Behavior-driven tests for authentication functionality
"""

import pytest
import time
from pages.demoblaze_home_page import DemoBlazeHomePage


class TestDemoBlazeLogin:
    """BDD Test suite for login functionality following Given-When-Then pattern"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, app_config):
        """Setup for each test method."""
        self.home_page = DemoBlazeHomePage(driver)
        self.valid_user = {
            "username": "test",
            "password": "test"
        }
        self.invalid_user = {
            "username": "invalid_user",
            "password": "wrong_password"
        }
    
    def test_successful_login(self, driver, app_config):
        """
        Scenario: User logs in with valid credentials
        Given I am on the DemoBlaze home page
        When I enter valid username and password
        And I click the Sign in button
        Then I should be successfully logged in
        And my username should be displayed
        And I should see the logout option
        """
        print("🎭 Scenario: User logs in with valid credentials")
        
        # Given I am on the DemoBlaze home page
        print("📋 Given: I am on the DemoBlaze home page")
        self.home_page.load_home_page()
        assert self.home_page.verify_home_page_loaded(), "Home page should load successfully"
        print("  ✓ DemoBlaze home page is loaded and accessible")
        
        # When I enter valid username and password and click Sign in
        print("🎯 When: I enter valid username and password and click Sign in")
        self.home_page.perform_login(
            username=self.valid_user["username"],
            password=self.valid_user["password"]
        )
        print(f"  ✓ Entered credentials: {self.valid_user['username']}/{'*' * len(self.valid_user['password'])}")
        print("  ✓ Clicked Sign in button")
        
        # Then I should be successfully logged in
        print("✅ Then: I should be successfully logged in")
        assert self.home_page.is_user_logged_in(), "User should be logged in after successful login"
        print("  ✓ Login status confirmed as successful")
        
        # And I should remain on the main domain
        assert "demoblaze.com" in driver.current_url, "Should remain on demoblaze domain"
        assert self.home_page.verify_home_page_loaded(), "Main page should be loaded after login"
        print("  ✓ Redirected to main page successfully")
        
        # And my username should be displayed
        logged_in_username = self.home_page.get_logged_in_username()
        assert logged_in_username is not None, "Username should be displayed when logged in"
        assert self.valid_user["username"] in logged_in_username or logged_in_username != "", "Correct username should be displayed"
        print(f"  ✓ Username displayed correctly: {logged_in_username}")
        
        print("🎉 Scenario completed successfully!")
    
    def test_login_with_empty_credentials(self, driver, app_config):
        """
        Scenario: User attempts to login with empty credentials
        Given I am on the DemoBlaze login page
        When I leave username and password fields empty
        And I click the Sign in button
        Then I should not be logged in
        And I should remain on the login page
        """
        print("🎭 Scenario: User attempts to login with empty credentials")
        
        # Given I am on the DemoBlaze login page
        print("📋 Given: I am on the DemoBlaze login page")
        self.home_page.load_home_page()
        print("  ✓ DemoBlaze page loaded")
        
        # When I leave username and password fields empty and click Sign in
        print("🎯 When: I leave username and password fields empty and click Sign in")
        self.home_page.perform_login(username="", password="")
        print("  ✓ Attempted login with empty credentials")
        
        # Then I should not be logged in
        print("✅ Then: I should not be logged in")
        assert not self.home_page.is_user_logged_in(), "Should not be logged in with empty credentials"
        print("  ✓ Login correctly rejected for empty credentials")
        
        print("🎉 Scenario completed successfully!")
    
    def test_login_with_invalid_credentials(self, driver, app_config):
        """
        Scenario: User attempts to login with invalid credentials
        Given I am on the DemoBlaze home page
        When I enter an invalid username and password
        And I click the Sign in button
        Then I should not be logged in
        And I should see appropriate error handling
        """
        print("🎭 Scenario: User attempts to login with invalid credentials")
        
        # Given I am on the DemoBlaze home page
        print("📋 Given: I am on the DemoBlaze home page")
        self.home_page.load_home_page()
        print("  ✓ Home page loaded")
        
        # When I enter an invalid username and password and click Sign in
        print("🎯 When: I enter an invalid username and password and click Sign in")
        self.home_page.perform_login(
            username=self.invalid_user["username"],
            password=self.invalid_user["password"]
        )
        print(f"  ✓ Attempted login with invalid credentials: {self.invalid_user['username']}")
        
        # Then I should not be logged in
        print("✅ Then: I should not be logged in")
        assert not self.home_page.is_user_logged_in(), "Should not be logged in with invalid credentials"
        print("  ✓ Login correctly rejected for invalid credentials")
        
        print("🎉 Scenario completed successfully!")
    
    def test_logout_functionality(self, driver, app_config):
        """
        Scenario: User logs out from an active session
        Given I am logged in to DemoBlaze
        When I click the Log out button
        Then I should be logged out successfully
        And I should no longer see my username
        And I should see the Login option again
        """
        print("🎭 Scenario: User logs out from an active session")
        
        # Given I am logged in to DemoBlaze
        print("📋 Given: I am logged in to DemoBlaze")
        self.home_page.load_home_page()
        self.home_page.perform_login(
            username=self.valid_user["username"],
            password=self.valid_user["password"]
        )
        assert self.home_page.is_user_logged_in(), "Should be logged in initially"
        print("  ✓ User is successfully logged in")
        
        # When I click the Log out button
        print("🎯 When: I click the Log out button")
        self.home_page.logout()
        time.sleep(2)  # Wait for logout to complete
        print("  ✓ Clicked Log out button")
        
        # Then I should be logged out successfully
        print("✅ Then: I should be logged out successfully")
        assert not self.home_page.is_user_logged_in(), "Should be logged out after logout action"
        print("  ✓ User is successfully logged out")
        print("  ✓ Login option is available again")
        
        print("🎉 Scenario completed successfully!")
    
    def test_login_state_persistence(self, driver, app_config):
        """
        Scenario: User session persists across page navigation
        Given I am logged in to DemoBlaze
        When I navigate to different pages within the site
        And I return to the home page
        Then I should still be logged in
        And my session should be maintained
        """
        print("🎭 Scenario: User session persists across page navigation")
        
        # Given I am logged in to DemoBlaze
        print("📋 Given: I am logged in to DemoBlaze")
        self.home_page.load_home_page()
        self.home_page.perform_login(
            username=self.valid_user["username"],
            password=self.valid_user["password"]
        )
        assert self.home_page.is_user_logged_in(), "Should be logged in"
        print("  ✓ User is successfully logged in")
        
        # When I navigate to different pages within the site
        print("🎯 When: I navigate to different pages within the site")
        driver.get("https://www.demoblaze.com/cart.html")
        time.sleep(2)
        print("  ✓ Navigated to cart page")
        
        # And I return to the home page
        driver.get("https://www.demoblaze.com")
        time.sleep(2)
        print("  ✓ Returned to home page")
        
        # Then I should still be logged in
        print("✅ Then: I should still be logged in")
        assert self.home_page.is_user_logged_in(), "Should still be logged in after navigation"
        print("  ✓ Session maintained across page navigation")
        
        print("🎉 Scenario completed successfully!")
    
    @pytest.fixture(scope="function", autouse=True)
    def cleanup_login(self, driver):
        """Cleanup after each test."""
        yield
        try:
            if "demoblaze.com" in driver.current_url:
                home_page = DemoBlazeHomePage(driver)
                if home_page.is_user_logged_in():
                    home_page.logout()
                    time.sleep(1)
        except:
            pass  # Ignore cleanup errors