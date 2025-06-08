"""
Tool manager for centralized tool handling.
"""
from .base import ToolRegistry
from .weather import WeatherTool


class ToolManager:
    """Centralized manager for tools."""
    
    def __init__(self):
        self.registry = ToolRegistry()
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize and register all tools."""
        self.registry.register(WeatherTool())
    
    def get_tool_schemas(self):
        """Get schemas for all registered tools."""
        return self.registry.get_schemas()
    
    def execute_tool(self, name: str, **kwargs):
        """Execute a tool by name."""
        return self.registry.execute_tool(name, **kwargs)
    
    def list_tools(self):
        """List all available tools."""
        return self.registry.list_tools()
    
    def register_tool(self, tool):
        """Register a new tool."""
        self.registry.register(tool)


# Global tool manager instance
tool_manager = ToolManager()