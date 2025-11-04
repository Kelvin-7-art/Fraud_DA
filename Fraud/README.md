# Credit Card Fraud Detection System

A professional Streamlit application for credit card fraud detection using machine learning.

## Features

- Multiple machine learning models:
  - Random Forest
  - Support Vector Machine (SVM)
  - Logistic Regression
  - Neural Network
- Comprehensive performance metrics
- Interactive data visualizations
- Transaction fraud predictor
- Modern, professional UI

## Project Structure

```
├── assets/            # Static assets (images, etc.)
├── data/              # Data files
│   └── creditcard.csv # Credit card transaction dataset
├── models/            # Saved models
│   ├── isolation_forest_model.pkl
│   └── scaler.pkl
├── notebooks/         # Jupyter notebooks
├── src/               # Source code
│   ├── components/    # UI components
│   ├── pages/         # Application pages
│   └── utils/         # Utility functions
└── app.py             # Main application file
```

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
streamlit run app.py
```

## Data

The application uses a credit card transaction dataset with the following features:
- Time: Seconds elapsed between each transaction and the first transaction
- Amount: Transaction amount
- V1-V28: PCA-transformed features for privacy
- Class: 1 for fraudulent transactions, 0 for legitimate ones

## Usage

1. Navigate to the "Fraud Detection" page to train and evaluate models
2. Use the "Transaction Predictor" to test individual transactions
3. Check the "About" page for more information

## Dependencies

- streamlit
- pandas
- numpy
- matplotlib
- plotly
- scikit-learn
- tensorflow
- joblib
- streamlit-option-menu
- Pillow