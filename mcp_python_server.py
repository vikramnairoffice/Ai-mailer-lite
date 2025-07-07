#!/usr/bin/env python3
"""
Simple MCP server for Python subprocess execution
"""

import subprocess
import sys
import json
import os
from typing import Dict, Any, List

class PythonMCPServer:
    def __init__(self):
        self.venv_path = "/home/amitr/projects/email-marketing-system/mcp_env"
        self.python_path = f"{self.venv_path}/bin/python"
        self.base_path = "/home/amitr/projects/email-marketing-system"
        
    def execute_python_code(self, code: str, working_dir: str = None) -> Dict[str, Any]:
        """Execute Python code in the virtual environment"""
        if working_dir is None:
            working_dir = self.base_path
            
        try:
            # Set up environment
            env = os.environ.copy()
            env["VIRTUAL_ENV"] = self.venv_path
            env["PATH"] = f"{self.venv_path}/bin:{env.get('PATH', '')}"
            env["PYTHONPATH"] = self.base_path
            
            # Execute code
            result = subprocess.run(
                [self.python_path, "-c", code],
                cwd=working_dir,
                env=env,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Execution timed out",
                "returncode": -1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
    
    def execute_python_file(self, filepath: str, args: List[str] = None) -> Dict[str, Any]:
        """Execute a Python file in the virtual environment"""
        if args is None:
            args = []
            
        try:
            # Set up environment
            env = os.environ.copy()
            env["VIRTUAL_ENV"] = self.venv_path
            env["PATH"] = f"{self.venv_path}/bin:{env.get('PATH', '')}"
            env["PYTHONPATH"] = self.base_path
            
            # Execute file
            cmd = [self.python_path, filepath] + args
            result = subprocess.run(
                cmd,
                cwd=self.base_path,
                env=env,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Execution timed out",
                "returncode": -1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
    
    def test_imports(self) -> Dict[str, Any]:
        """Test if all required modules can be imported"""
        modules_to_test = [
            "streamlit",
            "selenium",
            "pandas",
            "requests",
            "google.generativeai",
            "core.config",
            "content.spintax_generator",
            "testing.gmass_automation"
        ]
        
        results = {}
        for module in modules_to_test:
            try:
                result = self.execute_python_code(f"import {module}; print('{module} imported successfully')")
                results[module] = result["success"]
            except Exception as e:
                results[module] = False
                
        return results

if __name__ == "__main__":
    server = PythonMCPServer()
    
    # Test basic functionality
    print("Testing Python MCP Server...")
    
    # Test imports
    import_results = server.test_imports()
    print("Import test results:")
    for module, success in import_results.items():
        status = "✓" if success else "✗"
        print(f"  {status} {module}")
    
    # Test code execution
    test_code = """
from core.config import init_session_state
from content.spintax_generator import generate_short_spintax_content
print("All core modules working!")
"""
    
    result = server.execute_python_code(test_code)
    print(f"\nCode execution test: {'✓' if result['success'] else '✗'}")
    if result['stdout']:
        print(f"Output: {result['stdout']}")
    if result['stderr']:
        print(f"Error: {result['stderr']}")