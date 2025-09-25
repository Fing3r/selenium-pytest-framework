# MCP Server Integration for Selenium PyTest Framework

## Overview

The Model Context Protocol (MCP) server integration provides intelligent assistance for your Selenium PyTest test automation framework. It offers AI-powered code generation, framework analysis, and test management capabilities.

## Features

### 🤖 Intelligent Code Generation
- **Page Object Generation**: Automatically create page object classes with locators and methods
- **Test Case Generation**: Generate comprehensive test cases with proper structure
- **BDD Feature Creation**: Create Gherkin feature files for behavior-driven development

### 📊 Framework Analysis
- **Structure Analysis**: Evaluate framework organization and suggest improvements
- **Best Practices Check**: Ensure adherence to testing standards
- **Performance Recommendations**: Optimize test execution and maintenance

### 🛠️ Test Utilities
- **Test Data Generation**: Create realistic test data for various scenarios
- **Template Management**: Access code templates for consistent development
- **Resource Management**: Get framework documentation and best practices

## Installation & Setup

### 1. Install MCP Dependencies

```bash
# Install MCP server dependencies
pip install mcp uvloop

# Or install from requirements.txt (already included)
pip install -r requirements.txt
```

### 2. Verify MCP Server

```bash
# Navigate to framework directory
cd selenium_pytest_framework

# Test MCP assistant
python mcp_server/mcp_assistant.py --action analyze
```

### 3. Configure MCP Client

Add the MCP server configuration to your MCP client:

```json
{
  "mcpServers": {
    "selenium-pytest-assistant": {
      "command": "python",
      "args": ["mcp_server/server.py"],
      "cwd": "/path/to/selenium_pytest_framework",
      "env": {}
    }
  }
}
```

## Usage

### Command Line Interface

The MCP server includes a convenient CLI for direct interaction:

```bash
# Show available commands
python mcp_server/mcp_cli.py help

# Generate a new page object
python mcp_server/mcp_cli.py generate-page CheckoutPage /checkout '[{"name":"product_name","locator_type":"ID","locator_value":"product-name"}]'

# Generate test cases
python mcp_server/mcp_cli.py generate-test TestCheckout CheckoutPage '[{"scenario_name":"Add Product","description":"Test adding product to cart","test_type":"positive"}]'

# Analyze framework
python mcp_server/mcp_cli.py analyze structure

# Generate test data
python mcp_server/mcp_cli.py generate-data user_credentials 5 json

# Create BDD feature
python mcp_server/mcp_cli.py create-feature "Product Purchase" '[{"scenario_name":"Successful Purchase","given":["I am on product page"],"when":["I click buy now"],"then":["I see confirmation"]}]'
```

### MCP Client Integration

When integrated with an MCP-compatible client (like Claude Desktop), you can use natural language commands:

```
"Generate a page object for the shopping cart page with elements for quantity, price, and checkout button"

"Create test cases for login functionality including positive and negative scenarios"

"Analyze my test framework and suggest optimizations"

"Generate realistic user data for testing registration forms"
```

## Available Tools

### 1. generate_page_object

Generate new page object classes following POM best practices.

**Parameters:**
- `page_name`: Name of the page class (e.g., "LoginPage")
- `url`: Page URL or path
- `elements`: Array of element definitions with name, locator type, and value

**Example:**
```json
{
  "page_name": "LoginPage",
  "url": "/login",
  "elements": [
    {
      "name": "username",
      "locator_type": "ID", 
      "locator_value": "username",
      "description": "Username input field"
    },
    {
      "name": "password",
      "locator_type": "ID",
      "locator_value": "password", 
      "description": "Password input field"
    }
  ]
}
```

### 2. generate_test_case

Create comprehensive test cases for page objects.

**Parameters:**
- `test_name`: Name of the test class (e.g., "TestLogin")
- `page_object`: Page object class to test
- `test_scenarios`: Array of test scenarios

**Example:**
```json
{
  "test_name": "TestLogin",
  "page_object": "LoginPage",
  "test_scenarios": [
    {
      "scenario_name": "Valid Login",
      "description": "Test login with valid credentials",
      "test_type": "positive",
      "markers": ["smoke", "login"]
    }
  ]
}
```

### 3. analyze_framework

Analyze framework structure and provide optimization recommendations.

**Parameters:**
- `analysis_type`: Type of analysis ("structure", "performance", "maintainability", "all")

### 4. generate_test_data

Generate realistic test data for various scenarios.

**Parameters:**
- `data_type`: Type of data ("user_credentials", "form_data", "api_data", "custom")
- `count`: Number of data sets to generate (default: 5)
- `format`: Output format ("json", "yaml", "csv")

### 5. create_bdd_feature

Create BDD feature files with Gherkin syntax.

**Parameters:**
- `feature_name`: Name of the feature
- `scenarios`: Array of scenarios with Given/When/Then steps

## Advanced Usage

### Custom Page Object Templates

The MCP server can generate page objects with custom templates:

```python
# Example: Generate a complex e-commerce page object
python mcp_server/mcp_cli.py generate-page ProductPage /products '[
  {"name":"search_box","locator_type":"CSS_SELECTOR","locator_value":"input[type=\"search\"]"},
  {"name":"filter_dropdown","locator_type":"ID","locator_value":"category-filter"},
  {"name":"sort_dropdown","locator_type":"CSS_SELECTOR","locator_value":"select.sort-options"},
  {"name":"product_cards","locator_type":"CSS_SELECTOR","locator_value":".product-card"},
  {"name":"add_to_cart","locator_type":"CSS_SELECTOR","locator_value":"button.add-to-cart"}
]'
```

