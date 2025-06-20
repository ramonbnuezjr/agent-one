"""
Base MCP Server implementation for external data sources.
Provides the foundation for Wikipedia, arXiv, and other MCP servers.
"""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field
import aiohttp
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPRequest(BaseModel):
    """Base model for MCP requests."""
    method: str
    params: Dict[str, Any] = Field(default_factory=dict)
    id: Optional[str] = None

class MCPResponse(BaseModel):
    """Base model for MCP responses."""
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[str] = None

class MCPResource(BaseModel):
    """Model for MCP resource information."""
    uri: str
    name: str
    description: str
    mime_type: str
    size: Optional[int] = None
    last_modified: Optional[datetime] = None

class BaseMCPServer(ABC):
    """Base class for MCP servers providing external data access."""
    
    def __init__(self, name: str, description: str):
        """Initialize the MCP server.
        
        Args:
            name: Name of the MCP server
            description: Description of the server's capabilities
        """
        self.name = name
        self.description = description
        self.session: Optional[aiohttp.ClientSession] = None
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize the MCP server and create HTTP session."""
        if not self.is_initialized:
            self.session = aiohttp.ClientSession()
            await self._initialize_server()
            self.is_initialized = True
            logger.info(f"Initialized MCP server: {self.name}")
    
    @abstractmethod
    async def _initialize_server(self):
        """Initialize server-specific resources."""
        pass
    
    @abstractmethod
    async def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for information using the MCP server.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of search results
        """
        pass
    
    @abstractmethod
    async def get_content(self, resource_id: str) -> Optional[Dict[str, Any]]:
        """Get content for a specific resource.
        
        Args:
            resource_id: Identifier for the resource
            
        Returns:
            Resource content or None if not found
        """
        pass
    
    async def list_resources(self, query: Optional[str] = None) -> List[MCPResource]:
        """List available resources.
        
        Args:
            query: Optional filter query
            
        Returns:
            List of available resources
        """
        return []
    
    async def health_check(self) -> Dict[str, Any]:
        """Check the health of the MCP server.
        
        Returns:
            Health status information
        """
        return {
            "name": self.name,
            "status": "healthy" if self.is_initialized else "not_initialized",
            "description": self.description,
            "timestamp": datetime.now().isoformat()
        }
    
    async def cleanup(self):
        """Clean up server resources."""
        if self.session:
            await self.session.close()
            self.session = None
        self.is_initialized = False
        logger.info(f"Cleaned up MCP server: {self.name}")
    
    async def _make_request(self, url: str, method: str = "GET", 
                          headers: Optional[Dict[str, str]] = None,
                          params: Optional[Dict[str, Any]] = None,
                          data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make HTTP request with error handling.
        
        Args:
            url: Request URL
            method: HTTP method
            headers: Request headers
            params: Query parameters
            data: Request data
            
        Returns:
            Response data
            
        Raises:
            Exception: If request fails
        """
        if not self.session:
            raise Exception("MCP server not initialized")
        
        try:
            async with self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data
            ) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logger.error(f"Request failed for {url}: {str(e)}")
            raise
    
    def _format_response(self, data: Any, error: Optional[str] = None) -> MCPResponse:
        """Format response for MCP protocol.
        
        Args:
            data: Response data
            error: Error message if any
            
        Returns:
            Formatted MCP response
        """
        if error:
            return MCPResponse(error={"message": error})
        return MCPResponse(result=data) 