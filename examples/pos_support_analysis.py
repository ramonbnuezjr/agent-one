import asyncio
from agents.strategist.dss_strategist import DSSStrategist

async def main():
    """Test the DSS Strategist with POS Application Support analysis."""
    strategist = DSSStrategist()
    
    # Scenario 1: KPI Analysis for POS Support Team
    print("\n=== Scenario 1: POS Support Team KPI Analysis ===\n")
    
    kpi_data = {
        "tickets_per_analyst": 28,  # Average daily tickets per analyst
        "supervisor_tickets": 189,  # Supervisor's daily ticket load
        "team_total_tickets": 355,  # Total daily tickets (25,202/71 days)
        "analyst_count": 6,  # Number of analysts
        "supervisor_count": 1,  # Number of supervisors
        "work_days": 71  # Number of work days in analysis period
    }
    
    kpi_response = await strategist.analyze_kpis(kpi_data)
    print("KPI Analysis for POS Support Team:")
    print(kpi_response)
    
    # Scenario 2: Bottleneck Analysis
    print("\n=== Scenario 2: POS Support Process Bottleneck Analysis ===\n")
    
    process_data = {
        "ticket_distribution": {
            "supervisor": {
                "daily_tickets": 189,
                "percentage": 53.2,  # 13,449/25,202
                "role": "supervisor"
            },
            "analysts": {
                "daily_tickets": 166,  # (25,202-13,449)/71
                "percentage": 46.8,
                "average_per_analyst": 28
            }
        },
        "team_composition": {
            "supervisor": 1,
            "analysts": 6,
            "total_members": 7
        },
        "ticket_volume": {
            "total_tickets": 25202,
            "daily_average": 355,
            "period_days": 71
        },
        "location_field_issue": {
            "problem": "Empty location fields in POS-generated emails",
            "impact": "Reduced ticket tracking and analytics capabilities",
            "affected_system": "POS webAPI"
        }
    }
    
    bottleneck_response = await strategist.detect_bottlenecks(process_data)
    print("Bottleneck Analysis for POS Support Process:")
    print(bottleneck_response)
    
    # Scenario 3: Initiative Analysis for Location Field Fix
    print("\n=== Scenario 3: Location Field Fix Initiative Analysis ===\n")
    
    initiative_data = {
        "name": "POS Location Field Enhancement",
        "description": "Fix the location field population in POS-generated emails",
        "current_state": {
            "issue": "Empty location fields in POS-generated emails",
            "impact": "Reduced ticket tracking and analytics capabilities",
            "affected_system": "POS webAPI"
        },
        "proposed_solution": {
            "type": "Technical Enhancement",
            "components": [
                "Update POS webAPI to include location data",
                "Modify email generation process",
                "Add location field validation"
            ],
            "expected_outcomes": [
                "Complete location data in all tickets",
                "Improved ticket tracking",
                "Enhanced analytics capabilities"
            ]
        },
        "stakeholders": [
            "POS Application Support Team",
            "DSS IT Department",
            "ServiceNow Team",
            "End Users"
        ],
        "timeline": {
            "estimated_duration": "2-3 months",
            "phases": [
                "Requirements gathering",
                "Development",
                "Testing",
                "Deployment"
            ]
        },
        "resource_requirements": {
            "technical_team": "POS Development Team",
            "support_team": "POS Application Support",
            "testing_team": "QA Team"
        }
    }
    
    initiative_response = await strategist.analyze_initiative(initiative_data)
    print("Initiative Analysis for Location Field Fix:")
    print(initiative_response)
    
    # Scenario 4: Risk Assessment
    print("\n=== Scenario 4: Risk Assessment ===\n")
    
    risk_data = {
        "initiative": "POS Location Field Enhancement",
        "current_risks": {
            "technical": [
                "API integration complexity",
                "Data consistency across systems",
                "Performance impact"
            ],
            "operational": [
                "High ticket volume during transition",
                "Team capacity constraints",
                "Training requirements"
            ],
            "stakeholder": [
                "User adoption resistance",
                "Cross-team coordination",
                "Communication challenges"
            ]
        },
        "mitigation_strategies": {
            "technical": [
                "Phased implementation",
                "Comprehensive testing",
                "Performance monitoring"
            ],
            "operational": [
                "Staged rollout",
                "Capacity planning",
                "Documentation updates"
            ],
            "stakeholder": [
                "Early stakeholder engagement",
                "Clear communication plan",
                "User training program"
            ]
        }
    }
    
    risk_response = await strategist.assess_risks(risk_data)
    print("Risk Assessment:")
    print(risk_response)

if __name__ == "__main__":
    asyncio.run(main()) 