import os
import sys
import runpy
import importlib
import streamlit as st
from streamlit_option_menu import option_menu

# Pages that are safe to import directly (they expose clear functions)
from src.pages.welcome import show_welcome_page
#from src.pages.fraud_detection import fraud_detection_app
from src.pages.about import show_about_page

# Utilities (best-effort; don't crash the app if copy fails)
from src.utils.copy_models import copy_models
from src.utils.copy_notebook import copy_external_notebook

# Ensure project root on sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Copy static assets (best-effort)
try:
    copy_models()
except Exception as e:
    st.sidebar.warning(f"Model copy skipped: {e}")
try:
    copy_external_notebook()
except Exception as e:
    st.sidebar.warning(f"Notebook sync skipped: {e}")


# ---------- Styling ----------
def apply_custom_style():
    st.markdown("""
    <style>
    /* Fix for container issues */
    .element-container { margin: 0 !important; padding: 0 !important; }
    div[data-testid="stElementContainer"] { margin: 0 !important; padding: 0 !important; }
    .stMarkdown div[data-testid="stMarkdownContainer"] { margin: 0 !important; padding: 0 !important; }

    /* Ensure dropdowns are on top */
    div.stSelectbox > div[data-baseweb="select"] > div { z-index: 999 !important; }
    div.stMultiSelect > div[data-baseweb="select"] > div { z-index: 999 !important; }
    [data-testid="stSidebar"] .stSelectbox, 
    [data-testid="stSidebar"] .stMultiSelect { z-index: 999 !important; }

    /* Main app container */
    .stApp { max-width: 1200px; margin: 0 auto; background-color: #FAFAFA; }

    /* Main content area */
    .main .block-container {
        padding: 2.5rem; border-radius: 10px; background-color: #FFFFFF;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }

    /* Typography */
    h1 { color: #0F2041; font-weight: 700; font-size: 2.5rem; margin-bottom: 1.5rem;
         padding-bottom: 0.5rem; border-bottom: 2px solid #E5E7EB; }
    h2 { color: #1E3A8A; font-weight: 600; margin-top: 1.5rem; }
    h3 { color: #2C4A9A; font-weight: 600; }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #2C4A9A 0%, #1E3A8A 100%);
        color: white; border-radius: 6px; padding: 0.6rem 1.2rem; border: none; font-weight: 600;
        box-shadow: 0 4px 6px rgba(30,58,138,0.3); transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #3B5BC0 0%, #2C4A9A 100%);
        box-shadow: 0 6px 10px rgba(30,58,138,0.4); transform: translateY(-1px);
    }

    /* Inputs & selects */
    .stSelectbox label, .stSlider label, .stNumberInput label { color: #1E3A8A; font-weight: 500; }
    div[data-baseweb="select"] > div { background-color: white; border-radius: 6px; border: 1px solid #E5E7EB; }
    div[data-baseweb="select"] > div:hover { border: 1px solid #1E3A8A; }

    /* Section containers */
    .css-1r6slb0, .css-12oz5g7 {
        padding: 2rem; border-radius: 8px; background-color: #FFFFFF; border: 1px solid #F3F4F6;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }

    /* Expanders */
    .streamlit-expanderHeader { font-weight: 600; color: #1E3A8A; }

    /* Metric elements */
    .css-1xarl3l {
        background-color: #F8FAFC; padding: 1.5rem; border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03); border-left: 4px solid #1E3A8A;
    }

    /* Dataframes */
    .stDataFrame { border-radius: 8px; overflow: hidden; border: 1px solid #E5E7EB; }
    .stDataFrame [data-testid="stTable"] { border: none; }

    /* Tabs */
    button[role="tab"] {
        background-color: transparent; color: #6B7280; border-radius: 0;
        border-bottom: 2px solid #E5E7EB; padding: 0.75rem 1.25rem; font-weight: 500;
    }
    button[role="tab"][aria-selected="true"] {
        color: #1E3A8A; border-bottom-color: #1E3A8A; font-weight: 600;
    }
    div[role="tabpanel"] { padding: 1.5rem 0; }

    /* Checkbox */
    .stCheckbox label span { color: #1E3A8A; font-weight: 500; }

    /* Progress bar */
    .stProgress > div > div > div > div { background-color: #1E3A8A; }
    </style>
    """, unsafe_allow_html=True)


