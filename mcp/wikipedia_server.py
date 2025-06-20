"""
Wikipedia MCP Server implementation.
Provides access to Wikipedia content through the MediaWiki API.
"""

import re
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from bs4 import BeautifulSoup
from .base_server import BaseMCPServer, MCPResource
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

class WikipediaSearchResult(BaseModel):
    """Model for Wikipedia search results."""
    title: str
    snippet: str
    page_id: int
    url: str
    relevance_score: float = 0.0

class WikipediaContent(BaseModel):
    """Model for Wikipedia article content."""
    title: str
    content: str
    summary: str
    categories: List[str]
    references: List[str]
    last_modified: Optional[str] = None
    url: str

class WikipediaMCPServer(BaseMCPServer):
    """MCP server for Wikipedia content access."""
    
    def __init__(self):
        """Initialize the Wikipedia MCP server."""
        super().__init__(
            name="Wikipedia MCP Server",
            description="Provides access to Wikipedia articles and search functionality"
        )
        self.base_url = "https://en.wikipedia.org/api/rest_v1"
        self.search_url = "https://en.wikipedia.org/w/api.php"
        
    async def _initialize_server(self):
        """Initialize Wikipedia-specific resources."""
        # Test connection to Wikipedia API
        try:
            await self._make_request(f"{self.base_url}/page/summary/Test")
            logger.info("Wikipedia API connection successful")
        except Exception as e:
            logger.warning(f"Wikipedia API connection test failed: {e}")
    
    async def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search Wikipedia for articles.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of search results
        """
        try:
            params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": query,
                "srlimit": max_results,
                "srnamespace": 0,  # Main namespace only
                "srprop": "snippet|title|pageid"
            }
            
            response = await self._make_request(
                url=self.search_url,
                params=params
            )
            
            results = []
            if "query" in response and "search" in response["query"]:
                for item in response["query"]["search"]:
                    result = {
                        "title": item["title"],
                        "snippet": self._clean_html(item["snippet"]),
                        "page_id": item["pageid"],
                        "url": f"https://en.wikipedia.org/wiki/{item['title'].replace(' ', '_')}",
                        "relevance_score": self._calculate_relevance(item["snippet"], query)
                    }
                    results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Wikipedia search failed: {e}")
            return []
    
    async def get_content(self, resource_id: str) -> Optional[Dict[str, Any]]:
        """Get Wikipedia article content.
        
        Args:
            resource_id: Wikipedia page title or ID
            
        Returns:
            Article content or None if not found
        """
        try:
            # Try to get content by title first
            content = await self._get_article_by_title(resource_id)
            if not content:
                # Try by page ID
                content = await self._get_article_by_id(resource_id)
            
            return content
            
        except Exception as e:
            logger.error(f"Failed to get Wikipedia content for {resource_id}: {e}")
            return None
    
    async def _get_article_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        """Get article content by title."""
        try:
            # Get article summary
            summary_url = f"{self.base_url}/page/summary/{title.replace(' ', '_')}"
            summary_response = await self._make_request(summary_url)
            
            # Get full article content
            content_url = f"{self.base_url}/page/html/{title.replace(' ', '_')}"
            content_response = await self._make_request(content_url)
            
            # Parse HTML content - content_response should be a string
            if isinstance(content_response, str):
                soup = BeautifulSoup(content_response, 'html.parser')
            else:
                logger.error("Unexpected content response type")
                return None
            
            # Extract main content
            main_content = soup.find('div', {'id': 'content'})
            if not main_content:
                return None
            
            # Extract text content
            content_text = self._extract_article_text(main_content)
            
            # Extract categories
            categories = self._extract_categories(soup)
            
            # Extract references
            references = self._extract_references(soup)
            
            return {
                "title": summary_response.get("title", title),
                "content": content_text,
                "summary": summary_response.get("extract", ""),
                "categories": categories,
                "references": references,
                "last_modified": summary_response.get("timestamp"),
                "url": summary_response.get("content_urls", {}).get("desktop", {}).get("page", "")
            }
            
        except Exception as e:
            logger.error(f"Failed to get article by title {title}: {e}")
            return None
    
    async def _get_article_by_id(self, page_id: str) -> Optional[Dict[str, Any]]:
        """Get article content by page ID."""
        try:
            # First get the title from page ID
            params = {
                "action": "query",
                "format": "json",
                "pageids": page_id,
                "prop": "info"
            }
            
            response = await self._make_request(
                url=self.search_url,
                params=params
            )
            
            if "query" in response and "pages" in response["query"]:
                page_info = list(response["query"]["pages"].values())[0]
                if "title" in page_info:
                    return await self._get_article_by_title(page_info["title"])
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get article by ID {page_id}: {e}")
            return None
    
    def _clean_html(self, html_text: str) -> str:
        """Clean HTML tags from text."""
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.get_text()
    
    def _extract_article_text(self, content_div) -> str:
        """Extract main article text from HTML."""
        # Remove navigation, sidebars, etc.
        for element in content_div.find_all(['nav', 'aside', 'script', 'style']):
            element.decompose()
        
        # Find main content area
        main_content = content_div.find('div', {'id': 'mw-content-text'})
        if main_content:
            # Remove unwanted elements
            for element in main_content.find_all(['table', 'script', 'style', 'sup']):
                element.decompose()
            
            # Get text content
            text = main_content.get_text()
            # Clean up whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            return text
        
        return content_div.get_text()
    
    def _extract_categories(self, soup: BeautifulSoup) -> List[str]:
        """Extract article categories."""
        categories = []
        category_links = soup.find_all('a', href=re.compile(r'/wiki/Category:'))
        for link in category_links:
            category_name = link.get_text().replace('Category:', '').strip()
            if category_name:
                categories.append(category_name)
        return categories[:10]  # Limit to 10 categories
    
    def _extract_references(self, soup: BeautifulSoup) -> List[str]:
        """Extract article references."""
        references = []
        ref_section = soup.find('ol', {'class': 'references'})
        if ref_section:
            ref_links = ref_section.find_all('a', href=True)
            for link in ref_links:
                ref_url = link.get('href')
                if ref_url and ref_url.startswith('http'):
                    references.append(ref_url)
        return references[:20]  # Limit to 20 references
    
    def _calculate_relevance(self, snippet: str, query: str) -> float:
        """Calculate relevance score for search result."""
        query_terms = query.lower().split()
        snippet_lower = snippet.lower()
        
        score = 0
        for term in query_terms:
            if term in snippet_lower:
                score += 1
        
        return min(score / len(query_terms), 1.0) if query_terms else 0.0
    
    async def list_resources(self, query: Optional[str] = None) -> List[MCPResource]:
        """List available Wikipedia resources."""
        # This would typically return a list of featured articles or categories
        # For now, return a basic list
        return [
            MCPResource(
                uri="wikipedia://featured",
                name="Featured Articles",
                description="Wikipedia featured articles",
                mime_type="application/json"
            )
        ] 