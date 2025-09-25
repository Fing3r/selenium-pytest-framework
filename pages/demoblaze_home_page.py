"""
DemoBlaze Home Page Object - Enhanced for E-commerce Testing
Customized for login, product browsing, and cart functionality
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from pages.base_page import BasePage
import time
import random


class DemoBlazeHomePage(BasePage):
    """Enhanced Page Object for DemoBlaze main functionality"""
    
    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)
        self.url = "https://www.demoblaze.com"
    
    # Navigation Elements
    HOME_LINK = (By.CSS_SELECTOR, "a.nav-link[href='index.html']")
    CONTACT_LINK = (By.CSS_SELECTOR, "a.nav-link[data-target='#exampleModal']")
    ABOUT_US_LINK = (By.CSS_SELECTOR, "a.nav-link[data-target='#videoModal']")
    CART_LINK = (By.ID, "cartur")
    LOGIN_LINK = (By.ID, "login2")
    SIGN_UP_LINK = (By.ID, "signin2")
    LOGOUT_LINK = (By.ID, "logout2")
    USERNAME_DISPLAY = (By.ID, "nameofuser")
    
    # Login Modal Elements
    LOGIN_MODAL = (By.ID, "logInModal")
    LOGIN_USERNAME_INPUT = (By.ID, "loginusername")
    LOGIN_PASSWORD_INPUT = (By.ID, "loginpassword")
    LOGIN_SUBMIT_BTN = (By.CSS_SELECTOR, "button[onclick='logIn()']")
    LOGIN_CLOSE_BTN = (By.CSS_SELECTOR, "#logInModal .btn-secondary")
    
    # Sign Up Modal Elements
    SIGNUP_MODAL = (By.ID, "signInModal")
    SIGNUP_USERNAME_INPUT = (By.ID, "sign-username")
    SIGNUP_PASSWORD_INPUT = (By.ID, "sign-password")
    SIGNUP_SUBMIT_BTN = (By.CSS_SELECTOR, "button[onclick='register()']")
    SIGNUP_CLOSE_BTN = (By.CSS_SELECTOR, "#signInModal .btn-secondary")
    
    # Product Categories
    CATEGORIES_SECTION = (By.ID, "cat")
    PHONES_CATEGORY = (By.CSS_SELECTOR, "a[onclick*='phone']")
    LAPTOPS_CATEGORY = (By.CSS_SELECTOR, "a[onclick*='notebook']")
    MONITORS_CATEGORY = (By.CSS_SELECTOR, "a[onclick*='monitor']")
    
    # Product Listings
    PRODUCTS_CONTAINER = (By.ID, "tbodyid")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".card.h-100")
    PRODUCT_TITLES = (By.CSS_SELECTOR, ".card-title a")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".card-text")
    PRODUCT_IMAGES = (By.CSS_SELECTOR, ".card-img-top")
    
    # Pagination
    PREVIOUS_BTN = (By.ID, "prev2")
    NEXT_BTN = (By.ID, "next2")
    
    # Product Detail Page Elements (when viewing individual products)
    PRODUCT_NAME = (By.CSS_SELECTOR, ".name")
    PRODUCT_PRICE_DETAIL = (By.CSS_SELECTOR, ".price-container")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "a[onclick*='addToCart']")
    
    def load_home_page(self):
        """Navigate to the home page."""
        self.driver.get(self.url)
        self.wait_for_page_load()
        return self
    
    def wait_for_page_load(self):
        """Wait for home page to load completely."""
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(self.PRODUCTS_CONTAINER)
            )
            time.sleep(2)  # Allow for dynamic content and images
        except TimeoutException:
            raise Exception("Home page failed to load")
    
    def open_login_modal(self):
        """Open the login modal dialog."""
        login_link = self.wait_for_element_clickable(self.LOGIN_LINK)
        login_link.click()
        
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.LOGIN_MODAL)
        )
        return self
    
    def perform_login(self, username, password):
        """Perform login with given credentials."""
        self.open_login_modal()
        
        # Fill login form
        username_field = self.wait_for_element_visible(self.LOGIN_USERNAME_INPUT)
        username_field.clear()
        username_field.send_keys(username)
        
        password_field = self.wait_for_element_visible(self.LOGIN_PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)
        
        # Submit login
        login_btn = self.wait_for_element_clickable(self.LOGIN_SUBMIT_BTN)
        login_btn.click()
        
        # Wait a moment for login to process
        time.sleep(3)
        
        return self
    
    def is_user_logged_in(self):
        """Check if user is currently logged in."""
        try:
            username_element = self.driver.find_element(*self.USERNAME_DISPLAY)
            logout_element = self.driver.find_element(*self.LOGOUT_LINK)
            
            # Check if elements are visible and have text
            return (username_element.is_displayed() and 
                   logout_element.is_displayed() and 
                   "Welcome" in username_element.text)
        except NoSuchElementException:
            return False
    
    def get_logged_in_username(self):
        """Get the displayed username for logged-in user."""
        try:
            if self.is_user_logged_in():
                username_element = self.driver.find_element(*self.USERNAME_DISPLAY)
                # Extract username from "Welcome [username]" text
                welcome_text = username_element.text
                return welcome_text.replace("Welcome ", "").strip()
        except NoSuchElementException:
            pass
        return None
    
    def logout(self):
        """Perform logout."""
        if self.is_user_logged_in():
            logout_btn = self.wait_for_element_clickable(self.LOGOUT_LINK)
            logout_btn.click()
            time.sleep(2)  # Wait for logout to process
        return self
    
    def select_category(self, category_name):
        """Select a product category."""
        category_map = {
            "phones": self.PHONES_CATEGORY,
            "laptops": self.LAPTOPS_CATEGORY,
            "monitors": self.MONITORS_CATEGORY
        }
        
        category_locator = category_map.get(category_name.lower())
        if category_locator:
            category_link = self.wait_for_element_clickable(category_locator)
            category_link.click()
            time.sleep(3)  # Wait for products to load
        return self
    
    def get_product_list(self):
        """Get list of products currently displayed."""
        products = []
        try:
            product_elements = self.driver.find_elements(*self.PRODUCT_ITEMS)
            
            for product_element in product_elements:
                try:
                    title_element = product_element.find_element(*self.PRODUCT_TITLES)
                    price_element = product_element.find_element(*self.PRODUCT_PRICES)
                    
                    product_data = {
                        "name": title_element.text.strip(),
                        "price": price_element.text.strip(),
                        "element": product_element,
                        "link": title_element.get_attribute("href")
                    }
                    products.append(product_data)
                except NoSuchElementException:
                    continue
        except NoSuchElementException:
            pass
        
        return products
    
    def click_product(self, product_name):
        """Click on a specific product to view details."""
        products = self.get_product_list()
        
        for product in products:
            if product_name.lower() in product["name"].lower():
                title_link = product["element"].find_element(*self.PRODUCT_TITLES)
                title_link.click()
                time.sleep(3)  # Wait for product detail page
                return True
        
        return False
    
    def add_product_to_cart(self, product_name):
        """Add a specific product to cart."""
        # First click on the product to go to detail page
        if self.click_product(product_name):
            try:
                # Wait for product detail page to load
                add_to_cart_btn = WebDriverWait(self.driver, self.timeout).until(
                    EC.element_to_be_clickable(self.ADD_TO_CART_BTN)
                )
                
                # Click add to cart
                add_to_cart_btn.click()
                
                # Handle alert if present
                time.sleep(2)
                try:
                    alert = self.driver.switch_to.alert
                    alert_text = alert.text
                    alert.accept()
                    
                    # Navigate back to home
                    self.load_home_page()
                    
                    return "added successfully" in alert_text.lower()
                except:
                    # No alert, navigate back to home
                    self.load_home_page()
                    return True
                    
            except TimeoutException:
                return False
        
        return False
    
    def add_random_products_to_cart(self, count=2):
        """Add random products to cart for testing."""
        self.load_home_page()
        
        products = self.get_product_list()
        if len(products) < count:
            # If not enough products, load more or use all available
            count = len(products)
        
        selected_products = random.sample(products, count)
        added_products = []
        
        for product in selected_products:
            if self.add_product_to_cart(product["name"]):
                added_products.append(product["name"])
        
        return added_products
    
    def navigate_to_cart(self):
        """Navigate to shopping cart."""
        cart_link = self.wait_for_element_clickable(self.CART_LINK)
        cart_link.click()
        time.sleep(3)  # Wait for cart page to load
        return self
    
    def get_cart_item_count_from_navbar(self):
        """Get cart item count if displayed in navbar (site-specific implementation)."""
        # DemoBlaze doesn't show count in navbar, so we navigate to cart to count
        current_url = self.driver.current_url
        self.navigate_to_cart()
        
        # Import and use cart page to get count
        from pages.demoblaze_cart_page import DemoBlazeCartPage
        cart_page = DemoBlazeCartPage(self.driver)
        count = cart_page.get_cart_item_count()
        
        # Navigate back if we weren't already on cart page
        if "cart.html" not in current_url:
            self.driver.back()
            time.sleep(2)
        
        return count
    
    def search_product(self, product_name):
        """Search for a product in the current listing."""
        products = self.get_product_list()
        matching_products = []
        
        for product in products:
            if product_name.lower() in product["name"].lower():
                matching_products.append(product)
        
        return matching_products
    
    def wait_for_products_to_load(self):
        """Wait for product listings to load."""
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(self.PRODUCT_ITEMS)
            )
            time.sleep(2)  # Additional wait for all products
        except TimeoutException:
            raise Exception("Products failed to load")
    
    def get_page_title(self):
        """Get the page title."""
        return self.driver.title
    
    def verify_home_page_loaded(self):
        """Verify that home page has loaded successfully."""
        try:
            # Check for key elements
            products_container = self.driver.find_element(*self.PRODUCTS_CONTAINER)
            navbar = self.driver.find_element(By.CSS_SELECTOR, ".navbar")
            
            return (products_container.is_displayed() and 
                   navbar.is_displayed() and
                   "STORE" in self.driver.title)
        except NoSuchElementException:
            return False