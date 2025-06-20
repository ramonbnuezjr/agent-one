"""
arXiv MCP Server implementation.
Provides access to academic papers through the arXiv API.
"""

import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from .base_server import BaseMCPServer, MCPResource
from datetime import datetime
import xml.etree.ElementTree as ET

# Configure logging
logger = logging.getLogger(__name__)

class ArxivSearchResult(BaseModel):
    """Model for arXiv search results."""
    title: str
    authors: List[str]
    abstract: str
    arxiv_id: str
    categories: List[str]
    published_date: Optional[str] = None
    relevance_score: float = 0.0

class ArxivPaper(BaseModel):
    """Model for arXiv paper content."""
    title: str
    authors: List[str]
    abstract: str
    arxiv_id: str
    categories: List[str]
    published_date: Optional[str] = None
    updated_date: Optional[str] = None
    pdf_url: Optional[str] = None
    doi: Optional[str] = None

class ArxivMCPServer(BaseMCPServer):
    """MCP server for arXiv content access."""
    
    def __init__(self):
        """Initialize the arXiv MCP server."""
        super().__init__(
            name="arXiv MCP Server",
            description="Provides access to arXiv academic papers and search functionality"
        )
        self.base_url = "http://export.arxiv.org/api/query"
        
    async def _initialize_server(self):
        """Initialize arXiv-specific resources."""
        # Test connection to arXiv API
        try:
            test_params = {
                "search_query": "all:test",
                "start": 0,
                "max_results": 1
            }
            await self._make_request(self.base_url, params=test_params)
            logger.info("arXiv API connection successful")
        except Exception as e:
            logger.warning(f"arXiv API connection test failed: {e}")
    
    async def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search arXiv for papers.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of search results
        """
        try:
            params = {
                "search_query": query,
                "start": 0,
                "max_results": max_results,
                "sortBy": "relevance",
                "sortOrder": "descending"
            }
            
            response = await self._make_request(
                url=self.base_url,
                params=params
            )
            
            # Parse XML response
            results = self._parse_arxiv_response(response)
            
            # Calculate relevance scores
            for result in results:
                result["relevance_score"] = self._calculate_relevance(
                    result["title"] + " " + result["abstract"], query
                )
            
            return results
            
        except Exception as e:
            logger.error(f"arXiv search failed: {e}")
            return []
    
    async def get_content(self, resource_id: str) -> Optional[Dict[str, Any]]:
        """Get arXiv paper content.
        
        Args:
            resource_id: arXiv ID (e.g., "2103.12345")
            
        Returns:
            Paper content or None if not found
        """
        try:
            # Search for the specific paper
            params = {
                "id_list": resource_id,
                "start": 0,
                "max_results": 1
            }
            
            response = await self._make_request(
                url=self.base_url,
                params=params
            )
            
            # Parse XML response
            papers = self._parse_arxiv_response(response)
            
            if papers:
                paper = papers[0]
                return {
                    "title": paper["title"],
                    "authors": paper["authors"],
                    "abstract": paper["abstract"],
                    "arxiv_id": paper["arxiv_id"],
                    "categories": paper["categories"],
                    "published_date": paper["published_date"],
                    "pdf_url": f"https://arxiv.org/pdf/{paper['arxiv_id']}",
                    "doi": paper.get("doi")
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get arXiv content for {resource_id}: {e}")
            return None
    
    def _parse_arxiv_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse arXiv XML response."""
        try:
            root = ET.fromstring(response)
            
            # Define namespace
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            results = []
            for entry in root.findall('.//atom:entry', ns):
                paper = {}
                
                # Extract title
                title_elem = entry.find('atom:title', ns)
                if title_elem is not None:
                    paper["title"] = title_elem.text.strip()
                
                # Extract authors
                authors = []
                for author in entry.findall('.//atom:name', ns):
                    if author.text:
                        authors.append(author.text.strip())
                paper["authors"] = authors
                
                # Extract abstract
                summary_elem = entry.find('atom:summary', ns)
                if summary_elem is not None:
                    paper["abstract"] = summary_elem.text.strip()
                
                # Extract arXiv ID
                id_elem = entry.find('atom:id', ns)
                if id_elem is not None:
                    paper["arxiv_id"] = id_elem.text.split('/')[-1]
                
                # Extract categories
                categories = []
                for link in entry.findall('.//atom:link', ns):
                    if link.get('title') == 'pdf':
                        categories.append(link.get('title', ''))
                paper["categories"] = categories
                
                # Extract dates
                published_elem = entry.find('atom:published', ns)
                if published_elem is not None:
                    paper["published_date"] = published_elem.text
                
                results.append(paper)
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to parse arXiv response: {e}")
            return []
    
    def _calculate_relevance(self, text: str, query: str) -> float:
        """Calculate relevance score for search result."""
        query_terms = query.lower().split()
        text_lower = text.lower()
        
        score = 0
        for term in query_terms:
            if term in text_lower:
                score += 1
        
        return min(score / len(query_terms), 1.0) if query_terms else 0.0
    
    async def list_resources(self, query: Optional[str] = None) -> List[MCPResource]:
        """List available arXiv resources."""
        return [
            MCPResource(
                uri="arxiv://recent",
                name="Recent Papers",
                description="Recently published arXiv papers",
                mime_type="application/json"
            ),
            MCPResource(
                uri="arxiv://popular",
                name="Popular Papers",
                description="Popular arXiv papers",
                mime_type="application/json"
            )
        ] 