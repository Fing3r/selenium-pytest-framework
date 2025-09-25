#!/usr/bin/env python3
"""
Selenium PyTest MCP Assistant - Command Line Interface

This CLI provides easy access to the MCP server functionality for
test automation tasks.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from mcp_assistant import SeleniumPyTestMCPServer


class MCPCLIInterface:
    """Command Line Interface for MCP Server."""
    
    def __init__(self):
        self.server = SeleniumPyTestMCPServer()
        self.commands = {
            "generate-page": self._generate_page_command,
            "generate-test": self._generate_test_command,
            "analyze": self._analyze_command,
            "generate-data": self._generate_data_command,
            "create-feature": self._create_feature_command,
            "analyze-website": self._analyze_website_command,
            "generate-tests-from-url": self._generate_tests_from_url_command,
            "help": self._help_command,
            "list-tools": self._list_tools_command
        }
    
    def run(self, args: List[str]) -> None:
        """Run CLI with given arguments."""
        if not args:
            self._help_command()
            return
        
        command = args[0]
        if command in self.commands:
            try:
                self.commands[command](args[1:])
            except Exception as e:
                print(f"Error executing command '{command}': {e}")
        else:
            print(f"Unknown command: {command}")
            self._help_command()
    
    def _generate_page_command(self, args: List[str]) -> None:
        """Generate a new page object."""
        if len(args) < 2:
            print("Usage: generate-page <page_name> <url> [elements_json]")
            print("Example: generate-page LoginPage /login '[{\"name\":\"username\",\"locator_type\":\"ID\",\"locator_value\":\"username\"}]'")
            return
        
        page_name = args[0]
        url = args[1]
        elements = []
        
        if len(args) > 2:
            try:
                elements = json.loads(args[2])
            except json.JSONDecodeError:
                print("Error: Invalid JSON for elements")
                return
        
        request_args = {
            "page_name": page_name,
            "url": url,
            "elements": elements
        }
        
        result = self.server._generate_page_object(request_args)
        print(result)
    
    def _generate_test_command(self, args: List[str]) -> None:
        """Generate test cases."""
        if len(args) < 2:
            print("Usage: generate-test <test_name> <page_object> [scenarios_json]")
            print("Example: generate-test TestLogin LoginPage '[{\"scenario_name\":\"Valid Login\",\"description\":\"Test login with valid credentials\",\"test_type\":\"positive\"}]'")
            return
        
        test_name = args[0]
        page_object = args[1]
        scenarios = []
        
        if len(args) > 2:
            try:
                scenarios = json.loads(args[2])
            except json.JSONDecodeError:
                print("Error: Invalid JSON for scenarios")
                return
        
        request_args = {
            "test_name": test_name,
            "page_object": page_object,
            "test_scenarios": scenarios
        }
        
        result = self.server._generate_test_case(request_args)
        print(result)
    
    def _analyze_command(self, args: List[str]) -> None:
        """Analyze framework."""
        analysis_type = args[0] if args else "all"
        
        request_args = {"analysis_type": analysis_type}
        result = self.server._analyze_framework(request_args)
        print(result)
    
    def _generate_data_command(self, args: List[str]) -> None:
        """Generate test data."""
        if not args:
            print("Usage: generate-data <data_type> [count] [format]")
            print("Data types: user_credentials, form_data")
            print("Formats: json, yaml")
            return
        
        data_type = args[0]
        count = int(args[1]) if len(args) > 1 else 5
        format_type = args[2] if len(args) > 2 else "json"
        
        request_args = {
            "data_type": data_type,
            "count": count,
            "format": format_type
        }
        
        result = self.server._generate_test_data(request_args)
        print(result)
    
    def _create_feature_command(self, args: List[str]) -> None:
        """Create BDD feature file."""
        if not args:
            print("Usage: create-feature <feature_name> [scenarios_json]")
            print("Example: create-feature 'User Login' '[{\"scenario_name\":\"Successful Login\",\"given\":[\"I am on login page\"],\"when\":[\"I enter valid credentials\"],\"then\":[\"I am logged in\"]}]'")
            return
        
        feature_name = args[0]
        scenarios = []
        
        if len(args) > 1:
            try:
                scenarios = json.loads(args[1])
            except json.JSONDecodeError:
                print("Error: Invalid JSON for scenarios")
                return
        
        request_args = {
            "feature_name": feature_name,
            "scenarios": scenarios
        }
        
        result = self.server._create_bdd_feature(request_args)
        print(result)
    
    def _analyze_website_command(self, args: List[str]) -> None:
        """Analyze a website and identify testable elements."""
        if len(args) < 1:
            print("Usage: analyze-website <url> [analysis_depth]")
            print("Example: analyze-website https://example.com detailed")
            print("Analysis depths: standard, detailed")
            return
        
        url = args[0]
        analysis_depth = args[1] if len(args) > 1 else "standard"
        
        request_args = {
            "url": url,
            "analysis_depth": analysis_depth
        }
        
        print(f"Analyzing website: {url}")
        print("This may take a few moments...")
        
        result = self.server._analyze_website(request_args)
        print(result)
    
    def _generate_tests_from_url_command(self, args: List[str]) -> None:
        """Generate page objects and test cases from a website URL."""
        if len(args) < 1:
            print("Usage: generate-tests-from-url <url> [test_types] [output_format]")
            print("Example: generate-tests-from-url https://example.com 'functionality,navigation,forms' pytest")
            print("Test types: functionality, navigation, forms, validation")
            print("Output formats: pytest, unittest")
            return
        
        url = args[0]
        test_types = ["functionality", "navigation", "forms"]
        output_format = "pytest"
        
        if len(args) > 1:
            test_types = [t.strip() for t in args[1].split(',')]
        
        if len(args) > 2:
            output_format = args[2]
        
        request_args = {
            "url": url,
            "test_types": test_types,
            "output_format": output_format
        }
        
        print(f"Generating tests from website: {url}")
        print(f"Test types: {', '.join(test_types)}")
        print("This may take a few moments...")
        
        result = self.server._generate_tests_from_url(request_args)
        print(result)
    
    def _list_tools_command(self, args: List[str]) -> None:
        """List available tools."""
        print("Available MCP Tools:")
        print("=" * 50)
        for tool in self.server.tools:
            print(f"• {tool['name']}")
            print(f"  Description: {tool['description']}")
            print(f"  Parameters: {', '.join(tool['parameters'])}")
            print()
    
    def _help_command(self, args: List[str] = None) -> None:
        """Show help information."""
        print("Selenium PyTest MCP Assistant - CLI")
        print("=" * 40)
        print()
        print("Available commands:")
        print("  generate-page           <name> <url> [elements]     Generate new page object")
        print("  generate-test           <name> <page> [scenarios]   Generate test cases")
        print("  analyze                 [type]                      Analyze framework")
        print("  generate-data           <type> [count] [format]     Generate test data")
        print("  create-feature          <name> [scenarios]          Create BDD feature")
        print("  analyze-website         <url> [depth]               Analyze website structure")
        print("  generate-tests-from-url <url> [types] [format]      Generate tests from website")
        print("  list-tools                                          List available tools")
        print("  help                                                Show this help")
        print()
        print("Examples:")
        print("  python mcp_cli.py generate-page HomePage /home")
        print("  python mcp_cli.py generate-test TestHome HomePage")
        print("  python mcp_cli.py analyze structure")
        print("  python mcp_cli.py generate-data user_credentials 3")
        print("  python mcp_cli.py create-feature 'User Registration'")
        print("  python mcp_cli.py analyze-website https://example.com")
        print("  python mcp_cli.py generate-tests-from-url https://example.com")


def main():
    """Main entry point for CLI."""
    cli = MCPCLIInterface()
    cli.run(sys.argv[1:])


if __name__ == "__main__":
    main()