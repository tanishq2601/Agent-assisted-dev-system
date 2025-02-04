# Hivemind Technical Documentation

## System Overview

Hivemind is an AI-powered development workflow system that automates code generation, testing, and deployment using three specialized AI agents. The system uses the Agentic Framework and integrates with Azure OpenAI for AI capabilities.

## Core Components

### 1. Orchestrator (`orchestrator.py`)
- **Purpose**: Main entry point and workflow coordinator
- **Key Functions**:
  - `code(user_query, folder_path, file_name)`: Initiates code generation
  - `test(code_path)`: Manages code testing
  - `deploy(folder_path)`: Handles deployment
  - `orchestrate(user_query)`: Main driver function

### 2. Developer Agent (`coding_agent/coding_agent.py`)
- **Class**: `CodeGenratingAgent`
- **Capabilities**:
  - Code generation from user requirements
  - Code refactoring
  - Integration with Azure OpenAI
- **Key Methods**:
  - `code_generator()`: Generates code using AI
  - `refactor_code()`: Refactors problematic code
  - `assistant_run()`: Manages AI assistant interactions

### 3. QA Agent (`qa_tester/qa_tester.py`)
- **Class**: `QATester`
- **Features**:
  - Automated code testing
  - Code assessment
  - Bug detection and fixing
- **Key Methods**:
  - `qa_tester()`: Executes code tests
  - `code_assesment_agent()`: Evaluates code quality
  - `code_fixer()`: Fixes identified bugs

### 4. Deployment Agent (`deployment_agent/deployment_agent.py`)
- **Class**: `DeploymentAgent`
- **Capabilities**:
  - Azure App Service deployment
  - Azure CLI management
  - Automated authentication
- **Key Methods**:
  - `check_azure_cli()`: Verifies CLI installation
  - `install_azure_cli()`: Handles CLI installation
  - `deploy_code()`: Manages deployment process

## Workflow Process

1. **Code Generation**:
   - User provides requirements
   - Developer Agent generates initial code
   - Code is saved to specified path

2. **Testing Phase**:
   - QA Agent executes code
   - Performs automated assessment
   - Triggers fixes if needed

3. **Deployment**:
   - Creates deployment package
   - Verifies Azure CLI setup
   - Deploys to Azure App Service

## Dependencies

- **Azure OpenAI**: For AI code generation and assessment
- **Azure CLI**: For cloud deployment
- **Python Packages**:
  - autogen_ext
  - autogen_agentchat
  - autogen_core
  - yaml
  - asyncio

## Best Practices

1. **Code Generation**:
   - Provide clear, specific requirements
   - Use descriptive file names
   - Keep generated code in designated folders

2. **Testing**:
   - Allow automatic fixes for minor issues
   - Review generated code before deployment
   - Check execution logs for issues

3. **Deployment**:
   - Ensure Azure credentials are configured
   - Verify resource group and app service exist
   - Monitor deployment logs

## Common Issues and Solutions

1. **Azure CLI Missing**:
   - System will attempt automatic installation
   - Can be manually installed via package manager

2. **Authentication Failures**:
   - Run `az login` manually if needed
   - Verify Azure environment variables

3. **Code Generation Issues**:
   - Check prompt clarity
   - Verify Azure OpenAI API access
   - Review error messages in logs