"""
MCP Manager for coordinating multiple MCP servers.
Provides a unified interface for accessing external data sources.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from .base_server import BaseMCPServer, MCPResource

# Configure logging
logger = logging.getLogger(__name__)

class MCPSearchResult(BaseModel):
    """Unified model for MCP search results."""
    source: str
    title: str
    content: str
    url: Optional[str] = None
    relevance_score: float
    metadata: Dict[str, Any] = {}

class MCPManager:
    """Manager for coordinating multiple MCP servers."""
    
    def __init__(self):
        """Initialize the MCP manager."""
        self.servers: Dict[str, BaseMCPServer] = {}
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize all registered MCP servers."""
        if not self.is_initialized:
            logger.info("Initializing MCP Manager...")
            
            # Initialize all servers
            for server_name, server in self.servers.items():
                try:
                    await server.initialize()
                    logger.info(f"Initialized MCP server: {server_name}")
                except Exception as e:
                    logger.error(f"Failed to initialize MCP server {server_name}: {e}")
            
            self.is_initialized = True
            logger.info("MCP Manager initialization complete")
    
    def register_server(self, name: str, server: BaseMCPServer):
        """Register an MCP server.
        
        Args:
            name: Server name
            server: MCP server instance
        """
        self.servers[name] = server
        logger.info(f"Registered MCP server: {name}")
    
    async def search_all(self, query: str, max_results: int = 10, 
                        sources: Optional[List[str]] = None) -> List[MCPSearchResult]:
        """Search across all registered MCP servers.
        
        Args:
            query: Search query
            max_results: Maximum results per source
            sources: List of source names to search (None for all)
            
        Returns:
            List of unified search results
        """
        if not self.is_initialized:
            await self.initialize()
        
        results = []
        search_sources = sources if sources else list(self.servers.keys())
        
        # Search each source concurrently
        tasks = []
        for source_name in search_sources:
            if source_name in self.servers:
                task = self._search_source(source_name, query, max_results)
                tasks.append(task)
        
        # Wait for all searches to complete
        source_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine and format results
        for i, source_name in enumerate(search_sources):
            if source_name in self.servers:
                if isinstance(source_results[i], Exception):
                    logger.error(f"Search failed for {source_name}: {source_results[i]}")
                    continue
                
                for result in source_results[i]:
                    unified_result = MCPSearchResult(
                        source=source_name,
                        title=result.get("title", ""),
                        content=result.get("snippet", result.get("abstract", "")),
                        url=result.get("url"),
                        relevance_score=result.get("relevance_score", 0.0),
                        metadata=result
                    )
                    results.append(unified_result)
        
        # Sort by relevance score
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return results[:max_results * len(search_sources)]
    
    async def _search_source(self, source_name: str, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search a specific MCP source.
        
        Args:
            source_name: Name of the source
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of search results
        """
        try:
            server = self.servers[source_name]
            return await server.search(query, max_results)
        except Exception as e:
            logger.error(f"Search failed for {source_name}: {e}")
            return []
    
    async def get_content(self, source: str, resource_id: str) -> Optional[Dict[str, Any]]:
        """Get content from a specific MCP source.
        
        Args:
            source: Source name
            resource_id: Resource identifier
            
        Returns:
            Content data or None if not found
        """
        if not self.is_initialized:
            await self.initialize()
        
        if source not in self.servers:
            logger.error(f"Unknown MCP source: {source}")
            return None
        
        try:
            return await self.servers[source].get_content(resource_id)
        except Exception as e:
            logger.error(f"Failed to get content from {source}: {e}")
            return None
    
    async def list_all_resources(self, query: Optional[str] = None) -> Dict[str, List[MCPResource]]:
        """List resources from all MCP servers.
        
        Args:
            query: Optional filter query
            
        Returns:
            Dictionary mapping source names to resource lists
        """
        if not self.is_initialized:
            await self.initialize()
        
        resources = {}
        for source_name, server in self.servers.items():
            try:
                resources[source_name] = await server.list_resources(query)
            except Exception as e:
                logger.error(f"Failed to list resources for {source_name}: {e}")
                resources[source_name] = []
        
        return resources
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of all MCP servers.
        
        Returns:
            Health status for all servers
        """
        if not self.is_initialized:
            await self.initialize()
        
        health_status = {
            "manager_status": "healthy" if self.is_initialized else "not_initialized",
            "servers": {}
        }
        
        for source_name, server in self.servers.items():
            try:
                health_status["servers"][source_name] = await server.health_check()
            except Exception as e:
                health_status["servers"][source_name] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return health_status
    
    async def cleanup(self):
        """Clean up all MCP servers."""
        logger.info("Cleaning up MCP Manager...")
        
        cleanup_tasks = []
        for server_name, server in self.servers.items():
            task = server.cleanup()
            cleanup_tasks.append(task)
        
        await asyncio.gather(*cleanup_tasks, return_exceptions=True)
        self.is_initialized = False
        logger.info("MCP Manager cleanup complete")
    
    def get_available_sources(self) -> List[str]:
        """Get list of available MCP sources.
        
        Returns:
            List of source names
        """
        return list(self.servers.keys()) 