import os
import shutil

def create_project_zip(code_file_path):
    if not os.path.exists(code_file_path):  # Check the actual folder existence
        print(f"The directory {code_file_path} does not exist.")
    
    zip_path = f"{code_file_path}.zip"
    
    print(f"Creating zip file from {code_file_path}...")
    shutil.make_archive(code_file_path, 'zip', code_file_path)  # Create ZIP archive
    print(f"Zip file created successfully: {zip_path}")
    
    return True

def write_code_to_path(folder_path, file_name, content):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    with open(f"{folder_path}/{file_name}.py", "w") as file:
        file.write(content)
    
    return f"Code added to path {folder_path}/{file_name}.py"