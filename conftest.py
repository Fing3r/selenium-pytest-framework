"""
Pytest Configuration and Fixtures

This module contains pytest fixtures and configuration for the test framework.
Provides browser setup/teardown, test data, and other common test utilities.
"""

import pytest
import logging
import os
from datetime import datetime
from typing import Generator, Dict, Any

from utilities.browser_factory import BrowserFactory
from utilities.test_utils import TestUtils, ScreenshotHelper
from selenium import webdriver


def pytest_addoption(parser):
    """Add custom command line options for pytest."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome or firefox",
        choices=["chrome", "firefox"]
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="https://www.demoblaze.com",
        help="Base URL for DemoBlaze e-commerce application"
    )
    parser.addoption(
        "--timeout",
        action="store",
        default="10",
        help="Default timeout for explicit waits"
    )
    parser.addoption(
        "--window-size",
        action="store",
        default="1920,1080",
        help="Browser window size (width,height)"
    )


def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Create reports directory if it doesn't exist
    reports_dir = "reports"
    TestUtils.create_directory_if_not_exists(reports_dir)
    
    # Create screenshots directory if it doesn't exist
    screenshots_dir = "screenshots"
    TestUtils.create_directory_if_not_exists(screenshots_dir)
    
    # Setup logging
    log_file = os.path.join(reports_dir, f"test_log_{TestUtils.generate_timestamp()}.log")
    TestUtils.setup_logging(log_level="INFO", log_file=log_file)
    
    # Log test configuration
    browser = config.getoption("--browser")
    headless = config.getoption("--headless")
    base_url = config.getoption("--base-url")
    timeout = config.getoption("--timeout")
    window_size = config.getoption("--window-size")
    
    logging.info("="*80)
    logging.info("TEST CONFIGURATION")
    logging.info("="*80)
    logging.info(f"Browser: {browser}")
    logging.info(f"Headless: {headless}")
    logging.info(f"Base URL: {base_url}")
    logging.info(f"Timeout: {timeout}")
    logging.info(f"Window Size: {window_size}")
    logging.info("="*80)


def pytest_sessionstart(session):
    """Called after the Session object has been created."""
    logging.info("Starting test session...")


def pytest_sessionfinish(session, exitstatus):
    """Called after whole test run finished."""
    logging.info(f"Test session finished with exit status: {exitstatus}")
    
    # Generate comprehensive test report
    try:
        from utilities.test_reporter import TestReporter
        reporter = TestReporter()
        report = reporter.generate_comprehensive_report()
        
        # Print summary to console
        print("\n" + "=" * 80)
        print("🎯 FINAL TEST EXECUTION SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {report['execution_summary']['total_tests']}")
        print(f"✅ Passed: {report['execution_summary']['passed']}")
        print(f"❌ Failed: {report['execution_summary']['failed']}")
        print(f"⏭️  Skipped: {report['execution_summary']['skipped']}")
        print(f"📊 Pass Rate: {report['execution_summary']['pass_rate']}%")
        print(f"⏱️  Duration: {report['execution_summary']['execution_time']:.2f}s")
        print("=" * 80)
        print("📋 Detailed reports available in 'reports' directory:")
        print("   - test_execution_summary.html (Human-readable)")
        print("   - comprehensive_test_report.json (Machine-readable)")
        print("   - test_report.html (Pytest HTML report)")
        print("   - coverage/index.html (Coverage report)")
        print("=" * 80)
        
    except Exception as e:
        logging.error(f"Error generating comprehensive test report: {e}")
        print(f"\n❌ Failed to generate comprehensive report: {e}")


@pytest.fixture(scope="session")
def browser_config(request) -> Dict[str, Any]:
    """
    Session-scoped fixture providing browser configuration.
    
    Returns:
        Dict[str, Any]: Browser configuration dictionary
    """
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    window_size_str = request.config.getoption("--window-size")
    
    # Parse window size
    try:
        width, height = map(int, window_size_str.split(','))
        window_size = (width, height)
    except ValueError:
        window_size = (1920, 1080)
        logging.warning(f"Invalid window size format: {window_size_str}. Using default: {window_size}")
    
    config = {
        "browser": browser,
        "headless": headless,
        "window_size": window_size
    }
    
    logging.info(f"Browser configuration: {config}")
    return config


@pytest.fixture(scope="session")
def app_config(request) -> Dict[str, Any]:
    """
    Session-scoped fixture providing application configuration.
    
    Returns:
        Dict[str, Any]: Application configuration dictionary
    """
    base_url = request.config.getoption("--base-url")
    timeout = int(request.config.getoption("--timeout"))
    
    config = {
        "base_url": base_url,
        "timeout": timeout
    }
    
    logging.info(f"Application configuration: {config}")
    return config


@pytest.fixture(scope="function")
def driver(browser_config: Dict[str, Any]) -> Generator[webdriver.Remote, None, None]:
    """
    Function-scoped fixture providing WebDriver instance.
    
    Args:
        browser_config: Browser configuration from session fixture
        
    Yields:
        webdriver.Remote: WebDriver instance
    """
    browser_name = browser_config["browser"]
    headless = browser_config["headless"]
    window_size = browser_config["window_size"]
    
    logging.info(f"Creating {browser_name} driver instance (headless: {headless})")
    
    # Create driver instance
    driver_instance = BrowserFactory.get_browser(
        browser_name=browser_name,
        headless=headless,
        window_size=window_size
    )
    
    # Set implicit wait
    driver_instance.implicitly_wait(2)
    
    logging.info(f"Driver created successfully: {type(driver_instance).__name__}")
    
    yield driver_instance
    
    # Cleanup
    logging.info("Closing driver instance")
    BrowserFactory.quit_browser(driver_instance)


@pytest.fixture(scope="function")
def screenshot_helper() -> ScreenshotHelper:
    """
    Function-scoped fixture providing screenshot helper.
    
    Returns:
        ScreenshotHelper: Screenshot helper instance
    """
    return ScreenshotHelper()


@pytest.fixture(scope="session")
def test_data() -> Dict[str, Any]:
    """
    Session-scoped fixture providing test data.
    
    Returns:
        Dict[str, Any]: Test data dictionary
    """
    # You can load test data from files here
    # For now, we'll provide some default test data
    return {
        "valid_credentials": {
            "username": "tomsmith",
            "password": "SuperSecretPassword!"
        },
        "invalid_credentials": {
            "username": "invalid_user",
            "password": "invalid_password"
        },
        "test_urls": {
            "login": "/login",
            "secure": "/secure"
        }
    }


@pytest.fixture(scope="function", autouse=True)
def setup_test_logging(request):
    """
    Auto-use fixture to log test start and end.
    
    Args:
        request: Pytest request object
    """
    test_name = request.node.name
    logging.info(f"Starting test: {test_name}")
    
    def finalizer():
        logging.info(f"Finished test: {test_name}")
    
    request.addfinalizer(finalizer)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure.
    
    Args:
        item: Test item
        call: Test call information
    """
    outcome = yield
    rep = outcome.get_result()
    
    # Only capture on test call (not setup/teardown)
    if rep.when == "call" and rep.failed:
        # Get driver from test fixtures if available
        if hasattr(item, "funcargs") and "driver" in item.funcargs:
            driver = item.funcargs["driver"]
            screenshot_helper = ScreenshotHelper()
            screenshot_path = screenshot_helper.take_screenshot(
                driver=driver,
                test_name=item.name,
                status="failed"
            )
            
            # Add screenshot path to test report
            if screenshot_path:
                rep.extra = [{"screenshot": screenshot_path}]
                logging.info(f"Screenshot captured for failed test: {screenshot_path}")


# Pytest markers for organizing tests
pytest_markers = [
    "smoke: Quick smoke tests",
    "regression: Full regression test suite",
    "login: Login functionality tests",
    "dashboard: Dashboard functionality tests", 
    "chrome: Chrome browser specific tests",
    "firefox: Firefox browser specific tests",
    "slow: Slow running tests",
    "api: API tests",
    "ui: UI tests"
]


def pytest_collection_modifyitems(config, items):
    """
    Modify collected test items.
    Add markers based on test names or modules.
    
    Args:
        config: Pytest configuration
        items: List of collected test items
    """
    for item in items:
        # Add browser marker based on current browser selection
        browser = config.getoption("--browser")
        if browser == "chrome":
            item.add_marker(pytest.mark.chrome)
        elif browser == "firefox":
            item.add_marker(pytest.mark.firefox)
        
        # Add markers based on test file names
        if "login" in item.nodeid.lower():
            item.add_marker(pytest.mark.login)
        
        if "dashboard" in item.nodeid.lower():
            item.add_marker(pytest.mark.dashboard)
        
        # Add UI marker for all tests (since this is a UI framework)
        item.add_marker(pytest.mark.ui)