### Test Scenario Templates

Generate comprehensive test suites with multiple scenario types:

```python
# Example: Generate login test scenarios
python mcp_server/mcp_cli.py generate-test TestAuthentication LoginPage '[
  {"scenario_name":"valid_login","description":"Login with valid credentials","test_type":"positive","markers":["smoke"]},
  {"scenario_name":"invalid_password","description":"Login with invalid password","test_type":"negative","markers":["regression"]},
  {"scenario_name":"empty_fields","description":"Login with empty fields","test_type":"edge_case","markers":["regression"]},
  {"scenario_name":"sql_injection","description":"Test SQL injection prevention","test_type":"security","markers":["security"]}
]'
```

### BDD Feature Generation

Create complete BDD feature files:

```python
# Example: Generate user registration feature
python mcp_server/mcp_cli.py create-feature "User Registration" '[
  {
    "scenario_name": "Successful Registration",
    "given": ["I am on the registration page", "All required fields are available"],
    "when": ["I fill in all required information", "I click the register button"],
    "then": ["My account is created", "I receive a confirmation email", "I am redirected to the dashboard"]
  },
  {
    "scenario_name": "Registration with Invalid Email",
    "given": ["I am on the registration page"],
    "when": ["I enter an invalid email format", "I click the register button"],
    "then": ["I see an error message", "The form is not submitted", "I remain on the registration page"]
  }
]'
```

## Integration with Development Workflow

### 1. Page Object Development

```bash
# Step 1: Generate base page object
python mcp_server/mcp_cli.py generate-page NewFeaturePage /new-feature

# Step 2: Analyze and enhance generated code
python mcp_server/mcp_cli.py analyze structure

# Step 3: Generate corresponding tests
python mcp_server/mcp_cli.py generate-test TestNewFeature NewFeaturePage
```

### 2. Test Data Management

```bash
# Generate test data for different environments
python mcp_server/mcp_cli.py generate-data user_credentials 10 json > test_data/users.json
python mcp_server/mcp_cli.py generate-data form_data 5 yaml > test_data/forms.yaml
```

### 3. BDD Workflow Integration

```bash
# Create feature files for user stories
python mcp_server/mcp_cli.py create-feature "User Profile Management"
python mcp_server/mcp_cli.py create-feature "Shopping Cart Operations"
python mcp_server/mcp_cli.py create-feature "Payment Processing"
```

## Best Practices

### 1. Code Generation Guidelines

- **Review Generated Code**: Always review and customize generated code
- **Follow Naming Conventions**: Use consistent naming for page objects and tests
- **Add Documentation**: Enhance generated code with proper documentation
- **Customize Locators**: Verify and optimize element locators

### 2. Framework Analysis

- **Regular Analysis**: Run framework analysis regularly to maintain quality
- **Address Recommendations**: Implement suggested improvements
- **Monitor Metrics**: Track framework health over time
- **Update Dependencies**: Keep dependencies current based on analysis

### 3. Test Data Management

- **Environment-Specific Data**: Generate different data sets for different environments
- **Data Privacy**: Ensure generated test data doesn't contain sensitive information
- **Data Cleanup**: Implement cleanup strategies for generated test data
- **Data Versioning**: Version control your test data files

## Troubleshooting

### Common Issues

#### MCP Server Not Starting
```bash
# Check Python path
python --version

# Verify dependencies
pip install mcp uvloop

# Test server directly
python mcp_server/mcp_assistant.py --action analyze
```

#### Import Errors
```bash
# Ensure framework modules are importable
export PYTHONPATH=$PYTHONPATH:/path/to/selenium_pytest_framework

# Or use absolute imports in generated code
```

#### File Permission Issues
```bash
# Ensure write permissions for generated files
chmod +w pages/ tests/ features/
```

### Debugging

Enable debug logging in the MCP server:

```python
# In mcp_assistant.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Extending the MCP Server

### Adding Custom Tools

```python
# In mcp_assistant.py, add new tools to _get_available_tools()
{
    "name": "custom_tool",
    "description": "Custom functionality description",
    "parameters": ["param1", "param2"]
}

# Implement the tool handler
def _handle_custom_tool(self, args: Dict[str, Any]) -> str:
    # Your custom logic here
    return "Tool result"
```

### Custom Templates

```python
# Add custom templates to _get_code_templates()
templates = {
    "custom_template": {
        "description": "Custom template description",
        "template": "Your template content here"
    }
}
```

## Future Enhancements

- **AI-Powered Test Optimization**: Analyze test failures and suggest improvements
- **Intelligent Locator Generation**: Use AI to suggest robust element locators
- **Test Coverage Analysis**: Identify gaps in test coverage
- **Performance Monitoring**: Track and analyze test execution performance
- **Visual Testing Integration**: Generate visual regression tests
- **API Testing Integration**: Extend framework to support API testing

## Contributing

To contribute to the MCP server development:

1. Fork the repository
2. Create a feature branch
3. Implement your enhancement
4. Add comprehensive tests
5. Update documentation
6. Submit a pull request

## Support

For issues or questions about the MCP integration:

1. Check the troubleshooting section
2. Review the generated logs
3. Test with the CLI interface
4. Create an issue with detailed information

---

The MCP server integration transforms your Selenium PyTest framework into an intelligent, AI-assisted test automation platform, significantly improving productivity and code quality! 🚀