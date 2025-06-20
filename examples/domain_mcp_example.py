#!/usr/bin/env python3
"""
Domain-based MCP Architecture Example
Demonstrates agent segmentation by use case with specialized MCP server configurations.
"""

import asyncio
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp.domain_manager import DomainManager, AgentDomain, DEFAULT_DOMAIN_CONFIGS
from mcp.wikipedia_server import WikipediaMCPServer
from mcp.arxiv_server import ArxivMCPServer
from core.llm_service import LLMService

async def demonstrate_domain_architecture():
    """Demonstrate the domain-based MCP architecture."""
    print("🏗️  Domain-Based MCP Architecture Demonstration")
    print("=" * 60)
    print()
    
    # Initialize domain manager
    domain_manager = DomainManager()
    
    # Register domains with their configurations
    print("📋 Step 1: Registering Agent Domains...")
    for domain, config in DEFAULT_DOMAIN_CONFIGS.items():
        domain_manager.register_domain(domain, config)
        print(f"  ✅ {domain.value}: {config.description}")
    print()
    
    # Register MCP servers for different domains
    print("🔧 Step 2: Registering MCP Servers by Domain...")
    
    # Wikipedia server - available to research and general domains
    wikipedia_server = WikipediaMCPServer()
    domain_manager.register_server_for_domain(
        AgentDomain.RESEARCH, "wikipedia", wikipedia_server, priority=3
    )
    domain_manager.register_server_for_domain(
        AgentDomain.GENERAL, "wikipedia", wikipedia_server, priority=2
    )
    print("  ✅ Wikipedia server registered for RESEARCH and GENERAL domains")
    
    # arXiv server - available to research and general domains
    arxiv_server = ArxivMCPServer()
    domain_manager.register_server_for_domain(
        AgentDomain.RESEARCH, "arxiv", arxiv_server, priority=2
    )
    domain_manager.register_server_for_domain(
        AgentDomain.GENERAL, "arxiv", arxiv_server, priority=1
    )
    print("  ✅ arXiv server registered for RESEARCH and GENERAL domains")
    
    # Mock servers for other domains
    from mcp.base_server import BaseMCPServer
    
    class MockBusinessServer(BaseMCPServer):
        async def _initialize_server(self):
            pass
        async def search(self, query: str, max_results: int = 10):
            return [{"title": "Business Data", "snippet": "Strategic business information"}]
        async def get_content(self, resource_id: str):
            return {"title": "Business Content", "content": "Strategic business data"}
    
    class MockDataServer(BaseMCPServer):
        async def _initialize_server(self):
            pass
        async def search(self, query: str, max_results: int = 10):
            return [{"title": "Analytics Data", "snippet": "Data analysis results"}]
        async def get_content(self, resource_id: str):
            return {"title": "Analytics Content", "content": "Data analysis content"}
    
    # Register mock servers for strategic and data analysis domains
    business_server = MockBusinessServer("Business MCP Server", "Business data access")
    data_server = MockDataServer("Data MCP Server", "Data analysis access")
    
    domain_manager.register_server_for_domain(
        AgentDomain.STRATEGIC, "business_db", business_server, priority=3
    )
    domain_manager.register_server_for_domain(
        AgentDomain.DATA_ANALYSIS, "analytics_db", data_server, priority=3
    )
    print("  ✅ Mock servers registered for STRATEGIC and DATA_ANALYSIS domains")
    print()
    
    # Initialize all domains
    print("🚀 Step 3: Initializing Domain Managers...")
    await domain_manager.initialize_all()
    print("  ✅ All domain managers initialized")
    print()
    
    # Demonstrate domain-specific searches
    print("🔍 Step 4: Demonstrating Domain-Specific Searches...")
    
    # Research domain search
    print("  📚 RESEARCH Domain Search:")
    research_results = await domain_manager.search_domain(
        AgentDomain.RESEARCH, 
        "Model Context Protocol", 
        max_results=3
    )
    print(f"    Sources available: {domain_manager.get_domain_sources(AgentDomain.RESEARCH)}")
    print(f"    Results found: {len(research_results)}")
    for result in research_results[:2]:
        print(f"    - {result.title} (from {result.source})")
    print()
    
    # Strategic domain search
    print("  🎯 STRATEGIC Domain Search:")
    strategic_results = await domain_manager.search_domain(
        AgentDomain.STRATEGIC, 
        "business strategy", 
        max_results=3
    )
    print(f"    Sources available: {domain_manager.get_domain_sources(AgentDomain.STRATEGIC)}")
    print(f"    Results found: {len(strategic_results)}")
    for result in strategic_results:
        print(f"    - {result.title} (from {result.source})")
    print()
    
    # Data analysis domain search
    print("  📊 DATA_ANALYSIS Domain Search:")
    data_results = await domain_manager.search_domain(
        AgentDomain.DATA_ANALYSIS, 
        "data analysis", 
        max_results=3
    )
    print(f"    Sources available: {domain_manager.get_domain_sources(AgentDomain.DATA_ANALYSIS)}")
    print(f"    Results found: {len(data_results)}")
    for result in data_results:
        print(f"    - {result.title} (from {result.source})")
    print()
    
    # Demonstrate domain configurations
    print("⚙️  Step 5: Domain Configuration Analysis...")
    
    for domain in [AgentDomain.RESEARCH, AgentDomain.STRATEGIC, AgentDomain.DATA_ANALYSIS]:
        config = domain_manager.get_domain_config(domain)
        if config:
            print(f"  📋 {domain.value.upper()} Domain:")
            print(f"    Description: {config.description}")
            print(f"    Allowed Sources: {config.allowed_sources}")
            print(f"    Security Level: {config.security_level}")
            print(f"    Rate Limits: {config.rate_limits}")
            print(f"    Memory Config: {config.memory_config}")
            print()
    
    # Demonstrate health checks
    print("🏥 Step 6: Domain Health Checks...")
    health_status = await domain_manager.health_check_all()
    
    for domain_name, status in health_status["domains"].items():
        print(f"  🔍 {domain_name.upper()}: {status.get('manager_status', 'unknown')}")
        if 'servers' in status:
            for server_name, server_status in status['servers'].items():
                print(f"    - {server_name}: {server_status.get('status', 'unknown')}")
    print()
    
    # Demonstrate agent segmentation benefits
    print("🎯 Step 7: Agent Segmentation Benefits...")
    print("  ✅ WHY: Different agent groups have tailored toolsets and configurations")
    print("  ✅ HOW: Specialized MCP servers per function/domain")
    print("  ✅ BENEFIT: Cleaner, more maintainable configurations; fewer context collisions")
    print()
    
    # Show domain server priorities
    print("📈 Step 8: Domain Server Priorities...")
    for domain in [AgentDomain.RESEARCH, AgentDomain.STRATEGIC, AgentDomain.DATA_ANALYSIS]:
        servers = domain_manager.get_domain_servers(domain)
        print(f"  🎯 {domain.value.upper()} Domain Servers (by priority):")
        for server in servers:
            print(f"    - {server.server_name} (priority: {server.priority})")
        print()
    
    # Cleanup
    print("🧹 Step 9: Cleanup...")
    await domain_manager.cleanup_all()
    print("  ✅ All domain managers cleaned up")
    print()
    
    print("✅ Domain-Based MCP Architecture Demonstration Complete!")
    print()
    print("📚 Key Benefits Demonstrated:")
    print("  • Agent segmentation by use case")
    print("  • Domain-specific MCP server configurations")
    print("  • Tailored memory and context management")
    print("  • Security and rate limiting per domain")
    print("  • Cleaner, more maintainable architecture")

