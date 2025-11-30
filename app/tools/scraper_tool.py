"""
Web Scraping Tool
Extracts clean text content from web pages
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict
from langchain.tools import Tool
import json
from urllib.parse import urlparse


class WebScraperTool:
    """
    Scrapes and cleans web page content
    """
    
    def __init__(self, timeout: int = 10):
        """
        Initialize scraper
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape(self, url: str) -> Dict:
        """
        Scrape content from a URL
        
        Args:
            url: Web page URL to scrape
            
        Returns:
            Dictionary with title, content, and metadata
        """
        try:
            # Validate URL
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return {
                    "success": False,
                    "error": "Invalid URL format"
                }
            
            # Fetch page
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout,
                allow_redirects=True
            )
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Extract title
            title = self._extract_title(soup)
            
            # Extract main content
            content = self._extract_content(soup)
            
            # Calculate word count
            word_count = len(content.split())
            
            return {
                "success": True,
                "url": url,
                "title": title,
                "content": content,
                "word_count": word_count,
                "status_code": response.status_code
            }
            
        except requests.Timeout:
            return {
                "success": False,
                "error": "Request timeout"
            }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Scraping failed: {str(e)}"
            }
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        # Try <title> tag
        if soup.title and soup.title.string:
            return soup.title.string.strip()
        
        # Try <h1> tag
        h1 = soup.find('h1')
        if h1:
            return h1.get_text().strip()
        
        return "No title found"
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """
        Extract main content from page
        Removes scripts, styles, navigation, etc.
        """
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()
        
        # Try to find main content area
        main_content = (
            soup.find('main') or 
            soup.find('article') or 
            soup.find('div', class_=['content', 'main-content', 'post-content']) or
            soup.find('body')
        )
        
        if not main_content:
            return "No content found"
        
        # Extract text
        text = main_content.get_text(separator='\n', strip=True)
        
        # Clean up text
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        clean_text = '\n'.join(lines)
        
        # Limit length (prevent huge pages)
        max_chars = 10000
        if len(clean_text) > max_chars:
            clean_text = clean_text[:max_chars] + "...[truncated]"
        
        return clean_text
    
    def scrape_multiple(self, urls: list) -> list:
        """
        Scrape multiple URLs
        
        Args:
            urls: List of URLs to scrape
            
        Returns:
            List of scraping results
        """
        results = []
        for url in urls:
            result = self.scrape(url)
            results.append(result)
        return results


# Create LangChain Tool wrapper
def create_scraper_tool() -> Tool:
    """
    Create a LangChain Tool for the agent to use
    """
    scraper = WebScraperTool()
    
    return Tool(
        name="web_scraper",
        description=(
            "Extract text content from a web page. "
            "Input should be a valid URL. "
            "Returns the page title and main text content. "
            "Use this after searching to get detailed information from specific pages."
        ),
        func=lambda url: json.dumps(scraper.scrape(url), indent=2)
    )


# Test function
async def test_scraper_tool():
    """Test the scraper tool"""
    try:
        scraper = WebScraperTool()
        
        # Test with a reliable URL
        test_url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
        result = scraper.scrape(test_url)
        
        return {
            "status": "success",
            "test_url": test_url,
            "result": {
                "success": result.get("success"),
                "title": result.get("title"),
                "word_count": result.get("word_count"),
                "content_preview": result.get("content", "")[:200] + "..."
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }