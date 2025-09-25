"""
Browser Factory Module

This module contains the BrowserFactory class for managing browser instances
with support for Chrome and Firefox browsers.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import logging
from typing import Optional


class BrowserFactory:
    """Factory class for creating and managing browser instances."""
    
    @staticmethod
    def get_browser(browser_name: str = "chrome", headless: bool = False, 
                   window_size: tuple = (1920, 1080)) -> webdriver.Remote:
        """
        Create and return a browser instance based on the browser name.
        
        Args:
            browser_name (str): Name of the browser ('chrome' or 'firefox')
            headless (bool): Whether to run browser in headless mode
            window_size (tuple): Browser window size (width, height)
            
        Returns:
            webdriver.Remote: Browser instance
            
        Raises:
            ValueError: If unsupported browser name is provided
        """
        browser_name = browser_name.lower()
        
        if browser_name == "chrome":
            return BrowserFactory._create_chrome_browser(headless, window_size)
        elif browser_name == "firefox":
            return BrowserFactory._create_firefox_browser(headless, window_size)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}. "
                           "Supported browsers are 'chrome' and 'firefox'")
    
    @staticmethod
    def _create_chrome_browser(headless: bool = False, 
                              window_size: tuple = (1920, 1080)) -> webdriver.Chrome:
        """
        Create Chrome browser instance with optimized settings.
        
        Args:
            headless (bool): Whether to run browser in headless mode
            window_size (tuple): Browser window size (width, height)
            
        Returns:
            webdriver.Chrome: Chrome browser instance
        """
        chrome_options = ChromeOptions()
        
        # Performance optimizations
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        
        # Window management
        chrome_options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
        
        # Headless mode
        if headless:
            chrome_options.add_argument("--headless")
        
        # Additional stability options
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--ignore-certificate-errors")
        
        # Remove automation indicators
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.maximize_window()
            logging.info("Chrome browser initialized successfully")
            return driver
        except Exception as e:
            logging.error(f"Failed to initialize Chrome browser: {str(e)}")
            raise
    
    @staticmethod
    def _create_firefox_browser(headless: bool = False, 
                               window_size: tuple = (1920, 1080)) -> webdriver.Firefox:
        """
        Create Firefox browser instance with optimized settings for CI/CD environments.
        
        Args:
            headless (bool): Whether to run browser in headless mode
            window_size (tuple): Browser window size (width, height)
            
        Returns:
            webdriver.Firefox: Firefox browser instance
        """
        firefox_options = FirefoxOptions()
        
        # Essential CI/CD environment settings
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--disable-software-rasterizer")
        
        # Headless mode (always enable in CI, force headless if environment variable is set)
        import os
        if headless or os.getenv('HEADLESS') == 'true' or os.getenv('CI'):
            firefox_options.add_argument("--headless")
            logging.info("Firefox running in headless mode")
        
        # Window management - set before starting for consistent behavior
        firefox_options.add_argument(f"--width={window_size[0]}")
        firefox_options.add_argument(f"--height={window_size[1]}")
        
        # Performance optimizations
        firefox_options.set_preference("browser.cache.disk.enable", False)
        firefox_options.set_preference("browser.cache.memory.enable", False)
        firefox_options.set_preference("browser.cache.offline.enable", False)
        firefox_options.set_preference("network.http.use-cache", False)
        firefox_options.set_preference("permissions.default.image", 2)  # Block images for speed
        firefox_options.set_preference("javascript.enabled", False)  # Disable JS if not needed
        
        # Marionette and connection stability settings
        firefox_options.set_preference("marionette.port", 2828)  # Fixed port to avoid conflicts
        firefox_options.set_preference("marionette.log.level", "Info")
        firefox_options.set_preference("remote.log.level", "Info")
        
        # Security and stability preferences for CI environments
        firefox_options.set_preference("security.tls.insecure_fallback_hosts", "localhost")
        firefox_options.set_preference("security.tls.hello_downgrade_check", False)
        firefox_options.set_preference("browser.safebrowsing.enabled", False)
        firefox_options.set_preference("browser.safebrowsing.malware.enabled", False)
        
        # Disable update checks and crash reporting
        firefox_options.set_preference("app.update.enabled", False)
        firefox_options.set_preference("app.update.auto", False)
        firefox_options.set_preference("toolkit.crashreporter.enabled", False)
        firefox_options.set_preference("datareporting.healthreport.uploadEnabled", False)
        
        # Media and notification preferences for CI stability
        firefox_options.set_preference("media.volume_scale", "0.0")
        firefox_options.set_preference("dom.push.enabled", False)
        firefox_options.set_preference("dom.webnotifications.enabled", False)
        
        # Profile directory settings for CI environments
        firefox_options.set_preference("browser.download.folderList", 2)
        firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
        firefox_options.set_preference("browser.download.dir", "/tmp")
        
        try:
            # Create service with additional timeout for CI environments
            service = FirefoxService(
                executable_path=GeckoDriverManager().install(),
                log_path="/tmp/geckodriver.log"
            )
            
            # Create Firefox instance with extended timeout
            driver = webdriver.Firefox(service=service, options=firefox_options)
            
            # Set timeouts for stability
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)
            
            # Maximize window after creation for consistency
            try:
                driver.maximize_window()
            except Exception as e:
                logging.warning(f"Could not maximize Firefox window: {e}")
                # Fallback to manual window sizing
                driver.set_window_size(window_size[0], window_size[1])
            
            logging.info("Firefox browser initialized successfully for CI/CD environment")
            return driver
            
        except Exception as e:
            logging.error(f"Failed to initialize Firefox browser: {str(e)}")
            # Log additional debugging information
            logging.error("Firefox initialization failed. Common causes in CI:")
            logging.error("1. Missing system dependencies (X11 libraries)")
            logging.error("2. Marionette port conflicts")
            logging.error("3. Insufficient display/Xvfb setup")
            logging.error("4. Firefox version compatibility with GeckoDriver")
            raise
    
    @staticmethod
    def quit_browser(driver: Optional[webdriver.Remote]) -> None:
        """
        Safely quit the browser instance.
        
        Args:
            driver (webdriver.Remote): Browser instance to quit
        """
        if driver:
            try:
                driver.quit()
                logging.info("Browser closed successfully")
            except Exception as e:
                logging.error(f"Error while closing browser: {str(e)}")