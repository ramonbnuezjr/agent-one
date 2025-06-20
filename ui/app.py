#!/usr/bin/env python3
"""
Agent-One Web UI
A modern web interface for querying AI agents with domain-based MCP architecture.
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any, List

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import threading

# Import our agent system
from agents.researcher.researcher import Researcher
from agents.strategist.dss_strategist import DSSStrategist
from mcp.domain_manager import DomainManager, AgentDomain, DEFAULT_DOMAIN_CONFIGS
from mcp.wikipedia_server import WikipediaMCPServer
from mcp.arxiv_server import ArxivMCPServer
from core.llm_service import LLMService
from mcp.mcp_manager import MCPManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'agent-one-secret-key-2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables for agent instances
agents = {}
domain_manager = None
llm_service = None
mcp_manager = None

# Store agent configurations
agent_configs = {
    'strategist': {
        'memory_limit': 512,
        'request_rate': 60,
        'context_size': 4000,
        'security_level': 'high',
        'allowed_domains': ['strategic', 'general']
    },
    'researcher': {
        'memory_limit': 1024,
        'request_rate': 120,
        'context_size': 8000,
        'security_level': 'standard',
        'allowed_domains': ['research', 'general']
    },
    'data_analyst': {
        'memory_limit': 2048,
        'request_rate': 180,
        'context_size': 16000,
        'security_level': 'high',
        'allowed_domains': ['data_analysis', 'general']
    },
    'writer': {
        'memory_limit': 512,
        'request_rate': 60,
        'context_size': 4000,
        'security_level': 'standard',
        'allowed_domains': ['writer', 'general']
    }
}

def initialize_agents():
    """Initialize all agents and the domain manager."""
    global agents, domain_manager, llm_service, mcp_manager
    
    print("🔧 Initializing Agent-One System...")
    
    # Initialize LLM service
    llm_service = LLMService()
    
    # Initialize domain manager
    domain_manager = DomainManager()
    
    # Register all domains
    for domain, config in DEFAULT_DOMAIN_CONFIGS.items():
        domain_manager.register_domain(domain, config)
    
    # Register MCP servers for research domain
    wikipedia_server = WikipediaMCPServer()
    arxiv_server = ArxivMCPServer()
    
    domain_manager.register_server_for_domain(
        AgentDomain.RESEARCH, "wikipedia", wikipedia_server, priority=3
    )
    domain_manager.register_server_for_domain(
        AgentDomain.GENERAL, "wikipedia", wikipedia_server, priority=2
    )
    domain_manager.register_server_for_domain(
        AgentDomain.RESEARCH, "arxiv", arxiv_server, priority=2
    )
    domain_manager.register_server_for_domain(
        AgentDomain.GENERAL, "arxiv", arxiv_server, priority=1
    )
    
    # Initialize domain manager
    asyncio.run(domain_manager.initialize_all())
    
    # Initialize agents
    agents = {
        'researcher': Researcher(),
        'strategist': DSSStrategist()
    }
    
    # Initialize MCP manager
    mcp_manager = MCPManager()
    
    print("✅ Agent-One System initialized successfully!")

@app.route('/')
def index():
    """Main page with agent interface."""
    # Get the status of all domains
    domains = domain_manager.get_registered_domains()
    return render_template('index.html', domains=domains)

@app.route('/api/agents')
def get_agents():
    """Get available agents and their capabilities."""
    agent_info = {
        'researcher': {
            'name': 'Researcher',
            'description': 'Conducts comprehensive research and analysis',
            'capabilities': [
                'Web research',
                'Document analysis', 
                'MCP research',
                'Policy research',
                'Best practices research',
                'Comprehensive research'
            ],
            'domain': 'research'
        },
        'strategist': {
            'name': 'DSS Strategist',
            'description': 'Analyzes strategic initiatives and KPIs',
            'capabilities': [
                'KPI analysis',
                'Strategic planning',
                'Performance evaluation',
                'Policy recommendations'
            ],
            'domain': 'strategic'
        }
    }
    return jsonify(agent_info)

@app.route('/api/agent/<agent_type>/status')
def agent_status(agent_type):
    if agent_type not in agent_configs:
        return jsonify({'error': 'Agent not found'}), 404
    
    # Get the agent's configuration
    config = agent_configs[agent_type]
    
    # Mock dynamic status data
    status = {
        'status': 'active',
        'memory_usage': f"{config['memory_limit'] // 2}MB",
        'request_rate': f"{config['request_rate']}req/min",
        'uptime': '99.9%',
        'config': config
    }
    
    return jsonify(status)

@app.route('/api/agent/<agent_type>/configure', methods=['POST'])
def configure_agent(agent_type):
    if agent_type not in agent_configs:
        return jsonify({'error': 'Agent not found'}), 404
    
    data = request.json
    if not data:
        return jsonify({'error': 'No configuration data provided'}), 400
        
    try:
        # Update the agent's configuration
        agent_configs[agent_type].update({
            'memory_limit': int(data.get('memoryLimit', agent_configs[agent_type]['memory_limit'])),
            'request_rate': int(data.get('requestRate', agent_configs[agent_type]['request_rate'])),
            'context_size': int(data.get('contextSize', agent_configs[agent_type]['context_size'])),
            'security_level': data.get('securityLevel', agent_configs[agent_type]['security_level']),
            'allowed_domains': data.get('allowedDomains', agent_configs[agent_type]['allowed_domains'])
        })
        
        return jsonify({
            'status': 'success',
            'message': f'Configuration updated for {agent_type}',
            'config': agent_configs[agent_type]
        })
    except (ValueError, KeyError) as e:
        return jsonify({
            'error': 'Invalid configuration data',
            'message': str(e)
        }), 400

@app.route('/api/domains')
def get_domains():
    """Get available domains and their configurations."""
    domains = {}
    for domain, config in DEFAULT_DOMAIN_CONFIGS.items():
        domains[domain.value] = {
            'name': domain.value.replace('_', ' ').title(),
            'description': config.description,
            'allowed_sources': config.allowed_sources,
            'security_level': config.security_level,
            'rate_limits': config.rate_limits,
            'memory_config': config.memory_config,
            'context_rules': config.context_rules
        }
    return jsonify(domains)

@app.route('/api/query', methods=['POST'])
def query_agent():
    """Query a specific agent."""
    try:
        data = request.get_json()
        agent_type = data.get('agent')
        query_type = data.get('type', 'general')
        query_data = data.get('data', {})
        
        if agent_type not in agents:
            return jsonify({'error': f'Agent {agent_type} not found'}), 404
        
        agent = agents[agent_type]
        
        # Create request based on agent type
        if agent_type == 'researcher':
            request_data = {
                'type': query_type,
                'data': query_data
            }
        elif agent_type == 'strategist':
            request_data = {
                'type': query_type,
                'data': query_data
            }
        else:
            return jsonify({'error': f'Unknown agent type: {agent_type}'}), 400
        
        # Process request asynchronously
        async def process_request():
            try:
                response = await agent.process_request(request_data)
                return {
                    'success': response.success,
                    'message': response.message,
                    'data': response.data,
                    'errors': response.errors
                }
            except Exception as e:
                return {
                    'success': False,
                    'message': f'Error processing request: {str(e)}',
                    'data': {},
                    'errors': [str(e)]
                }
        
        # Run async function in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(process_request())
        finally:
            loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mcp/search', methods=['POST'])
def mcp_search():
    """Search using domain-specific MCP servers."""
    try:
        data = request.get_json()
        domain_name = data.get('domain', 'research')
        query = data.get('query', '')
        max_results = data.get('max_results', 10)
        
        # Convert domain name to enum
        domain = None
        for d in AgentDomain:
            if d.value == domain_name:
                domain = d
                break
        
        if not domain:
            return jsonify({'error': f'Unknown domain: {domain_name}'}), 400
        
        # Perform domain-specific search
        async def search_domain():
            try:
                results = await domain_manager.search_domain(domain, query, max_results)
                return [result.dict() for result in results]
            except Exception as e:
                return {'error': str(e)}
        
        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            results = loop.run_until_complete(search_domain())
        finally:
            loop.close()
        
        return jsonify({'results': results})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Check system health."""
    try:
        # Check domain manager health
        async def check_health():
            return await domain_manager.health_check_all()
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            health_status = loop.run_until_complete(check_health())
        finally:
            loop.close()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'domains': health_status
        })
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'running',
        'agents': {
            'strategist': {'status': 'active'},
            'researcher': {'status': 'active'},
            'data_analyst': {'status': 'active'},
            'writer': {'status': 'active'}
        },
        'domains': domain_manager.get_registered_domains()
    })

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection."""
    print(f"Client connected: {request.sid}")
    emit('status', {'message': 'Connected to Agent-One'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection."""
    print(f"Client disconnected: {request.sid}")

