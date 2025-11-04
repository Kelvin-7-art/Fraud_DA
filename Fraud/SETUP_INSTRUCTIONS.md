# Fraud Detection Application - Setup Instructions

## Overview

The original single-file Streamlit application has been refactored into a well-organized project with the following improvements:

1. **Modular Structure**:
   - Separated code into logical modules under src/
   - Organized pages, components, and utilities
   - Improved maintainability and readability

2. **Enhanced UI**:
   - Professional color scheme and styling
   - Responsive layout with better spacing
   - Card-based content presentation
   - Improved navigation with dedicated pages

3. **Feature Enhancements**:
   - Better visualizations
   - More intuitive controls
   - Improved error handling
   - Organized input sections

## Running the Application

1. Make sure you have all dependencies installed:
   ```
   pip install -r requirements.txt
   ```

2. Run the application using:
   ```
   streamlit run app.py
   ```
   
   Or simply double-click the `run_app.bat` file.

## Project Structure

```
Fraud Detection/
├── app.py                  # Main application entry point
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
├── run_app.bat             # Windows batch file to run the app
├── assets/                 # Static assets
│   └── banner.jpg          # Welcome page banner image
├── data/                   # Data files
│   └── creditcard.csv      # Credit card transaction dataset
├── models/                 # Saved machine learning models
│   ├── isolation_forest_model.pkl  # Isolation Forest model for transaction prediction
│   └── scaler.pkl          # Standard scaler for feature normalization
├── notebooks/              # Jupyter notebooks
│   └── Detecting Credit Card Fraud.ipynb  # Analysis notebook
└── src/                    # Source code
    ├── components/         # Reusable UI components
    ├── pages/              # Application pages
    │   ├── about.py        # About page
    │   ├── fraud_detection.py  # Model training page
    │   ├── transaction_predictor.py  # Prediction page
    │   └── welcome.py      # Home page
    └── utils/              # Utility functions
        ├── banner_generator.py  # Script to generate banner image
        ├── create_scaler.py     # Script to create feature scaler
        ├── data_loader.py       # Data loading utilities
        └── visualization.py     # Plotting and visualization functions
```

## Key Improvements

1. **Code Organization**:
   - Separated different pages into individual modules
   - Created utility functions for common operations
   - Improved code readability and maintainability

2. **UI Enhancements**:
   - Professional color scheme using blue tones
   - Card-based layout for better content organization
   - Improved navigation with intuitive sidebar menu
   - Better spacing and typography

3. **Functionality Improvements**:
   - Enhanced error handling
   - Better progress indicators during model training
   - More intuitive parameter controls
   - Improved data visualization options

The refactored application preserves all the original functionality while providing a more professional and user-friendly experience.