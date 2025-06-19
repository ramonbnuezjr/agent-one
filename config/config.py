from typing import Dict, Any
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Project settings and configuration"""
    
    # Agent Configuration
    AGENT_NAME: str = "DSS Strategist"
    AGENT_ROLE: str = "Data-informed advisor for senior leaders at NYC DSS"
    
    # KPI Framework Configuration
    KPI_TARGETS: Dict[str, float] = {
        "time_to_benefit": 30.0,  # Target: 30 days
        "case_resolution": 0.85,  # Target: 85% resolution rate
        "client_satisfaction": 0.90,  # Target: 90% satisfaction rate
        "service_access": 0.95,  # Target: 95% service accessibility
        "digital_inclusion": 0.80  # Target: 80% digital service adoption
    }
    
    # Process Metrics Configuration
    PROCESS_THRESHOLDS: Dict[str, Dict[str, float]] = {
        "application_intake": {
            "max_processing_time": 60,  # minutes
            "max_queue_length": 30,
            "max_error_rate": 0.10
        },
        "document_verification": {
            "max_processing_time": 90,  # minutes
            "max_queue_length": 20,
            "max_error_rate": 0.05
        }
    }
    
    # Risk Assessment Configuration
    RISK_LEVELS: Dict[str, Dict[str, Any]] = {
        "regulatory": {
            "high": ["Data Privacy", "HIPAA Compliance"],
            "medium": ["Document Retention", "Access Control"],
            "low": ["Reporting Requirements"]
        },
        "political": {
            "high": ["Public Perception", "Stakeholder Opposition"],
            "medium": ["Inter-agency Coordination"],
            "low": ["Internal Communication"]
        }
    }
    
    # Initiative Analysis Configuration
    INITIATIVE_PARAMETERS: Dict[str, Dict[str, Any]] = {
        "time_to_deploy": {
            "small": {"min": 1, "max": 3},  # months
            "medium": {"min": 3, "max": 6},
            "large": {"min": 6, "max": 12}
        },
        "resource_requirements": {
            "small": {"team_size": 2, "budget_range": (100000, 300000)},
            "medium": {"team_size": 5, "budget_range": (300000, 700000)},
            "large": {"team_size": 10, "budget_range": (700000, 1500000)}
        }
    }
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a global settings instance
settings = Settings() 