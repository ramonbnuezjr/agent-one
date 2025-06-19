from typing import Dict, Any, Optional
import ollama
from pydantic import BaseModel

class LLMResponse(BaseModel):
    """Model for LLM response."""
    content: str
    metadata: Optional[Dict[str, Any]] = None

class LLMService:
    """Service for interacting with Ollama LLM."""
    
    def __init__(self, model_name: str = "mistral"):
        """Initialize the LLM service.
        
        Args:
            model_name: Name of the model to use (default: "mistral")
        """
        self.model_name = model_name
        
    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """Generate a response from the LLM.
        
        Args:
            prompt: The input prompt
            system_prompt: Optional system prompt to guide the model's behavior
            
        Returns:
            LLMResponse containing the generated content and metadata
        """
        try:
            # Prepare the messages
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            # Generate response from Ollama
            response = ollama.chat(
                model=self.model_name,
                messages=messages
            )
            
            return LLMResponse(
                content=response['message']['content'],
                metadata={
                    'model': self.model_name,
                    'total_duration': response.get('total_duration'),
                    'load_duration': response.get('load_duration'),
                    'prompt_eval_count': response.get('prompt_eval_count'),
                    'prompt_eval_duration': response.get('prompt_eval_duration'),
                    'eval_count': response.get('eval_count'),
                    'eval_duration': response.get('eval_duration')
                }
            )
            
        except Exception as e:
            raise Exception(f"Error generating response from LLM: {str(e)}")
    
    async def analyze_kpis(self, kpis: Dict[str, float]) -> str:
        """Analyze KPI data and provide insights.
        
        Args:
            kpis: Dictionary of KPI metrics and their values
            
        Returns:
            Analysis of the KPI data
        """
        prompt = f"""Analyze the following KPI metrics and provide insights:
        {kpis}
        
        Consider:
        1. Current performance levels
        2. Areas needing improvement
        3. Potential strategies for optimization
        4. Impact on service delivery
        """
        
        system_prompt = """You are a DSS Strategist analyzing KPI metrics. 
        Provide clear, actionable insights focused on improving service delivery 
        and operational efficiency."""
        
        response = await self.generate_response(prompt, system_prompt)
        return response.content
    
    async def analyze_bottlenecks(self, process_data: Dict[str, Any]) -> str:
        """Analyze process data to identify bottlenecks.
        
        Args:
            process_data: Dictionary containing process metrics and data
            
        Returns:
            Analysis of bottlenecks and recommendations
        """
        prompt = f"""Analyze the following process data to identify bottlenecks:
        {process_data}
        
        Consider:
        1. Process flow and dependencies
        2. Resource utilization
        3. Queue lengths and wait times
        4. Error rates and their impact
        5. Staff allocation and workload
        """
        
        system_prompt = """You are a DSS Strategist analyzing process bottlenecks. 
        Identify key bottlenecks and provide specific, actionable recommendations 
        for improvement."""
        
        response = await self.generate_response(prompt, system_prompt)
        return response.content
    
    async def analyze_initiative(self, initiative_data: Dict[str, Any]) -> str:
        """Analyze a proposed initiative.
        
        Args:
            initiative_data: Dictionary containing initiative details
            
        Returns:
            Analysis of the initiative and recommendations
        """
        prompt = f"""Analyze the following initiative:
        {initiative_data}
        
        Consider:
        1. Strategic alignment
        2. Resource requirements
        3. Implementation timeline
        4. Stakeholder impact
        5. Risk factors
        6. Success metrics
        """
        
        system_prompt = """You are a DSS Strategist analyzing initiatives. 
        Provide a comprehensive analysis focusing on strategic value, 
        implementation feasibility, and potential impact."""
        
        response = await self.generate_response(prompt, system_prompt)
        return response.content
    
    async def assess_risks(self, policy_data: Dict[str, Any]) -> str:
        """Assess risks associated with a policy change.
        
        Args:
            policy_data: Dictionary containing policy change details
            
        Returns:
            Risk assessment and mitigation strategies
        """
        prompt = f"""Assess risks for the following policy change:
        {policy_data}
        
        Consider:
        1. Operational impact
        2. Stakeholder concerns
        3. Resource implications
        4. Timeline risks
        5. Compliance requirements
        6. Service delivery impact
        """
        
        system_prompt = """You are a DSS Strategist assessing policy changes. 
        Identify potential risks and provide specific mitigation strategies 
        while considering operational impact and stakeholder needs."""
        
        response = await self.generate_response(prompt, system_prompt)
        return response.content 