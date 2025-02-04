# Hivemind

## Objective

Develop an AI-powered development workflow utilizing the Agentic Framework. This workflow will consist of three primary agents:

1. **Developer Agent**: This AI agent will be responsible for generating Python code based on given requirements or specifications.
2. **QA Agent**: This AI agent will automatically check and validate the code produced by the Python Developer Agent, ensuring quality and adherence to standards.
3. **Infrastructure Agent**: Upon successful QA checks, this agent will deploy the code to the designated cloud platform, taking into account the allocated resources.

## Framework

The Agentic Framework will be the foundation for the development and orchestration of these AI agents.

## Expected Outcome

A streamlined, automated development process that leverages AI to accelerate code creation, testing, and deployment.

## First Experiment

1. Create a Developer Agent that takes a prompt for a specific coding assignment, creates the code, and hands it over to the QA agent.
2. The QA agent will review the code and provide feedback to the Developer Agent.
3. This interaction continues until the QA agent passes the code.

## Project Structure

```
hivemind/
├── agent_requirements/    # Dependencies and requirements
├── code_refactor/        # Storage for refactored code
├── coding_agent/         # Developer Agent implementation
├── deployment_agent/     # Infrastructure Agent for deployment
├── qa_tester/           # QA Agent implementation
├── helper.py            # Utility functions
├── orchestrator.py      # Main orchestration logic
└── prompts.yaml         # Agent prompts and configurations
```

## Architecture

The project follows a three-agent architecture:

1. **Developer Agent** (`coding_agent/`)
   - Generates Python code based on user requirements
   - Uses GPT-4 for code generation
   - Supports code refactoring capabilities

2. **QA Agent** (`qa_tester/`)
   - Validates and tests generated code
   - Executes code in isolated environment
   - Provides automated code assessment
   - Can trigger code fixes when issues are found

3. **Infrastructure Agent** (`deployment_agent/`)
   - Handles Azure cloud deployments
   - Manages Azure CLI installation and authentication
   - Automates deployment process using Azure App Service

## Configuration

1. **Environment Variables**:
   Create a `.env` file with the following variables:
   ```
   AZURE_API_BASE=your_azure_endpoint
   AZURE_API_KEY=your_azure_api_key
   AZURE_APP_SERVICE_RG=your_resource_group
   AZURE_APP_SERVICE_NAME=your_app_service_name
   ```

2. **Azure Configuration**:
   - Requires Azure subscription
   - Azure CLI will be automatically installed if not present
   - App Service must be pre-configured

## Getting Started

1. **Clone the repository**:
    ```sh
    git clone <repository_url>
    cd <repository_name>
    ```

2. **Install dependencies**:
    ```sh
    pip install -r agent_requirements/requirements.txt
    ```

3. **Run the main script**:
    ```sh
    python orchestrator.py
    ```

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
