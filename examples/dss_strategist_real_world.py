import asyncio
from agents.strategist.dss_strategist import DSSStrategist


async def main():
    strategist = DSSStrategist()
    
    # Scenario 1: SNAP Benefits Processing Optimization
    print("\n=== Scenario 1: SNAP Benefits Processing Optimization ===")
    snap_request = {
        "type": "kpi_analysis",
        "metrics": {
            "time_to_benefit": 42,  # Current: 42 days
            "case_resolution": 0.68,  # Current: 68% resolution rate
            "client_satisfaction": 0.72,  # Current: 72% satisfaction
            "service_access": 0.85,  # Current: 85% accessibility
            "digital_inclusion": 0.45  # Current: 45% digital adoption
        }
    }
    
    snap_response = await strategist.process_request(snap_request)
    print("\nKPI Analysis for SNAP Benefits:")
    print(snap_response.dict())
    
    # Scenario 2: Document Processing Bottleneck
    print("\n=== Scenario 2: Document Processing Bottleneck ===")
    doc_request = {
        "type": "bottleneck_detection",
        "process_data": {
            "document_intake": {
                "avg_processing_time": 180,  # 3 hours
                "queue_length": 120,
                "error_rate": 0.25,
                "staff_count": 8,
                "documents_per_day": 150
            },
            "verification": {
                "avg_processing_time": 240,  # 4 hours
                "queue_length": 85,
                "error_rate": 0.15,
                "staff_count": 12,
                "documents_per_day": 100
            },
            "approval": {
                "avg_processing_time": 120,  # 2 hours
                "queue_length": 45,
                "error_rate": 0.08,
                "staff_count": 5,
                "documents_per_day": 80
            }
        }
    }
    
    doc_response = await strategist.process_request(doc_request)
    print("\nBottleneck Analysis for Document Processing:")
    print(doc_response.dict())
    
    # Scenario 3: Digital Transformation Initiative
    print("\n=== Scenario 3: Digital Transformation Initiative ===")
    digital_request = {
        "type": "initiative_analysis",
        "initiative": {
            "name": "DSS Digital Service Platform",
            "description": (
                "Modernize client-facing services with AI-powered document "
                "processing and automated eligibility screening"
            ),
            "department": "DSS",
            "budget": 2500000,
            "timeline": "18 months",
            "stakeholders": [
                "DSS Leadership",
                "HRA",
                "DHS",
                "NYC Office of Technology",
                "Client Advocacy Groups"
            ],
            "key_features": [
                "AI document classification",
                "Automated eligibility screening",
                "Mobile-friendly application portal",
                "Real-time status updates",
                "Multilingual support"
            ]
        }
    }
    
    digital_response = await strategist.process_request(digital_request)
    print("\nInitiative Analysis for Digital Transformation:")
    print(digital_response.dict())
    
    # Scenario 4: Risk Assessment for Policy Change
    print("\n=== Scenario 4: Risk Assessment for Policy Change ===")
    policy_request = {
        "type": "risk_assessment",
        "initiative": {
            "name": "Streamlined SNAP Recertification",
            "description": (
                "Implement simplified recertification process with automated "
                "income verification"
            ),
            "scope": "SNAP program recertification process",
            "stakeholders": [
                "DSS Leadership",
                "SNAP Program Office",
                "Client Advocacy Groups",
                "State DSS",
                "Federal FNS"
            ],
            "key_changes": [
                "Automated income verification",
                "Reduced documentation requirements",
                "Online recertification portal",
                "Proactive renewal notifications"
            ],
            "timeline": "12 months",
            "budget": 1500000
        }
    }
    
    policy_response = await strategist.process_request(policy_request)
    print("\nRisk Assessment for Policy Change:")
    print(policy_response.dict())


if __name__ == "__main__":
    asyncio.run(main()) 