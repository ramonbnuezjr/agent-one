import pytest
import asyncio
from mcp.mcp_manager import MCPManager, MCPSearchResult
from mcp.wikipedia_server import WikipediaMCPServer
from mcp.arxiv_server import ArxivMCPServer

@pytest.fixture
async def mcp_manager():
    """Create an MCP manager instance for testing."""
    manager = MCPManager()
    yield manager
    await manager.cleanup()

@pytest.fixture
def wikipedia_server():
    """Create a Wikipedia MCP server instance for testing."""
    return WikipediaMCPServer()

@pytest.fixture
def arxiv_server():
    """Create an arXiv MCP server instance for testing."""
    return ArxivMCPServer()

@pytest.mark.asyncio
async def test_mcp_manager_initialization():
    """Test that MCP manager initializes correctly."""
    manager = MCPManager()
    assert manager.is_initialized is False
    await manager.initialize()
    assert manager.is_initialized is True
    await manager.cleanup()

@pytest.mark.asyncio
async def test_mcp_server_registration():
    """Test MCP server registration."""
    manager = MCPManager()
    wikipedia_server = WikipediaMCPServer()
    
    manager.register_server("wikipedia", wikipedia_server)
    assert "wikipedia" in manager.servers
    assert manager.get_available_sources() == ["wikipedia"]
    
    await manager.cleanup()

@pytest.mark.asyncio
async def test_mcp_search_result_model():
    """Test MCPSearchResult model validation."""
    result = MCPSearchResult(
        source="wikipedia",
        title="Test Article",
        content="This is test content.",
        url="https://example.com",
        relevance_score=0.8,
        metadata={"page_id": 123}
    )
    
    assert result.source == "wikipedia"
    assert result.title == "Test Article"
    assert result.relevance_score == 0.8

@pytest.mark.asyncio
async def test_wikipedia_server_initialization(wikipedia_server):
    """Test Wikipedia server initialization."""
    assert wikipedia_server.name == "Wikipedia MCP Server"
    assert wikipedia_server.is_initialized is False
    await wikipedia_server.initialize()
    assert wikipedia_server.is_initialized is True
    await wikipedia_server.cleanup()

@pytest.mark.asyncio
async def test_arxiv_server_initialization(arxiv_server):
    """Test arXiv server initialization."""
    assert arxiv_server.name == "arXiv MCP Server"
    assert arxiv_server.is_initialized is False
    await arxiv_server.initialize()
    assert arxiv_server.is_initialized is True
    await arxiv_server.cleanup()

@pytest.mark.asyncio
async def test_mcp_manager_health_check():
    """Test MCP manager health check."""
    manager = MCPManager()
    wikipedia_server = WikipediaMCPServer()
    
    manager.register_server("wikipedia", wikipedia_server)
    await manager.initialize()
    
    health_status = await manager.health_check()
    
    assert health_status["manager_status"] == "healthy"
    assert "wikipedia" in health_status["servers"]
    assert health_status["servers"]["wikipedia"]["status"] == "healthy"
    
    await manager.cleanup()

@pytest.mark.asyncio
async def test_mcp_manager_cleanup():
    """Test MCP manager cleanup."""
    manager = MCPManager()
    wikipedia_server = WikipediaMCPServer()
    
    manager.register_server("wikipedia", wikipedia_server)
    await manager.initialize()
    assert manager.is_initialized is True
    
    await manager.cleanup()
    assert manager.is_initialized is False

@pytest.mark.asyncio
async def test_wikipedia_server_cleanup(wikipedia_server):
    """Test Wikipedia server cleanup."""
    await wikipedia_server.initialize()
    assert wikipedia_server.is_initialized is True
    
    await wikipedia_server.cleanup()
    assert wikipedia_server.is_initialized is False

@pytest.mark.asyncio
async def test_arxiv_server_cleanup(arxiv_server):
    """Test arXiv server cleanup."""
    await arxiv_server.initialize()
    assert arxiv_server.is_initialized is True
    
    await arxiv_server.cleanup()
    assert arxiv_server.is_initialized is False

@pytest.mark.asyncio
async def test_mcp_manager_list_resources():
    """Test MCP manager resource listing."""
    manager = MCPManager()
    wikipedia_server = WikipediaMCPServer()
    
    manager.register_server("wikipedia", wikipedia_server)
    await manager.initialize()
    
    resources = await manager.list_all_resources()
    
    assert "wikipedia" in resources
    assert isinstance(resources["wikipedia"], list)
    
    await manager.cleanup()

@pytest.mark.asyncio
async def test_wikipedia_server_list_resources(wikipedia_server):
    """Test Wikipedia server resource listing."""
    await wikipedia_server.initialize()
    
    resources = await wikipedia_server.list_resources()
    
    assert isinstance(resources, list)
    assert len(resources) > 0
    
    await wikipedia_server.cleanup()

@pytest.mark.asyncio
async def test_arxiv_server_list_resources(arxiv_server):
    """Test arXiv server resource listing."""
    await arxiv_server.initialize()
    
    resources = await arxiv_server.list_resources()
    
    assert isinstance(resources, list)
    assert len(resources) > 0
    
    await arxiv_server.cleanup() 