async def demonstrate_agent_integration():
    """Demonstrate how agents would integrate with domain-based MCP."""
    print("\n🤖 Agent Integration with Domain-Based MCP")
    print("=" * 50)
    
    # Initialize domain manager
    domain_manager = DomainManager()
    
    # Register research domain
    research_config = DEFAULT_DOMAIN_CONFIGS[AgentDomain.RESEARCH]
    domain_manager.register_domain(AgentDomain.RESEARCH, research_config)
    
    # Register servers for research domain
    wikipedia_server = WikipediaMCPServer()
    arxiv_server = ArxivMCPServer()
    
    domain_manager.register_server_for_domain(
        AgentDomain.RESEARCH, "wikipedia", wikipedia_server, priority=3
    )
    domain_manager.register_server_for_domain(
        AgentDomain.RESEARCH, "arxiv", arxiv_server, priority=2
    )
    
    await domain_manager.initialize_all()
    
    # Simulate researcher agent using domain-specific MCP
    print("🔬 Simulating Researcher Agent with Domain-Specific MCP...")
    
    # Research query
    query = "Model Context Protocol configuration"
    
    # Domain-specific search
    results = await domain_manager.search_domain(
        AgentDomain.RESEARCH, 
        query, 
        max_results=5
    )
    
    print(f"  📝 Query: {query}")
    print(f"  🎯 Domain: {AgentDomain.RESEARCH.value}")
    print(f"  📊 Results: {len(results)}")
    print(f"  🔧 Available Sources: {domain_manager.get_domain_sources(AgentDomain.RESEARCH)}")
    
    # Show domain configuration
    config = domain_manager.get_domain_config(AgentDomain.RESEARCH)
    if config:
        print(f"  ⚙️  Context Rules: {config.context_rules}")
        print(f"  🚦 Rate Limits: {config.rate_limits}")
        print(f"  🔒 Security Level: {config.security_level}")
    
    await domain_manager.cleanup_all()
    print("  ✅ Agent integration demonstration complete")

if __name__ == "__main__":
    asyncio.run(demonstrate_domain_architecture())
    asyncio.run(demonstrate_agent_integration()) 