# ---------- Robust lazy loader ----------
def _lazy_run(module_name: str, func_candidates=None, file_candidates=None):
    """
    Try to run a callable from a module; if not found, execute a script file.
    """
    if func_candidates is None:
        func_candidates = ("transaction_predictor", "fraud_detection_app2",
                           "main", "run", "app", "render", "show")

    # 1) Try importing the module and calling a known function
    try:
        mod = importlib.import_module(module_name)
        for fname in func_candidates:
            fn = getattr(mod, fname, None)
            if callable(fn):
                return fn()
    except ModuleNotFoundError:
        pass
    except Exception as e:
        st.warning(f"Issue importing {module_name}: {e}")

    # 2) Fall back to executing a script file
    if file_candidates is None:
        root = os.path.dirname(os.path.abspath(__file__))
        file_candidates = [
            # Transaction Predictor script candidates
            os.path.join(root, "src", "pages", "03_Transaction_Predictor.py"),
            os.path.join(root, "pages", "03_Transaction_Predictor.py"),
            os.path.join(root, "03_Transaction_Predictor.py"),
            # Fraud Detection App2 script candidates
            os.path.join(root, "src", "pages", "fraud_detection_app2.py"),
            os.path.join(root, "src", "pages", "Fraud_Detection_App2.py"),
            os.path.join(root, "pages", "fraud_detection_app2.py"),
            os.path.join(root, "pages", "Fraud_Detection_App2.py"),
            os.path.join(root, "fraud_detection_app2.py"),
            os.path.join(root, "Fraud_Detection_App2.py"),
        ]

    for path in file_candidates:
        if os.path.exists(path):
            try:
                runpy.run_path(path, run_name="__main__")
                return
            except Exception as e:
                st.error(f"Failed to execute {os.path.basename(path)}: {e}")

    st.error(
        "Could not find a runnable target.\n\n"
        "Ensure one of these exists with a callable function:\n"
        "• `src/pages/transaction_predictor.py` (transaction_predictor/main/run/...)\n"
        "• `src/pages/fraud_detection_app2.py` (fraud_detection_app2/main/run/...)\n"
        "Or provide the scripts `03_Transaction_Predictor.py` / `fraud_detection_app2.py`."
    )


def render_transaction_predictor():
    # Prefer module; fall back to script
    # Try both common module names for safety
    _lazy_run("src.pages.transaction_predictor")


def render_fraud_detection_app2():
    # Try lower/upper module names, then script fallbacks
    try:
        _lazy_run("src.pages.fraud_detection_app2",
                  func_candidates=("fraud_detection_app2", "main", "run", "app", "render", "show"))
    except Exception:
        _lazy_run("src.pages.Fraud_Detection_App2",
                  func_candidates=("fraud_detection_app2", "main", "run", "app", "render", "show"))


# ---------- Main ----------
def main():
    apply_custom_style()

    # Sidebar menu
    with st.sidebar:
        st.markdown("""
        <style>
        .element-container, div[data-testid="stElementContainer"], 
        .stMarkdown div[data-testid="stMarkdownContainer"] { margin: 0 !important; padding: 0 !important; }

        [data-testid="stSidebar"] {
            background-color: #0F2041; padding-top: 1rem;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
        }
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1.5rem; padding-left: 1.5rem; padding-right: 1.5rem;
        }
        </style>
        """, unsafe_allow_html=True)

        # Logo / brand
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #FFFFFF; margin-bottom: 0;">Fraud</h2>
            <h2 style="color: #D4AF37; margin-top: 0;">Detection</h2>
            <div style="width: 50px; height: 3px; background: linear-gradient(90deg, #D4AF37, #FFFFFF); margin: 10px auto;"></div>
        </div>
        """, unsafe_allow_html=True)

        choice = option_menu(
            menu_title=None,
            options=[
                "Home",
                "Fraud Detection",
                "Fraud Detection (RAW/PCA)",   # <-- Added App2 entry
                "Transaction Predictor",
                "About"
            ],
            icons=["house-fill", "bar-chart-line-fill", "graph-up", "calculator-fill", "info-circle-fill"],
            menu_icon="menu-button-wide",
            default_index=0,
            styles={
                "container": {
                    "padding": "10px",
                    "background-color": "#0F2041",
                    "border-radius": "10px",
                    "margin-top": "10px",
                },
                "icon": {"color": "#D4AF37", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "8px 0",
                    "border-radius": "7px",
                    "color": "#FFFFFF",
                    "font-weight": "500",
                    "padding": "12px 15px",
                },
                "nav-link-selected": {
                    "background": "linear-gradient(90deg, rgba(212, 175, 55, 0.2) 0%, rgba(212, 175, 55, 0) 100%)",
                    "color": "#D4AF37",
                    "border-left": "3px solid #D4AF37",
                    "font-weight": "600",
                },
            },
        )

        # Sidebar footer
        st.markdown("""
        <div style="position: fixed; bottom: 20px; left: 20px; right: 20px; text-align: center;">
            <div style="width: 30px; height: 1px; background: #3B4B72; margin: 10px auto;"></div>
            <p style="color: #8896BF; font-size: 12px; margin-bottom: 5px;">Advanced Analytics</p>
            <p style="color: #8896BF; font-size: 10px;">© 2025</p>
        </div>
        """, unsafe_allow_html=True)

    # Router
    if choice == "Home":
        show_welcome_page()

    elif choice == "Fraud Detection (RAW/PCA)":
        render_fraud_detection_app2()
    elif choice == "Transaction Predictor":
        render_transaction_predictor()
    elif choice == "About":
        show_about_page()


if __name__ == "__main__":
    main()
