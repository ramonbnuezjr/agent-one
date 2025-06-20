# Agent One: AI-Powered Operational Strategy System

Agent One is a sophisticated, multi-agent system designed to provide data-informed strategic guidance and operational support. Initially conceived for the NYC Department of Social Services (DSS), it leverages a suite of specialized AI agents to analyze data, conduct research, and generate actionable insights. The system is managed through a web-based dashboard that allows for real-time monitoring, configuration, and interaction with the agents.

## Key Features

- **Multi-Agent Architecture:** A collection of specialized agents (Strategist, Researcher, etc.) that collaborate to solve complex problems.
- **Model Context Protocol (MCP):** A domain-based architecture that allows agents to access and share context from various data sources (e.g., Wikipedia, Arxiv) in a structured way.
- **Interactive Web Dashboard:** A Flask-based user interface for monitoring agent status, viewing details, and interacting directly with agents through a chat interface.
- **Dynamic Configuration:** Agents and their underlying models can be configured on-the-fly from the dashboard.
- **Local LLM Integration:** Powered by local language models through Ollama, ensuring data privacy and control.

## Project Structure

```
agent-one/
├── agents/              # Contains the core logic for each specialized agent
│   ├── researcher/
│   └── strategist/
├── config/              # Configuration files for the system
├── core/                # Core components like the base agent and LLM service
├── mcp/                 # Model Context Protocol implementation
├── ui/                  # Web dashboard front-end and back-end
│   ├── templates/
│   └── app.py
├── README.md            # This file
└── requirements.txt     # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed and running locally.
- A locally available model, such as `mistral`. You can pull it by running:
  ```bash
  ollama pull mistral
  ```

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd agent-one
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

Once the setup is complete, you can start the Agent One dashboard:

```bash
python ui/app.py
```

The application will be accessible at `http://localhost:8080`.

## How to Use the Dashboard

- **Agent Cards:** The main view shows all available agents and their current status.
- **View Details:** Click "View Details" on any agent card to see its capabilities and current performance metrics.
- **Agent Interaction:** Once viewing details, a chat interface will appear, allowing you to send prompts directly to that agent.
- **Configuration:** Click "Configure" to open a modal where you can adjust settings for each agent (Note: Backend integration for configuration is still in progress).
- **Registered Domains:** See all active data domains that the agents can access via the Model Context Protocol.

## License

MIT License 