import pandas as pd
from sklearn.preprocessing import LabelEncoder
import streamlit as st

@st.cache_data(persist=True)
def load_data(file_path):
    """
    Load CSV data and encode object columns to numeric.
    
    Parameters:
        file_path (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: Preprocessed dataframe.
    """
    try:
        data = pd.read_csv(file_path)
        
        # Encode categorical object columns if any
        labelencoder = LabelEncoder()
        for col in data.select_dtypes(include=['object']).columns:
            data[col] = labelencoder.fit_transform(data[col])
        
        return data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        raise