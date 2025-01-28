import os
import yaml
from distutils.util import strtobool

from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_core import CancellationToken
from autogen_core.models import UserMessage
from autogen_core.code_executor import CodeBlock
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

from coding_agent import CodeGenratingAgent

import warnings
warnings.filterwarnings("ignore")


from dotenv import load_dotenv

load_dotenv(override=True)

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
        refactored_code = asyncio.run(code_generator.refactor_code(buggy_code_file_path))

        fixed_code_block = qa_tester.read_code("code_refactor/code_refactored.py")
        fixed_executed_code = asyncio.run(qa_tester.qa_tester("code_refactor/code_refactored.py"))

        return fixed_executed_code.output
    
    
if __name__ == "__main__":
    import asyncio
    import json

    qa_tester = QATester()
    
    executed_code = asyncio.run(qa_tester.qa_tester("sample/code_buggy.py"))
    
    output_verification = asyncio.run(qa_tester.code_assesment_agent(executed_code))
    output_verification = bool(strtobool(output_verification.content))
    
    if not output_verification:
        print("Uhoh! Code execution failed. Fixing the code...")
        fixed_executed_code = qa_tester.code_fixer("sample/code_buggy.py")
        print("Code is now fixed and running fine 🥳")    
    else:
        print("Code is working fine 🥳")
        