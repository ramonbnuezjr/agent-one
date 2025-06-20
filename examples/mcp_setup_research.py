import asyncio
from agents.researcher.researcher import Researcher
from mcp.mcp_manager import MCPManager
from mcp.wikipedia_server import WikipediaMCPServer
from mcp.arxiv_server import ArxivMCPServer

async def research_mcp_setup():
    """Research MCP setup configuration using MCP-enabled Researcher Agent."""
    print("🔍 Researching: What is a basic configuration of a Model Context Protocol (MCP) setup?")
    print("=" * 80)
    
    # Set up MCP servers
    print("🔧 Setting up MCP Servers...")
    mcp_manager = MCPManager()
    mcp_manager.register_server("wikipedia", WikipediaMCPServer())
    mcp_manager.register_server("arxiv", ArxivMCPServer())
    await mcp_manager.initialize()
    print(f"✅ MCP Servers initialized: {mcp_manager.get_available_sources()}")

    # Create researcher
    researcher = Researcher()

    # Define the research query
    mcp_request = {
        "type": "mcp_research",
        "data": {
            "query": "What is a basic configuration of a Model Context Protocol (MCP) setup?",
            "max_results": 8,
            "sources": ["wikipedia", "arxiv"]
        }
    }

    print("\n🔍 Conducting MCP Research...")
    # Run the research
    response = await researcher.process_request(mcp_request)
    
    if response.success:
        print("✅ MCP research completed successfully!")
        print(f"📊 Found {len(response.data['sources'])} sources")
        print(f"🔗 MCP sources used: {response.data['mcp_sources']}")
        
        print("\n" + "=" * 80)
        print("📝 RESEARCH SYNTHESIS")
        print("=" * 80)
        print(response.data['synthesis'])
        
        print("\n" + "=" * 80)
        print("🎯 KEY FINDINGS")
        print("=" * 80)
        for i, finding in enumerate(response.data['key_findings'], 1):
            print(f"{i}. {finding}")
        
        print("\n" + "=" * 80)
        print("💡 RECOMMENDATIONS")
        print("=" * 80)
        for i, recommendation in enumerate(response.data['recommendations'], 1):
            print(f"{i}. {recommendation}")
        
        print("\n" + "=" * 80)
        print("📚 SOURCE DETAILS")
        print("=" * 80)
        for i, source in enumerate(response.data['sources'], 1):
            print(f"{i}. {source['title']}")
            print(f"   Source: {source['source_type']}")
            print(f"   Relevance: {source['relevance_score']:.2f}")
            print(f"   URL: {source.get('url', 'N/A')}")
            print()
            
    else:
        print(f"❌ MCP research failed: {response.errors}")

    # Cleanup
    await mcp_manager.cleanup()
    await researcher.cleanup()
    print("🧹 Cleanup completed")

if __name__ == "__main__":
    asyncio.run(research_mcp_setup()) 