@socketio.on('query_agent')
def handle_agent_query(data):
    """Handle agent queries via WebSocket."""
    try:
        agent_type = data.get('agent')
        query_type = data.get('type', 'general')
        query_data = data.get('data', {})
        
        if agent_type not in agents:
            emit('query_response', {'error': f'Agent {agent_type} not found'})
            return
        
        agent = agents[agent_type]
        
        # Create request
        request_data = {
            'type': query_type,
            'data': query_data
        }
        
        # Process request asynchronously
        async def process_request():
            try:
                response = await agent.process_request(request_data)
                return {
                    'success': response.success,
                    'message': response.message,
                    'data': response.data,
                    'errors': response.errors
                }
            except Exception as e:
                return {
                    'success': False,
                    'message': f'Error processing request: {str(e)}',
                    'data': {},
                    'errors': [str(e)]
                }
        
        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(process_request())
        finally:
            loop.close()
        
        emit('query_response', result)
        
    except Exception as e:
        emit('query_response', {'error': str(e)})

@app.route('/api/agent/<agent_type>/prompt', methods=['POST'])
async def handle_prompt(agent_type):
    if agent_type not in agents:
        return jsonify({'error': 'Agent not found'}), 404
    
    agent = agents[agent_type]
    if agent is None:
        return jsonify({
            'response': f"I apologize, but the {agent_type} agent is not yet implemented. Please try the strategist or researcher agents."
        })
    
    data = request.json
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    
    try:
        # Handle different agent types
        if agent_type == 'strategist':
            response = await agent.analyze_strategy(prompt)
        elif agent_type == 'researcher':
            response = await agent.research(prompt)
        else:
            response = "This agent type is not yet implemented."
        
        return jsonify({
            'response': response
        })
    except Exception as e:
        print(f"Error processing prompt: {str(e)}")
        return jsonify({
            'error': 'Failed to process prompt',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    # Initialize agents in a separate thread
    def init_system():
        initialize_agents()
    
    init_thread = threading.Thread(target=init_system)
    init_thread.start()
    init_thread.join()
    
    print("🚀 Starting Agent-One Web UI...")
    print("📱 Access the UI at: http://localhost:8080")
    
    socketio.run(app, host='0.0.0.0', port=8080, debug=True) 