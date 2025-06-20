import asyncio
import json
from agents.researcher.researcher import Researcher

async def test_web_research():
    """Test web research functionality."""
    print("🔍 Testing Web Research...")
    
    researcher = Researcher()
    
    # Test web research for DSS-related topic
    research_request = {
        "type": "web_research",
        "data": {
            "topic": "DSS service delivery optimization",
            "keywords": ["social services", "efficiency", "digital transformation"],
            "scope": "focused",
            "sources": ["web"],
            "max_results": 5
        }
    }
    
    response = await researcher.process_request(research_request)
    
    if response.success:
        print("✅ Web research completed successfully!")
        print(f"📊 Found {len(response.data['sources'])} relevant sources")
        print(f"📝 Synthesis: {response.data['synthesis'][:200]}...")
        print(f"🎯 Key findings: {len(response.data['key_findings'])} identified")
        print(f"💡 Recommendations: {len(response.data['recommendations'])} generated")
    else:
        print(f"❌ Web research failed: {response.errors}")
    
    await researcher.cleanup()

async def test_document_analysis():
    """Test document analysis functionality."""
    print("\n📄 Testing Document Analysis...")
    
    researcher = Researcher()
    
    # Sample documents for analysis
    documents = [
        {
            "title": "DSS Annual Report 2023",
            "content": """
            The Department of Social Services (DSS) has made significant progress in 
            improving service delivery through digital transformation initiatives. 
            Key achievements include reducing application processing times by 40% 
            and increasing client satisfaction scores to 85%. However, challenges 
            remain in staff training and system integration.
            """
        },
        {
            "title": "Social Services Policy Review",
            "content": """
            Recent policy changes have expanded eligibility for social services 
            programs, resulting in a 25% increase in applications. This has 
            created operational challenges that require additional resources and 
            process improvements to maintain service quality.
            """
        }
    ]
    
    analysis_request = {
        "type": "document_analysis",
        "data": {
            "documents": documents,
            "analysis_type": "strategic"
        }
    }
    
    response = await researcher.process_request(analysis_request)
    
    if response.success:
        print("✅ Document analysis completed successfully!")
        print(f"📊 Analyzed {len(response.data['individual_analyses'])} documents")
        print(f"🔍 Cross-document synthesis: {response.data['cross_document_synthesis'][:200]}...")
        print(f"💡 Key insights: {len(response.data['key_insights'])} identified")
    else:
        print(f"❌ Document analysis failed: {response.errors}")
    
    await researcher.cleanup()

async def test_policy_research():
    """Test policy research functionality."""
    print("\n📋 Testing Policy Research...")
    
    researcher = Researcher()
    
    policy_request = {
        "type": "policy_research",
        "data": {
            "policy_topic": "Digital transformation of social services",
            "jurisdiction": "NYC"
        }
    }
    
    response = await researcher.process_request(policy_request)
    
    if response.success:
        print("✅ Policy research completed successfully!")
        print(f"📊 Policy topic: {response.data['policy_topic']}")
        print(f"🏛️ Jurisdiction: {response.data['jurisdiction']}")
        print(f"📝 Analysis: {response.data['analysis'][:200]}...")
        print(f"⚖️ Key implications: {len(response.data['key_implications'])} identified")
        print(f"💡 Policy recommendations: {len(response.data['recommendations'])} generated")
    else:
        print(f"❌ Policy research failed: {response.errors}")
    
    await researcher.cleanup()

async def test_best_practices_research():
    """Test best practices research functionality."""
    print("\n⭐ Testing Best Practices Research...")
    
    researcher = Researcher()
    
    practices_request = {
        "type": "best_practices_research",
        "data": {
            "practice_area": "Client case management systems",
            "context": "DSS operations"
        }
    }
    
    response = await researcher.process_request(practices_request)
    
    if response.success:
        print("✅ Best practices research completed successfully!")
        print(f"📊 Practice area: {response.data['practice_area']}")
        print(f"🏢 Context: {response.data['context']}")
        print(f"📝 Best practices: {response.data['best_practices'][:200]}...")
        print(f"🎯 Key practices: {len(response.data['key_practices'])} identified")
        print(f"📋 Implementation guide: {len(response.data['implementation_guide'])} characters")
    else:
        print(f"❌ Best practices research failed: {response.errors}")
    
    await researcher.cleanup()

async def test_research_synthesis():
    """Test research synthesis functionality."""
    print("\n🔬 Testing Research Synthesis...")
    
    researcher = Researcher()
    
    # Sample research sources
    sources = [
        {
            "title": "Digital Transformation in Social Services",
            "content": "Research shows that digital transformation can improve service delivery efficiency by up to 60% while reducing costs by 30%."
        },
        {
            "title": "Client Experience in Government Services",
            "content": "Studies indicate that improving client experience leads to better outcomes and higher satisfaction rates in social services programs."
        },
        {
            "title": "Staff Training for Digital Systems",
            "content": "Comprehensive staff training is essential for successful digital transformation, with training programs showing 40% improvement in system adoption."
        }
    ]
    
    synthesis_request = {
        "type": "synthesis_research",
        "data": {
            "sources": sources,
            "research_question": "How can DSS optimize service delivery through digital transformation?"
        }
    }
    
    response = await researcher.process_request(synthesis_request)
    
    if response.success:
        print("✅ Research synthesis completed successfully!")
        print(f"🔍 Research question: {response.data['research_question']}")
        print(f"📝 Synthesis: {response.data['synthesis'][:200]}...")
        print(f"🎯 Key findings: {len(response.data['key_findings'])} identified")
        print(f"💡 Recommendations: {len(response.data['recommendations'])} generated")
    else:
        print(f"❌ Research synthesis failed: {response.errors}")
    
    await researcher.cleanup()

async def test_researcher_integration():
    """Test integration between Researcher and Strategist agents."""
    print("\n🤝 Testing Researcher-Strategist Integration...")
    
    from agents.strategist.dss_strategist import DSSStrategist
    
    researcher = Researcher()
    strategist = DSSStrategist()
    
    # First, conduct research
    research_request = {
        "type": "web_research",
        "data": {
            "topic": "DSS performance optimization",
            "keywords": ["efficiency", "metrics", "improvement"],
            "scope": "focused",
            "sources": ["web"],
            "max_results": 3
        }
    }
    
    research_response = await researcher.process_request(research_request)
    
    if research_response.success:
        print("✅ Research completed for strategist")
        
        # Use research findings to inform strategic analysis
        kpi_data = {
            "research_findings": research_response.data['synthesis'],
            "key_insights": research_response.data['key_findings'],
            "recommendations": research_response.data['recommendations']
        }
        
        strategy_request = {
            "type": "kpi_analysis",
            "data": kpi_data
        }
        
        strategy_response = await strategist.process_request(strategy_request)
        
        if strategy_response.success:
            print("✅ Strategic analysis completed using research data")
            print(f"📊 Strategy insights: {strategy_response.data['analysis'][:200]}...")
        else:
            print(f"❌ Strategic analysis failed: {strategy_response.errors}")
    else:
        print(f"❌ Research failed: {research_response.errors}")
    
    await researcher.cleanup()

async def main():
    """Run all researcher tests."""
    print("🚀 Starting Researcher Agent Tests\n")
    
    # Test individual functionalities
    await test_web_research()
    await test_document_analysis()
    await test_policy_research()
    await test_best_practices_research()
    await test_research_synthesis()
    
    # Test integration
    await test_researcher_integration()
    
    print("\n🎉 All Researcher Agent tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 