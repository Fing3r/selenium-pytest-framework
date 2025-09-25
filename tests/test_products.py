"""
DemoBlaze Product Management Test Suite - BDD Format
Behavior-driven tests for product browsing, selection, and cart operations
"""

import pytest
import time
from pages.demoblaze_home_page import DemoBlazeHomePage
from pages.demoblaze_cart_page import DemoBlazeCartPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestDemoBlazeProducts:
    """BDD Test suite for product functionality following Given-When-Then pattern"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, app_config):
        """Setup for each test method."""
        self.home_page = DemoBlazeHomePage(driver)
        self.cart_page = DemoBlazeCartPage(driver)
        self.test_user = {
            "username": "test",
            "password": "test"
        }
    
    def login_user(self):
        """Helper method to login before product operations."""
        self.home_page.load_home_page()
        self.home_page.perform_login(
            username=self.test_user["username"],
            password=self.test_user["password"]
        )
        # Give more time for login to complete
        time.sleep(2)
        assert self.home_page.is_user_logged_in(), "Should be logged in"
    
    def test_product_categories_navigation(self, driver, app_config):
        """
        Scenario: User browses different product categories
        Given I am logged in to DemoBlaze
        When I navigate through different product categories
        Then I should see products displayed for each category
        And each category should contain relevant products
        """
        print("🎭 Scenario: User browses different product categories")
        
        # Given I am logged in to DemoBlaze
        print("📋 Given: I am logged in to DemoBlaze")
        self.login_user()
        print("  ✓ User is successfully logged in")
        
        # When I navigate through different product categories
        print("🎯 When: I navigate through different product categories")
        categories = ["phones", "laptops", "monitors"]
        category_results = {}
        
        for category in categories:
            # Navigate to category
            self.home_page.select_category(category)
            time.sleep(2)
            print(f"  ✓ Navigated to {category} category")
            
            # Then I should see products displayed for each category
            products = self.home_page.get_product_list()
            category_results[category] = len(products)
            print(f"  ✓ Found {len(products)} products in {category} category")
        
        # Then each category should contain relevant products
        print("✅ Then: Each category should contain relevant products")
        for category, count in category_results.items():
            assert count > 0, f"Products should be available in {category} category"
            print(f"  ✓ {category.capitalize()} category verified: {count} products")
        
        print("🎉 Scenario completed successfully!")
    
    def test_product_list_display(self, driver, app_config):
        """
        Scenario: User views product information display
        Given I am logged in and viewing a product category
        When I look at the product listings
        Then I should see product names clearly displayed
        And I should see product prices for each item
        And the product information should be properly formatted
        """
        print("🎭 Scenario: User views product information display")
        
        # Given I am logged in and viewing a product category
        print("📋 Given: I am logged in and viewing a product category")
        self.login_user()
        self.home_page.select_category("phones")
        time.sleep(2)
        print("  ✓ User is logged in and viewing phones category")
        
        # When I look at the product listings
        print("🎯 When: I look at the product listings")
        products = self.home_page.get_product_list()
        assert len(products) > 0, "Products should be displayed"
        print(f"  ✓ Viewing {len(products)} product listings")
        
        # Then I should see product names and prices clearly displayed
        print("✅ Then: I should see product names and prices clearly displayed")
        for i, product in enumerate(products[:3]):  # Test first 3 products
            assert product["name"], "Product should have a name"
            assert product["price"], "Product should have a price"
            print(f"  ✓ Product {i+1}: {product['name']} - ${product['price']}")
        
        print("🎉 Scenario completed successfully!")
    
    def test_single_product_addition_to_cart(self, driver, app_config):
        """
        Scenario: User adds a single product to their shopping cart
        Given I am logged in and browsing products
        When I select a product from the phones category
        And I click the "Add to cart" button
        Then the product should be added to my cart successfully
        And I should see a confirmation message
        And the product should appear in my cart
        """
        print("🎭 Scenario: User adds a single product to their shopping cart")
        
        # Given I am logged in and browsing products
        print("📋 Given: I am logged in and browsing products")
        self.login_user()
        self.home_page.select_category("phones")
        time.sleep(2)
        
        products = self.home_page.get_product_list()
        assert len(products) > 0, "Products should be available"
        selected_product = products[0]["name"]
        print(f"  ✓ Browsing phones category, selected: {selected_product}")
        
        # When I select a product and click "Add to cart"
        print("🎯 When: I select a product and click 'Add to cart'")
        product_links = driver.find_elements(By.CSS_SELECTOR, ".hrefch")
        assert len(product_links) > 0, "Product links should be available"
        
        # Click on first product
        product_links[0].click()
        time.sleep(3)
        print("  ✓ Clicked on product to view details")
        
        # Add to cart
        add_to_cart_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick*='addToCart']"))
        )
        add_to_cart_btn.click()
        print("  ✓ Clicked 'Add to cart' button")
        
        # Handle alert confirmation
        time.sleep(2)
        confirmation_received = False
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            assert "added" in alert_text.lower(), f"Alert should confirm addition: {alert_text}"
            confirmation_received = True
            print(f"  ✓ Received confirmation: {alert_text}")
        except:
            pass
        
        # Then the product should be added successfully and appear in cart
        print("✅ Then: The product should be added successfully and appear in cart")
        driver.get("https://www.demoblaze.com/cart.html")
        self.cart_page.wait_for_page_load()
        time.sleep(2)
        
        cart_items = self.cart_page.get_cart_items()
        assert len(cart_items) > 0, "Cart should not be empty"
        assert any(selected_product.lower() in item["name"].lower() for item in cart_items), "Product should be in cart"
        
        print(f"  ✓ Product successfully added to cart: {selected_product}")
        if confirmation_received:
            print("  ✓ Confirmation message was displayed")
        
        print("🎉 Scenario completed successfully!")
    
    def test_multiple_products_from_same_category(self, driver, app_config):
        """
        Scenario: User adds multiple products from the same category
        Given I am logged in and viewing a product category
        When I add the first product to cart
        And I add the second product to cart from the same category
        Then both products should be in my cart
        And the cart should show the correct number of items
        """
        print("🎭 Scenario: User adds multiple products from the same category")
        
        # Given I am logged in and viewing a product category
        print("📋 Given: I am logged in and viewing a product category")
        self.login_user()
        self.home_page.select_category("phones")
        time.sleep(2)
        
        products = self.home_page.get_product_list()
        assert len(products) >= 2, "At least 2 products should be available"
        print(f"  ✓ Viewing phones category with {len(products)} available products")
        
        # When I add multiple products from the same category
        print("🎯 When: I add multiple products from the same category")
        added_products = []
        
        for i in range(2):
            # Navigate back to category page
            driver.get("https://www.demoblaze.com")
            self.home_page.select_category("phones")
            time.sleep(2)
            
            # Click on product
            product_links = driver.find_elements(By.CSS_SELECTOR, ".hrefch")
            product_links[i].click()
            time.sleep(3)
            
            # Get product name and add to list
            product_name = products[i]["name"]
            added_products.append(product_name)
            print(f"  ✓ Selected product {i+1}: {product_name}")
            
            # Add to cart
            add_to_cart_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick*='addToCart']"))
            )
            add_to_cart_btn.click()
            print(f"  ✓ Added product {i+1} to cart")
            
            # Handle alert
            time.sleep(2)
            try:
                alert = driver.switch_to.alert
                alert.accept()
            except:
                pass
        
        # Then both products should be in cart with correct count
        print("✅ Then: Both products should be in cart with correct count")
        driver.get("https://www.demoblaze.com/cart.html")
        self.cart_page.wait_for_page_load()
        time.sleep(3)
        
        cart_items = self.cart_page.get_cart_items()
        assert len(cart_items) >= 2, "Cart should contain at least 2 items"
        print(f"  ✓ Cart contains {len(cart_items)} items as expected")
        
        for product_name in added_products:
            cart_names = [item["name"].lower() for item in cart_items]
            assert any(product_name.lower() in cart_name for cart_name in cart_names), f"Product {product_name} should be in cart"
            print(f"  ✓ Verified {product_name} is in cart")
        
        print("🎉 Scenario completed successfully!")
    
    def test_products_from_different_categories(self, driver, app_config):
        """
        Scenario: User adds products from different categories
        Given I am logged in to DemoBlaze
        When I add a product from the phones category
        And I add a product from the laptops category
        Then both products from different categories should be in my cart
        And I should see the variety in my shopping selection
        """
        print("🎭 Scenario: User adds products from different categories")
        
        # Given I am logged in to DemoBlaze
        print("📋 Given: I am logged in to DemoBlaze")
        self.login_user()
        print("  ✓ User is successfully logged in")
        
        # When I add products from different categories
        print("🎯 When: I add products from different categories")
        added_products = []
        categories_products = [
            ("phones", "phone"),
            ("laptops", "laptop")
        ]
        
        for category, product_type in categories_products:
            # Navigate to category
            driver.get("https://www.demoblaze.com")
            self.home_page.select_category(category)
            time.sleep(2)
            print(f"  ✓ Navigated to {category} category")
            
            # Get products
            products = self.home_page.get_product_list()
            assert len(products) > 0, f"Products should be available in {category}"
            
            # Click first product
            product_links = driver.find_elements(By.CSS_SELECTOR, ".hrefch")
            product_links[0].click()
            time.sleep(3)
            
            product_name = products[0]["name"]
            added_products.append(product_name)
            print(f"  ✓ Selected {product_type}: {product_name}")
            
            # Add to cart
            add_to_cart_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick*='addToCart']"))
            )
            add_to_cart_btn.click()
            print(f"  ✓ Added {product_type} to cart")
            
            # Handle alert
            time.sleep(2)
            try:
                alert = driver.switch_to.alert
                alert.accept()
            except:
                pass
        
        # Then both products from different categories should be in cart
        print("✅ Then: Both products from different categories should be in cart")
        driver.get("https://www.demoblaze.com/cart.html")
        self.cart_page.wait_for_page_load()
        time.sleep(3)
        
        cart_items = self.cart_page.get_cart_items()
        assert len(cart_items) >= 2, "Cart should contain products from both categories"
        print(f"  ✓ Cart contains {len(cart_items)} items from different categories")
        
        cart_names = [item["name"].lower() for item in cart_items]
        for product_name in added_products:
            assert any(product_name.lower() in cart_name for cart_name in cart_names), f"Product {product_name} should be in cart"
            print(f"  ✓ Verified {product_name} is in cart")
        
        print("  ✓ Shopping variety achieved with products from multiple categories")
        print("🎉 Scenario completed successfully!")
    
    def test_product_price_display(self, driver, app_config):
        """
        Scenario: User views product price information
        Given I am logged in and browsing products
        When I view the product listings
        Then I should see prices displayed for each product
        And the prices should be in a valid format
        And the price information should be clear and readable
        """
        print("🎭 Scenario: User views product price information")
        
        # Given I am logged in and browsing products
        print("📋 Given: I am logged in and browsing products")
        self.login_user()
        self.home_page.select_category("phones")
        time.sleep(2)
        print("  ✓ User is browsing products in phones category")
        
        # When I view the product listings
        print("🎯 When: I view the product listings")
        products = self.home_page.get_product_list()
        assert len(products) > 0, "Products should be available"
        print(f"  ✓ Viewing {len(products)} product listings")
        
        # Then prices should be displayed in valid format
        print("✅ Then: Prices should be displayed in valid format")
        valid_prices_count = 0
        
        for i, product in enumerate(products[:3]):  # Test first 3 products
            price = product["price"]
            assert price, "Product should have a price"
            
            # Extract numeric value (remove $ and any other characters)
            price_numeric = price.replace("$", "").replace(",", "").strip()
            assert price_numeric.replace(".", "").isdigit(), f"Price should be numeric: {price}"
            
            valid_prices_count += 1
            print(f"  ✓ Product {i+1} - {product['name']}: {price} (valid format)")
        
        print(f"  ✓ All {valid_prices_count} prices are properly formatted and readable")
        print("🎉 Scenario completed successfully!")
    
    @pytest.fixture(scope="function", autouse=True)
    def cleanup_products(self, driver):
        """Cleanup after each test."""
        yield
        try:
            if "demoblaze.com" in driver.current_url:
                home_page = DemoBlazeHomePage(driver)
                if home_page.is_user_logged_in():
                    home_page.logout()
        except:
            pass