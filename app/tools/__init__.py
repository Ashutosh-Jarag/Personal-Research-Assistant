"""
Tool Manager - Central place to get all tools
"""

from app.tools.search_tool import create_search_tool, WebSearchTool
from app.tools.scraper_tool import create_scraper_tool, WebScraperTool
from typing import List
from langchain.tools import Tool


def get_all_tools() -> List[Tool]:
    """
    Get all available tools for the agent
    
    Returns:
        List of LangChain Tools
    """
    return [
        create_search_tool(),
        create_scraper_tool()
    ]


def get_tool_by_name(tool_name: str) -> Tool:
    """
    Get a specific tool by name
    
    Args:
        tool_name: Name of the tool ('web_search' or 'web_scraper')
        
    Returns:
        Tool instance
    """
    tools = {
        'web_search': create_search_tool(),
        'web_scraper': create_scraper_tool()
    }
    
    return tools.get(tool_name)


# Export for easy imports
__all__ = [
    'get_all_tools',
    'get_tool_by_name',
    'WebSearchTool',
    'WebScraperTool',
    'create_search_tool',
    'create_scraper_tool'
]