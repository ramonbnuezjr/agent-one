import asyncio
import json
from agents.researcher.researcher import Researcher
from mcp.mcp_manager import MCPManager
from mcp.wikipedia_server import WikipediaMCPServer
from mcp.arxiv_server import ArxivMCPServer

async def setup_mcp_servers():
    """Set up and register MCP servers."""
    print("🔧 Setting up MCP Servers...")
    
    mcp_manager = MCPManager()
    
    # Register Wikipedia MCP server
    wikipedia_server = WikipediaMCPServer()
    mcp_manager.register_server("wikipedia", wikipedia_server)
    
    # Register arXiv MCP server
    arxiv_server = ArxivMCPServer()
    mcp_manager.register_server("arxiv", arxiv_server)
    
    # Initialize all servers
    await mcp_manager.initialize()
    
    print(f"✅ MCP Servers initialized: {mcp_manager.get_available_sources()}")
    return mcp_manager

async def test_mcp_research():
    """Test MCP research functionality."""
    print("\n🔍 Testing MCP Research...")
    
    # Set up MCP servers
    mcp_manager = await setup_mcp_servers()
    
    # Create researcher with MCP integration
    researcher = Researcher()
    
    # Test MCP research
    mcp_request = {
        "type": "mcp_research",
        "data": {
            "query": "What is a basic configuration of a Model Context Protocol (MCP) setup?",
            "max_results": 5,
            "sources": ["wikipedia", "arxiv"]
        }
    }
    
    response = await researcher.process_request(mcp_request)
    
    if response.success:
        print("✅ MCP research completed successfully!")
        print(f"📊 Found {len(response.data['sources'])} sources")
        print(f"🔗 MCP sources: {response.data['mcp_sources']}")
        print(f"📝 Synthesis: {response.data['synthesis'][:200]}...")
        print(f"🎯 Key findings: {len(response.data['key_findings'])} identified")
        print(f"💡 Recommendations: {len(response.data['recommendations'])} generated")
    else:
        print(f"❌ MCP research failed: {response.errors}")
    
    await mcp_manager.cleanup()
    await researcher.cleanup()

async def test_comprehensive_research():
    """Test comprehensive research (web + MCP)."""
    print("\n🌐 Testing Comprehensive Research (Web + MCP)...")
    
    # Set up MCP servers
    mcp_manager = await setup_mcp_servers()
    
    # Create researcher with MCP integration
    researcher = Researcher()
    
    # Test comprehensive research
    comprehensive_request = {
        "type": "comprehensive_research",
        "data": {
            "query": "DSS service delivery optimization",
            "max_results": 3,
            "include_web": True,
            "include_mcp": True
        }
    }
    
    response = await researcher.process_request(comprehensive_request)
    
    if response.success:
        print("✅ Comprehensive research completed successfully!")
        print(f"📊 Found {len(response.data['sources'])} total sources")
        print(f"🌐 Web sources: {response.data['source_breakdown']['web_sources']}")
        print(f"🔗 MCP sources: {response.data['source_breakdown']['mcp_sources']}")
        print(f"📝 Synthesis: {response.data['synthesis'][:200]}...")
        print(f"🎯 Key findings: {len(response.data['key_findings'])} identified")
        print(f"💡 Recommendations: {len(response.data['recommendations'])} generated")
    else:
        print(f"❌ Comprehensive research failed: {response.errors}")
    
    await mcp_manager.cleanup()
    await researcher.cleanup()

async def test_wikipedia_specific():
    """Test Wikipedia-specific research."""
    print("\n📚 Testing Wikipedia-Specific Research...")
    
    # Set up MCP servers
    mcp_manager = await setup_mcp_servers()
    
    # Create researcher with MCP integration
    researcher = Researcher()
    
    # Test Wikipedia research
    wikipedia_request = {
        "type": "mcp_research",
        "data": {
            "query": "social welfare programs",
            "max_results": 3,
            "sources": ["wikipedia"]
        }
    }
    
    response = await researcher.process_request(wikipedia_request)
    
    if response.success:
        print("✅ Wikipedia research completed successfully!")
        print(f"📊 Found {len(response.data['sources'])} Wikipedia sources")
        print(f"📝 Synthesis: {response.data['synthesis'][:200]}...")
        print(f"🎯 Key findings: {len(response.data['key_findings'])} identified")
    else:
        print(f"❌ Wikipedia research failed: {response.errors}")
    
    await mcp_manager.cleanup()
    await researcher.cleanup()

