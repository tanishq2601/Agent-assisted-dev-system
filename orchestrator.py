import uuid
import asyncio
import json
from distutils.util import strtobool

from helper import write_code_to_path, create_project_zip
from coding_agent.coding_agent import CodeGenratingAgent
from qa_tester.qa_tester import QATester
from deployment_agent.deployment_agent import DeploymentAgent


from dotenv import load_dotenv

load_dotenv(override=True)

def code(user_query: str, folder_path: str, file_name: str):
    code_generator = CodeGenratingAgent(user_query)
    
    assistant_response = asyncio.run(code_generator.assistant_run())

    parsed_response = json.loads(assistant_response.chat_message.content)
    code_content = parsed_response["content"]

    cleaned_code = code_content.replace("```", "").replace("python", "")

    write_code_to_path(folder_path, file_name, cleaned_code)

    return f"{folder_path}/{file_name}.py"

def test(code_path: str):
    qa_tester = QATester()

    executed_code = asyncio.run(qa_tester.qa_tester(code_path))
    
    output_verification = asyncio.run(qa_tester.code_assesment_agent(executed_code))
    output_verification = bool(strtobool(output_verification.content))

    return output_verification

def deploy(folder_path):
    deployment_agent = DeploymentAgent()

    print(f"file path to be 🤐 : {folder_path}")
    create_project_zip(folder_path)
    asyncio.run(deployment_agent.deploy_code(f"{folder_path}.zip"))


# driver function
def orchestrate(user_query: str):
    folder_path = "sample"
    file_name = "test_sample"

    qa_tester = QATester()
    code_path = code(user_query, folder_path, file_name)

    verification_status = test(code_path)

    if not verification_status:
        print("Uhoh! Code execution failed. Fixing the code...")
        fixed_executed_code, code_path = qa_tester.code_fixer(f"{folder_path}/{file_name}.py")
        print("Code is now fixed and running fine 🥳")    
    else:
        print("Code is working fine 🥳")
    
    zip_folder = code_path.split("/")[0]
    deploy(zip_folder)    


if __name__ == "__main__":
    orchestrate("Build a fastapi to print the fibonacci series from 1 to 100.")