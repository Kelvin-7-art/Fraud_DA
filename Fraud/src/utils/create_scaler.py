import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib

# This script creates a scaler for the transaction predictor
# It should be run once to create the scaler.pkl file

def create_scaler(data_path, output_path):
    """Create a StandardScaler and save it to a file"""
    try:
        # Load the credit card data
        data = pd.read_csv(data_path)
        
        # Get features (all columns except Class)
        features = data.drop(columns=['Class'])
        
        # Create and fit the scaler
        scaler = StandardScaler()
        scaler.fit(features)
        
        # Save the scaler
        joblib.dump(scaler, output_path)
        print(f"Scaler saved to {output_path}")
        
    except Exception as e:
        print(f"Error creating scaler: {str(e)}")

if __name__ == "__main__":
    # Define paths
    data_path = "../data/creditcard.csv"
    output_path = "../models/scaler.pkl"
    
    # Create and save the scaler
    create_scaler(data_path, output_path)