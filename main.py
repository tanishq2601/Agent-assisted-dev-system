import os
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_core.models import UserMessage
from autogen_agentchat.agents import AssistantAgent

import warnings
warnings.filterwarnings("ignore")


from dotenv import load_dotenv

load_dotenv(override=True)


class CodeGenratingAgent:
    def __init__(self, user_query=None):
        self.user_query = user_query
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


if __name__ == "__main__":
    import asyncio
    import json

    code_generator = CodeGenratingAgent("Write code to print fibonnaci series between 1 and 100. Only and only provide the code, no unnecessary\
                          text or explanations around it.")
    
    assistant_response = asyncio.run(code_generator.assistant_run())

    parsed_response = json.loads(assistant_response.chat_message.content)
    code_content = parsed_response["content"]

    cleaned_code = code_content.replace("```", "").replace("python", "")

    with open("sample/code.py", "w") as code_file:
        code_file.write(cleaned_code)
