import os
import yaml
import json

from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_core.models import UserMessage
from autogen_agentchat.agents import AssistantAgent

import warnings
warnings.filterwarnings("ignore")


from dotenv import load_dotenv

load_dotenv(override=True)


with open("prompts.yaml", "r") as f:
    prompts = yaml.safe_load(f)

class CodeGenratingAgent:
    def __init__(self, user_query=None):
        self.user_query = user_query
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
        generated_code = await self.model_client.create([UserMessage(content=user_query, source="user")])
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
    
    async def refactor_code(self, code_file_path):
        buggy_code = self.read_code(code_file_path)
        refactored_code = await self.model_client.create([UserMessage(content=self.refactor_code_agent_prompt.format(buggy_code=buggy_code), source="user")])
        
        cleaned_code = refactored_code.content.replace("```", "").replace("python", "")
        
        with open("code_refactor/code_refactored.py", "w") as code_file:
            code_file.write(cleaned_code)

        return cleaned_code


if __name__ == "__main__":
    import asyncio

    code_generator = CodeGenratingAgent("Build a FastAPI code to print fibonnaci series between 1 and 100 in python.The code should be perfectly deployable along \
                                        with everything added related to CORS middleware. Only and only provide the code, no unnecessary\
                                        text or explanations around it.")
    
    assistant_response = asyncio.run(code_generator.assistant_run())

    parsed_response = json.loads(assistant_response.chat_message.content)
    code_content = parsed_response["content"]

    cleaned_code = code_content.replace("```", "").replace("python", "")

    with open("sample/code_buggy.py", "w") as code_file:
        code_file.write(cleaned_code)
