from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel


class AgentResponse(BaseModel):
    """Standard response format for all agents"""
    success: bool
    message: str
    data: Dict[str, Any] = {}
    errors: List[str] = []


class BaseAgent(ABC):
    """Base class for all AI agents in the system"""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.context = {}
    
    @abstractmethod
    async def process_request(self, request: Dict[str, Any]) -> AgentResponse:
        """Process an incoming request and return a response"""
        pass
    
    def update_context(self, new_context: Dict[str, Any]) -> None:
        """Update the agent's context with new information"""
        self.context.update(new_context)
    
    def clear_context(self) -> None:
        """Clear the agent's context"""
        self.context = {}
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the agent"""
        return {
            "name": self.name,
            "role": self.role,
            "context_size": len(self.context)
        } 