async def test_arxiv_specific():
    """Test arXiv-specific research."""
    print("\n📄 Testing arXiv-Specific Research...")
    
    # Set up MCP servers
    mcp_manager = await setup_mcp_servers()
    
    # Create researcher with MCP integration
    researcher = Researcher()
    
    # Test arXiv research
    arxiv_request = {
        "type": "mcp_research",
        "data": {
            "query": "machine learning social services",
            "max_results": 3,
            "sources": ["arxiv"]
        }
    }
    
    response = await researcher.process_request(arxiv_request)
    
    if response.success:
        print("✅ arXiv research completed successfully!")
        print(f"📊 Found {len(response.data['sources'])} arXiv sources")
        print(f"📝 Synthesis: {response.data['synthesis'][:200]}...")
        print(f"🎯 Key findings: {len(response.data['key_findings'])} identified")
    else:
        print(f"❌ arXiv research failed: {response.errors}")
    
    await mcp_manager.cleanup()
    await researcher.cleanup()

async def test_mcp_health_check():
    """Test MCP server health checks."""
    print("\n🏥 Testing MCP Health Checks...")
    
    # Set up MCP servers
    mcp_manager = await setup_mcp_servers()
    
    # Check health status
    health_status = await mcp_manager.health_check()
    
    print("✅ MCP Health Check Results:")
    print(f"📊 Manager Status: {health_status['manager_status']}")
    print("🔗 Server Status:")
    for server_name, status in health_status['servers'].items():
        print(f"  - {server_name}: {status.get('status', 'unknown')}")
    
    await mcp_manager.cleanup()

async def test_mcp_integration_with_strategist():
    """Test MCP research integration with the Strategist agent."""
    print("\n🤝 Testing MCP-Strategist Integration...")
    
    from agents.strategist.dss_strategist import DSSStrategist
    
    # Set up MCP servers
    mcp_manager = await setup_mcp_servers()
    
    # Create agents
    researcher = Researcher()
    strategist = DSSStrategist()
    
    # Conduct MCP research
    mcp_request = {
        "type": "mcp_research",
        "data": {
            "query": "government service delivery efficiency",
            "max_results": 3,
            "sources": ["wikipedia", "arxiv"]
        }
    }
    
    research_response = await researcher.process_request(mcp_request)
    
    if research_response.success:
        print("✅ MCP research completed for strategist")
        
        # Use research findings to inform strategic analysis
        kpi_data = {
            "research_findings": research_response.data['synthesis'],
            "key_insights": research_response.data['key_findings'],
            "recommendations": research_response.data['recommendations'],
            "mcp_sources": research_response.data['mcp_sources']
        }
        
        strategy_request = {
            "type": "kpi_analysis",
            "data": kpi_data
        }
        
        strategy_response = await strategist.process_request(strategy_request)
        
        if strategy_response.success:
            print("✅ Strategic analysis completed using MCP research data")
            print(f"📊 Strategy insights: {strategy_response.data['analysis'][:200]}...")
            print(f"🔗 MCP sources used: {kpi_data['mcp_sources']}")
        else:
            print(f"❌ Strategic analysis failed: {strategy_response.errors}")
    else:
        print(f"❌ MCP research failed: {research_response.errors}")
    
    await mcp_manager.cleanup()
    await researcher.cleanup()

async def main():
    """Run all MCP integration tests."""
    print("🚀 Starting MCP Integration Tests\n")
    
    # Test individual MCP functionalities
    await test_mcp_research()
    await test_comprehensive_research()
    await test_wikipedia_specific()
    await test_arxiv_specific()
    await test_mcp_health_check()
    
    # Test integration with other agents
    await test_mcp_integration_with_strategist()
    
    print("\n🎉 All MCP Integration tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 