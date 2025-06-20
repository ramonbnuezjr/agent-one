import pytest
import asyncio
from agents.researcher.researcher import Researcher, ResearchQuery, ResearchSource

@pytest.fixture
def researcher():
    """Create a researcher instance for testing."""
    return Researcher()

@pytest.mark.asyncio
async def test_researcher_initialization(researcher):
    """Test that researcher initializes correctly."""
    assert researcher.name == "Researcher"
    assert researcher.role == "Conducts deep research and analysis for DSS strategic initiatives"
    assert researcher.llm_service is not None

@pytest.mark.asyncio
async def test_research_query_model():
    """Test ResearchQuery model validation."""
    query = ResearchQuery(
        topic="DSS optimization",
        keywords=["efficiency", "digital transformation"],
        scope="focused",
        sources=["web"],
        max_results=5
    )
    
    assert query.topic == "DSS optimization"
    assert len(query.keywords) == 2
    assert query.scope == "focused"
    assert query.max_results == 5

@pytest.mark.asyncio
async def test_research_source_model():
    """Test ResearchSource model validation."""
    source = ResearchSource(
        url="https://example.com",
        title="Test Document",
        content="This is test content for research.",
        source_type="web",
        timestamp="2024-01-01",
        relevance_score=0.8
    )
    
    assert source.url == "https://example.com"
    assert source.title == "Test Document"
    assert source.relevance_score == 0.8

@pytest.mark.asyncio
async def test_document_analysis(researcher):
    """Test document analysis functionality."""
    documents = [
        {
            "title": "Test Document 1",
            "content": "This is a test document about DSS improvements."
        }
    ]
    
    request = {
        "type": "document_analysis",
        "data": {
            "documents": documents,
            "analysis_type": "strategic"
        }
    }
    
    response = await researcher.process_request(request)
    
    assert response.success is True
    assert "individual_analyses" in response.data
    assert "cross_document_synthesis" in response.data
    assert "key_insights" in response.data

@pytest.mark.asyncio
async def test_policy_research(researcher):
    """Test policy research functionality."""
    request = {
        "type": "policy_research",
        "data": {
            "policy_topic": "Digital transformation",
            "jurisdiction": "NYC"
        }
    }
    
    response = await researcher.process_request(request)
    
    assert response.success is True
    assert response.data["policy_topic"] == "Digital transformation"
    assert response.data["jurisdiction"] == "NYC"
    assert "analysis" in response.data

@pytest.mark.asyncio
async def test_best_practices_research(researcher):
    """Test best practices research functionality."""
    request = {
        "type": "best_practices_research",
        "data": {
            "practice_area": "Case management",
            "context": "DSS operations"
        }
    }
    
    response = await researcher.process_request(request)
    
    assert response.success is True
    assert response.data["practice_area"] == "Case management"
    assert response.data["context"] == "DSS operations"
    assert "best_practices" in response.data

@pytest.mark.asyncio
async def test_research_synthesis(researcher):
    """Test research synthesis functionality."""
    sources = [
        {
            "title": "Source 1",
            "content": "First research source content."
        },
        {
            "title": "Source 2", 
            "content": "Second research source content."
        }
    ]
    
    request = {
        "type": "synthesis_research",
        "data": {
            "sources": sources,
            "research_question": "How to improve DSS services?"
        }
    }
    
    response = await researcher.process_request(request)
    
    assert response.success is True
    assert response.data["research_question"] == "How to improve DSS services?"
    assert "synthesis" in response.data
    assert "key_findings" in response.data

@pytest.mark.asyncio
async def test_invalid_request_type(researcher):
    """Test handling of invalid request type."""
    request = {
        "type": "invalid_type",
        "data": {}
    }
    
    response = await researcher.process_request(request)
    
    assert response.success is False
    assert "Unknown request type" in response.message

@pytest.mark.asyncio
async def test_researcher_cleanup(researcher):
    """Test researcher cleanup functionality."""
    # This test ensures cleanup doesn't raise errors
    await researcher.cleanup()
    assert True  # If we get here, cleanup worked

@pytest.mark.asyncio
async def test_relevance_calculation(researcher):
    """Test relevance score calculation."""
    content = "This document discusses DSS social services and policy improvements."
    search_terms = "DSS social services"
    
    relevance = researcher._calculate_relevance(content, search_terms)
    
    assert isinstance(relevance, float)
    assert 0.0 <= relevance <= 1.0
    assert relevance > 0.0  # Should find some relevance

@pytest.mark.asyncio
async def test_theme_extraction(researcher):
    """Test theme extraction functionality."""
    analysis = """
    Key themes identified:
    1. Digital transformation
    2. Staff training
    3. Client experience
    4. Process optimization
    5. Policy alignment
    """
    
    themes = await researcher._extract_themes(analysis)
    
    assert isinstance(themes, list)
    assert len(themes) <= 5  # Should extract up to 5 themes
    assert all(isinstance(theme, str) for theme in themes) 