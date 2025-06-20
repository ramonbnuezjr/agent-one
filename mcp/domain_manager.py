"""
Domain Manager for MCP Agent Segmentation by Use Case.
Supports specialized MCP server configurations for different agent groups.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Set
from pydantic import BaseModel, Field
from enum import Enum
from .mcp_manager import MCPManager, MCPSearchResult
from .base_server import BaseMCPServer

# Configure logging
logger = logging.getLogger(__name__)

class AgentDomain(Enum):
    """Enumeration of agent domains/use cases."""
    RESEARCH = "research"
    STRATEGIC = "strategic"
    DATA_ANALYSIS = "data_analysis"
    WRITER = "writer"
    OPS_MANAGER = "ops_manager"
    CUSTOMER_SUPPORT = "customer_support"
    RAG = "rag"
    GENERAL = "general"

class DomainConfig(BaseModel):
    """Configuration for a specific agent domain."""
    domain: AgentDomain
    description: str
    allowed_sources: List[str] = Field(default_factory=list)
    memory_config: Dict[str, Any] = Field(default_factory=dict)
    context_rules: Dict[str, Any] = Field(default_factory=dict)
    rate_limits: Dict[str, int] = Field(default_factory=dict)
    security_level: str = "standard"  # "low", "standard", "high", "restricted"

class DomainMCPServer(BaseModel):
    """MCP server configuration for a specific domain."""
    server_name: str
    domain: AgentDomain
    priority: int = 1  # Higher number = higher priority
    enabled: bool = True
    custom_config: Dict[str, Any] = Field(default_factory=dict)

class DomainManager:
    """Manager for domain-specific MCP configurations and agent segmentation."""
    
    def __init__(self):
        """Initialize the domain manager."""
        self.domains: Dict[AgentDomain, DomainConfig] = {}
        self.domain_servers: Dict[AgentDomain, List[DomainMCPServer]] = {}
        self.global_mcp_manager = MCPManager()
        self.domain_managers: Dict[AgentDomain, MCPManager] = {}
        self.is_initialized = False
        
    def register_domain(self, domain: AgentDomain, config: DomainConfig):
        """Register a new agent domain with its configuration.
        
        Args:
            domain: The agent domain
            config: Domain configuration
        """
        self.domains[domain] = config
        self.domain_servers[domain] = []
        logger.info(f"Registered domain: {domain.value}")
    
    def register_server_for_domain(self, domain: AgentDomain, server_name: str, 
                                 server: BaseMCPServer, priority: int = 1,
                                 custom_config: Optional[Dict[str, Any]] = None):
        """Register an MCP server for a specific domain.
        
        Args:
            domain: The agent domain
            server_name: Name of the server
            server: MCP server instance
            priority: Priority level (higher = more important)
            custom_config: Domain-specific server configuration
        """
        if domain not in self.domains:
            raise ValueError(f"Domain {domain.value} not registered")
        
        # Register with global manager
        self.global_mcp_manager.register_server(server_name, server)
        
        # Register with domain-specific manager
        if domain not in self.domain_managers:
            self.domain_managers[domain] = MCPManager()
        
        self.domain_managers[domain].register_server(server_name, server)
        
        # Add to domain server list
        domain_server = DomainMCPServer(
            server_name=server_name,
            domain=domain,
            priority=priority,
            custom_config=custom_config or {}
        )
        self.domain_servers[domain].append(domain_server)
        
        # Sort by priority
        self.domain_servers[domain].sort(key=lambda x: x.priority, reverse=True)
        
        logger.info(f"Registered server {server_name} for domain {domain.value} (priority: {priority})")
    
    async def initialize_domain(self, domain: AgentDomain):
        """Initialize MCP servers for a specific domain.
        
        Args:
            domain: The agent domain to initialize
        """
        if domain not in self.domain_managers:
            logger.warning(f"Domain {domain.value} not found in domain managers")
            return
        
        await self.domain_managers[domain].initialize()
        logger.info(f"Initialized domain: {domain.value}")
    
    async def initialize_all(self):
        """Initialize all domain managers."""
        if self.is_initialized:
            return
        
        logger.info("Initializing Domain Manager...")
        
        # Initialize global manager
        await self.global_mcp_manager.initialize()
        
        # Initialize all domain managers
        for domain in self.domain_managers:
            await self.initialize_domain(domain)
        
        self.is_initialized = True
        logger.info("Domain Manager initialization complete")
    
    async def search_domain(self, domain: AgentDomain, query: str, 
                          max_results: int = 10, 
                          sources: Optional[List[str]] = None) -> List[MCPSearchResult]:
        """Search using domain-specific MCP servers.
        
        Args:
            domain: The agent domain
            query: Search query
            max_results: Maximum results per source
            sources: List of source names to search (None for domain defaults)
            
        Returns:
            List of search results from domain-specific sources
        """
        if not self.is_initialized:
            await self.initialize_all()
        
        if domain not in self.domain_managers:
            logger.warning(f"Domain {domain.value} not found, using global search")
            return await self.global_mcp_manager.search_all(query, max_results, sources)
        
        # Use domain-specific sources if none specified
        if sources is None:
            domain_config = self.domains.get(domain)
            if domain_config and domain_config.allowed_sources:
                sources = domain_config.allowed_sources
        
        return await self.domain_managers[domain].search_all(query, max_results, sources)
    
    async def get_content_domain(self, domain: AgentDomain, source: str, 
                               resource_id: str) -> Optional[Dict[str, Any]]:
        """Get content from a domain-specific MCP source.
        
        Args:
            domain: The agent domain
            source: Source name
            resource_id: Resource identifier
            
        Returns:
            Content data or None if not found
        """
        if not self.is_initialized:
            await self.initialize_all()
        
        if domain not in self.domain_managers:
            logger.warning(f"Domain {domain.value} not found, using global manager")
            return await self.global_mcp_manager.get_content(source, resource_id)
        
        return await self.domain_managers[domain].get_content(source, resource_id)
    
    def get_domain_sources(self, domain: AgentDomain) -> List[str]:
        """Get available sources for a specific domain.
        
        Args:
            domain: The agent domain
            
        Returns:
            List of available source names for the domain
        """
        if domain not in self.domain_managers:
            return []
        
        return self.domain_managers[domain].get_available_sources()
    
    def get_domain_config(self, domain: AgentDomain) -> Optional[DomainConfig]:
        """Get configuration for a specific domain.
        
        Args:
            domain: The agent domain
            
        Returns:
            Domain configuration or None if not found
        """
        return self.domains.get(domain)
    
    async def health_check_domain(self, domain: AgentDomain) -> Dict[str, Any]:
        """Check health of MCP servers for a specific domain.
        
        Args:
            domain: The agent domain
            
        Returns:
            Health status for the domain
        """
        if domain not in self.domain_managers:
            return {"status": "domain_not_found", "error": f"Domain {domain.value} not registered"}
        
        return await self.domain_managers[domain].health_check()
    
    async def health_check_all(self) -> Dict[str, Any]:
        """Check health of all domain managers.
        
        Returns:
            Health status for all domains
        """
        health_status = {
            "global_manager": await self.global_mcp_manager.health_check(),
            "domains": {}
        }
        
        for domain in self.domain_managers:
            health_status["domains"][domain.value] = await self.health_check_domain(domain)
        
        return health_status
    
    def list_domains(self) -> List[AgentDomain]:
        """List all registered domains.
        
        Returns:
            List of registered domains
        """
        return list(self.domains.keys())
    
    def get_domain_servers(self, domain: AgentDomain) -> List[DomainMCPServer]:
        """Get servers configured for a specific domain.
        
        Args:
            domain: The agent domain
            
        Returns:
            List of domain server configurations
        """
        return self.domain_servers.get(domain, [])
    
    async def cleanup_domain(self, domain: AgentDomain):
        """Clean up MCP servers for a specific domain.
        
        Args:
            domain: The agent domain
        """
        if domain in self.domain_managers:
            await self.domain_managers[domain].cleanup()
            logger.info(f"Cleaned up domain: {domain.value}")
    
    async def cleanup_all(self):
        """Clean up all domain managers."""
        logger.info("Cleaning up Domain Manager...")
        
        # Clean up global manager
        await self.global_mcp_manager.cleanup()
        
        # Clean up all domain managers
        cleanup_tasks = []
        for domain in self.domain_managers:
            cleanup_tasks.append(self.cleanup_domain(domain))
        
        await asyncio.gather(*cleanup_tasks, return_exceptions=True)
        self.is_initialized = False
        logger.info("Domain Manager cleanup complete")

    def get_registered_domains(self):
        """Return a list of all registered domains and their statuses."""
        domains_list = []
        for domain in self.domains:
            domain_info = {
                'name': domain.value,  # Use .value to get the string representation
                'status': 'active',
                'servers': []
            }
            if domain in self.domain_servers:
                for server_info in self.domain_servers[domain]:
                    if isinstance(server_info, tuple) and len(server_info) == 2:
                        server, priority = server_info
                        domain_info['servers'].append({
                            'name': server.server_name if hasattr(server, 'server_name') else str(server),
                            'priority': priority
                        })
            domains_list.append(domain_info)
        return domains_list

# Predefined domain configurations
DEFAULT_DOMAIN_CONFIGS = {
    AgentDomain.RESEARCH: DomainConfig(
        domain=AgentDomain.RESEARCH,
        description="Research agents with access to academic and web sources",
        allowed_sources=["wikipedia", "arxiv", "web_search", "academic_db"],
        memory_config={"cache_duration": 3600, "max_cache_size": 1000},
        context_rules={"max_context_length": 8000, "include_metadata": True},
        rate_limits={"requests_per_minute": 60, "daily_limit": 10000},
        security_level="standard"
    ),
    
    AgentDomain.STRATEGIC: DomainConfig(
        domain=AgentDomain.STRATEGIC,
        description="Strategic agents with access to business and policy data",
        allowed_sources=["business_db", "policy_db", "financial_data", "market_research"],
        memory_config={"cache_duration": 7200, "max_cache_size": 500},
        context_rules={"max_context_length": 12000, "include_metadata": True},
        rate_limits={"requests_per_minute": 30, "daily_limit": 5000},
        security_level="high"
    ),
    
    AgentDomain.DATA_ANALYSIS: DomainConfig(
        domain=AgentDomain.DATA_ANALYSIS,
        description="Data analysis agents with access to databases and analytics tools",
        allowed_sources=["postgres", "mongodb", "analytics_db", "data_warehouse"],
        memory_config={"cache_duration": 1800, "max_cache_size": 2000},
        context_rules={"max_context_length": 16000, "include_metadata": True},
        rate_limits={"requests_per_minute": 120, "daily_limit": 20000},
        security_level="high"
    ),
    
    AgentDomain.WRITER: DomainConfig(
        domain=AgentDomain.WRITER,
        description="Writer agents with access to content and style guides",
        allowed_sources=["style_guides", "content_db", "templates", "reference_materials"],
        memory_config={"cache_duration": 14400, "max_cache_size": 300},
        context_rules={"max_context_length": 6000, "include_metadata": False},
        rate_limits={"requests_per_minute": 45, "daily_limit": 8000},
        security_level="standard"
    ),
    
    AgentDomain.OPS_MANAGER: DomainConfig(
        domain=AgentDomain.OPS_MANAGER,
        description="Operations manager agents with access to operational data",
        allowed_sources=["ops_db", "monitoring", "logs", "performance_metrics"],
        memory_config={"cache_duration": 900, "max_cache_size": 1500},
        context_rules={"max_context_length": 10000, "include_metadata": True},
        rate_limits={"requests_per_minute": 90, "daily_limit": 15000},
        security_level="high"
    ),
    
    AgentDomain.CUSTOMER_SUPPORT: DomainConfig(
        domain=AgentDomain.CUSTOMER_SUPPORT,
        description="Customer support agents with access to support databases",
        allowed_sources=["support_db", "knowledge_base", "ticket_system", "faq_db"],
        memory_config={"cache_duration": 3600, "max_cache_size": 800},
        context_rules={"max_context_length": 4000, "include_metadata": False},
        rate_limits={"requests_per_minute": 150, "daily_limit": 25000},
        security_level="standard"
    ),
    
    AgentDomain.RAG: DomainConfig(
        domain=AgentDomain.RAG,
        description="RAG agents with access to vector databases and embeddings",
        allowed_sources=["vector_db", "embeddings", "document_store", "semantic_search"],
        memory_config={"cache_duration": 300, "max_cache_size": 3000},
        context_rules={"max_context_length": 20000, "include_metadata": True},
        rate_limits={"requests_per_minute": 200, "daily_limit": 30000},
        security_level="standard"
    ),
    
    AgentDomain.GENERAL: DomainConfig(
        domain=AgentDomain.GENERAL,
        description="General purpose agents with access to all sources",
        allowed_sources=[],  # Empty means all sources
        memory_config={"cache_duration": 1800, "max_cache_size": 1000},
        context_rules={"max_context_length": 8000, "include_metadata": True},
        rate_limits={"requests_per_minute": 60, "daily_limit": 10000},
        security_level="standard"
    )
} 