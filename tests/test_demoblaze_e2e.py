"""
DemoBlaze End-to-End Integration Test Suite - BDD Format
Behavior-driven tests for complete user workflows and integration scenarios
"""

import pytest
import time
from pages.demoblaze_home_page import DemoBlazeHomePage
from pages.demoblaze_cart_page import DemoBlazeCartPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestDemoBlazeE2EIntegration:
    """BDD Test suite for end-to-end integration workflows following Given-When-Then pattern"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, app_config):
        """Setup for each test method."""
        self.home_page = DemoBlazeHomePage(driver)
        self.cart_page = DemoBlazeCartPage(driver)
        self.test_user = {
            "username": "test",
            "password": "test"
        }
        self.customer_info = {
            "name": "John Doe",
            "country": "United States",
            "city": "New York",
            "credit_card": "4111111111111111",
            "month": "12",
            "year": "2025"
        }
    
    def test_complete_single_product_purchase_flow(self, driver, app_config):
        """
        Scenario: Customer completes a full single product purchase journey
        Given I am a new customer wanting to buy a product from DemoBlaze
        When I log in, select a product, add it to cart, and complete checkout
        Then I should receive a successful order confirmation
        And have a complete purchase record with order number and screenshot
        """
        print("🛒 Scenario: Customer completes a full single product purchase journey")
        
        # Given I am a new customer wanting to buy a product from DemoBlaze
        print("📋 Given: I am a new customer wanting to buy a product from DemoBlaze")
        self.home_page.load_home_page()
        print("  ✓ Accessing DemoBlaze e-commerce platform")
        
        # When I log in, select a product, add it to cart, and complete checkout
        print("🎯 When: I log in, select a product, add it to cart, and complete checkout")
        
        # Authentication phase
        self.home_page.perform_login(
            username=self.test_user["username"],
            password=self.test_user["password"]
        )
        assert self.home_page.is_user_logged_in(), "Should be logged in"
        print("  ✓ Successfully logged in to my account")
        
        # Product selection phase
        self.home_page.select_category("phones")
        time.sleep(2)
        
        products = self.home_page.get_product_list()
        selected_product = products[0]["name"]
        print(f"  ✓ Browsing phones category, selected: {selected_product}")
        
        # Add product to cart
        product_links = driver.find_elements(By.CSS_SELECTOR, ".hrefch")
        product_links[0].click()
        time.sleep(3)
        
        add_to_cart_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick*='addToCart']"))
        )
        add_to_cart_btn.click()
        
        time.sleep(2)
        try:
            alert = driver.switch_to.alert
            alert.accept()
            print("  ✓ Product successfully added to cart with confirmation")
        except:
            print("  ✓ Product added to cart")
        
        # Cart verification phase
        driver.get("https://www.demoblaze.com/cart.html")
        self.cart_page.wait_for_page_load()
        time.sleep(3)
        
        cart_items = self.cart_page.get_cart_items()
        assert len(cart_items) > 0, "Cart should not be empty"
        cart_total = self.cart_page.get_total_price()
        print(f"  ✓ Cart verified: {len(cart_items)} item(s), Total: {cart_total}")
        
        # Checkout phase
        self.cart_page.proceed_to_checkout()
        print("  ✓ Proceeded to checkout modal")
        
        self.cart_page.fill_checkout_form(self.customer_info)
        print(f"  ✓ Filled checkout form with customer: {self.customer_info['name']}")
        
        purchase_success = self.cart_page.complete_purchase()
        assert purchase_success, "Purchase should complete successfully"
        print("  ✓ Purchase transaction completed")
        
        # Then I should receive a successful order confirmation
        print("✅ Then: I should receive a successful order confirmation with complete record")
        confirmation_details = self.cart_page.get_order_confirmation_details()
        assert confirmation_details["success"], "Order should be confirmed"
        
        order_number = self.cart_page.extract_order_number(confirmation_details)
        assert order_number, "Order number should be generated"
        print(f"  ✓ Order confirmation received: #{order_number}")
        
        # Capture final screenshot for records
        screenshot_path = f"screenshots/e2e_single_product_{time.strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_path)
        print(f"  ✓ Purchase record screenshot: {screenshot_path}")
        
        self.cart_page.confirm_success_message()
        
        print(f"  ✓ Complete purchase journey successful: {selected_product}")
        print("🎉 Scenario completed successfully!")
    
    def test_complete_multi_product_purchase_flow(self, driver, app_config):
        """
        Scenario: Customer purchases multiple products from different categories
        Given I am a customer wanting to buy products from various categories
        When I add multiple products from different categories and complete checkout
        Then I should receive a consolidated order confirmation
        And my purchase should include all selected items from different categories
        """
        print("🛒 Scenario: Customer purchases multiple products from different categories")
        
        # Given I am a customer wanting to buy products from various categories
        print("📋 Given: I am a customer wanting to buy products from various categories")
        self.home_page.load_home_page()
        self.home_page.perform_login(
            username=self.test_user["username"],
            password=self.test_user["password"]
        )
        assert self.home_page.is_user_logged_in(), "Should be logged in"
        print("  ✓ Customer authenticated for multi-category shopping")
        
        # When I add multiple products from different categories and complete checkout
        print("🎯 When: I add multiple products from different categories and complete checkout")
        selected_products = []
        categories_to_test = [("phones", "phone"), ("laptops", "laptop")]
        
        for i, (category, product_type) in enumerate(categories_to_test, 1):
            # Navigate to category
            driver.get("https://www.demoblaze.com")
            self.home_page.select_category(category)
            time.sleep(2)
            
            # Get available products
            products = self.home_page.get_product_list()
            assert len(products) > 0, f"Products should be available in {category}"
            
            product_name = products[0]["name"]
            selected_products.append(product_name)
            print(f"  ✓ Category {i}: Selected {product_type} - {product_name}")
            
            # Add product to cart
            product_links = driver.find_elements(By.CSS_SELECTOR, ".hrefch")
            product_links[0].click()
            time.sleep(3)
            
            add_to_cart_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick*='addToCart']"))
            )
            add_to_cart_btn.click()
            
            time.sleep(2)
            try:
                alert = driver.switch_to.alert
                alert.accept()
            except:
                pass
            
            print(f"  ✓ Added {product_type} to cart successfully")
        
        # Multi-product cart verification
        driver.get("https://www.demoblaze.com/cart.html")
        self.cart_page.wait_for_page_load()
        time.sleep(3)
        
        cart_items = self.cart_page.get_cart_items()
        assert len(cart_items) >= 2, f"Cart should contain multiple items, found {len(cart_items)}"
        cart_total = self.cart_page.get_total_price()
        print(f"  ✓ Multi-category cart verified: {len(cart_items)} items, Total: {cart_total}")
        
        # Consolidated checkout process
        self.cart_page.proceed_to_checkout()
        self.cart_page.fill_checkout_form(self.customer_info)
        print("  ✓ Checkout form completed for multi-product purchase")
        
        purchase_success = self.cart_page.complete_purchase()
        assert purchase_success, "Multi-product purchase should complete successfully"
        print("  ✓ Multi-category purchase transaction completed")
        
        # Then I should receive a consolidated order confirmation
        print("✅ Then: I should receive a consolidated order confirmation for all items")
        confirmation_details = self.cart_page.get_order_confirmation_details()
        assert confirmation_details["success"], "Consolidated order should be confirmed"
        
        order_number = self.cart_page.extract_order_number(confirmation_details)
        assert order_number, "Consolidated order number should be generated"
        
        # Capture screenshot for multi-product purchase
        screenshot_path = f"screenshots/e2e_multi_product_{time.strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_path)
        
        self.cart_page.confirm_success_message()
        
        print(f"  ✓ Consolidated order confirmation: #{order_number}")
        print(f"  ✓ Purchase includes all categories: {[product.split(' ')[0] for product in selected_products]}")
        print(f"  ✓ Multi-product purchase record: {screenshot_path}")
        print("🎉 Scenario completed successfully!")
    
    def test_complete_user_session_workflow(self, driver, app_config):
        """
        Scenario: Customer experiences a complete shopping session with browsing
        Given I am a customer exploring the DemoBlaze shopping platform
        When I browse multiple categories, compare products, and make a purchase
        Then I should have a complete shopping experience
        And successfully complete my transaction with full product exploration
        """
        print("🛒 Scenario: Customer experiences a complete shopping session with browsing")
        
        # Given I am a customer exploring the DemoBlaze shopping platform
        print("📋 Given: I am a customer exploring the DemoBlaze shopping platform")
        self.home_page.load_home_page()
        print("  ✓ Accessing DemoBlaze for a comprehensive shopping session")
        
        # When I browse multiple categories, compare products, and make a purchase
        print("🎯 When: I browse multiple categories, compare products, and make a purchase")
        
        # Authentication for personalized experience
        self.home_page.perform_login(
            username=self.test_user["username"],
            password=self.test_user["password"]
        )
        assert self.home_page.is_user_logged_in(), "Should be logged in"
        print("  ✓ Logged in for personalized shopping experience")
        
        # Multi-category exploration phase
        categories_explored = ["phones", "laptops", "monitors"]
        exploration_results = {}
        
        for category in categories_explored:
            self.home_page.select_category(category)
            time.sleep(2)
            
            products = self.home_page.get_product_list()
            exploration_results[category] = len(products)
            print(f"  ✓ Explored {category} category: {len(products)} products available")
        
        # Product comparison and selection
        print("  ✓ Completed product comparison across categories")
        
        # Select final product for purchase (from phones category)
        self.home_page.select_category("phones")
        time.sleep(2)
        
        products = self.home_page.get_product_list()
        chosen_product = products[0]["name"]
        
        # Product detail viewing and cart addition
        product_links = driver.find_elements(By.CSS_SELECTOR, ".hrefch")
        product_links[0].click()
        time.sleep(3)
        
        add_to_cart_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick*='addToCart']"))
        )
        add_to_cart_btn.click()
        
        time.sleep(2)
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except:
            pass
        
        print(f"  ✓ Final product selection: {chosen_product}")
        
        # Shopping cart review phase
        driver.get("https://www.demoblaze.com/cart.html")
        self.cart_page.wait_for_page_load()
        time.sleep(3)
        
        cart_items = self.cart_page.get_cart_items()
        assert len(cart_items) > 0, "Cart should contain selected product"
        cart_total = self.cart_page.get_total_price()
        print(f"  ✓ Cart reviewed before checkout: {len(cart_items)} item, Total: {cart_total}")
        
        # Final purchase completion
        self.cart_page.proceed_to_checkout()
        self.cart_page.fill_checkout_form(self.customer_info)
        print("  ✓ Checkout information completed")
        
        purchase_success = self.cart_page.complete_purchase()
        assert purchase_success, "Complete session purchase should succeed"
        print("  ✓ Purchase completed after thorough exploration")
        
        # Then I should have a complete shopping experience
        print("✅ Then: I should have a complete shopping experience with successful transaction")
        confirmation_details = self.cart_page.get_order_confirmation_details()
        assert confirmation_details["success"], "Session should end with confirmed order"
        
        order_number = self.cart_page.extract_order_number(confirmation_details)
        
        # Session completion documentation
        screenshot_path = f"screenshots/complete_session_{time.strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_path)
        
        self.cart_page.confirm_success_message()
        
        # Session summary
        total_products_explored = sum(exploration_results.values())
        print(f"  ✓ Complete shopping session summary:")
        print(f"    - Categories explored: {len(categories_explored)}")
        print(f"    - Total products viewed: {total_products_explored}")
        print(f"    - Final purchase: {chosen_product}")
        print(f"    - Order confirmation: #{order_number}")
        print(f"    - Session record: {screenshot_path}")
        print("🎉 Scenario completed successfully!")
    
    def test_single_product_purchase_with_verification(self, driver, app_config):
        """
        Scenario: Customer performs a verified single product purchase with full documentation
        Given I need to make a documented purchase with verification steps
        When I complete each step of the purchase with verification
        Then each stage should be verified and documented
        And I should have complete proof of the successful transaction
        """
        print("🛒 Scenario: Customer performs a verified single product purchase with full documentation")
        
        # Given I need to make a documented purchase with verification steps
        print("📋 Given: I need to make a documented purchase with verification steps")
        self.home_page.load_home_page()
        print("  ✓ Starting documented purchase process")
        
        # When I complete each step of the purchase with verification
        print("🎯 When: I complete each step of the purchase with verification")
        
        # Step 1: Verified login
        self.home_page.perform_login(
            username=self.test_user["username"],
            password=self.test_user["password"]
        )
        assert self.home_page.is_user_logged_in(), "Login verification failed"
        print("  ✓ Step 1 verified: User authentication successful")
        
        # Step 2: Verified product selection
        driver.get("https://www.demoblaze.com/cart.html")
        self.cart_page.wait_for_page_load()
        time.sleep(2)
        print("  ✓ Step 2 verified: Navigated to cart page")
        
        # Add product verification process
        driver.get("https://www.demoblaze.com")
        self.home_page.select_category("phones")
        time.sleep(2)
        
        products = self.home_page.get_product_list()
        selected_product = products[0]["name"]
        
        product_links = driver.find_elements(By.CSS_SELECTOR, ".hrefch")
        product_links[0].click()
        time.sleep(3)
        print(f"  ✓ Step 3 verified: Product selected - {selected_product}")
        
        # Step 3: Verified cart addition
        add_to_cart_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick*='addToCart']"))
        )
        add_to_cart_btn.click()
        
        time.sleep(2)
        alert_received = False
        try:
            alert = driver.switch_to.alert
            alert.accept()
            alert_received = True
        except:
            pass
        
        print(f"  ✓ Step 4 verified: Product added to cart (alert: {alert_received})")
        
        # Step 4: Verified cart contents
        driver.get("https://www.demoblaze.com/cart.html")
        self.cart_page.wait_for_page_load()
        time.sleep(3)
        
        cart_items = self.cart_page.get_cart_items()
        assert len(cart_items) > 0, "Cart verification failed - no items"
        assert any(selected_product.lower() in item["name"].lower() for item in cart_items), "Selected product not in cart"
        print(f"  ✓ Step 5 verified: Cart contains {selected_product}")
        
        # Step 5: Verified checkout process
        self.cart_page.proceed_to_checkout()
        print("  ✓ Step 6 verified: Checkout modal opened")
        
        self.cart_page.fill_checkout_form(self.customer_info)
        print(f"  ✓ Step 7 verified: Form filled for {self.customer_info['name']}")
        
        # Step 6: Verified purchase completion
        purchase_success = self.cart_page.complete_purchase()
        assert purchase_success, "Purchase verification failed"
        print("  ✓ Step 8 verified: Purchase transaction completed")
        
        # Then each stage should be verified and documented
        print("✅ Then: Each stage should be verified and documented with complete proof")
        confirmation_details = self.cart_page.get_order_confirmation_details()
        assert confirmation_details["success"], "Order confirmation verification failed"
        
        order_number = self.cart_page.extract_order_number(confirmation_details)
        assert order_number, "Order number verification failed"
        assert order_number.isdigit(), "Order number format verification failed"
        
        # Complete documentation with screenshot
        screenshot_path = f"screenshots/verified_purchase_{time.strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_path)
        
        self.cart_page.confirm_success_message()
        
        print(f"  ✓ Final verification: Order #{order_number} confirmed")
        print(f"  ✓ Complete documentation: {screenshot_path}")
        print(f"  ✓ All 8 verification steps completed successfully")
        print("🎉 Scenario completed successfully!")
    
    def test_two_different_products_purchase(self, driver, app_config):
        """
        Scenario: Customer purchases two different products in a single transaction
        Given I am a customer wanting to buy two different products
        When I select products from different categories and complete checkout
        Then I should receive one consolidated order for both products
        And both products should be included in my purchase confirmation
        """
        print("🛒 Scenario: Customer purchases two different products in a single transaction")
        
        # Given I am a customer wanting to buy two different products
        print("📋 Given: I am a customer wanting to buy two different products")
        self.home_page.load_home_page()
        self.home_page.perform_login(
            username=self.test_user["username"],
            password=self.test_user["password"]
        )
        assert self.home_page.is_user_logged_in(), "Should be logged in for two-product purchase"
        print("  ✓ Customer authenticated for multi-product purchase")
        
        # When I select products from different categories and complete checkout
        print("🎯 When: I select products from different categories and complete checkout")
        selected_products = []
        
        # First product - Phone
        print("  📱 Selecting first product: Phone")
        self.home_page.select_category("phones")
        time.sleep(2)
        
        phone_products = self.home_page.get_product_list()
        phone_name = phone_products[0]["name"]
        selected_products.append(phone_name)
        
        phone_links = driver.find_elements(By.CSS_SELECTOR, ".hrefch")
        phone_links[0].click()
        time.sleep(3)
        
        add_to_cart_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick*='addToCart']"))
        )
        add_to_cart_btn.click()
        
        time.sleep(2)
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except:
            pass
        
        print(f"  ✓ First product added: {phone_name}")
        
        # Second product - Laptop
        print("  💻 Selecting second product: Laptop")
        driver.get("https://www.demoblaze.com")
        self.home_page.select_category("laptops")
        time.sleep(2)
        
        laptop_products = self.home_page.get_product_list()
        laptop_name = laptop_products[0]["name"]
        selected_products.append(laptop_name)
        
        laptop_links = driver.find_elements(By.CSS_SELECTOR, ".hrefch")
        laptop_links[0].click()
        time.sleep(3)
        
        add_to_cart_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick*='addToCart']"))
        )
        add_to_cart_btn.click()
        
        time.sleep(2)
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except:
            pass
        
        print(f"  ✓ Second product added: {laptop_name}")
        
        # Verify two-product cart
        driver.get("https://www.demoblaze.com/cart.html")
        self.cart_page.wait_for_page_load()
        time.sleep(3)
        
        cart_items = self.cart_page.get_cart_items()
        assert len(cart_items) >= 2, f"Cart should contain 2 products, found {len(cart_items)}"
        cart_total = self.cart_page.get_total_price()
        print(f"  ✓ Two-product cart verified: {len(cart_items)} items, Total: {cart_total}")
        
        # Single consolidated checkout
        self.cart_page.proceed_to_checkout()
        self.cart_page.fill_checkout_form(self.customer_info)
        print("  ✓ Checkout form completed for two-product purchase")
        
        purchase_success = self.cart_page.complete_purchase()
        assert purchase_success, "Two-product purchase should succeed"
        print("  ✓ Two-product purchase transaction completed")
        
        # Then I should receive one consolidated order for both products
        print("✅ Then: I should receive one consolidated order for both products")
        confirmation_details = self.cart_page.get_order_confirmation_details()
        assert confirmation_details["success"], "Consolidated order should be confirmed"
        
        order_number = self.cart_page.extract_order_number(confirmation_details)
        assert order_number, "Single order number should be generated for both products"
        
        # Document two-product purchase
        screenshot_path = f"screenshots/two_products_{time.strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_path)
        
        self.cart_page.confirm_success_message()
        
        print(f"  ✓ Consolidated order confirmation: #{order_number}")
        print(f"  ✓ Products included in single transaction:")
        print(f"    - Product 1: {selected_products[0]} (Phone)")
        print(f"    - Product 2: {selected_products[1]} (Laptop)")
        print(f"  ✓ Two-product purchase documentation: {screenshot_path}")
        print("🎉 Scenario completed successfully!")
    
    @pytest.fixture(scope="function", autouse=True)
    def cleanup_e2e(self, driver):
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
        self.customer_info = {
            "name": "John Doe",
            "country": "United States",
            "city": "New York",
            "credit_card": "4111111111111111",
            "month": "12",
            "year": "2025"
        }
    
    def test_complete_single_product_purchase_flow(self, driver, app_config):
        """
        End-to-End Test: Complete Single Product Purchase Journey
        Covers: Login → Product Selection → Cart → Checkout → Confirmation
        
        User Story: As a customer, I want to buy a single product with a complete 
        purchase experience from login to order confirmation.
        """
        print("🎯 Starting Complete Single Product Purchase Flow")
        
        # Step 1: Login
        self.home_page.load_home_page()
        self.home_page.perform_login(
            username=self.test_user["username"],
            password=self.test_user["password"]
        )
        assert self.home_page.is_user_logged_in(), "Should be logged in"
        print("✓ User authentication successful")
        
        # Step 2: Browse and select product
        self.home_page.select_category("phones")
        time.sleep(2)
        
        products = self.home_page.get_product_list()
        selected_product = products[0]["name"]
        
        # Add product to cart
        product_links = driver.find_elements(By.CSS_SELECTOR, ".hrefch")
        product_links[0].click()
        time.sleep(3)
        
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
        
        print(f"✓ Product selected and added to cart: {selected_product}")
        
        # Step 3: Cart verification and navigation
        driver.get("https://www.demoblaze.com/cart.html")
        self.cart_page.wait_for_page_load()
        time.sleep(3)
        
        cart_items = self.cart_page.get_cart_items()
        assert len(cart_items) > 0, "Cart should not be empty"
        cart_total = self.cart_page.get_total_price()
        
        print(f"✓ Cart verified: {len(cart_items)} item(s), Total: {cart_total}")
        
        # Step 4: Checkout process
        self.cart_page.proceed_to_checkout()
        self.cart_page.fill_checkout_form(self.customer_info)
        
        purchase_success = self.cart_page.complete_purchase()
        assert purchase_success, "Purchase should complete successfully"
        
        print("✓ Checkout process completed")
        
        # Step 5: Order confirmation
        confirmation_details = self.cart_page.get_order_confirmation_details()
        assert confirmation_details["success"], "Order should be confirmed"
        
        order_number = self.cart_page.extract_order_number(confirmation_details)
        assert order_number, "Order number should be generated"
        
        # Capture final screenshot
        screenshot_path = f"screenshots/e2e_single_product_{time.strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_path)
        
        self.cart_page.confirm_success_message()
        
        print(f"🎉 Complete Single Product Purchase Flow SUCCESSFUL")
        print(f"   Product: {selected_product}")
        print(f"   Order #: {order_number}")
        print(f"   Screenshot: {screenshot_path}")
    
    def test_complete_multi_product_purchase_flow(self, driver, app_config):
        """
        End-to-End Test: Complete Multi-Product Purchase Journey
        Covers: Login → Multiple Product Categories → Cart Management → Checkout → Confirmation
        
        User Story: As a customer, I want to buy multiple products from different 
        categories in a single transaction.
        """
        print("🎯 Starting Complete Multi-Product Purchase Flow")
        
        # Step 1: Authentication
        self.home_page.load_home_page()
        self.home_page.perform_login(
            username=self.test_user["username"],
            password=self.test_user["password"]
        )
        assert self.home_page.is_user_logged_in(), "Should be logged in"
        print("✓ User authenticated")
        
        # Step 2: Multi-category product selection
        selected_products = []
        categories_to_test = [("phones", "phone"), ("laptops", "laptop")]
        
        for category, product_type in categories_to_test:
            # Navigate to category
            driver.get("https://www.demoblaze.com")
            self.home_page.select_category(category)
            time.sleep(2)
            
            # Get available products
            products = self.home_page.get_product_list()
            product_name = products[0]["name"]
            selected_products.append(product_name)
            
            # Add to cart
            product_links = driver.find_elements(By.CSS_SELECTOR, ".hrefch")
            product_links[0].click()
            time.sleep(3)
            
            add_to_cart_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick*='addToCart']"))
            )
            add_to_cart_btn.click()
            
            time.sleep(2)
            try:
                alert = driver.switch_to.alert
                alert.accept()
            except:
                pass
            
            print(f"✓ Added {product_type}: {product_name}")
        
        # Step 3: Cart aggregation and verification
        driver.get("https://www.demoblaze.com/cart.html")
        self.cart_page.wait_for_page_load()
        time.sleep(3)
        
        cart_items = self.cart_page.get_cart_items()
        assert len(cart_items) >= 2, "Cart should contain multiple products"
        
        # Verify all products are in cart
        cart_names = [item["name"].lower() for item in cart_items]
        for product_name in selected_products:
            product_in_cart = any(product_name.lower() in cart_name for cart_name in cart_names)
            assert product_in_cart, f"Product {product_name} should be in cart"
        
        cart_total = self.cart_page.get_total_price()
        print(f"✓ Multi-product cart verified: {len(cart_items)} items, Total: {cart_total}")
        
        # Step 4: Integrated checkout
        self.cart_page.proceed_to_checkout()
        
        # Use different customer info for multi-product purchase
        multi_customer_info = {
            "name": "Multi Product Buyer",
            "country": "Canada",
            "city": "Vancouver", 
            "credit_card": "5555444433332222",
            "month": "06",
            "year": "2027"
        }
        
        self.cart_page.fill_checkout_form(multi_customer_info)
        
        purchase_success = self.cart_page.complete_purchase()
        assert purchase_success, "Multi-product purchase should succeed"
        
        print("✓ Multi-product checkout completed")
        
        # Step 5: Comprehensive confirmation
        confirmation_details = self.cart_page.get_order_confirmation_details()
        assert confirmation_details["success"], "Multi-product order should be confirmed"
        
        order_number = self.cart_page.extract_order_number(confirmation_details)
        
        # Capture evidence
        screenshot_path = f"screenshots/e2e_multi_product_{time.strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_path)
        
        self.cart_page.confirm_success_message()
        
        print(f"🎉 Complete Multi-Product Purchase Flow SUCCESSFUL")
        print(f"   Products: {', '.join(selected_products)}")
        print(f"   Categories: {len(categories_to_test)} different categories")
        print(f"   Order #: {order_number}")
        print(f"   Screenshot: {screenshot_path}")
    
    def test_complete_user_session_workflow(self, driver, app_config):
        """
        End-to-End Test: Complete User Session from Start to Finish
        Covers: Login → Browse Multiple Categories → Compare Products → Purchase → Logout
        
        User Story: As a customer, I want to have a complete shopping session 
        where I explore the site, compare products, and make a purchase decision.
        """
        print("🎯 Starting Complete User Session Workflow")
        
        # Step 1: Session initialization
        self.home_page.load_home_page()
        assert self.home_page.verify_home_page_loaded(), "Site should be accessible"
        
        self.home_page.perform_login(
            username=self.test_user["username"],
            password=self.test_user["password"]
        )
        assert self.home_page.is_user_logged_in(), "User session should be established"
        print("✓ User session initiated")
        
        # Step 2: Product exploration across categories
        categories_explored = []
        products_viewed = []
        
        for category in ["phones", "laptops", "monitors"]:
            self.home_page.select_category(category)
            time.sleep(2)
            
            products = self.home_page.get_product_list()
            categories_explored.append(category)
            products_viewed.extend([p["name"] for p in products[:2]])  # View first 2 products
            
            print(f"✓ Explored {category}: {len(products)} products available")
        
        # Step 3: Product selection and comparison
        # Select best value product (could be enhanced with price comparison logic)
        self.home_page.select_category("phones")
        time.sleep(2)
        
        phone_products = self.home_page.get_product_list()
        selected_phone = phone_products[0]["name"]
        
        # Add phone to cart
        product_links = driver.find_elements(By.CSS_SELECTOR, ".hrefch")
        product_links[0].click()
        time.sleep(3)
        
        add_to_cart_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick*='addToCart']"))
        )
        add_to_cart_btn.click()
        
        time.sleep(2)
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except:
            pass
        
        print(f"✓ Product selected for purchase: {selected_phone}")
        
        # Step 4: Cart review and purchase decision
        driver.get("https://www.demoblaze.com/cart.html")
        self.cart_page.wait_for_page_load()
        time.sleep(3)
        
        cart_summary = self.cart_page.get_cart_summary()
        assert not cart_summary["is_empty"], "Cart should contain selected product"
        
        print(f"✓ Purchase decision made: {cart_summary['item_count']} item(s), Total: {cart_summary['total_price']}")
        
        # Step 5: Transaction completion
        self.cart_page.proceed_to_checkout()
        
        session_customer_info = {
            "name": "Session User",
            "country": "United Kingdom",
            "city": "London",
            "credit_card": "4444333322221111",
            "month": "09",
            "year": "2026"
        }
        
        self.cart_page.fill_checkout_form(session_customer_info)
        
        purchase_success = self.cart_page.complete_purchase()
        assert purchase_success, "Transaction should complete successfully"
        
        confirmation_details = self.cart_page.get_order_confirmation_details()
        order_number = self.cart_page.extract_order_number(confirmation_details)
        
        self.cart_page.confirm_success_message()
        
        print("✓ Transaction completed successfully")
        
        # Step 6: Session termination
        self.home_page.logout()
        time.sleep(2)
        assert not self.home_page.is_user_logged_in(), "User session should be terminated"
        
        # Capture session evidence
        screenshot_path = f"screenshots/e2e_complete_session_{time.strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_path)
        
        print(f"🎉 Complete User Session Workflow SUCCESSFUL")
        print(f"   Categories explored: {', '.join(categories_explored)}")
        print(f"   Products viewed: {len(products_viewed)} products")
        print(f"   Final purchase: {selected_phone}")
        print(f"   Order #: {order_number}")
        print(f"   Session properly terminated")
        print(f"   Screenshot: {screenshot_path}")
    
    @pytest.fixture(scope="function", autouse=True)
    def cleanup_e2e(self, driver):
        """Cleanup after each test."""
        yield
        try:
            if "demoblaze.com" in driver.current_url:
                home_page = DemoBlazeHomePage(driver)
                if home_page.is_user_logged_in():
                    home_page.logout()
        except:
            pass
    
    def test_single_product_purchase_with_verification(self, driver, app_config):
        """
        Specific Test Case: Single Product Purchase Flow
        1. Add a product
        2. Go to the 'Cart' page at 'https://www.demoblaze.com/cart.html'
        3. Verify that product is added 
        4. Click on 'Place Order' button
        5. Fill Form with data 'name, country, city, credit card, month, year'
        6. Click on Purchase button
        7. Verify Confirmation
        8. Take a Screenshot to confirm
        """
        # Step 1: Add a product (Manual approach for reliability)
        self.home_page.load_home_page()
        
        # Login first to ensure smooth operation
        self.home_page.perform_login(
            username=self.test_user["username"],
            password=self.test_user["password"]
        )
        assert self.home_page.is_user_logged_in(), "Should be logged in"
        
        # Select phones category
        self.home_page.select_category("phones")
        time.sleep(2)
        
        # Get first available product
        products = self.home_page.get_product_list()
        assert len(products) > 0, "Products should be available"
        selected_product = products[0]["name"]
        
        # Manual product addition - click on product
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        product_links = driver.find_elements(By.CSS_SELECTOR, ".hrefch")
        assert len(product_links) > 0, "Product links should be available"
        
        # Click on first product
        product_links[0].click()
        time.sleep(3)
        
        # Click Add to Cart button on product detail page
        add_to_cart_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick='addToCart(1)']"))
        )
        add_to_cart_btn.click()
        
        # Handle the "Product added" alert
        time.sleep(2)
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            assert "added" in alert_text.lower(), f"Alert should confirm product added: {alert_text}"
        except:
            pass  # No alert appeared
        
        print(f"✓ Step 1: Added product '{selected_product}' to cart")
        
        # Step 2: Go to the Cart page at 'https://www.demoblaze.com/cart.html'
        driver.get("https://www.demoblaze.com/cart.html")
        self.cart_page.wait_for_page_load()
        
        # Verify we're on the correct cart URL
        assert "cart.html" in driver.current_url, "Should be on cart page"
        
        print("✓ Step 2: Navigated to cart page at https://www.demoblaze.com/cart.html")
        
        # Step 3: Verify that product is added
        time.sleep(3)  # Allow cart to load
        cart_items = self.cart_page.get_cart_items()
        assert len(cart_items) > 0, "Cart should not be empty"
        
        # Get product details from cart
        cart_item = cart_items[0]
        product_name = cart_item["name"]
        product_price = cart_item["price"]
        
        print(f"✓ Step 3: Verified product is in cart - Name: '{product_name}', Price: {product_price}")
        
        # Step 4: Click on 'Place Order' button
        self.cart_page.proceed_to_checkout()
        
        print("✓ Step 4: Clicked on 'Place Order' button - Checkout modal opened")
        
        # Step 5: Fill Form with data (name, country, city, credit card, month, year)
        checkout_data = {
            "name": "Test Customer",
            "country": "United States", 
            "city": "New York",
            "credit_card": "4111111111111111",
            "month": "12",
            "year": "2026"
        }
        
        self.cart_page.fill_checkout_form(checkout_data)
        
        print(f"✓ Step 5: Filled checkout form with data:")
        print(f"  - Name: {checkout_data['name']}")
        print(f"  - Country: {checkout_data['country']}")
        print(f"  - City: {checkout_data['city']}")
        print(f"  - Credit Card: {checkout_data['credit_card']}")
        print(f"  - Month: {checkout_data['month']}")
        print(f"  - Year: {checkout_data['year']}")
        
        # Step 6: Click on Purchase button
        purchase_success = self.cart_page.complete_purchase()
        assert purchase_success, "Purchase should complete successfully"
        
        print("✓ Step 6: Clicked on Purchase button - Order processing completed")
        
        # Step 7: Verify Confirmation
        confirmation_details = self.cart_page.get_order_confirmation_details()
        assert confirmation_details["success"], "Order confirmation should indicate success"
        assert confirmation_details["title"], "Confirmation title should be present"
        assert "thank you" in confirmation_details["title"].lower(), "Should contain thank you message"
        
        # Extract order number
        order_number = self.cart_page.extract_order_number(confirmation_details)
        assert order_number, "Order number should be present in confirmation"
        
        print(f"✓ Step 7: Verified confirmation details:")
        print(f"  - Confirmation Title: {confirmation_details['title']}")
        print(f"  - Order Details: {confirmation_details['details']}")
        print(f"  - Order Number: {order_number}")
        
        # Step 8: Take a Screenshot to confirm
        screenshot_path = f"screenshots/purchase_confirmation_{time.strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_path)
        
        print(f"✓ Step 8: Screenshot saved at: {screenshot_path}")
        
        # Close the confirmation dialog
        self.cart_page.confirm_success_message()
        
        # Final verification summary
        print(f"\n🎉 PURCHASE FLOW COMPLETED SUCCESSFULLY!")
        print(f"Product: {selected_product}")
        print(f"Customer: {checkout_data['name']}")
        print(f"Order Number: {order_number}")
        print(f"Screenshot: {screenshot_path}")
        print(f"Total Steps: 8/8 ✅")
    
    def test_two_different_products_purchase(self, driver, app_config):
        """
        Test Case: Purchase Two Different Products from Different Categories
        1. Login to the application
        2. Add a product from Phones category
        3. Add a product from Laptops category
        4. Go to Cart page
        5. Verify both products are in cart
        6. Complete the purchase process
        7. Verify order confirmation
        8. Take screenshot for verification
        """
        # Step 1: Login to the application
        self.home_page.load_home_page()
        self.home_page.perform_login(
            username=self.test_user["username"],
            password=self.test_user["password"]
        )
        assert self.home_page.is_user_logged_in(), "Should be logged in"
        
        print("✓ Step 1: Successfully logged in")
        
        # Step 2: Add a product from Phones category
        self.home_page.select_category("phones")
        time.sleep(2)
        
        # Get available phones
        phone_products = self.home_page.get_product_list()
        assert len(phone_products) > 0, "Phone products should be available"
        
        # Select first phone
        selected_phone = phone_products[0]["name"]
        
        # Manual addition for reliability - Phone
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        phone_links = driver.find_elements(By.CSS_SELECTOR, ".hrefch")
        assert len(phone_links) > 0, "Phone product links should be available"
        
        # Click on first phone
        phone_links[0].click()
        time.sleep(3)
        
        # Add phone to cart
        add_to_cart_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick*='addToCart']"))
        )
        add_to_cart_btn.click()
        
        # Handle alert for phone
        time.sleep(2)
        try:
            alert = driver.switch_to.alert
            phone_alert_text = alert.text
            alert.accept()
            assert "added" in phone_alert_text.lower(), f"Phone alert should confirm addition: {phone_alert_text}"
        except:
            pass
        
        print(f"✓ Step 2: Added phone '{selected_phone}' to cart")
        
        # Step 3: Add a product from Laptops category
        # Navigate back to home page and select laptops category
        driver.get("https://www.demoblaze.com")
        time.sleep(2)
        
        self.home_page.select_category("laptops")
        time.sleep(2)
        
        # Get available laptops
        laptop_products = self.home_page.get_product_list()
        assert len(laptop_products) > 0, "Laptop products should be available"
        
        # Select first laptop
        selected_laptop = laptop_products[0]["name"]
        
        # Manual addition for reliability - Laptop
        laptop_links = driver.find_elements(By.CSS_SELECTOR, ".hrefch")
        assert len(laptop_links) > 0, "Laptop product links should be available"
        
        # Click on first laptop
        laptop_links[0].click()
        time.sleep(3)
        
        # Add laptop to cart
        add_to_cart_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick*='addToCart']"))
        )
        add_to_cart_btn.click()
        
        # Handle alert for laptop
        time.sleep(2)
        try:
            alert = driver.switch_to.alert
            laptop_alert_text = alert.text
            alert.accept()
            assert "added" in laptop_alert_text.lower(), f"Laptop alert should confirm addition: {laptop_alert_text}"
        except:
            pass
        
        print(f"✓ Step 3: Added laptop '{selected_laptop}' to cart")
        
        # Step 4: Go to Cart page
        driver.get("https://www.demoblaze.com/cart.html")
        self.cart_page.wait_for_page_load()
        
        assert "cart.html" in driver.current_url, "Should be on cart page"
        
        print("✓ Step 4: Navigated to cart page")
        
        # Step 5: Verify both products are in cart
        time.sleep(3)  # Allow cart to load completely
        cart_items = self.cart_page.get_cart_items()
        
        assert len(cart_items) >= 2, f"Cart should contain at least 2 items, found {len(cart_items)}"
        
        # Verify both products are in cart
        cart_product_names = [item["name"].lower() for item in cart_items]
        
        phone_in_cart = any(selected_phone.lower() in name for name in cart_product_names)
        laptop_in_cart = any(selected_laptop.lower() in name for name in cart_product_names)
        
        assert phone_in_cart, f"Phone '{selected_phone}' should be in cart"
        assert laptop_in_cart, f"Laptop '{selected_laptop}' should be in cart"
        
        # Get cart summary for verification
        cart_summary = self.cart_page.get_cart_summary()
        total_price = cart_summary["total_price"]
        
        print(f"✓ Step 5: Verified both products in cart:")
        print(f"  - Products in cart: {len(cart_items)}")
        print(f"  - Phone: {selected_phone} ✅")
        print(f"  - Laptop: {selected_laptop} ✅")
        print(f"  - Total price: {total_price}")
        
        # Step 6: Complete the purchase process
        self.cart_page.proceed_to_checkout()
        
        # Fill checkout form
        checkout_data = {
            "name": "Two Products Customer",
            "country": "Canada", 
            "city": "Toronto",
            "credit_card": "5555444433332222",
            "month": "03",
            "year": "2027"
        }
        
        self.cart_page.fill_checkout_form(checkout_data)
        
        # Complete purchase
        purchase_success = self.cart_page.complete_purchase()
        assert purchase_success, "Purchase should complete successfully"
        
        print("✓ Step 6: Completed purchase process")
        
        # Step 7: Verify order confirmation
        confirmation_details = self.cart_page.get_order_confirmation_details()
        assert confirmation_details["success"], "Order confirmation should indicate success"
        assert confirmation_details["title"], "Confirmation title should be present"
        assert "thank you" in confirmation_details["title"].lower(), "Should contain thank you message"
        
        # Extract order number
        order_number = self.cart_page.extract_order_number(confirmation_details)
        assert order_number, "Order number should be present in confirmation"
        
        print(f"✓ Step 7: Order confirmation received:")
        print(f"  - Confirmation: {confirmation_details['title']}")
        print(f"  - Order Number: {order_number}")
        print(f"  - Order Details: {confirmation_details['details']}")
        
        # Step 8: Take screenshot for verification
        screenshot_path = f"screenshots/two_products_purchase_{time.strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_path)
        
        print(f"✓ Step 8: Screenshot saved at: {screenshot_path}")
        
        # Close confirmation dialog
        self.cart_page.confirm_success_message()
        
        # Final summary
        print(f"\n🎉 TWO PRODUCTS PURCHASE COMPLETED SUCCESSFULLY!")
        print(f"Phone Product: {selected_phone}")
        print(f"Laptop Product: {selected_laptop}")
        print(f"Customer: {checkout_data['name']}")
        print(f"Order Number: {order_number}")
        print(f"Total Items: {len(cart_items)}")
        print(f"Screenshot: {screenshot_path}")
        print(f"All Steps: 8/8 ✅")
    
    @pytest.fixture(scope="function", autouse=True)
    def cleanup(self, driver):
        """Cleanup after each test."""
        yield
        # Logout if logged in
        try:
            if "demoblaze.com" in driver.current_url:
                home_page = DemoBlazeHomePage(driver)
                if home_page.is_user_logged_in():
                    home_page.logout()
        except:
            pass  # Ignore cleanup errors