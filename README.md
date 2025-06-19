# AI Agent Team - Company of One

This project implements a team of AI agents designed to function as a "company of one" for various clients, with a current focus on the City of New York Department of Social Services (DSS).

## Agent Team Members

1. **Strategist**: Data-informed advisor for senior leaders, specializing in identifying leverage points and accelerating decision-making
2. **Operations Manager**: Manages workflows and coordinates between agents
3. **Researcher**: Conducts deep research and analysis
4. **Writer**: Creates clear, compelling content and communications
5. **Data Analyst**: Processes and analyzes data to inform decisions

## Project Structure

```
.
├── agents/                 # Individual agent implementations
│   ├── strategist/        # DSS Strategist agent
│   ├── ops_manager/       # Operations Manager agent
│   ├── researcher/        # Researcher agent
│   ├── writer/           # Writer agent
│   └── data_analyst/     # Data Analyst agent
├── core/                  # Shared core functionality
├── config/               # Configuration files
├── tests/               # Test suite
└── examples/            # Example usage and scenarios
```

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run the example:
```bash
python examples/dss_strategist_example.py
```

## Current Focus: DSS Strategist

The DSS Strategist agent is currently implemented as an MVP, designed to:
- Drive KPI-based public impact strategy
- Detect operational bottlenecks and policy misalignments
- Map risks and political sensitivities
- Provide "What Would It Take" analysis for initiatives
- Ensure mission alignment and filter distractions

## License

MIT License 