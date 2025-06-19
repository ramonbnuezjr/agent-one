import asyncio
from agents.strategist.dss_strategist import DSSStrategist


async def main():
    # Initialize the DSS Strategist agent
    strategist = DSSStrategist()
    
    # Example 1: KPI Analysis
    kpi_request = {
        "type": "kpi_analysis",
        "metrics": {
            "time_to_benefit": 45,  # days
            "case_resolution": 0.75,  # 75% resolution rate
            "client_satisfaction": 0.82  # 82% satisfaction rate
        }
    }
    
    kpi_response = await strategist.process_request(kpi_request)
    print("\nKPI Analysis Results:")
    print(kpi_response.dict())
    
    # Example 2: Bottleneck Detection
    bottleneck_request = {
        "type": "bottleneck_detection",
        "process_data": {
            "application_intake": {
                "avg_processing_time": 120,  # minutes
                "queue_length": 45,
                "error_rate": 0.15
            },
            "document_verification": {
                "avg_processing_time": 180,  # minutes
                "queue_length": 30,
                "error_rate": 0.08
            }
        }
    }
    
    bottleneck_response = await strategist.process_request(bottleneck_request)
    print("\nBottleneck Analysis Results:")
    print(bottleneck_response.dict())
    
    # Example 3: Risk Assessment
    risk_request = {
        "type": "risk_assessment",
        "initiative": {
            "name": "Digital Benefits Portal",
            "scope": "Online application and document submission",
            "stakeholders": ["DSS", "HRA", "Clients"],
            "timeline": "6 months"
        }
    }
    
    risk_response = await strategist.process_request(risk_request)
    print("\nRisk Assessment Results:")
    print(risk_response.dict())
    
    # Example 4: Initiative Analysis
    initiative_request = {
        "type": "initiative_analysis",
        "initiative": {
            "name": "Automated Document Processing",
            "description": "Implement AI-powered document classification",
            "department": "DSS",
            "budget": 500000
        }
    }
    
    initiative_response = await strategist.process_request(initiative_request)
    print("\nInitiative Analysis Results:")
    print(initiative_response.dict())


if __name__ == "__main__":
    asyncio.run(main()) 