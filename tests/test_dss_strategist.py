import pytest
from agents.strategist.dss_strategist import DSSStrategist


@pytest.fixture
def strategist():
    return DSSStrategist()


@pytest.mark.asyncio
async def test_kpi_analysis(strategist):
    request = {
        "type": "kpi_analysis",
        "metrics": {
            "time_to_benefit": 45,
            "case_resolution": 0.75,
            "client_satisfaction": 0.82
        }
    }
    
    response = await strategist.process_request(request)
    assert response.success
    assert "analysis" in response.data
    assert isinstance(response.data["analysis"], dict)


@pytest.mark.asyncio
async def test_bottleneck_detection(strategist):
    request = {
        "type": "bottleneck_detection",
        "process_data": {
            "application_intake": {
                "avg_processing_time": 120,
                "queue_length": 45,
                "error_rate": 0.15
            }
        }
    }
    
    response = await strategist.process_request(request)
    assert response.success
    assert "bottlenecks" in response.data
    assert isinstance(response.data["bottlenecks"], list)


@pytest.mark.asyncio
async def test_risk_assessment(strategist):
    request = {
        "type": "risk_assessment",
        "initiative": {
            "name": "Digital Benefits Portal",
            "scope": "Online application and document submission",
            "stakeholders": ["DSS", "HRA", "Clients"],
            "timeline": "6 months"
        }
    }
    
    response = await strategist.process_request(request)
    assert response.success
    assert "risks" in response.data
    assert isinstance(response.data["risks"], list)


@pytest.mark.asyncio
async def test_initiative_analysis(strategist):
    request = {
        "type": "initiative_analysis",
        "initiative": {
            "name": "Automated Document Processing",
            "description": "Implement AI-powered document classification",
            "department": "DSS",
            "budget": 500000
        }
    }
    
    response = await strategist.process_request(request)
    assert response.success
    assert "analysis" in response.data
    assert isinstance(response.data["analysis"], dict)


@pytest.mark.asyncio
async def test_invalid_request_type(strategist):
    request = {
        "type": "invalid_type",
        "data": {}
    }
    
    response = await strategist.process_request(request)
    assert not response.success
    assert "Invalid request type specified" in response.errors 