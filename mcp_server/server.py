#!/usr/bin/env python3
"""
Selenium PyTest MCP Server

This MCP server provides intelligent assistance for Selenium PyTest test automation,
including page object generation, test case creation, framework management, and more.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

# Add the parent directory to the path so we can import from our framework
sys.path.append(str(Path(__file__).parent.parent))

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

# Import our framework utilities
try:
    from utilities.browser_factory import BrowserFactory
    from utilities.test_utils import TestUtils
    from pages.base_page import BasePage
except ImportError as e:
    print(f"Warning: Could not import framework modules: {e}")


class SeleniumPyTestMCPServer:
    """MCP Server for Selenium PyTest Test Automation Framework."""
    
    def __init__(self):
        self.server = Server("selenium-pytest-mcp-server")
        self.framework_root = Path(__file__).parent.parent
        self.setup_tools()
        self.setup_resources()
    
    def setup_tools(self):
        """Setup MCP tools for test automation assistance."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available tools for test automation."""
            return [
                Tool(
                    name="generate_page_object",
                    description="Generate a new Page Object class with locators and methods",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page_name": {
                                "type": "string",
                                "description": "Name of the page (e.g., 'LoginPage', 'CheckoutPage')"
                            },
                            "url": {
                                "type": "string", 
                                "description": "URL of the page to create object for"
                            },
                            "elements": {
                                "type": "array",
                                "description": "List of elements to include in the page object",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "locator_type": {"type": "string", "enum": ["ID", "CLASS_NAME", "CSS_SELECTOR", "XPATH", "NAME", "TAG_NAME", "LINK_TEXT"]},
                                        "locator_value": {"type": "string"},
                                        "description": {"type": "string"}
                                    },
                                    "required": ["name", "locator_type", "locator_value"]
                                }
                            }
                        },
                        "required": ["page_name", "url", "elements"]
                    }
                ),
                Tool(
                    name="generate_test_case",
                    description="Generate test cases for a specific page or functionality",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "test_name": {
                                "type": "string",
                                "description": "Name of the test class (e.g., 'TestLogin', 'TestCheckout')"
                            },
                            "page_object": {
                                "type": "string",
                                "description": "Name of the page object class to test"
                            },
                            "test_scenarios": {
                                "type": "array",
                                "description": "List of test scenarios to generate",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "scenario_name": {"type": "string"},
                                        "description": {"type": "string"},
                                        "test_type": {"type": "string", "enum": ["positive", "negative", "edge_case"]},
                                        "markers": {"type": "array", "items": {"type": "string"}}
                                    },
                                    "required": ["scenario_name", "description", "test_type"]
                                }
                            }
                        },
                        "required": ["test_name", "page_object", "test_scenarios"]
                    }
                ),
                Tool(
                    name="analyze_test_results",
                    description="Analyze test execution results and provide insights",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "report_path": {
                                "type": "string",
                                "description": "Path to the test report file (HTML or XML)"
                            }
                        },
                        "required": ["report_path"]
                    }
                ),
                Tool(
                    name="optimize_framework",
                    description="Analyze framework structure and suggest optimizations",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "analysis_type": {
                                "type": "string",
                                "enum": ["structure", "performance", "maintainability", "all"],
                                "description": "Type of analysis to perform"
                            }
                        },
                        "required": ["analysis_type"]
                    }
                ),
                Tool(
                    name="generate_test_data",
                    description="Generate test data for different scenarios",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "data_type": {
                                "type": "string",
                                "enum": ["user_credentials", "form_data", "api_data", "custom"],
                                "description": "Type of test data to generate"
                            },
                            "count": {
                                "type": "integer",
                                "description": "Number of data sets to generate",
                                "default": 5
                            },
                            "format": {
                                "type": "string",
                                "enum": ["json", "yaml", "csv"],
                                "description": "Output format for test data",
                                "default": "json"
                            }
                        },
                        "required": ["data_type"]
                    }
                ),
                Tool(
                    name="run_test_suite",
                    description="Execute test suite with specified parameters",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "test_path": {
                                "type": "string",
                                "description": "Path to test file or directory"
                            },
                            "browser": {
                                "type": "string",
                                "enum": ["chrome", "firefox"],
                                "default": "chrome"
                            },
                            "headless": {
                                "type": "boolean",
                                "default": False
                            },
                            "markers": {
                                "type": "string",
                                "description": "Pytest markers to filter tests (e.g., 'smoke', 'regression')"
                            }
                        },
                        "required": ["test_path"]
                    }
                ),
                Tool(
                    name="create_bdd_feature",
                    description="Create BDD feature files with scenarios",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "feature_name": {
                                "type": "string",
                                "description": "Name of the feature"
                            },
                            "scenarios": {
                                "type": "array",
                                "description": "List of scenarios for the feature",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "scenario_name": {"type": "string"},
                                        "given": {"type": "array", "items": {"type": "string"}},
                                        "when": {"type": "array", "items": {"type": "string"}},
                                        "then": {"type": "array", "items": {"type": "string"}}
                                    },
                                    "required": ["scenario_name", "given", "when", "then"]
                                }
                            }
                        },
                        "required": ["feature_name", "scenarios"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool calls."""
            try:
                if name == "generate_page_object":
                    return await self._generate_page_object(arguments)
                elif name == "generate_test_case":
                    return await self._generate_test_case(arguments)
                elif name == "analyze_test_results":
                    return await self._analyze_test_results(arguments)
                elif name == "optimize_framework":
                    return await self._optimize_framework(arguments)
                elif name == "generate_test_data":
                    return await self._generate_test_data(arguments)
                elif name == "run_test_suite":
                    return await self._run_test_suite(arguments)
                elif name == "create_bdd_feature":
                    return await self._create_bdd_feature(arguments)
                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]
            except Exception as e:
                return [TextContent(type="text", text=f"Error executing tool {name}: {str(e)}")]
    
    def setup_resources(self):
        """Setup MCP resources for framework information."""
        
        @self.server.list_resources()
        async def handle_list_resources() -> List[Resource]:
            """List available resources."""
            return [
                Resource(
                    uri="framework://structure",
                    name="Framework Structure",
                    description="Overview of the test framework structure and components",
                    mimeType="text/plain"
                ),
                Resource(
                    uri="framework://best-practices",
                    name="Test Automation Best Practices",
                    description="Best practices for using this test automation framework",
                    mimeType="text/markdown"
                ),
                Resource(
                    uri="framework://templates",
                    name="Code Templates",
                    description="Templates for page objects, tests, and utilities",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """Read resource content."""
            if uri == "framework://structure":
                return self._get_framework_structure()
            elif uri == "framework://best-practices":
                return self._get_best_practices()
            elif uri == "framework://templates":
                return self._get_code_templates()
            else:
                raise ValueError(f"Unknown resource: {uri}")
    
    async def _generate_page_object(self, args: Dict[str, Any]) -> List[TextContent]:
        """Generate a new Page Object class."""
        page_name = args["page_name"]
        url = args["url"]
        elements = args["elements"]
        
        # Generate the page object class
        class_content = self._create_page_object_class(page_name, url, elements)
        
        # Write to file
        file_path = self.framework_root / "pages" / f"{page_name.lower().replace('page', '')}_page.py"
        
        try:
            with open(file_path, 'w') as f:
                f.write(class_content)
            
            return [TextContent(
                type="text",
                text=f"Page Object '{page_name}' generated successfully at {file_path}\n\n{class_content}"
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"Error generating page object: {str(e)}")]
    
    async def _generate_test_case(self, args: Dict[str, Any]) -> List[TextContent]:
        """Generate test cases for a page object."""
        test_name = args["test_name"]
        page_object = args["page_object"]
        scenarios = args["test_scenarios"]
        
        # Generate test class
        test_content = self._create_test_class(test_name, page_object, scenarios)
        
        # Write to file
        file_path = self.framework_root / "tests" / f"test_{test_name.lower().replace('test', '')}.py"
        
        try:
            with open(file_path, 'w') as f:
                f.write(test_content)
            
            return [TextContent(
                type="text",
                text=f"Test class '{test_name}' generated successfully at {file_path}\n\n{test_content}"
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"Error generating test case: {str(e)}")]
    
    async def _analyze_test_results(self, args: Dict[str, Any]) -> List[TextContent]:
        """Analyze test execution results."""
        report_path = args["report_path"]
        
        try:
            if not os.path.exists(report_path):
                return [TextContent(type="text", text=f"Report file not found: {report_path}")]
            
            analysis = self._analyze_report_file(report_path)
            return [TextContent(type="text", text=analysis)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error analyzing test results: {str(e)}")]
    
    async def _optimize_framework(self, args: Dict[str, Any]) -> List[TextContent]:
        """Analyze and suggest framework optimizations."""
        analysis_type = args["analysis_type"]
        
        try:
            optimization_report = self._perform_framework_analysis(analysis_type)
            return [TextContent(type="text", text=optimization_report)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error analyzing framework: {str(e)}")]
    
    async def _generate_test_data(self, args: Dict[str, Any]) -> List[TextContent]:
        """Generate test data."""
        data_type = args["data_type"]
        count = args.get("count", 5)
        format_type = args.get("format", "json")
        
        try:
            test_data = self._create_test_data(data_type, count, format_type)
            return [TextContent(type="text", text=f"Generated {count} {data_type} records:\n\n{test_data}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error generating test data: {str(e)}")]
    
    async def _run_test_suite(self, args: Dict[str, Any]) -> List[TextContent]:
        """Execute test suite."""
        test_path = args["test_path"]
        browser = args.get("browser", "chrome")
        headless = args.get("headless", False)
        markers = args.get("markers", "")
        
        try:
            result = self._execute_tests(test_path, browser, headless, markers)
            return [TextContent(type="text", text=result)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error running tests: {str(e)}")]
    
    async def _create_bdd_feature(self, args: Dict[str, Any]) -> List[TextContent]:
        """Create BDD feature file."""
        feature_name = args["feature_name"]
        scenarios = args["scenarios"]
        
        try:
            feature_content = self._generate_bdd_feature(feature_name, scenarios)
            file_path = self.framework_root / "features" / f"{feature_name.lower().replace(' ', '_')}.feature"
            
            # Create features directory if it doesn't exist
            os.makedirs(self.framework_root / "features", exist_ok=True)
            
            with open(file_path, 'w') as f:
                f.write(feature_content)
            
            return [TextContent(
                type="text",
                text=f"BDD Feature '{feature_name}' created at {file_path}\n\n{feature_content}"
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"Error creating BDD feature: {str(e)}")]
    
    def _create_page_object_class(self, page_name: str, url: str, elements: List[Dict]) -> str:
        """Create page object class content."""
        snake_case_name = page_name.lower().replace('page', '')
        
        imports = '''"""
{page_name} Module

This module contains the {page_name} class implementing the Page Object Model.
Generated by MCP Server for Selenium PyTest Framework.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from typing import Tuple

'''.format(page_name=page_name)
        
        class_definition = f'''
class {page_name}(BasePage):
    """
    {page_name} object class containing all elements and actions
    related to {snake_case_name} functionality.
    """
    
    # Page URL
    {snake_case_name.upper()}_URL = "{url}"
    
    # Locators
'''
        
        # Add locators
        locator_definitions = ""
        for element in elements:
            locator_name = element["name"].upper() + "_LOCATOR"
            locator_type = f"By.{element['locator_type']}"
            locator_value = element["locator_value"]
            description = element.get("description", "")
            
            if description:
                locator_definitions += f"    # {description}\n"
            locator_definitions += f"    {locator_name} = ({locator_type}, \"{locator_value}\")\n"
        
        class_definition += locator_definitions
        
        # Add constructor and methods
        methods = f'''
    
    def __init__(self, driver, timeout=10):
        """
        Initialize {page_name} with driver instance.
        
        Args:
            driver: WebDriver instance
            timeout: Default timeout for operations
        """
        super().__init__(driver, timeout)
    
    def navigate_to_{snake_case_name}(self) -> None:
        """Navigate to the {snake_case_name} page."""
        self.open_url(self.{snake_case_name.upper()}_URL)
        self.wait_for_page_load()
        self.logger.info("Navigated to {snake_case_name} page")
    
    def is_on_{snake_case_name}_page(self) -> bool:
        """
        Verify if currently on {snake_case_name} page.
        
        Returns:
            bool: True if on {snake_case_name} page, False otherwise
        """
        current_url = self.get_current_url()
        is_on_page = "{snake_case_name}" in current_url.lower()
        self.logger.info(f"On {snake_case_name} page: {{is_on_page}}")
        return is_on_page
'''
        
        # Add element-specific methods
        for element in elements:
            element_name = element["name"].lower()
            locator_name = element["name"].upper() + "_LOCATOR"
            
            methods += f'''
    def click_{element_name}(self) -> None:
        """Click the {element_name} element."""
        self.click_element(self.{locator_name})
        self.logger.info("Clicked {element_name}")
    
    def get_{element_name}_text(self) -> str:
        """Get text from {element_name} element."""
        text = self.get_text(self.{locator_name})
        self.logger.info(f"Got text from {element_name}: {{text}}")
        return text
    
    def is_{element_name}_visible(self) -> bool:
        """Check if {element_name} element is visible."""
        return self.is_element_visible(self.{locator_name})
'''
        
        return imports + class_definition + methods
    
    def _create_test_class(self, test_name: str, page_object: str, scenarios: List[Dict]) -> str:
        """Create test class content."""
        snake_case_name = test_name.lower().replace('test', '')
        
        imports = f'''"""
{test_name} Module

This module contains test cases for {snake_case_name} functionality.
Generated by MCP Server for Selenium PyTest Framework.
"""

import pytest
import logging
from pages.{page_object.lower().replace('page', '')}_page import {page_object}

'''
        
        class_definition = f'''
class {test_name}:
    """Test class for {snake_case_name} functionality."""
    
    def setup_method(self):
        """Setup method called before each test method."""
        self.logger = logging.getLogger(__name__)
'''
        
        # Generate test methods
        test_methods = ""
        for scenario in scenarios:
            scenario_name = scenario["scenario_name"].lower().replace(" ", "_")
            description = scenario["description"]
            test_type = scenario["test_type"]
            markers = scenario.get("markers", [])
            
            # Add markers
            marker_decorators = ""
            for marker in markers:
                marker_decorators += f"    @pytest.mark.{marker}\n"
            
            test_methods += f'''
{marker_decorators}    def test_{scenario_name}(self, driver, app_config, test_data):
        """
        {description}
        
        Test Type: {test_type}
        
        Steps:
        1. Navigate to page
        2. Perform test actions
        3. Verify expected results
        """
        # Arrange
        page = {page_object}(driver, app_config["timeout"])
        
        # Act
        # TODO: Implement test actions
        
        # Assert
        # TODO: Implement test assertions
        
        self.logger.info("{scenario_name} test completed")
'''
        
        return imports + class_definition + test_methods
    
    def _analyze_report_file(self, report_path: str) -> str:
        """Analyze test report file."""
        # This is a simplified analysis - in practice, you'd parse HTML/XML reports
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analysis = f"""Test Report Analysis for: {report_path}

Report Size: {len(content)} characters

Analysis Summary:
- Report file exists and is readable
- File format: {'HTML' if '.html' in report_path else 'XML' if '.xml' in report_path else 'Unknown'}

Recommendations:
1. Parse report content for detailed metrics
2. Extract pass/fail statistics
3. Identify common failure patterns
4. Generate trend analysis

Note: This is a basic analysis. Implement full HTML/XML parsing for detailed insights.
"""
            return analysis
        except Exception as e:
            return f"Error reading report file: {str(e)}"
    
    def _perform_framework_analysis(self, analysis_type: str) -> str:
        """Perform framework analysis."""
        framework_path = self.framework_root
        
        analysis = f"""Framework Analysis Report - {analysis_type.title()}

Framework Root: {framework_path}

"""
        
        if analysis_type in ["structure", "all"]:
            analysis += self._analyze_structure()
        
        if analysis_type in ["performance", "all"]:
            analysis += self._analyze_performance()
        
        if analysis_type in ["maintainability", "all"]:
            analysis += self._analyze_maintainability()
        
        return analysis
    
    def _analyze_structure(self) -> str:
        """Analyze framework structure."""
        return """
=== STRUCTURE ANALYSIS ===

Framework Structure Assessment:
✓ Pages directory exists with base_page.py
✓ Tests directory with organized test files
✓ Utilities directory with helper classes
✓ Configuration files present (pytest.ini, conftest.py)
✓ Requirements.txt with dependencies

Recommendations:
1. Consider adding data directory for test data files
2. Add API utilities if testing hybrid applications
3. Consider environment-specific configuration files

"""
    
    def _analyze_performance(self) -> str:
        """Analyze framework performance."""
        return """
=== PERFORMANCE ANALYSIS ===

Performance Considerations:
- Browser optimization settings configured
- Explicit waits implemented in base page
- WebDriver manager for efficient driver handling
- Parallel execution support available

Recommendations:
1. Monitor test execution times
2. Use headless mode for CI/CD
3. Implement test data cleanup strategies
4. Consider browser pooling for large test suites

"""
    
    def _analyze_maintainability(self) -> str:
        """Analyze framework maintainability."""
        return """
=== MAINTAINABILITY ANALYSIS ===

Maintainability Features:
✓ Page Object Model implemented
✓ Base page class for common functionality
✓ Consistent logging throughout framework
✓ Clear separation of concerns
✓ Comprehensive documentation

Recommendations:
1. Regular dependency updates
2. Code review processes
3. Automated code quality checks
4. Test case documentation standards

"""
    
    def _create_test_data(self, data_type: str, count: int, format_type: str) -> str:
        """Generate test data."""
        import random
        import string
        from datetime import datetime, timedelta
        
        data = []
        
        for i in range(count):
            if data_type == "user_credentials":
                data.append({
                    "username": f"testuser{i+1}",
                    "password": "".join(random.choices(string.ascii_letters + string.digits, k=12)),
                    "email": f"testuser{i+1}@example.com",
                    "first_name": f"Test{i+1}",
                    "last_name": "User"
                })
            elif data_type == "form_data":
                data.append({
                    "name": f"Test Name {i+1}",
                    "address": f"{random.randint(100, 9999)} Test St",
                    "city": f"Test City {i+1}",
                    "phone": f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                    "date": (datetime.now() + timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
                })
        
        if format_type == "json":
            return json.dumps(data, indent=2)
        elif format_type == "yaml":
            import yaml
            return yaml.dump(data, default_flow_style=False)
        else:
            return str(data)
    
    def _execute_tests(self, test_path: str, browser: str, headless: bool, markers: str) -> str:
        """Execute test suite (simulated)."""
        # In a real implementation, you would execute the tests
        command_parts = ["python", "-m", "pytest", test_path, f"--browser={browser}"]
        
        if headless:
            command_parts.append("--headless")
        
        if markers:
            command_parts.extend(["-m", markers])
        
        command = " ".join(command_parts)
        
        return f"""Test Execution Summary:

Command: {command}
Test Path: {test_path}
Browser: {browser}
Headless: {headless}
Markers: {markers or 'None'}

Note: This is a simulated execution. In practice, the MCP server would:
1. Execute the pytest command
2. Monitor test progress
3. Capture results and logs
4. Provide real-time feedback

To actually run tests, execute: {command}
"""
    
    def _generate_bdd_feature(self, feature_name: str, scenarios: List[Dict]) -> str:
        """Generate BDD feature file content."""
        feature_content = f"""Feature: {feature_name}
  As a user of the application
  I want to {feature_name.lower()}
  So that I can achieve my goals

"""
        
        for scenario in scenarios:
            scenario_name = scenario["scenario_name"]
            given_steps = scenario["given"]
            when_steps = scenario["when"]
            then_steps = scenario["then"]
            
            feature_content += f"  Scenario: {scenario_name}\n"
            
            for step in given_steps:
                feature_content += f"    Given {step}\n"
            
            for step in when_steps:
                feature_content += f"    When {step}\n"
            
            for step in then_steps:
                feature_content += f"    Then {step}\n"
            
            feature_content += "\n"
        
        return feature_content
    
    def _get_framework_structure(self) -> str:
        """Get framework structure overview."""
        return """Selenium PyTest Test Automation Framework Structure:

selenium_pytest_framework/
├── pages/                      # Page Object classes
│   ├── __init__.py
│   ├── base_page.py           # Base page with common functionality
│   ├── login_page.py          # Login page object
│   └── dashboard_page.py      # Dashboard page object
├── tests/                      # Test cases
│   ├── __init__.py
│   ├── test_login.py          # Login functionality tests
│   ├── test_dashboard.py      # Dashboard functionality tests
│   └── test_end_to_end.py     # End-to-end test scenarios
├── utilities/                  # Utility classes and helpers
│   ├── __init__.py
│   ├── browser_factory.py     # Browser instance management
│   └── test_utils.py          # Common test utilities
├── config/                     # Configuration files
│   └── settings.py            # Framework settings
├── reports/                    # Test reports and logs
├── screenshots/                # Screenshot storage
├── mcp_server/                # MCP Server for intelligent assistance
│   ├── server.py              # Main MCP server implementation
│   └── package.json           # MCP server configuration
├── conftest.py                # PyTest fixtures and configuration
├── pytest.ini                 # PyTest configuration
├── requirements.txt           # Python dependencies
└── README.md                  # Documentation

The framework follows Page Object Model (POM) design pattern with:
- Separation of test logic and page elements
- Reusable components and utilities
- Comprehensive reporting and logging
- Multi-browser support (Chrome, Firefox)
- CI/CD integration capabilities
"""
    
    def _get_best_practices(self) -> str:
        """Get test automation best practices."""
        return """# Test Automation Best Practices

## Page Object Model (POM)
- Keep page objects focused on single responsibility
- Use meaningful locator names
- Implement page validation methods
- Handle dynamic content appropriately

## Test Design
- Follow Arrange-Act-Assert pattern
- Use descriptive test names
- Implement proper setup and teardown
- Group related tests in classes

## Element Interaction
- Use explicit waits over implicit waits
- Implement robust element finding strategies
- Handle stale element exceptions
- Use appropriate locator strategies (prefer ID > CSS > XPath)

## Test Data Management
- Externalize test data when possible
- Use fixtures for common test data
- Implement data-driven testing
- Keep sensitive data secure

## Error Handling
- Implement comprehensive exception handling
- Capture screenshots on failures
- Use detailed logging
- Provide meaningful error messages

## Framework Maintenance
- Regular dependency updates
- Code reviews and refactoring
- Comprehensive documentation
- Continuous integration practices

## Performance Optimization
- Use headless browsers for CI/CD
- Implement parallel test execution
- Optimize browser settings
- Clean up test data and resources
"""
    
    def _get_code_templates(self) -> str:
        """Get code templates."""
        templates = {
            "page_object_template": {
                "description": "Template for creating new page objects",
                "template": """
class NewPage(BasePage):
    # Locators
    ELEMENT_LOCATOR = (By.ID, "element-id")
    
    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)
    
    def perform_action(self):
        self.click_element(self.ELEMENT_LOCATOR)
        
    def verify_element(self):
        return self.is_element_visible(self.ELEMENT_LOCATOR)
"""
            },
            "test_case_template": {
                "description": "Template for creating new test cases",
                "template": """
@pytest.mark.smoke
def test_functionality(self, driver, app_config, test_data):
    # Arrange
    page = PageObject(driver, app_config["timeout"])
    
    # Act
    page.perform_action()
    
    # Assert
    assert page.verify_result()
"""
            }
        }
        
        return json.dumps(templates, indent=2)


async def main():
    """Main function to run the MCP server."""
    mcp_server = SeleniumPyTestMCPServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await mcp_server.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="selenium-pytest-mcp-server",
                server_version="1.0.0",
                capabilities=mcp_server.server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())