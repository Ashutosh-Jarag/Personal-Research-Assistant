"""
Web Search Tool using Tavily API
Tavily is optimized for AI agents - returns clean, relevant results
"""

try:
    from langchain.tools import Tool
except Exception:
    # langchain may not be installed in some environments (tests, CI, local dev).
    # Delay hard failures and provide a fallback in create_search_tool.
    Tool = None
from app.core.config import settings
from typing import List, Dict
import json


class WebSearchTool:
    """
    Wrapper for Tavily search optimized for research
    """
    
    def __init__(self, api_key: str | None = None, max_results: int = 5):
        """Initialize Tavily search.

        If no API key is available, the tool will be disabled but
        the module will not crash at import time. This makes it safe
        to import the package in environments where the key isn't set
        (e.g., during local development or unit tests).
        """
        self._enabled = False
        self._init_error: str | None = None

        resolved_key = api_key or settings.TAVILY_API_KEY
        # Lazy import of TavilySearchResults to avoid import-time errors when the
        # optional dependency isn't installed (e.g., during local dev or in CI).
        try:
            from langchain_community.tools.tavily_search import TavilySearchResults
        except Exception as e:
            # Dependency missing or import failure
            self.tavily = None
            self._init_error = (
                "langchain_community or Tavily client not available: "
                f"{e}. Install 'langchain-community' or add the package that provides "
                "TavilySearchResults to enable web search."
            )
            return
        if not resolved_key:
            # Do not raise here; provide a helpful message and keep the tool disabled
            self.tavily = None
            self._init_error = (
                "TAVILY_API_KEY is not set. To enable web search, set the environment "
                "variable `TAVILY_API_KEY` or pass `api_key` when creating WebSearchTool."
            )
            return

        # Try to initialize the Tavily client and capture initialization errors
        try:
            self.tavily = TavilySearchResults(
                api_key=resolved_key,
                max_results=max_results,  # Number of results per search
                search_depth="advanced",  # "basic" or "advanced"
                include_answer=True,  # Get AI-generated answer
                include_raw_content=False,  # We'll scrape ourselves
                include_images=False,
            )
            self._enabled = True
        except Exception as e:
            # Store the error and keep the tool disabled instead of raising
            self.tavily = None
            self._init_error = f"Failed to initialize TavilySearchResults: {e}"
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Perform web search
        
        Args:
            query: Search query string
            max_results: Maximum number of results
            
        Returns:
            List of search results with url, title, content
        """
        # If the Tavily client couldn't be initialized, return an empty list
        if not getattr(self, "_enabled", False) or self.tavily is None:
            # Provide a helpful message for developers/operators
            err_msg = (
                self._init_error
                or "Tavily search is disabled because a valid API key could not be found."
            )
            print(f"WebSearchTool unavailable: {err_msg}")
            return []

        try:
            # Update max_results
            self.tavily.max_results = max_results

            # Perform search
            results = self.tavily.invoke({"query": query})
            
            # Parse results
            parsed_results = []
            for result in results:
                parsed_results.append({
                    "url": result.get("url", ""),
                    "title": result.get("title", "No title"),
                    "content": result.get("content", ""),
                    "score": result.get("score", 0.0)
                })
            
            return parsed_results
            
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []
    
    def search_with_context(self, topic: str, context: str = "") -> List[Dict]:
        """
        Search with additional context for better results
        
        Args:
            topic: Main search topic
            context: Additional context to refine search
            
        Returns:
            List of search results
        """
        # Build enhanced query
        query = f"{topic}"
        if context:
            query += f" {context}"
        
        return self.search(query)


# Create LangChain Tool wrapper
def create_search_tool() -> object:
    """
    Create a LangChain Tool for the agent to use
    
    This wraps our WebSearchTool in LangChain's Tool interface
    so the agent can call it
    """
    search_tool = WebSearchTool()

    description = (
        "Search the web for current information. "
        "Input should be a search query string. "
        "Returns a list of relevant web pages with titles and summaries. "
        "Use this when you need to find recent information or sources."
    )

    # If langchain is available, return a proper Tool instance. Otherwise return
    # a lightweight dict-like fallback so importing this module doesn't fail.
    if Tool is not None:
        return Tool(
            name="web_search",
            description=description,
            func=lambda query: json.dumps(search_tool.search(query), indent=2),
        )

    # Fallback: return a simple object (dict) so code importing create_search_tool
    # can still call the function in environments without langchain installed.
    return {
        "name": "web_search",
        "description": description,
        "func": lambda query: json.dumps(search_tool.search(query), indent=2),
    }


# Test function
async def test_search_tool():
    """Test the search tool"""
    try:
        tool = WebSearchTool()
        results = tool.search("quantum computing breakthroughs 2024", max_results=3)
        
        return {
            "status": "success",
            "query": "quantum computing breakthroughs 2024",
            "results_count": len(results),
            "results": results
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }