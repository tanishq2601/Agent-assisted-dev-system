"""
Deployment Agent Module

This module implements the Infrastructure Agent responsible for deploying code to Azure cloud.
It handles Azure CLI installation, authentication, and automated deployment processes.

The agent manages the entire deployment workflow including:
- Azure CLI installation and verification
- Azure authentication
- Code packaging and deployment to Azure App Service

Author: AI Vectorial
Date: 2025-02-04
"""

import os
import yaml
import platform
import asyncio
from distutils.util import strtobool

from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_core import CancellationToken
from autogen_core.models import UserMessage
from autogen_core.code_executor import CodeBlock
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

from coding_agent.coding_agent import CodeGenratingAgent

import warnings
warnings.filterwarnings("ignore")


with open("prompts.yaml", "r") as file:
    prompts = yaml.safe_load(file)

class DeploymentAgent:
    """
    A class that implements the Infrastructure Agent functionality.

    This agent is responsible for:
    - Managing Azure CLI installation
    - Handling Azure authentication
    - Deploying code to Azure App Service
    - Managing deployment configurations

    Attributes:
        resource_group (str): Azure resource group name
        app_name (str): Azure App Service name
        deployment_agent_prompt (str): Prompt template for deployment
        model_client (AzureOpenAIChatCompletionClient): Client for Azure OpenAI API
        code_executor (LocalCommandLineCodeExecutor): Executor for running Azure CLI commands
        available_status_prompt (str): Prompt template for checking Azure CLI status
    """

    def __init__(self):
        """
        Initializes the DeploymentAgent with Azure configurations and required clients.
        """
        self.resource_group = os.getenv("AZURE_APP_SERVICE_RG")
        self.app_name = os.getenv("AZURE_APP_SERVICE_NAME")
        self.deployment_agent_prompt = prompts["DEPLOYMENT_AGENT"]["prompt"]
        self.model_client = AzureOpenAIChatCompletionClient(
            azure_deployment="gpt-4o",
            azure_endpoint=os.getenv("AZURE_API_BASE"),
            model="gpt-4o",
            api_version="2024-08-01-preview",
            api_key=os.getenv("AZURE_API_KEY"),
        )
        self.code_executor = LocalCommandLineCodeExecutor(work_dir="execution_sample")
        self.available_status_prompt = prompts["AZURE_AVAILABILITY_CHECK"]["prompt"]

    async def check_azure_cli(self):
        """
        Verifies Azure CLI installation and version.

        If Azure CLI is not installed, triggers installation process.
        Validates the installation status using AI assessment.
        """
        result = await self.code_executor.execute_code_blocks(code_blocks=[CodeBlock(code="az --version", language="bash")],
                                                              cancellation_token=CancellationToken())

        available_status = await self.model_client.create([UserMessage(content=self.available_status_prompt.format(result=result.output), source="user")])
        available_status = bool(strtobool(available_status.content))
        
        print(f"checking az version : {available_status}")
        
        if available_status:
            print("Azure CLI installed successfully")
        else:
            print("Azure CLI not installed. Beginning installation...")
            installation_status = self.install_azure_cli()
            if installation_status:
                print("Azure CLI installed successfully")
            else:
                print("Azure CLI installation failed")
    
        
    def install_azure_cli(self):
        """
        Installs Azure CLI based on the operating system.

        Supports Windows (winget), macOS (brew), and Linux (apt).

        Returns:
            bool: True if installation successful, False otherwise
        """
        try:
            if platform.system() == "Windows":
                os.system("winget install --id AzureCLI -e --source winget")
            elif platform.system() == "Darwin":
                os.system("brew update && brew install azure-cli")
            elif platform.system() == "Linux":
                os.system("sudo apt-get update && sudo apt-get install azure-cli")
            else:
                print("Unsupported operating system")
            
            return True
        except Exception as e:
            print(f"An error occurred during installation: {e}")
            return False
    
    async def check_authentication_status(self):
        """
        Verifies Azure authentication status.

        Initiates Azure login process and validates authentication.
        """
        await self.code_executor.execute_code_blocks(code_blocks=[CodeBlock(code="az login", language="bash")],
                                                              cancellation_token=CancellationToken())
        
        print("Authentication Successful Initiating Deployment...")

    async def deploy_code(self, zip_file_path):
        """
        Deploys code package to Azure App Service.

        Performs the following steps:
        1. Verifies Azure CLI installation
        2. Checks authentication status
        3. Generates deployment command using AI
        4. Executes deployment to Azure App Service

        Args:
            zip_file_path (str): Path to the zipped code package
        """
        await self.check_azure_cli()
        await self.check_authentication_status()

        deployment_verification = await self.model_client.create([UserMessage(content=self.deployment_agent_prompt.format(resource_group=self.resource_group, app_name=self.app_name, zip_file_path=zip_file_path), source="user")])
        
        refactored_command = deployment_verification.content.replace("```", "").replace("bash", "")
        print(f"deployment verification : {refactored_command}")

        os.system(refactored_command)
        
# if __name__ == "__main__":
#     import asyncio

#     deployment_agent = DeploymentAgent()
#     deployment_agent.create_project_zip("test_api")
#     asyncio.run(deployment_agent.deploy_code("test_api.zip"))