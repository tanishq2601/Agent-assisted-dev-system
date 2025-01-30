import os
import yaml
import platform
import shutil
from distutils.util import strtobool
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_core import CancellationToken
from autogen_core.models import UserMessage
from autogen_core.code_executor import CodeBlock
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

from coding_agent.coding_agent import CodeGenratingAgent

import warnings
warnings.filterwarnings("ignore")


from dotenv import load_dotenv

load_dotenv(override=True)

with open("prompts.yaml", "r") as file:
    prompts = yaml.safe_load(file)

class DeploymentAgent:
    def __init__(self):
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
    

    def create_project_zip(self, code_file_path):
        if not os.path.exists(code_file_path):  # Check the actual folder existence
            print(f"The directory {code_file_path} does not exist.")
            return False

        zip_path = f"{code_file_path}.zip"
        
        print(f"Creating zip file from {code_file_path}...")
        shutil.make_archive(code_file_path, 'zip', code_file_path)  # Create ZIP archive
        print(f"Zip file created successfully: {zip_path}")
        
        return True
        
    def install_azure_cli(self):
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
        await self.code_executor.execute_code_blocks(code_blocks=[CodeBlock(code="az login", language="bash")],
                                                              cancellation_token=CancellationToken())
        
        print("Authentication Successful 🥳 Initiating Deployment...")

    async def deploy_code(self, zip_file_path):
        await self.check_azure_cli()
        await self.check_authentication_status()

        deployment_verification = await self.model_client.create([UserMessage(content=self.deployment_agent_prompt.format(resource_group=self.resource_group, app_name=self.app_name, zip_file_path=zip_file_path), source="user")])
        
        refactored_command = deployment_verification.content.replace("```", "").replace("bash", "")
        print(f"deployment verification : {refactored_command}")

        os.system(refactored_command)
        
if __name__ == "__main__":
    import asyncio

    deployment_agent = DeploymentAgent()
    deployment_agent.create_project_zip("test_api")
    asyncio.run(deployment_agent.deploy_code("test_api.zip"))