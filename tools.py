from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import json
import os
import subprocess
import requests
from datetime import datetime

class Tool(ABC):
    """Base class for AI agent tools."""
    
    @abstractmethod
    def name(self) -> str:
        """Return the name of the tool."""
        pass
    
    @abstractmethod
    def description(self) -> str:
        """Return a description of what the tool does."""
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> str:
        """Execute the tool with given parameters."""
        pass

class FileManagerTool(Tool):
    """Tool for file operations."""
    
    def name(self) -> str:
        return "file_manager"
    
    def description(self) -> str:
        return "Read, write, and manage files. Usage: action='read/write/list', path='file_path', content='text' (for write)"
    
    def execute(self, **kwargs) -> str:
        action = kwargs.get('action', '').lower()
        path = kwargs.get('path', '')
        content = kwargs.get('content', '')
        
        try:
            if action == 'read':
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        return f"File content of {path}:\n{f.read()}"
                else:
                    return f"File {path} does not exist."
            
            elif action == 'write':
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return f"Successfully wrote to {path}"
            
            elif action == 'list':
                if os.path.isdir(path):
                    files = os.listdir(path)
                    return f"Files in {path}:\n" + "\n".join(files)
                else:
                    return f"{path} is not a directory."
            
            else:
                return "Invalid action. Use 'read', 'write', or 'list'."
        
        except Exception as e:
            return f"Error: {str(e)}"

class CalculatorTool(Tool):
    """Tool for mathematical calculations."""
    
    def name(self) -> str:
        return "calculator"
    
    def description(self) -> str:
        return "Perform mathematical calculations. Usage: expression='math_expression'"
    
    def execute(self, **kwargs) -> str:
        expression = kwargs.get('expression', '')
        
        try:
            # Safe evaluation of mathematical expressions
            allowed_names = {
                k: v for k, v in __builtins__.items() 
                if k in ('abs', 'round', 'min', 'max', 'sum', 'pow')
            }
            allowed_names.update({
                'pi': 3.141592653589793,
                'e': 2.718281828459045
            })
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return f"Result: {result}"
        
        except Exception as e:
            return f"Error calculating '{expression}': {str(e)}"

class SystemCommandTool(Tool):
    """Tool for executing system commands."""
    
    def name(self) -> str:
        return "system_command"
    
    def description(self) -> str:
        return "Execute system commands. Usage: command='your_command'"
    
    def execute(self, **kwargs) -> str:
        command = kwargs.get('command', '')
        
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            output = result.stdout if result.stdout else result.stderr
            return f"Command: {command}\nOutput:\n{output}"
        
        except subprocess.TimeoutExpired:
            return f"Command '{command}' timed out after 30 seconds."
        except Exception as e:
            return f"Error executing '{command}': {str(e)}"

class WebSearchTool(Tool):
    """Tool for web search (simplified version)."""
    
    def name(self) -> str:
        return "web_search"
    
    def description(self) -> str:
        return "Search the web for information. Usage: query='search_terms'"
    
    def execute(self, **kwargs) -> str:
        query = kwargs.get('query', '')
        
        # This is a simplified implementation
        # In a real scenario, you'd integrate with a search API
        return f"Web search for '{query}' - This tool needs API integration for full functionality."

class ToolManager:
    """Manages available tools for the AI agent."""
    
    def __init__(self):
        self.tools = {
            'file_manager': FileManagerTool(),
            'calculator': CalculatorTool(),
            'system_command': SystemCommandTool(),
            'web_search': WebSearchTool()
        }
    
    def get_tool_descriptions(self) -> str:
        """Get descriptions of all available tools."""
        descriptions = []
        for tool in self.tools.values():
            descriptions.append(f"- {tool.name()}: {tool.description()}")
        return "\n".join(descriptions)
    
    def execute_tool(self, tool_name: str, **kwargs) -> str:
        """Execute a specific tool."""
        if tool_name in self.tools:
            return self.tools[tool_name].execute(**kwargs)
        else:
            return f"Tool '{tool_name}' not found. Available tools: {list(self.tools.keys())}"
    
    def add_tool(self, tool: Tool) -> None:
        """Add a new tool."""
        self.tools[tool.name()] = tool
