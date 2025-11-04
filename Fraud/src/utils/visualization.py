import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from sklearn.metrics import (
    confusion_matrix, ConfusionMatrixDisplay,
    RocCurveDisplay, PrecisionRecallDisplay
)

# Plotting functions for metrics
def st_plot_confusion(cm, labels):
    """Create and display a confusion matrix plot in Streamlit"""
    fig, ax = plt.subplots(figsize=(5, 5))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(ax=ax, cmap=plt.cm.Blues, values_format='d')
    plt.title("Confusion Matrix", fontsize=14)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

def st_plot_roc_from_estimator(estimator, x_test, y_test):
    """Create and display a ROC curve from an estimator in Streamlit"""
    fig, ax = plt.subplots(figsize=(6, 5))
    RocCurveDisplay.from_estimator(estimator, x_test, y_test, ax=ax)
    plt.title("ROC Curve", fontsize=14)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

def st_plot_pr_from_estimator(estimator, x_test, y_test):
    """Create and display a Precision-Recall curve from an estimator in Streamlit"""
    fig, ax = plt.subplots(figsize=(6, 5))
    PrecisionRecallDisplay.from_estimator(estimator, x_test, y_test, ax=ax)
    plt.title("Precision-Recall Curve", fontsize=14)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

def st_plot_roc_from_predictions(y_test, y_score):
    """Create and display a ROC curve from prediction scores in Streamlit"""
    fig, ax = plt.subplots(figsize=(6, 5))
    RocCurveDisplay.from_predictions(y_test, y_score, ax=ax)
    plt.title("ROC Curve", fontsize=14)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

def st_plot_pr_from_predictions(y_test, y_score):
    """Create and display a Precision-Recall curve from prediction scores in Streamlit"""
    fig, ax = plt.subplots(figsize=(6, 5))
    PrecisionRecallDisplay.from_predictions(y_test, y_score, ax=ax)
    plt.title("Precision-Recall Curve", fontsize=14)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# Consolidated plotting function for metrics
def plot_metrics(metrics_list, model, x_test, y_test, y_score=None, class_names=["Legitimate", "Fraudulent"], is_nn=False):
    """
    Display selected metrics in Streamlit.
    
    Parameters:
        metrics_list (list): List of metric names to display
        model: Trained model
        x_test: Test features
        y_test: Test labels
        y_score: Prediction scores (required for neural networks)
        class_names: Labels for classes
        is_nn (bool): Whether the model is a neural network
    """
    if "Confusion Matrix" in metrics_list:
        predictions = model.predict(x_test) if not is_nn else (y_score > 0.5).astype(int)
        cm = confusion_matrix(y_test, predictions)
        st.subheader("Confusion Matrix")
        st_plot_confusion(cm, class_names)

    if "ROC Curve" in metrics_list:
        st.subheader("ROC Curve")
        if is_nn:
            st_plot_roc_from_predictions(y_test, y_score)
        else:
            st_plot_roc_from_estimator(model, x_test, y_test)

    if "Precision-Recall Curve" in metrics_list:
        st.subheader("Precision-Recall Curve")
        if is_nn:
            st_plot_pr_from_predictions(y_test, y_score)
        else:
            st_plot_pr_from_estimator(model, x_test, y_test)

# Feature visualization functions
def create_feature_distribution_plot(df, feature):
    """Create a histogram showing feature distribution by class"""
    fig = px.histogram(
        df,
        x=feature,
        color='Class',
        barmode='overlay',
        title=f'Feature Distribution: {feature}',
        width=700,
        height=400,
        color_discrete_map={0: "#4CAF50", 1: "#F44336"},
        labels={'Class': 'Transaction Type', 0: 'Legitimate', 1: 'Fraudulent'},
        opacity=0.7,
        template='plotly_white'
    )
    fig.update_layout(
        legend=dict(
            title="Transaction Type",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis_title=feature,
        yaxis_title="Count"
    )
    return fig

def create_feature_boxplot(df, feature):
    """Create a boxplot showing feature distribution by class"""
    df_plot = df.copy()
    df_plot['Class_Label'] = df_plot['Class'].map({0: 'Legitimate', 1: 'Fraudulent'})
    
    fig = px.box(
        df_plot,
        x="Class_Label",
        y=feature,
        color="Class_Label",
        points="outliers",
        title=f'Boxplot: {feature} by Transaction Type',
        width=700,
        height=400,
        color_discrete_map={'Legitimate': "#4CAF50", 'Fraudulent': "#F44336"},
        template='plotly_white'
    )
    fig.update_layout(
        showlegend=False,
        xaxis_title="Transaction Type",
        yaxis_title=feature
    )
    return fig

def create_scatterplot(df, x_feature, y_feature, title):
    """Create a scatterplot of two features colored by class"""
    df_plot = df.copy()
    df_plot['Class_Label'] = df_plot['Class'].map({0: 'Legitimate', 1: 'Fraudulent'})
    
    # Update title if it contains "Amount" but not already "R"
    if "Amount" in title and "R" not in title:
        title = title.replace("Amount", "Amount (R)")
    
    fig = px.scatter(
        df_plot,
        x=x_feature,
        y=y_feature,
        color="Class_Label",
        title=title,
        width=700,
        height=500,
        color_discrete_map={'Legitimate': "#4CAF50", 'Fraudulent': "#F44336"},
        opacity=0.7,
        template='plotly_white'
    )
    fig.update_layout(
        legend=dict(
            title="Transaction Type",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis_title=x_feature,
        yaxis_title=y_feature
    )
    return fig