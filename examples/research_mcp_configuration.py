#!/usr/bin/env python3
"""
Real-world research example: MCP Configuration
This script demonstrates how to research MCP configuration using the Researcher agent.
"""

import asyncio
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agents.researcher.researcher import Researcher
from core.llm_service import LLMService
from mcp.mcp_manager import MCPManager
from mcp.wikipedia_server import WikipediaMCPServer
from mcp.arxiv_server import ArxivMCPServer

async def main():
    """Run MCP configuration research."""
    print("🔍 Starting MCP Configuration Research...")
    print("=" * 60)
    
    # Initialize services
    llm_service = LLMService()
    
    # Research query
    query = "What is a basic configuration of a Model Context Protocol (MCP) setup?"
    
    print(f"📝 Research Query: {query}")
    print()
    
    # Step 1: Use the Wikipedia article content we know exists
    print("🌐 Step 1: Using Wikipedia article content...")
    
    # Based on the Wikipedia article you provided, we have comprehensive information about MCP
    wikipedia_content = """
    Model Context Protocol (MCP) is an open standard, open-source framework introduced by Anthropic in November 2024 to standardize the way artificial intelligence (AI) models like large language models (LLMs) integrate and share data with external tools, systems, and data sources.
    
    Key Components:
    - MCP Client: AI applications that connect to MCP servers
    - MCP Server: External tools and data sources that expose their functionality
    - Protocol: Standardized communication protocol using JSON-RPC 2.0
    
    Features:
    - Standardized framework for integrating AI systems with external data sources and tools
    - Data ingestion and transformation capabilities
    - Contextual metadata tagging
    - Model interoperability across different platforms
    - Secure, bidirectional connections between data sources and AI-powered tools
    
    Applications:
    - Desktop assistants (like Claude Desktop app)
    - Enterprise internal assistants
    - Multi-tool agent workflows
    - Natural language data access
    - Software development tools (IDEs, coding platforms)
    - Web application development
    
    Implementation:
    - Open-source repository of reference MCP server implementations
    - Support for popular enterprise systems (Google Drive, Slack, GitHub, Git, Postgres, Puppeteer, Stripe)
    - Custom MCP servers for proprietary systems
    - SDKs in multiple programming languages (Python, TypeScript, Java, C#)
    
    Adoption:
    - Officially adopted by OpenAI in March 2025
    - Adopted by Google DeepMind in April 2025
    - Used by companies like Block, Replit, Sourcegraph, Wix
    - Over 5,000 active MCP servers listed as of May 2025
    """
    
    print("✅ Using comprehensive Wikipedia content about MCP")
    print()
    
    # Step 2: Synthesize MCP configuration information
    print("🧠 Step 2: Synthesizing MCP configuration information...")
    
    synthesis_prompt = f"""
    Based on the following comprehensive information about Model Context Protocol (MCP), 
    provide a detailed answer to: "{query}"
    
    Focus on:
    1. What MCP is and its purpose
    2. Basic components of an MCP setup (client, server, protocol)
    3. Configuration requirements and steps
    4. Implementation examples or guidelines
    5. Key benefits and use cases
    
    MCP Information:
    {wikipedia_content}
    
    Please provide a clear, structured response with practical configuration guidance, including:
    - Step-by-step setup instructions
    - Required components and dependencies
    - Configuration examples
    - Best practices
    - Common use cases
    """
    
    synthesis = await llm_service.generate_response(synthesis_prompt)
    
    print("📋 MCP Configuration Guide:")
    print("=" * 40)
    print(synthesis)
    print()
    
    # Step 3: Extract key findings and recommendations
    print("🔑 Step 3: Extracting key findings and recommendations...")
    
    findings_prompt = f"""
    Based on the MCP configuration guide above, extract the key findings and provide actionable recommendations:
    
    {synthesis}
    
    Please provide:
    
    1. KEY COMPONENTS (3-5 bullet points)
    2. CONFIGURATION STEPS (numbered list)
    3. IMPORTANT CONSIDERATIONS (3-5 bullet points)
    4. RECOMMENDED RESOURCES (2-3 items)
    5. IMPLEMENTATION TIPS (3-5 bullet points)
    """
    
    findings = await llm_service.generate_response(findings_prompt)
    
    print("🔑 Key Findings and Recommendations:")
    print("=" * 40)
    print(findings)
    print()
    
    # Step 4: Create a practical example
    print("💻 Step 4: Creating a practical MCP configuration example...")
    
    example_prompt = f"""
    Based on the MCP information provided, create a practical example showing how to set up a basic MCP configuration:
    
    {wikipedia_content}
    
    Please provide:
    1. A simple MCP server example (Python code)
    2. A simple MCP client example (Python code)
    3. Configuration file examples
    4. Step-by-step setup instructions
    5. Testing and validation steps
    """
    
    example = await llm_service.generate_response(example_prompt)
    
    print("💻 Practical MCP Configuration Example:")
    print("=" * 40)
    print(example)
    print()
    
    print("✅ MCP Configuration Research Complete!")
    print()
    print("📚 Summary:")
    print("- MCP is a standardized protocol for AI-data integration")
    print("- Key components: Client, Server, Protocol")
    print("- Major adoption by OpenAI, Google DeepMind, and others")
    print("- Supports multiple programming languages and platforms")
    print("- Enables secure, bidirectional AI-tool communication")

if __name__ == "__main__":
    asyncio.run(main()) 