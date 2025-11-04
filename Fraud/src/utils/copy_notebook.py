"""
Utility to ensure the correct version of the notebook is used in the project.
This copies the external notebook "Copy of Detecting Credit Card Fraud.ipynb" 
from Downloads to the project's notebooks directory.
"""

import os
import shutil

def copy_external_notebook():
    """
    Copy the external notebook to the project's notebooks directory.
    """
    external_notebook = r"C:\Users\HP\Downloads\Copy of Detecting Credit Card Fraud.ipynb"
    project_notebook = r"notebooks/Detecting Credit Card Fraud.ipynb"
    
    # Create notebooks directory if it doesn't exist
    os.makedirs("notebooks", exist_ok=True)
    
    # Copy the external notebook to the project
    try:
        if os.path.exists(external_notebook):
            shutil.copy(external_notebook, project_notebook)
            print(f"Copied notebook from {external_notebook} to {project_notebook}")
            return True
        else:
            print(f"External notebook not found: {external_notebook}")
            return False
    except Exception as e:
        print(f"Error copying notebook file: {str(e)}")
        return False

if __name__ == "__main__":
    copy_external_notebook()