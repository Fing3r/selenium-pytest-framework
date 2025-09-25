"""
DemoBlaze Test Data Configuration
Contains test data for e-commerce testing scenarios
"""

# Test User Credentials
# Note: For real testing, you would need to register these users first
# or use existing valid credentials
TEST_USERS = {
    "valid_user": {
        "username": "test",
        "password": "test"
    },
    "admin_user": {
        "username": "admin",
        "password": "admin123"
    }
}

# Customer Information for Checkout
CUSTOMER_DATA = {
    "customer1": {
        "name": "John Doe",
        "country": "United States",
        "city": "New York",
        "credit_card": "4111111111111111",
        "month": "12",
        "year": "2025"
    },
    "customer2": {
        "name": "Jane Smith",
        "country": "Canada",
        "city": "Toronto",
        "credit_card": "5555555555554444",
        "month": "06",
        "year": "2026"
    },
    "international_customer": {
        "name": "Carlos Rodriguez",
        "country": "Mexico",
        "city": "Mexico City",
        "credit_card": "378282246310005",
        "month": "03",
        "year": "2027"
    }
}

# Product Categories for Testing
PRODUCT_CATEGORIES = {
    "phones": [
        "Samsung galaxy s6",
        "Nokia lumia 1520",
        "Nexus 6",
        "Samsung galaxy s7",
        "Iphone 6 32gb",
        "Sony xperia z5",
        "HTC One M9"
    ],
    "laptops": [
        "Sony vaio i5",
        "Sony vaio i7",
        "MacBook air",
        "Dell i7 8gb",
        "2017 Dell 15.6 Inch",
        "MacBook Pro"
    ],
    "monitors": [
        "Apple monitor 24",
        "ASUS Full HD"
    ]
}

# Test Scenarios Configuration
TEST_CONFIG = {
    "default_timeout": 10,
    "page_load_timeout": 15,
    "explicit_wait_timeout": 10,
    "products_to_add_to_cart": 2,
    "retry_attempts": 3
}

# Expected Messages and Validations
EXPECTED_MESSAGES = {
    "add_to_cart_success": "Product added",
    "login_success_indicator": "Welcome",
    "purchase_success": "Thank you for your purchase!",
    "empty_cart_message": "",  # DemoBlaze doesn't show specific message for empty cart
    "invalid_login": "User does not exist"
}

# URL Endpoints
URLS = {
    "base_url": "https://www.demoblaze.com",
    "home": "https://www.demoblaze.com/index.html",
    "cart": "https://www.demoblaze.com/cart.html"
}

# Browser-specific configurations
BROWSER_CONFIG = {
    "chrome": {
        "window_size": "1920,1080",
        "headless": False
    },
    "firefox": {
        "window_size": "1920,1080", 
        "headless": False
    }
}