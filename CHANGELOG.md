# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-08-02

### Added

- **Web Dashboard:** Created a new Flask-based UI to monitor and interact with the agents.
- **Agent Interaction:** Implemented a chat interface in the dashboard to send prompts to agents and receive real-time responses.
- **Agent Details View:** Added a details panel to show agent capabilities and live status metrics.
- **Configuration Modal:** Built a modal for agent configuration (frontend only).
- **Domain Listing:** The dashboard now displays all registered MCP domains and their status.
- **Simplified Agent Methods:** Added `research()` and `analyze_strategy()` methods to the Researcher and Strategist agents, respectively, to allow for direct string-based prompting from the UI.
- **New Dependencies:** Added `Flask`, `flask-socketio`, `aiohttp`, and `ollama` to `requirements.txt`.

### Fixed

- Resolved multiple `ModuleNotFoundError` issues by installing and tracking required dependencies.
- Corrected agent response handling to fix "undefined" and "error processing request" messages in the UI.
- Addressed linter errors in agent and service modules.
- Fixed an issue where subsequent prompts to an agent would fail after a successful first prompt.
- Standardized the server startup process to ensure the correct code is always running.

### Changed

- Updated the project's `README.md` with comprehensive setup and usage instructions for the new web dashboard. 