"""
Base tool interface for extensible tool system.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseTool(ABC):
    """Base class for all tools."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description."""
        pass
    
    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """Get tool schema for OpenAI function calling."""
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool with given parameters."""
        pass


class ToolRegistry:
    """Registry for managing tools."""
    
    def __init__(self):
        self._tools = {}
    
    def register(self, tool: BaseTool):
        """Register a tool."""
        self._tools[tool.name] = tool
    
    def get(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return self._tools.get(name)
    
    def list_tools(self) -> list[str]:
        """List all registered tool names."""
        return list(self._tools.keys())
    
    def get_schemas(self) -> list[Dict[str, Any]]:
        """Get schemas for all registered tools."""
        return [tool.get_schema() for tool in self._tools.values()]
    
    def execute_tool(self, name: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool by name."""
        tool = self.get(name)
        if not tool:
            return {"error": True, "message": f"Tool '{name}' not found"}
        
        try:
            return tool.execute(**kwargs)
        except Exception as e:
            return {
                "error": True,
                "message": f"Error executing tool '{name}': {str(e)}",
                "error_type": "execution_error"
            }