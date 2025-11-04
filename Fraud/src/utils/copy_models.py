import os
import shutil
import joblib

def copy_models():
    """
    Copy model files from external location to the project's models directory.
    This helps ensure the models are available in the expected location.
    """
    # Source and destination paths - using raw strings for Windows paths
    source_model = r"C:\Users\HP\Downloads\New folder 1\New folder\model.pkl"
    source_scaler = r"C:\Users\HP\Downloads\New folder 1\New folder\Scaler.pkl"
    
    dest_model = "models/model.pkl"
    dest_scaler = "models/scaler.pkl"
    
    # Create the models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)
    
    # Copy the files
    try:
        if os.path.exists(source_model):
            shutil.copy(source_model, dest_model)
            print(f"Copied model from {source_model} to {dest_model}")
        else:
            print(f"Source model file not found: {source_model}")
            
        if os.path.exists(source_scaler):
            shutil.copy(source_scaler, dest_scaler)
            print(f"Copied scaler from {source_scaler} to {dest_scaler}")
        else:
            print(f"Source scaler file not found: {source_scaler}")
    except Exception as e:
        print(f"Error copying model files: {str(e)}")

if __name__ == "__main__":
    copy_models()