import os
import yaml
import json
import asyncio

from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_core.models import UserMessage
from autogen_agentchat.agents import AssistantAgent

import warnings
warnings.filterwarnings("ignore")

with open("prompts.yaml", "r") as f:
    prompts = yaml.safe_load(f)

class CodeGenratingAgent:
    def __init__(self, user_query=None):
        self.user_query = user_query
        self.developer_agent_prompt = prompts["DEVELOPER_AGENT"]["prompt"]
        self.refactor_code_agent_prompt = prompts["REFACTOR_CODE_AGENT"]["prompt"]
        self.model_client = AzureOpenAIChatCompletionClient(
            azure_deployment="gpt-4o",
            azure_endpoint=os.getenv("AZURE_API_BASE"),
            model="gpt-4o",
            api_version="2024-08-01-preview",
            api_key=os.getenv("AZURE_API_KEY"),
        )
    
    def initiate_coding_assistant(self):
        self.model_assistant = AssistantAgent(name="coding_assistant",
                                              model_client=self.model_client,
                                              tools=[self.code_generator])
        return self.model_assistant

    async def code_generator(self):
        user_query = self.user_query
        generated_code = await self.model_client.create([UserMessage(content=self.developer_agent_prompt.format(user_query=user_query), source="user")])
        return generated_code

    async def assistant_run(self):
        self.model_assistant = self.initiate_coding_assistant()
        response = await self.model_assistant.on_messages(
            [TextMessage(content="Write efficient, scalable python code.", source="user")],
            cancellation_token=CancellationToken(),
        )
        return response
    
    def read_code(self, file_path):
        with open(file_path, "r") as f:
            code = f.read()
        return code
    
    async def refactor_code(self, code_file_path, new_folder_path="code_refactor", file_name="code_refactored"):
        new_code_path = f"{new_folder_path}/{file_name}.py"

        buggy_code = self.read_code(code_file_path)
        refactored_code = await self.model_client.create([UserMessage(content=self.refactor_code_agent_prompt.format(buggy_code=buggy_code), source="user")])
        
        cleaned_code = refactored_code.content.replace("```", "").replace("python", "")
        
        with open(new_code_path, "w") as code_file:
            code_file.write(cleaned_code)

        return cleaned_code, new_code_path



