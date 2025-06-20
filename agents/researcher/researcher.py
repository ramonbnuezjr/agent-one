from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin, urlparse
from core.base_agent import BaseAgent, AgentResponse
from core.llm_service import LLMService
from mcp.mcp_manager import MCPManager, MCPSearchResult

class ResearchSource(BaseModel):
    """Model for research source information."""
    url: str
    title: str
    content: str
    source_type: str  # "web", "document", "api", "mcp"
    timestamp: str
    relevance_score: float

class ResearchQuery(BaseModel):
    """Model for research query."""
    topic: str
    keywords: List[str]
    scope: str  # "broad", "focused", "deep"
    sources: List[str]  # ["web", "documents", "apis", "mcp"]
    max_results: int = 10

class ResearchResult(BaseModel):
    """Model for research result."""
    query: ResearchQuery
    sources: List[ResearchSource]
    synthesis: str
    key_findings: List[str]
    recommendations: List[str]
    confidence_score: float

class Researcher(BaseAgent):
    """Researcher agent for conducting comprehensive research and analysis."""
    
    def __init__(self):
        """Initialize the Researcher agent."""
        super().__init__(
            name="Researcher",
            role="Conducts deep research and analysis for DSS strategic initiatives"
        )
        self.llm_service = LLMService()
        self.session = None
        self.research_cache = {}
        self.mcp_manager = MCPManager()
        
    async def process_request(self, request: Dict[str, Any]) -> AgentResponse:
        """Process incoming research requests.
        
        Args:
            request: Dictionary containing the research request details
            
        Returns:
            AgentResponse containing the research results
        """
        try:
            request_type = request.get("type", "")
            
            if request_type == "web_research":
                response = await self.conduct_web_research(request.get("data", {}))
            elif request_type == "document_analysis":
                response = await self.analyze_documents(request.get("data", {}))
            elif request_type == "synthesis_research":
                response = await self.synthesize_research(request.get("data", {}))
            elif request_type == "policy_research":
                response = await self.research_policy_implications(request.get("data", {}))
            elif request_type == "best_practices_research":
                response = await self.research_best_practices(request.get("data", {}))
            elif request_type == "mcp_research":
                response = await self.conduct_mcp_research(request.get("data", {}))
            elif request_type == "comprehensive_research":
                response = await self.conduct_comprehensive_research(request.get("data", {}))
            else:
                return AgentResponse(
                    success=False,
                    message="Unknown request type",
                    errors=["Invalid request type specified"]
                )
            
            return AgentResponse(
                success=response["success"],
                message=response["message"],
                data=response["data"],
                errors=response["errors"]
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message="Error processing research request",
                errors=[str(e)]
            )
    
    async def _get_session(self):
        """Get or create aiohttp session for web requests."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def conduct_mcp_research(self, query_data: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct research using MCP servers.
        
        Args:
            query_data: Dictionary containing MCP research query details
            
        Returns:
            Dictionary containing MCP research results
        """
        try:
            query = query_data.get("query", "")
            max_results = query_data.get("max_results", 10)
            sources = query_data.get("sources", None)  # None for all sources
            
            # Search across MCP servers
            mcp_results = await self.mcp_manager.search_all(
                query=query,
                max_results=max_results,
                sources=sources
            )
            
            # Convert to ResearchSource format
            sources = []
            for result in mcp_results:
                source = ResearchSource(
                    url=result.url or "",
                    title=result.title,
                    content=result.content,
                    source_type=f"mcp_{result.source}",
                    timestamp="2024-01-01",  # Would be actual timestamp
                    relevance_score=result.relevance_score
                )
                sources.append(source)
            
            # Synthesize findings
            synthesis = await self._synthesize_mcp_findings(mcp_results, query)
            
            return {
                "success": True,
                "message": "MCP research completed",
                "data": {
                    "query": query,
                    "sources": [source.dict() for source in sources],
                    "synthesis": synthesis,
                    "key_findings": await self._extract_key_findings(synthesis),
                    "recommendations": await self._generate_recommendations(synthesis, 
                        ResearchQuery(topic=query, keywords=[], scope="focused", sources=[])),
                    "mcp_sources": self.mcp_manager.get_available_sources()
                },
                "errors": []
            }
        except Exception as e:
            return {
                "success": False,
                "message": "MCP research failed",
                "data": {},
                "errors": [str(e)]
            }
    
    async def conduct_comprehensive_research(self, query_data: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct comprehensive research using both web and MCP sources.
        
        Args:
            query_data: Dictionary containing comprehensive research query details
            
        Returns:
            Dictionary containing comprehensive research results
        """
        try:
            query = query_data.get("query", "")
            max_results = query_data.get("max_results", 10)
            include_web = query_data.get("include_web", True)
            include_mcp = query_data.get("include_mcp", True)
            
            all_sources = []
            
            # Conduct web research if requested
            if include_web:
                web_query = ResearchQuery(
                    topic=query,
                    keywords=query.split(),
                    scope="focused",
                    sources=["web"],
                    max_results=max_results
                )
                web_results = await self._search_web_sources(web_query)
                all_sources.extend(web_results)
            
            # Conduct MCP research if requested
            if include_mcp:
                mcp_results = await self.mcp_manager.search_all(
                    query=query,
                    max_results=max_results
                )
                
                for result in mcp_results:
                    source = ResearchSource(
                        url=result.url or "",
                        title=result.title,
                        content=result.content,
                        source_type=f"mcp_{result.source}",
                        timestamp="2024-01-01",
                        relevance_score=result.relevance_score
                    )
                    all_sources.append(source)
            
            # Sort by relevance
            all_sources.sort(key=lambda x: x.relevance_score, reverse=True)
            
            # Synthesize all findings
            synthesis = await self._synthesize_comprehensive_findings(all_sources, query)
            
            return {
                "success": True,
                "message": "Comprehensive research completed",
                "data": {
                    "query": query,
                    "sources": [source.dict() for source in all_sources],
                    "synthesis": synthesis,
                    "key_findings": await self._extract_key_findings(synthesis),
                    "recommendations": await self._generate_recommendations(synthesis,
                        ResearchQuery(topic=query, keywords=[], scope="focused", sources=[])),
                    "source_breakdown": {
                        "web_sources": len([s for s in all_sources if s.source_type.startswith("web")]),
                        "mcp_sources": len([s for s in all_sources if s.source_type.startswith("mcp")])
                    }
                },
                "errors": []
            }
        except Exception as e:
            return {
                "success": False,
                "message": "Comprehensive research failed",
                "data": {},
                "errors": [str(e)]
            }
    
    async def _synthesize_mcp_findings(self, mcp_results: List[MCPSearchResult], query: str) -> str:
        """Synthesize findings from MCP search results."""
        if not mcp_results:
            return "No relevant MCP sources found for the research query."
        
        # Prepare content for synthesis
        content_summary = "\n\n".join([
            f"Source: {result.source}\nTitle: {result.title}\nContent: {result.content[:500]}..."
            for result in mcp_results
        ])
        
        prompt = f"""Synthesize the following MCP research findings for a DSS strategist:

Research Query: {query}

MCP Sources:
{content_summary}

Please provide a comprehensive synthesis that:
1. Identifies key themes and patterns across MCP sources
2. Highlights relevant insights for DSS operations
3. Notes any gaps in current knowledge
4. Suggests areas for further investigation
5. Relates findings to DSS strategic priorities

Focus on practical implications for DSS service delivery and policy development."""

        system_prompt = """You are a DSS Research Specialist synthesizing MCP information for strategic decision-making. 
        Provide clear, actionable insights that can inform policy and operational improvements."""
        
        response = await self.llm_service.generate_response(prompt, system_prompt)
        return response.content
    
    async def _synthesize_comprehensive_findings(self, sources: List[ResearchSource], query: str) -> str:
        """Synthesize findings from comprehensive research sources."""
        if not sources:
            return "No relevant sources found for the research query."
        
        # Prepare content for synthesis
        content_summary = "\n\n".join([
            f"Source Type: {source.source_type}\nTitle: {source.title}\nContent: {source.content[:500]}..."
            for source in sources
        ])
        
        prompt = f"""Synthesize the following comprehensive research findings for a DSS strategist:

Research Query: {query}

Sources (Web + MCP):
{content_summary}

Please provide a comprehensive synthesis that:
1. Identifies key themes and patterns across all sources
2. Highlights relevant insights for DSS operations
3. Compares findings from different source types
4. Notes any gaps in current knowledge
5. Suggests areas for further investigation
6. Relates findings to DSS strategic priorities

Focus on practical implications for DSS service delivery and policy development."""

        system_prompt = """You are a DSS Research Specialist synthesizing comprehensive research for strategic decision-making. 
        Provide clear, actionable insights that can inform policy and operational improvements."""
        
        response = await self.llm_service.generate_response(prompt, system_prompt)
        return response.content
    
    async def conduct_web_research(self, query_data: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct web research on a given topic.
        
        Args:
            query_data: Dictionary containing research query details
            
        Returns:
            Dictionary containing research results
        """
        try:
            query = ResearchQuery(**query_data)
            
            # Search for relevant sources
            sources = await self._search_web_sources(query)
            
            # Extract and analyze content
            analyzed_sources = await self._analyze_sources(sources, query)
            
            # Synthesize findings
            synthesis = await self._synthesize_findings(analyzed_sources, query)
            
            return {
                "success": True,
                "message": "Web research completed",
                "data": {
                    "query": query.dict(),
                    "sources": [source.dict() for source in analyzed_sources],
                    "synthesis": synthesis,
                    "key_findings": await self._extract_key_findings(synthesis),
                    "recommendations": await self._generate_recommendations(synthesis, query)
                },
                "errors": []
            }
        except Exception as e:
            return {
                "success": False,
                "message": "Web research failed",
                "data": {},
                "errors": [str(e)]
            }
    
    async def _search_web_sources(self, query: ResearchQuery) -> List[Dict[str, Any]]:
        """Search for web sources related to the query."""
        # For now, we'll use a simple approach with predefined sources
        # In a full implementation, you'd integrate with search APIs
        
        sources = []
        search_terms = " ".join([query.topic] + query.keywords)
        
        # DSS-relevant sources
        dss_sources = [
            "https://www1.nyc.gov/site/dss/index.page",
            "https://www.nyc.gov/site/hra/index.page",
            "https://www.nyc.gov/site/dhs/index.page"
        ]
        
        session = await self._get_session()
        
        for source_url in dss_sources:
            try:
                async with session.get(source_url) as response:
                    if response.status == 200:
                        content = await response.text()
                        soup = BeautifulSoup(content, 'html.parser')
                        
                        # Extract relevant content
                        title = soup.find('title')
                        title_text = title.get_text() if title else "No title"
                        
                        # Simple relevance scoring
                        relevance_score = self._calculate_relevance(content, search_terms)
                        
                        sources.append({
                            "url": source_url,
                            "title": title_text,
                            "content": self._extract_main_content(soup),
                            "source_type": "web",
                            "timestamp": "2024-01-01",  # Would be actual timestamp
                            "relevance_score": relevance_score
                        })
            except Exception as e:
                print(f"Error fetching {source_url}: {e}")
                continue
        
        return sources
    
    def _calculate_relevance(self, content: str, search_terms: str) -> float:
        """Calculate relevance score for content."""
        content_lower = content.lower()
        terms = search_terms.lower().split()
        
        score = 0
        for term in terms:
            score += content_lower.count(term)
        
        return min(score / len(terms), 1.0) if terms else 0.0
    
    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from HTML."""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:2000]  # Limit content length
    
    async def _analyze_sources(self, sources: List[Dict[str, Any]], query: ResearchQuery) -> List[ResearchSource]:
        """Analyze and filter sources based on relevance."""
        analyzed_sources = []
        
        for source in sources:
            if source["relevance_score"] > 0.1:  # Minimum relevance threshold
                research_source = ResearchSource(**source)
                analyzed_sources.append(research_source)
        
        # Sort by relevance score
        analyzed_sources.sort(key=lambda x: x.relevance_score, reverse=True)
        
        # Limit to max_results
        return analyzed_sources[:query.max_results]
    
    async def _synthesize_findings(self, sources: List[ResearchSource], query: ResearchQuery) -> str:
        """Synthesize findings from multiple sources."""
        if not sources:
            return "No relevant sources found for the research query."
        
        # Prepare content for synthesis
        content_summary = "\n\n".join([
            f"Source: {source.title}\nRelevance: {source.relevance_score}\nContent: {source.content[:500]}..."
            for source in sources
        ])
        
        prompt = f"""Synthesize the following research findings for a DSS strategist:

Research Topic: {query.topic}
Keywords: {', '.join(query.keywords)}

Sources:
{content_summary}

Please provide a comprehensive synthesis that:
1. Identifies key themes and patterns
2. Highlights relevant insights for DSS operations
3. Notes any gaps in current knowledge
4. Suggests areas for further investigation
5. Relates findings to DSS strategic priorities

Focus on practical implications for DSS service delivery and policy development."""

        system_prompt = """You are a DSS Research Specialist synthesizing information for strategic decision-making. 
        Provide clear, actionable insights that can inform policy and operational improvements."""
        
        response = await self.llm_service.generate_response(prompt, system_prompt)
        return response.content
    
    async def _extract_key_findings(self, synthesis: str) -> List[str]:
        """Extract key findings from synthesis."""
        prompt = f"""Extract 3-5 key findings from this research synthesis:

{synthesis}

Format each finding as a clear, concise statement that would be useful for DSS leadership."""

        system_prompt = """You are extracting key findings for DSS leadership. 
        Focus on actionable insights and strategic implications."""
        
        response = await self.llm_service.generate_response(prompt, system_prompt)
        
        # Parse findings (simple approach - in production you'd use more sophisticated parsing)
        findings = [line.strip() for line in response.content.split('\n') if line.strip() and not line.startswith('#')]
        return findings[:5]  # Limit to 5 findings
    
    async def _generate_recommendations(self, synthesis: str, query: ResearchQuery) -> List[str]:
        """Generate recommendations based on research findings."""
        prompt = f"""Based on this research synthesis, generate 3-5 specific recommendations for DSS:

{synthesis}

Research Topic: {query.topic}

Provide recommendations that are:
1. Specific and actionable
2. Relevant to DSS operations
3. Feasible to implement
4. Aligned with DSS mission
5. Prioritized by impact and effort"""

        system_prompt = """You are a DSS Research Specialist providing recommendations. 
        Focus on practical, implementable suggestions that will improve service delivery."""
        
        response = await self.llm_service.generate_response(prompt, system_prompt)
        
        # Parse recommendations
        recommendations = [line.strip() for line in response.content.split('\n') if line.strip() and not line.startswith('#')]
        return recommendations[:5]  # Limit to 5 recommendations
    
    async def analyze_documents(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze documents for insights and patterns.
        
        Args:
            document_data: Dictionary containing document content and metadata
            
        Returns:
            Dictionary containing document analysis results
        """
        try:
            documents = document_data.get("documents", [])
            analysis_type = document_data.get("analysis_type", "general")
            
            # Analyze each document
            document_analyses = []
            for doc in documents:
                analysis = await self._analyze_single_document(doc, analysis_type)
                document_analyses.append(analysis)
            
            # Synthesize across documents
            cross_document_synthesis = await self._synthesize_document_analyses(document_analyses)
            
            return {
                "success": True,
                "message": "Document analysis completed",
                "data": {
                    "individual_analyses": document_analyses,
                    "cross_document_synthesis": cross_document_synthesis,
                    "key_insights": await self._extract_document_insights(cross_document_synthesis)
                },
                "errors": []
            }
        except Exception as e:
            return {
                "success": False,
                "message": "Document analysis failed",
                "data": {},
                "errors": [str(e)]
            }
    
    async def _analyze_single_document(self, document: Dict[str, Any], analysis_type: str) -> Dict[str, Any]:
        """Analyze a single document."""
        content = document.get("content", "")
        title = document.get("title", "Untitled")
        
        prompt = f"""Analyze this document for DSS strategic insights:

Title: {title}
Content: {content[:2000]}...

Analysis Type: {analysis_type}

Please provide:
1. Key themes and topics
2. Relevant policy implications
3. Operational considerations
4. Stakeholder impacts
5. Recommendations for DSS"""

        system_prompt = """You are a DSS Document Analyst. 
        Focus on extracting strategic insights and practical implications for DSS operations."""
        
        response = await self.llm_service.generate_response(prompt, system_prompt)
        
        return {
            "title": title,
            "analysis": response.content,
            "key_themes": await self._extract_themes(response.content),
            "relevance_score": self._calculate_relevance(content, "DSS social services policy")
        }
    
    async def _extract_themes(self, analysis: str) -> List[str]:
        """Extract key themes from analysis."""
        prompt = f"""Extract 3-5 key themes from this analysis:

{analysis}

List each theme as a short phrase."""

        response = await self.llm_service.generate_response(prompt)
        themes = [line.strip() for line in response.content.split('\n') if line.strip()]
        return themes[:5]
    
    async def _synthesize_document_analyses(self, analyses: List[Dict[str, Any]]) -> str:
        """Synthesize multiple document analyses."""
        if not analyses:
            return "No documents analyzed."
        
        content = "\n\n".join([
            f"Document: {analysis['title']}\nAnalysis: {analysis['analysis']}"
            for analysis in analyses
        ])
        
        prompt = f"""Synthesize insights from these document analyses:

{content}

Provide a comprehensive synthesis that identifies:
1. Common themes across documents
2. Contradictions or gaps
3. Strategic implications for DSS
4. Priority areas for action"""

        system_prompt = """You are synthesizing document analyses for DSS leadership. 
        Focus on strategic insights and actionable recommendations."""
        
        response = await self.llm_service.generate_response(prompt, system_prompt)
        return response.content
    
    async def _extract_document_insights(self, synthesis: str) -> List[str]:
        """Extract key insights from document synthesis."""
        prompt = f"""Extract 3-5 key insights from this document synthesis:

{synthesis}

Format as clear, actionable insights for DSS leadership."""

        response = await self.llm_service.generate_response(prompt)
        insights = [line.strip() for line in response.content.split('\n') if line.strip()]
        return insights[:5]
    
    async def synthesize_research(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize multiple research sources into a comprehensive report.
        
        Args:
            research_data: Dictionary containing multiple research sources
            
        Returns:
            Dictionary containing synthesized research report
        """
        try:
            sources = research_data.get("sources", [])
            research_question = research_data.get("research_question", "")
            
            # Combine all source content
            combined_content = "\n\n".join([
                f"Source {i+1}: {source.get('content', '')}"
                for i, source in enumerate(sources)
            ])
            
            # Generate comprehensive synthesis
            synthesis = await self._generate_comprehensive_synthesis(
                combined_content, research_question
            )
            
            return {
                "success": True,
                "message": "Research synthesis completed",
                "data": {
                    "research_question": research_question,
                    "synthesis": synthesis,
                    "key_findings": await self._extract_key_findings(synthesis),
                    "recommendations": await self._generate_recommendations(synthesis, 
                        ResearchQuery(topic=research_question, keywords=[], scope="focused", sources=[]))
                },
                "errors": []
            }
        except Exception as e:
            return {
                "success": False,
                "message": "Research synthesis failed",
                "data": {},
                "errors": [str(e)]
            }
    
    async def _generate_comprehensive_synthesis(self, content: str, research_question: str) -> str:
        """Generate comprehensive synthesis of research content."""
        prompt = f"""Generate a comprehensive research synthesis for DSS leadership:

Research Question: {research_question}

Research Content:
{content}

Please provide:
1. Executive Summary
2. Key Findings
3. Analysis and Implications
4. Strategic Recommendations
5. Areas for Further Research

Focus on practical implications for DSS operations and policy development."""

        system_prompt = """You are a DSS Research Specialist creating comprehensive reports for leadership. 
        Structure your response clearly and focus on actionable insights."""
        
        response = await self.llm_service.generate_response(prompt, system_prompt)
        return response.content
    
    async def research_policy_implications(self, policy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Research policy implications for DSS initiatives.
        
        Args:
            policy_data: Dictionary containing policy research details
            
        Returns:
            Dictionary containing policy research results
        """
        try:
            policy_topic = policy_data.get("policy_topic", "")
            jurisdiction = policy_data.get("jurisdiction", "NYC")
            
            # This would integrate with policy databases and legal sources
            # For now, we'll use the LLM to generate policy analysis
            
            prompt = f"""Research policy implications for this DSS initiative:

Policy Topic: {policy_topic}
Jurisdiction: {jurisdiction}

Please analyze:
1. Current policy landscape
2. Potential policy changes needed
3. Stakeholder implications
4. Implementation challenges
5. Success factors
6. Risk mitigation strategies

Focus on practical policy considerations for DSS implementation."""

            system_prompt = """You are a DSS Policy Research Specialist. 
            Provide comprehensive policy analysis with practical implementation guidance."""
            
            response = await self.llm_service.generate_response(prompt, system_prompt)
            
            return {
                "success": True,
                "message": "Policy research completed",
                "data": {
                    "policy_topic": policy_topic,
                    "jurisdiction": jurisdiction,
                    "analysis": response.content,
                    "key_implications": await self._extract_policy_implications(response.content),
                    "recommendations": await self._generate_policy_recommendations(response.content)
                },
                "errors": []
            }
        except Exception as e:
            return {
                "success": False,
                "message": "Policy research failed",
                "data": {},
                "errors": [str(e)]
            }
    
    async def _extract_policy_implications(self, analysis: str) -> List[str]:
        """Extract key policy implications from analysis."""
        prompt = f"""Extract 3-5 key policy implications from this analysis:

{analysis}

Format as clear implications for DSS policy development."""

        response = await self.llm_service.generate_response(prompt)
        implications = [line.strip() for line in response.content.split('\n') if line.strip()]
        return implications[:5]
    
    async def _generate_policy_recommendations(self, analysis: str) -> List[str]:
        """Generate policy recommendations from analysis."""
        prompt = f"""Generate 3-5 specific policy recommendations based on this analysis:

{analysis}

Focus on actionable policy changes for DSS."""

        response = await self.llm_service.generate_response(prompt)
        recommendations = [line.strip() for line in response.content.split('\n') if line.strip()]
        return recommendations[:5]
    
    async def research_best_practices(self, practice_data: Dict[str, Any]) -> Dict[str, Any]:
        """Research best practices for DSS initiatives.
        
        Args:
            practice_data: Dictionary containing best practices research details
            
        Returns:
            Dictionary containing best practices research results
        """
        try:
            practice_area = practice_data.get("practice_area", "")
            context = practice_data.get("context", "DSS operations")
            
            prompt = f"""Research best practices for this DSS initiative:

Practice Area: {practice_area}
Context: {context}

Please identify:
1. Industry best practices
2. Successful implementations in similar organizations
3. Key success factors
4. Common pitfalls to avoid
5. Implementation strategies
6. Performance metrics and benchmarks

Focus on practices that can be adapted to DSS operations."""

            system_prompt = """You are a DSS Best Practices Research Specialist. 
            Identify practical, proven approaches that can improve DSS service delivery."""
            
            response = await self.llm_service.generate_response(prompt, system_prompt)
            
            return {
                "success": True,
                "message": "Best practices research completed",
                "data": {
                    "practice_area": practice_area,
                    "context": context,
                    "best_practices": response.content,
                    "key_practices": await self._extract_key_practices(response.content),
                    "implementation_guide": await self._generate_implementation_guide(response.content)
                },
                "errors": []
            }
        except Exception as e:
            return {
                "success": False,
                "message": "Best practices research failed",
                "data": {},
                "errors": [str(e)]
            }
    
    async def _extract_key_practices(self, content: str) -> List[str]:
        """Extract key best practices from content."""
        prompt = f"""Extract 5-7 key best practices from this research:

{content}

Format as actionable practices for DSS implementation."""

        response = await self.llm_service.generate_response(prompt)
        practices = [line.strip() for line in response.content.split('\n') if line.strip()]
        return practices[:7]
    
    async def _generate_implementation_guide(self, content: str) -> str:
        """Generate implementation guide from best practices."""
        prompt = f"""Create an implementation guide based on these best practices:

{content}

Provide a step-by-step guide for DSS implementation including:
1. Preparation phase
2. Implementation steps
3. Key milestones
4. Success metrics
5. Risk mitigation"""

        response = await self.llm_service.generate_response(prompt)
        return response.content
    
    async def cleanup(self):
        """Clean up resources."""
        if self.session:
            await self.session.close()
            self.session = None
        await self.mcp_manager.cleanup()

    async def research(self, prompt: str) -> str:
        """A simplified research method for direct prompts."""
        try:
            research_data = {
                "query": prompt,
                "max_results": 5,
                "include_web": True,
                "include_mcp": True
            }
            
            result = await self.conduct_comprehensive_research(research_data)
            
            if result.get("success"):
                return result.get("data", {}).get("synthesis", "No synthesis available.")
            else:
                return f"Research failed: {result.get('errors', ['Unknown error'])}"
                
        except Exception as e:
            return f"An unexpected error occurred during research: {str(e)}" 