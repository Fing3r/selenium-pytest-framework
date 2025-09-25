"""
DemoBlaze Cart Page Object - Enhanced for E-commerce Testing
Auto-generated and customized for comprehensive cart functionality
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
import time


class DemoBlazeCartPage(BasePage):
    """Page Object for DemoBlaze Shopping Cart functionality"""
    
    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)
        self.url = "https://www.demoblaze.com/cart.html"
    
    # Locators
    CART_ITEMS = (By.CSS_SELECTOR, "#tbodyid tr")
    CART_ITEM_NAME = (By.CSS_SELECTOR, "td:nth-child(2)")
    CART_ITEM_PRICE = (By.CSS_SELECTOR, "td:nth-child(3)")
    DELETE_BUTTONS = (By.CSS_SELECTOR, "td:nth-child(4) a")
    TOTAL_PRICE = (By.ID, "totalp")
    PLACE_ORDER_BTN = (By.CSS_SELECTOR, "button[data-target='#orderModal']")
    
    # Checkout Modal Elements
    ORDER_MODAL = (By.ID, "orderModal")
    NAME_INPUT = (By.ID, "name")
    COUNTRY_INPUT = (By.ID, "country")
    CITY_INPUT = (By.ID, "city")
    CREDIT_CARD_INPUT = (By.ID, "card")
    MONTH_INPUT = (By.ID, "month")
    YEAR_INPUT = (By.ID, "year")
    PURCHASE_BUTTON = (By.CSS_SELECTOR, "button[onclick='purchaseOrder()']")
    CLOSE_MODAL_BTN = (By.CSS_SELECTOR, "#orderModal .btn-secondary")
    
    # Success Elements
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".sweet-alert")
    SUCCESS_MESSAGE_TEXT = (By.CSS_SELECTOR, ".sweet-alert h2")
    SUCCESS_DETAILS = (By.CSS_SELECTOR, ".sweet-alert p")
    CONFIRM_SUCCESS_BTN = (By.CSS_SELECTOR, ".confirm")
    
    def load_cart_page(self):
        """Navigate to the cart page."""
        self.driver.get(self.url)
        self.wait_for_page_load()
        return self
    
    def wait_for_page_load(self):
        """Wait for cart page to load completely."""
        try:
            # Wait for either the cart table or a general page element
            WebDriverWait(self.driver, self.timeout).until(
                EC.any_of(
                    EC.presence_of_element_located((By.ID, "tbodyid")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".table")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
                )
            )
            time.sleep(2)  # Allow for dynamic content
        except TimeoutException:
            # If specific elements don't load, just wait for basic page structure
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            except TimeoutException:
                raise Exception("Cart page failed to load")
    
    def get_cart_items(self):
        """Get all items in the cart with their details."""
        items = []
        try:
            cart_rows = self.driver.find_elements(*self.CART_ITEMS)
            for row in cart_rows:
                if row.find_elements(By.TAG_NAME, "td"):
                    name_element = row.find_element(*self.CART_ITEM_NAME)
                    price_element = row.find_element(*self.CART_ITEM_PRICE)
                    
                    item_data = {
                        "name": name_element.text.strip(),
                        "price": price_element.text.strip(),
                        "element": row
                    }
                    items.append(item_data)
        except NoSuchElementException:
            pass  # Cart might be empty
        
        return items
    
    def get_cart_item_count(self):
        """Get the number of items in the cart."""
        return len(self.get_cart_items())
    
    def get_total_price(self):
        """Get the total price displayed in the cart."""
        try:
            total_element = self.wait_for_element_visible(self.TOTAL_PRICE)
            return total_element.text.strip()
        except TimeoutException:
            return "0"
    
    def verify_item_in_cart(self, product_name):
        """Verify that a specific product is in the cart."""
        cart_items = self.get_cart_items()
        for item in cart_items:
            if product_name.lower() in item["name"].lower():
                return True
        return False
    
    def verify_cart_total_calculation(self):
        """Verify that the cart total matches the sum of individual items."""
        items = self.get_cart_items()
        calculated_total = 0
        
        for item in items:
            # Extract numeric value from price (remove $ and any other characters)
            price_text = item["price"].replace("$", "").replace(",", "").strip()
            try:
                price = float(price_text)
                calculated_total += price
            except ValueError:
                continue
        
        displayed_total_text = self.get_total_price().replace("$", "").replace(",", "").strip()
        try:
            displayed_total = float(displayed_total_text)
            return abs(calculated_total - displayed_total) < 0.01  # Account for rounding
        except ValueError:
            return False
    
    def remove_item_from_cart(self, product_name):
        """Remove a specific item from the cart."""
        items = self.get_cart_items()
        for item in items:
            if product_name.lower() in item["name"].lower():
                delete_btn = item["element"].find_element(*self.DELETE_BUTTONS)
                delete_btn.click()
                time.sleep(2)  # Wait for removal
                return True
        return False
    
    def proceed_to_checkout(self):
        """Click the Place Order button to start checkout."""
        place_order_btn = self.wait_for_element_clickable(self.PLACE_ORDER_BTN)
        place_order_btn.click()
        
        # Wait for modal to appear
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.ORDER_MODAL)
        )
        return self
    
    def fill_checkout_form(self, customer_info):
        """Fill the checkout form with customer information."""
        # Wait for modal to be fully loaded
        self.wait_for_element_visible(self.ORDER_MODAL)
        
        # Fill form fields
        name_field = self.wait_for_element_visible(self.NAME_INPUT)
        name_field.clear()
        name_field.send_keys(customer_info.get("name", ""))
        
        country_field = self.wait_for_element_visible(self.COUNTRY_INPUT)
        country_field.clear()
        country_field.send_keys(customer_info.get("country", ""))
        
        city_field = self.wait_for_element_visible(self.CITY_INPUT)
        city_field.clear()
        city_field.send_keys(customer_info.get("city", ""))
        
        card_field = self.wait_for_element_visible(self.CREDIT_CARD_INPUT)
        card_field.clear()
        card_field.send_keys(customer_info.get("credit_card", ""))
        
        month_field = self.wait_for_element_visible(self.MONTH_INPUT)
        month_field.clear()
        month_field.send_keys(customer_info.get("month", ""))
        
        year_field = self.wait_for_element_visible(self.YEAR_INPUT)
        year_field.clear()
        year_field.send_keys(customer_info.get("year", ""))
        
        return self
    
    def complete_purchase(self):
        """Complete the purchase by clicking the Purchase button."""
        purchase_btn = self.wait_for_element_clickable(self.PURCHASE_BUTTON)
        purchase_btn.click()
        
        # Wait for success message
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.SUCCESS_MESSAGE)
            )
            return True
        except TimeoutException:
            return False
    
    def get_order_confirmation_details(self):
        """Extract order confirmation details from success message."""
        try:
            success_element = self.wait_for_element_visible(self.SUCCESS_MESSAGE)
            
            # Get the main message
            title_element = success_element.find_element(*self.SUCCESS_MESSAGE_TEXT)
            title = title_element.text if title_element else ""
            
            # Get the details (contains order info)
            details_element = success_element.find_element(*self.SUCCESS_DETAILS)
            details = details_element.text if details_element else ""
            
            return {
                "title": title,
                "details": details,
                "success": "Thank you for your purchase!" in title
            }
        except (TimeoutException, NoSuchElementException):
            return {"title": "", "details": "", "success": False}
    
    def extract_order_number(self, confirmation_details):
        """Extract order number/ID from confirmation details."""
        details_text = confirmation_details.get("details", "")
        
        # Look for common patterns for order numbers
        import re
        patterns = [
            r"Id:\s*(\d+)",
            r"Order.*?(\d+)",
            r"#(\d+)",
            r"ID:\s*(\d+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, details_text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def confirm_success_message(self):
        """Click OK on the success message to close it."""
        try:
            confirm_btn = self.wait_for_element_clickable(self.CONFIRM_SUCCESS_BTN)
            confirm_btn.click()
            time.sleep(1)
            return True
        except TimeoutException:
            return False
    
    def is_cart_empty(self):
        """Check if the cart is empty."""
        return self.get_cart_item_count() == 0
    
    def get_cart_summary(self):
        """Get a complete summary of the cart contents."""
        items = self.get_cart_items()
        total = self.get_total_price()
        
        return {
            "items": items,
            "item_count": len(items),
            "total_price": total,
            "is_empty": len(items) == 0
        }