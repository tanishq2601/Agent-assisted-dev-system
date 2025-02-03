import os
import yaml
from distutils.util import strtobool
import asyncio

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


class QATester:
    def __init__(self):
        self.code_assessment_agent_prompt = prompts["CODE_ASSESSMENT_AGENT"]["prompt"]
        self.work_dir = "execution_sample"
        if not os.path.exists(self.work_dir):
            os.makedirs(self.work_dir, exist_ok=True)
        self.model_client = AzureOpenAIChatCompletionClient(
            azure_deployment="gpt-4o",
            azure_endpoint=os.getenv("AZURE_API_BASE"),
            model="gpt-4o",
            api_version="2024-08-01-preview",
            api_key=os.getenv("AZURE_API_KEY"),
        )
        self.code_executor = LocalCommandLineCodeExecutor(work_dir=self.work_dir)
    
    def read_code(self, file_path):
        with open(file_path, "r") as f:
            code = f.read()
        return code
    
    async def code_assesment_agent(self, code_string):
        output_verification = await self.model_client.create([UserMessage(content=self.code_assessment_agent_prompt.format(code_string=code_string), source="user")])
        return output_verification
    
    async def qa_tester(self, code_file_path):
        code_string = self.read_code(code_file_path)
        result = await self.code_executor.execute_code_blocks(
            code_blocks=[
                CodeBlock(language="python", code=code_string),
            ],
            cancellation_token=CancellationToken(),
        )
        return result
    
    def code_fixer(self, buggy_code_file_path):
        code_generator = CodeGenratingAgent("Fix the bug in this code and provide me the correct code.")
        refactored_code, new_code_path = asyncio.run(code_generator.refactor_code(buggy_code_file_path))

        fixed_code_block = self.read_code(new_code_path)
        fixed_executed_code = asyncio.run(self.qa_tester(new_code_path))

        return fixed_executed_code.output, new_code_path
    
        