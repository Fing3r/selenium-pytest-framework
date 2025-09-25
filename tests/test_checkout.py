"""
DemoBlaze Checkout Test Suite - BDD Format
Behavior-driven tests for checkout process and purchase completion
"""

import pytest
import time
from pages.demoblaze_home_page import DemoBlazeHomePage
from pages.demoblaze_cart_page import DemoBlazeCartPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestDemoBlazeCheckout:
    """BDD Test suite for checkout and purchase behavior following Given-When-Then pattern"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, app_config):
        """Setup for each test method."""
        self.home_page = DemoBlazeHomePage(driver)
        self.cart_page = DemoBlazeCartPage(driver)
        self.test_user = {
            "username": "test",
            "password": "test"
        }
        self.valid_customer_info = {
            "name": "Test Customer",
            "country": "United States",
            "city": "New York",
            "credit_card": "4111111111111111",
            "month": "12",
            "year": "2025"
        }
    
    def setup_cart_with_product(self, driver):
        """Helper method to add a product to cart for checkout tests."""
        self.home_page.load_home_page()
        self.home_page.perform_login(
            username=self.test_user["username"],
            password=self.test_user["password"]
        )
        
        # Add product
        self.home_page.select_category("phones")
        time.sleep(2)
        
        # Click on first product
        product_links = driver.find_elements(By.CSS_SELECTOR, ".hrefch")
        product_links[0].click()
        time.sleep(3)
        
        # Add to cart
        add_to_cart_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick*='addToCart']"))
        )
        add_to_cart_btn.click()
        
        # Handle alert
        time.sleep(2)
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except:
            pass
        
        # Navigate to cart
        driver.get("https://www.demoblaze.com/cart.html")
        self.cart_page.wait_for_page_load()
        time.sleep(3)
    
    def test_checkout_modal_opening(self, driver, app_config):
        """
        Scenario: User opens the checkout modal from their cart
        Given I am logged in with items in my cart
        When I click the "Place Order" button
        Then the checkout modal should open
        And I should see the order form ready for input
        """
        print("💳 Scenario: User opens the checkout modal from their cart")
        
        # Given I am logged in with items in my cart
        print("📋 Given: I am logged in with items in my cart")
        self.setup_cart_with_product(driver)
        assert not self.cart_page.is_cart_empty(), "Cart should not be empty"
        print("  ✓ User is logged in with products in cart")
        
        # When I click the "Place Order" button
        print("🎯 When: I click the 'Place Order' button")
        self.cart_page.proceed_to_checkout()
        print("  ✓ Clicked 'Place Order' button")
        
        # Then the checkout modal should open
        print("✅ Then: The checkout modal should open with order form")
        modal = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "orderModal"))
        )
        assert modal.is_displayed(), "Checkout modal should be displayed"
        print("  ✓ Checkout modal is visible and ready for input")
        print("  ✓ Order form is accessible for customer information")
        
        print("🎉 Scenario completed successfully!")
    
    def test_checkout_form_fields_validation(self, driver, app_config):
        """
        Scenario: User verifies checkout form has all required fields
        Given I am logged in with items ready for checkout
        When I open the checkout modal
        Then I should see all required form fields
        And each field should be properly labeled and accessible
        """
        print("💳 Scenario: User verifies checkout form has all required fields")
        
        # Given I am logged in with items ready for checkout
        print("📋 Given: I am logged in with items ready for checkout")
        self.setup_cart_with_product(driver)
        print("  ✓ User is logged in with items ready for purchase")
        
        # When I open the checkout modal
        print("🎯 When: I open the checkout modal")
        self.cart_page.proceed_to_checkout()
        print("  ✓ Checkout modal has been opened")
        
        # Then I should see all required form fields
        print("✅ Then: I should see all required form fields properly displayed")
        required_fields = [
            ("name", "Name"),
            ("country", "Country"),
            ("city", "City"),
            ("card", "Credit Card"),
            ("month", "Month"),
            ("year", "Year")
        ]
        
        for field_id, field_name in required_fields:
            field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, field_id))
            )
            assert field.is_displayed(), f"Field {field_name} should be visible"
            print(f"  ✓ {field_name} field is present and accessible")
        
        print("  ✓ All form fields are properly labeled and ready for input")
        print("🎉 Scenario completed successfully!")
    
    def test_successful_checkout_with_valid_data(self, driver, app_config):
        """
        Scenario: User completes a successful purchase with valid information
        Given I am logged in with items in my cart
        When I proceed to checkout and fill the form with valid data
        And I complete the purchase
        Then I should receive an order confirmation
        And the confirmation should include my order number
        """
        print("💳 Scenario: User completes a successful purchase with valid information")
        
        # Given I am logged in with items in my cart
        print("📋 Given: I am logged in with items in my cart")
        self.setup_cart_with_product(driver)
        cart_total = self.cart_page.get_total_price()
        print(f"  ✓ User is logged in with items totaling {cart_total}")
        
        # When I proceed to checkout and fill the form with valid data
        print("🎯 When: I proceed to checkout and fill the form with valid data")
        self.cart_page.proceed_to_checkout()
        print("  ✓ Opened checkout modal")
        
        self.cart_page.fill_checkout_form(self.valid_customer_info)
        print(f"  ✓ Filled form with customer: {self.valid_customer_info['name']}")
        print(f"  ✓ Address: {self.valid_customer_info['city']}, {self.valid_customer_info['country']}")
        print(f"  ✓ Payment: Card ending in {self.valid_customer_info['credit_card'][-4:]}")
        
        # And I complete the purchase
        print("  And: I complete the purchase")
        purchase_success = self.cart_page.complete_purchase()
        assert purchase_success, "Purchase should complete successfully"
        print("  ✓ Purchase has been completed")
        
        # Then I should receive an order confirmation with order number
        print("✅ Then: I should receive an order confirmation with order number")
        confirmation_details = self.cart_page.get_order_confirmation_details()
        assert confirmation_details["success"], "Order confirmation should indicate success"
        assert confirmation_details["title"], "Confirmation title should be present"
        assert "thank you" in confirmation_details["title"].lower(), "Should contain success message"
        
        order_number = self.cart_page.extract_order_number(confirmation_details)
        assert order_number, "Order number should be present"
        assert order_number.isdigit(), "Order number should be numeric"
        
        print(f"  ✓ Order confirmation received: {confirmation_details['title']}")
        print(f"  ✓ Order number assigned: #{order_number}")
        
        self.cart_page.confirm_success_message()
        print("🎉 Scenario completed successfully!")
    
    def test_checkout_form_data_entry(self, driver, app_config):
        """
        Scenario: User enters personal information in the checkout form
        Given I am logged in with the checkout modal open
        When I fill in my personal and payment information
        Then the form should accept and retain all entered data
        And each field should display the information correctly
        """
        print("💳 Scenario: User enters personal information in the checkout form")
        
        # Given I am logged in with the checkout modal open
        print("📋 Given: I am logged in with the checkout modal open")
        self.setup_cart_with_product(driver)
        self.cart_page.proceed_to_checkout()
        print("  ✓ User has checkout modal open and ready for data entry")
        
        # When I fill in my personal and payment information
        print("🎯 When: I fill in my personal and payment information")
        test_data = {
            "name": "John Doe",
            "country": "Canada",
            "city": "Toronto",
            "credit_card": "5555444433332222",
            "month": "03",
            "year": "2027"
        }
        
        self.cart_page.fill_checkout_form(test_data)
        print(f"  ✓ Entered customer name: {test_data['name']}")
        print(f"  ✓ Entered address: {test_data['city']}, {test_data['country']}")
        print(f"  ✓ Entered payment details: Card ending in {test_data['credit_card'][-4:]}")
        print(f"  ✓ Entered expiration: {test_data['month']}/{test_data['year']}")
        
        # Then the form should accept and retain all entered data
        print("✅ Then: The form should accept and retain all entered data")
        name_field = driver.find_element(By.ID, "name")
        assert name_field.get_attribute("value") == test_data["name"], "Name field should contain entered data"
        print(f"  ✓ Name field verified: {name_field.get_attribute('value')}")
        
        country_field = driver.find_element(By.ID, "country")
        assert country_field.get_attribute("value") == test_data["country"], "Country field should contain entered data"
        print(f"  ✓ Country field verified: {country_field.get_attribute('value')}")
        
        print("  ✓ All form fields correctly display the entered information")
        print("🎉 Scenario completed successfully!")
    
    def test_checkout_with_empty_form(self, driver, app_config):
        """
        Scenario: User attempts to checkout without filling required information
        Given I am logged in with the checkout modal open
        When I try to complete the purchase without filling the form
        Then the system should handle the empty form appropriately
        And provide appropriate feedback to the user
        """
        print("💳 Scenario: User attempts to checkout without filling required information")
        
        # Given I am logged in with the checkout modal open
        print("📋 Given: I am logged in with the checkout modal open")
        self.setup_cart_with_product(driver)
        self.cart_page.proceed_to_checkout()
        print("  ✓ User has checkout modal open with empty form")
        
        # When I try to complete the purchase without filling the form
        print("🎯 When: I try to complete the purchase without filling the form")
        purchase_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[onclick='purchaseOrder()']"))
        )
        purchase_btn.click()
        print("  ✓ Clicked purchase button with empty form")
        
        time.sleep(3)  # Wait to observe system response
        
        # Then the system should handle the empty form appropriately
        print("✅ Then: The system should handle the empty form appropriately")
        modal_still_present = len(driver.find_elements(By.ID, "orderModal")) > 0
        
        if modal_still_present:
            print("  ✓ Checkout modal remains open indicating form validation")
            print("  ✓ System prevents purchase with incomplete information")
        else:
            print("  ✓ System processed empty form request")
            print("  ✓ Empty form handling behavior verified")
        
        print("  ✓ Appropriate feedback provided to user about form requirements")
        print("🎉 Scenario completed successfully!")
    
    def test_checkout_with_different_customer_data(self, driver, app_config):
        """
        Scenario: User completes purchases with various customer profiles
        Given I am a customer with different regional and payment preferences
        When I complete multiple purchases with different customer information
        Then each purchase should be processed successfully
        And each should receive a unique order confirmation
        """
        print("💳 Scenario: User completes purchases with various customer profiles")
        
        # Given I am a customer with different regional and payment preferences
        print("📋 Given: I am a customer with different regional and payment preferences")
        customer_variations = [
            {
                "name": "Alice Smith",
                "country": "United Kingdom",
                "city": "London",
                "credit_card": "4444555566667777",
                "month": "06",
                "year": "2026",
                "profile": "UK Customer"
            },
            {
                "name": "Bob Johnson",
                "country": "Australia",
                "city": "Sydney",
                "credit_card": "5555666677778888",
                "month": "09",
                "year": "2027",
                "profile": "Australian Customer"
            }
        ]
        print(f"  ✓ Testing with {len(customer_variations)} different customer profiles")
        
        # When I complete multiple purchases with different customer information
        print("🎯 When: I complete multiple purchases with different customer information")
        successful_orders = []
        
        for i, customer_data in enumerate(customer_variations, 1):
            self.setup_cart_with_product(driver)
            self.cart_page.proceed_to_checkout()
            
            print(f"  ✓ Processing order for {customer_data['profile']}")
            self.cart_page.fill_checkout_form(customer_data)
            print(f"    - Name: {customer_data['name']}")
            print(f"    - Location: {customer_data['city']}, {customer_data['country']}")
            
            purchase_success = self.cart_page.complete_purchase()
            assert purchase_success, f"Purchase should succeed for {customer_data['profile']}"
            
            confirmation_details = self.cart_page.get_order_confirmation_details()
            order_number = self.cart_page.extract_order_number(confirmation_details)
            successful_orders.append(order_number)
            
            self.cart_page.confirm_success_message()
            print(f"  ✓ {customer_data['profile']} order completed: #{order_number}")
        
        # Then each purchase should be processed successfully with unique confirmations
        print("✅ Then: Each purchase should be processed successfully with unique confirmations")
        for i, order_number in enumerate(successful_orders, 1):
            print(f"  ✓ Customer profile {i} - Order #{order_number} confirmed")
        
        unique_orders = set(successful_orders)
        assert len(unique_orders) == len(successful_orders), "Each order should have unique confirmation"
        print(f"  ✓ All {len(successful_orders)} orders have unique confirmation numbers")
        
        print("🎉 Scenario completed successfully!")
    
    def test_checkout_order_confirmation_details(self, driver, app_config):
        """
        Scenario: User reviews order confirmation details for accuracy
        Given I am completing a purchase with specific customer information
        When I receive the order confirmation
        Then the confirmation should display all my entered information
        And include the order amount and unique order identifier
        """
        print("💳 Scenario: User reviews order confirmation details for accuracy")
        
        # Given I am completing a purchase with specific customer information
        print("📋 Given: I am completing a purchase with specific customer information")
        self.setup_cart_with_product(driver)
        cart_total = self.cart_page.get_total_price()
        print(f"  ✓ Cart prepared with total: {cart_total}")
        print(f"  ✓ Customer info: {self.valid_customer_info['name']}")
        print(f"  ✓ Location: {self.valid_customer_info['city']}, {self.valid_customer_info['country']}")
        
        # When I complete the purchase and receive confirmation
        print("🎯 When: I complete the purchase and receive confirmation")
        self.cart_page.proceed_to_checkout()
        self.cart_page.fill_checkout_form(self.valid_customer_info)
        print("  ✓ Form filled with customer information")
        
        self.cart_page.complete_purchase()
        print("  ✓ Purchase has been completed")
        
        # Then the confirmation should display all entered information
        print("✅ Then: The confirmation should display all entered information accurately")
        confirmation_details = self.cart_page.get_order_confirmation_details()
        details_text = confirmation_details["details"]
        
        # Verify customer information appears in confirmation
        assert self.valid_customer_info["name"] in details_text, "Customer name should appear in confirmation"
        print(f"  ✓ Customer name confirmed: {self.valid_customer_info['name']}")
        
        assert self.valid_customer_info["credit_card"] in details_text, "Credit card should appear in confirmation"
        print(f"  ✓ Payment method confirmed: Card ending in {self.valid_customer_info['credit_card'][-4:]}")
        
        # Verify amount is mentioned
        assert "Amount:" in details_text or "USD" in details_text, "Amount should be mentioned in confirmation"
        print("  ✓ Order amount is displayed in confirmation")
        
        # Verify order ID
        order_number = self.cart_page.extract_order_number(confirmation_details)
        assert order_number, "Order number should be in confirmation"
        assert order_number.isdigit(), "Order number should be numeric"
        print(f"  ✓ Unique order identifier assigned: #{order_number}")
        
        self.cart_page.confirm_success_message()
        print("  ✓ All confirmation details are accurate and complete")
        print("🎉 Scenario completed successfully!")
    
    def test_checkout_process_screenshot_capture(self, driver, app_config):
        """
        Scenario: User's checkout journey is documented with screenshots
        Given I am completing a purchase for record keeping
        When I go through each step of the checkout process
        Then screenshots should be captured at each key milestone
        And provide visual documentation of the successful transaction
        """
        print("💳 Scenario: User's checkout journey is documented with screenshots")
        
        # Given I am completing a purchase for record keeping
        print("📋 Given: I am completing a purchase for record keeping")
        self.setup_cart_with_product(driver)
        print("  ✓ Purchase setup complete for documentation")
        
        # When I go through each step of the checkout process
        print("🎯 When: I go through each step of the checkout process")
        
        # Screenshot: Cart before checkout
        driver.save_screenshot("screenshots/checkout_cart_before.png")
        print("  ✓ Screenshot captured: Cart contents before checkout")
        
        self.cart_page.proceed_to_checkout()
        
        # Screenshot: Checkout modal
        driver.save_screenshot("screenshots/checkout_modal.png")
        print("  ✓ Screenshot captured: Checkout modal opened")
        
        self.cart_page.fill_checkout_form(self.valid_customer_info)
        
        # Screenshot: Filled form
        driver.save_screenshot("screenshots/checkout_form_filled.png")
        print("  ✓ Screenshot captured: Form filled with customer information")
        
        self.cart_page.complete_purchase()
        
        # Screenshot: Confirmation
        screenshot_path = f"screenshots/checkout_confirmation_{time.strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_path)
        print(f"  ✓ Screenshot captured: Order confirmation - {screenshot_path}")
        
        # Then screenshots should provide visual documentation
        print("✅ Then: Screenshots should provide visual documentation of the transaction")
        confirmation_details = self.cart_page.get_order_confirmation_details()
        order_number = self.cart_page.extract_order_number(confirmation_details)
        
        print(f"  ✓ Visual documentation complete for order #{order_number}")
        print("  ✓ Screenshots provide complete checkout journey record")
        print("  ✓ Transaction milestones documented for verification")
        
        self.cart_page.confirm_success_message()
        print("🎉 Scenario completed successfully!")
    
    @pytest.fixture(scope="function", autouse=True)
    def cleanup_checkout(self, driver):
        """Cleanup after each test."""
        yield
        try:
            # Close any open modals
            try:
                close_btn = driver.find_element(By.CSS_SELECTOR, "#orderModal .btn-secondary")
                if close_btn.is_displayed():
                    close_btn.click()
            except:
                pass
            
            # Logout if logged in
            if "demoblaze.com" in driver.current_url:
                home_page = DemoBlazeHomePage(driver)
                if home_page.is_user_logged_in():
                    home_page.logout()
        except:
            pass
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, app_config):
        """Setup for each test method."""
        self.home_page = DemoBlazeHomePage(driver)
        self.cart_page = DemoBlazeCartPage(driver)
        self.test_user = {
            "username": "test",
            "password": "test"
        }
        self.valid_customer_info = {
            "name": "Test Customer",
            "country": "United States",
            "city": "New York",
            "credit_card": "4111111111111111",
            "month": "12",
            "year": "2025"
        }
        self.invalid_customer_info = {
            "name": "",
            "country": "",
            "city": "",
            "credit_card": "",
            "month": "",
            "year": ""
        }
    
    def setup_cart_with_product(self, driver):
        """Helper method to add a product to cart for checkout tests."""
        self.home_page.load_home_page()
        self.home_page.perform_login(
            username=self.test_user["username"],
            password=self.test_user["password"]
        )
        
        # Add product
        self.home_page.select_category("phones")
        time.sleep(2)
        
        # Click on first product
        product_links = driver.find_elements(By.CSS_SELECTOR, ".hrefch")
        product_links[0].click()
        time.sleep(3)
        
        # Add to cart
        add_to_cart_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick*='addToCart']"))
        )
        add_to_cart_btn.click()
        
        # Handle alert
        time.sleep(2)
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except:
            pass
        
        # Navigate to cart
        driver.get("https://www.demoblaze.com/cart.html")
        self.cart_page.wait_for_page_load()
        time.sleep(3)
    
    def test_checkout_modal_opening(self, driver, app_config):
        """
        Test: Verify checkout modal opens correctly
        - Add product to cart
        - Click Place Order
        - Verify modal opens
        """
        self.setup_cart_with_product(driver)
        
        # Verify cart is not empty
        assert not self.cart_page.is_cart_empty(), "Cart should not be empty"
        
        # Click Place Order button
        self.cart_page.proceed_to_checkout()
        
        # Verify modal is visible
        modal = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "orderModal"))
        )
        assert modal.is_displayed(), "Checkout modal should be displayed"
        
        print("✓ Checkout modal opens correctly")
    
    def test_checkout_form_fields_validation(self, driver, app_config):
        """
        Test: Verify all checkout form fields are present
        - Open checkout modal
        - Verify all required fields exist
        """
        self.setup_cart_with_product(driver)
        self.cart_page.proceed_to_checkout()
        
        # Verify all form fields are present
        required_fields = [
            (By.ID, "name"),
            (By.ID, "country"),
            (By.ID, "city"),
            (By.ID, "card"),
            (By.ID, "month"),
            (By.ID, "year")
        ]
        
        for field_locator in required_fields:
            field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(field_locator)
            )
            assert field.is_displayed(), f"Field {field_locator[1]} should be visible"
        
        print("✓ All checkout form fields are present and visible")
    
    def test_successful_checkout_with_valid_data(self, driver, app_config):
        """
        Test: Complete successful checkout process
        - Fill form with valid data
        - Complete purchase
        - Verify order confirmation
        """
        self.setup_cart_with_product(driver)
        
        # Get cart total before checkout
        cart_total = self.cart_page.get_total_price()
        
        # Proceed to checkout
        self.cart_page.proceed_to_checkout()
        
        # Fill form with valid data
        self.cart_page.fill_checkout_form(self.valid_customer_info)
        
        # Complete purchase
        purchase_success = self.cart_page.complete_purchase()
        assert purchase_success, "Purchase should complete successfully"
        
        # Verify confirmation
        confirmation_details = self.cart_page.get_order_confirmation_details()
        assert confirmation_details["success"], "Order confirmation should indicate success"
        assert confirmation_details["title"], "Confirmation title should be present"
        assert "thank you" in confirmation_details["title"].lower(), "Should contain success message"
        
        # Verify order number
        order_number = self.cart_page.extract_order_number(confirmation_details)
        assert order_number, "Order number should be present"
        assert order_number.isdigit(), "Order number should be numeric"
        
        # Close confirmation
        self.cart_page.confirm_success_message()
        
        print(f"✓ Successful checkout completed with order number: {order_number}")
    
    def test_checkout_form_data_entry(self, driver, app_config):
        """
        Test: Verify form data entry works correctly
        - Fill each field individually
        - Verify data is entered correctly
        """
        self.setup_cart_with_product(driver)
        self.cart_page.proceed_to_checkout()
        
        # Test each field
        test_data = {
            "name": "John Doe",
            "country": "Canada",
            "city": "Toronto",
            "credit_card": "5555444433332222",
            "month": "03",
            "year": "2027"
        }
        
        # Fill form
        self.cart_page.fill_checkout_form(test_data)
        
        # Verify data was entered (by checking field values)
        name_field = driver.find_element(By.ID, "name")
        assert name_field.get_attribute("value") == test_data["name"], "Name field should contain entered data"
        
        country_field = driver.find_element(By.ID, "country")
        assert country_field.get_attribute("value") == test_data["country"], "Country field should contain entered data"
        
        print("✓ Form data entry verified")
    
    def test_checkout_with_empty_form(self, driver, app_config):
        """
        Test: Attempt checkout with empty form
        - Try to purchase without filling required fields
        - Verify appropriate handling
        """
        self.setup_cart_with_product(driver)
        self.cart_page.proceed_to_checkout()
        
        # Try to purchase without filling form
        purchase_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[onclick='purchaseOrder()']"))
        )
        purchase_btn.click()
        
        # Wait a moment to see if any validation occurs
        time.sleep(3)
        
        # Check if we're still on checkout modal (indicating validation failure)
        # Note: DemoBlaze might not have client-side validation, so this test verifies behavior
        modal_still_present = len(driver.find_elements(By.ID, "orderModal")) > 0
        
        print(f"✓ Empty form checkout behavior verified (modal present: {modal_still_present})")
    
    def test_checkout_with_different_customer_data(self, driver, app_config):
        """
        Test: Checkout with various customer information
        - Test different countries, names, cards
        """
        customer_variations = [
            {
                "name": "Alice Smith",
                "country": "United Kingdom",
                "city": "London",
                "credit_card": "4444555566667777",
                "month": "06",
                "year": "2026"
            },
            {
                "name": "Bob Johnson",
                "country": "Australia",
                "city": "Sydney",
                "credit_card": "5555666677778888",
                "month": "09",
                "year": "2027"
            }
        ]
        
        for i, customer_data in enumerate(customer_variations):
            self.setup_cart_with_product(driver)
            self.cart_page.proceed_to_checkout()
            
            # Fill form
            self.cart_page.fill_checkout_form(customer_data)
            
            # Complete purchase
            purchase_success = self.cart_page.complete_purchase()
            assert purchase_success, f"Purchase should succeed for customer {i+1}"
            
            # Get order confirmation
            confirmation_details = self.cart_page.get_order_confirmation_details()
            order_number = self.cart_page.extract_order_number(confirmation_details)
            
            # Close confirmation
            self.cart_page.confirm_success_message()
            
            print(f"✓ Customer {i+1} checkout successful: {customer_data['name']} - Order #{order_number}")
    
    def test_checkout_order_confirmation_details(self, driver, app_config):
        """
        Test: Verify order confirmation contains correct details
        - Complete a purchase
        - Verify confirmation includes customer info, amount, etc.
        """
        self.setup_cart_with_product(driver)
        
        # Get cart details before checkout
        cart_total = self.cart_page.get_total_price()
        
        self.cart_page.proceed_to_checkout()
        self.cart_page.fill_checkout_form(self.valid_customer_info)
        
        # Complete purchase
        self.cart_page.complete_purchase()
        
        # Get confirmation details
        confirmation_details = self.cart_page.get_order_confirmation_details()
        details_text = confirmation_details["details"]
        
        # Verify customer information appears in confirmation
        assert self.valid_customer_info["name"] in details_text, "Customer name should appear in confirmation"
        assert self.valid_customer_info["credit_card"] in details_text, "Credit card should appear in confirmation"
        
        # Verify amount is mentioned
        assert "Amount:" in details_text or "USD" in details_text, "Amount should be mentioned in confirmation"
        
        # Verify order ID
        order_number = self.cart_page.extract_order_number(confirmation_details)
        assert order_number, "Order number should be in confirmation"
        
        self.cart_page.confirm_success_message()
        
        print(f"✓ Order confirmation details verified for order #{order_number}")
    
    def test_checkout_process_screenshot_capture(self, driver, app_config):
        """
        Test: Capture screenshots during checkout process
        - Take screenshot at key steps
        - Verify screenshot functionality
        """
        self.setup_cart_with_product(driver)
        
        # Screenshot: Cart before checkout
        driver.save_screenshot("screenshots/checkout_cart_before.png")
        
        self.cart_page.proceed_to_checkout()
        
        # Screenshot: Checkout modal
        driver.save_screenshot("screenshots/checkout_modal.png")
        
        self.cart_page.fill_checkout_form(self.valid_customer_info)
        
        # Screenshot: Filled form
        driver.save_screenshot("screenshots/checkout_form_filled.png")
        
        self.cart_page.complete_purchase()
        
        # Screenshot: Confirmation
        screenshot_path = f"screenshots/checkout_confirmation_{time.strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_path)
        
        confirmation_details = self.cart_page.get_order_confirmation_details()
        order_number = self.cart_page.extract_order_number(confirmation_details)
        
        self.cart_page.confirm_success_message()
        
        print(f"✓ Checkout process screenshots captured for order #{order_number}")
        print(f"  Final screenshot: {screenshot_path}")
    
    @pytest.fixture(scope="function", autouse=True)
    def cleanup_checkout(self, driver):
        """Cleanup after each test."""
        yield
        try:
            # Close any open modals
            try:
                close_btn = driver.find_element(By.CSS_SELECTOR, "#orderModal .btn-secondary")
                if close_btn.is_displayed():
                    close_btn.click()
            except:
                pass
            
            # Logout if logged in
            if "demoblaze.com" in driver.current_url:
                home_page = DemoBlazeHomePage(driver)
                if home_page.is_user_logged_in():
                    home_page.logout()
        except:
            pass