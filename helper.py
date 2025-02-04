"""
Helper Module

This module provides utility functions for file operations and code management.
It handles common tasks such as writing code to files and creating deployment packages.

Author: AI Vectorial
Date: 2025-02-04
"""

import os
import shutil

def create_project_zip(code_file_path):
    """
    Creates a ZIP archive of a project directory.

    Useful for preparing code for deployment to cloud services.

    Args:
        code_file_path (str): Path to the directory to zip

    Returns:
        bool: True if ZIP creation successful
    """
    if not os.path.exists(code_file_path):  # Check the actual folder existence
        print(f"The directory {code_file_path} does not exist.")
    
    zip_path = f"{code_file_path}.zip"
    
    print(f"Creating zip file from {code_file_path}...")
    shutil.make_archive(code_file_path, 'zip', code_file_path)  # Create ZIP archive
    print(f"Zip file created successfully: {zip_path}")
    
    return True

def write_code_to_path(folder_path, file_name, content):
    """
    Writes code content to a specified file path.

    Creates the target directory if it doesn't exist and writes
    the code content to a Python file.

    Args:
        folder_path (str): Directory path where the file will be created
        file_name (str): Name of the file (without extension)
        content (str): Code content to write

    Returns:
        str: Message confirming the file creation with path
    """
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    with open(f"{folder_path}/{file_name}.py", "w") as file:
        file.write(content)
    
    return f"Code added to path {folder_path}/{file_name}.py"