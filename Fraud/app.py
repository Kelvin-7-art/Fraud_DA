# app.py — main entry for Streamlit, resilient loaders + styled UI

import os
import sys
import runpy
import importlib
import importlib.util
from pathlib import Path
import streamlit as st

# ---------- Optional menu dependency with fallback ----------
try:
    from streamlit_option_menu import option_menu as _option_menu
    def sidebar_menu(**kwargs):
        return _option_menu(**kwargs)
    HAS_MENU = True
except Exception:
    HAS_MENU = False
    def sidebar_menu(menu_title=None, options=(), icons=None, menu_icon=None, default_index=0, styles=None):
        return st.sidebar.radio(menu_title or "Menu", options, index=default_index)

# ---------- Safe imports for first-party pages (welcome/about) ----------
def _safe_import_attr(mod_name, attr_name, fallback=None):
    try:
        mod = importlib.import_module(mod_name)
        fn = getattr(mod, attr_name, None)
        if callable(fn):
            return fn
    except ModuleNotFoundError:
        pass
    except Exception as e:
        st.sidebar.warning(f"Issue importing {mod_name}.{attr_name}: {e}")
    return fallback

show_welcome_page = _safe_import_attr("src.pages.welcome", "show_welcome_page", lambda: st.markdown("## Welcome"))
show_about_page   = _safe_import_attr("src.pages.about",   "show_about_page",   lambda: st.markdown("## About"))

# Utilities (best-effort; don't crash the app if copy fails)
copy_models = _safe_import_attr("src.utils.copy_models", "copy_models", lambda: None)
copy_external_notebook = _safe_import_attr("src.utils.copy_notebook", "copy_external_notebook", lambda: None)

# ---------- Ensure project root on sys.path ----------
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

# ---------- One-time asset copy (best effort) ----------
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

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0F2041; padding-top: 1rem;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
    }
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] li { color: #FFFFFF !important; }

    /* Progress bar */
    .stProgress > div > div > div > div { background-color: #1E3A8A; }
    </style>
    """, unsafe_allow_html=True)

# ---------- Robust lazy runner ----------
def _lazy_run(module_name: str, func_candidates=None, file_candidates=None):
    """
    Try to call a function from a module; otherwise execute a script file.
    """
    if func_candidates is None:
        func_candidates = ("transaction_predictor", "fraud_detection_app2",
                           "main", "run", "app", "render", "show")

    # 1) Try importing the module
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

    # 2) Fall back to known script file paths
    if file_candidates is None:
        file_candidates = [
            # Transaction Predictor
            ROOT / "src" / "pages" / "03_Transaction_Predictor.py",
            ROOT / "pages" / "03_Transaction_Predictor.py",
            ROOT / "03_Transaction_Predictor.py",
            ROOT / "src" / "pages" / "transaction_predictor.py",
            ROOT / "pages" / "transaction_predictor.py",

            # Fraud Detection App2 (RAW/PCA)
            ROOT / "src" / "pages" / "fraud_detection_app2.py",
            ROOT / "src" / "pages" / "Fraud_Detection_App2.py",
            ROOT / "pages" / "fraud_detection_app2.py",
            ROOT / "pages" / "Fraud_Detection_App2.py",
            ROOT / "fraud_detection_app2.py",
            ROOT / "Fraud_Detection_App2.py",

            # Legacy Fraud Detection
            ROOT / "src" / "pages" / "fraud_detection.py",
            ROOT / "pages" / "fraud_detection.py",
            ROOT / "fraud_detection.py",
        ]

    for path in file_candidates:
        path = Path(path)
        if path.exists():
            try:
                runpy.run_path(str(path), run_name="__main__")
                return
            except Exception as e:
                st.error(f"Failed to execute {path.name}: {e}")

    st.error(
        "Could not find a runnable target.\n\n"
        "Expected one of these:\n"
        "• Module `src.pages.transaction_predictor` or script `03_Transaction_Predictor.py`\n"
        "• Module `src.pages.fraud_detection_app2` or script `fraud_detection_app2.py`\n"
        "• (Optional legacy) `src.pages.fraud_detection`"
    )

# ---------- Page renderers ----------
def render_transaction_predictor():
    _lazy_run("src.pages.transaction_predictor")

def render_fraud_detection_app2():
    # Try lower/upper module names, then fallbacks handled inside _lazy_run
    try:
        _lazy_run("src.pages.fraud_detection_app2",
                  func_candidates=("fraud_detection_app2", "main", "run", "app", "render", "show"))
    except Exception:
        _lazy_run("src.pages.Fraud_Detection_App2",
                  func_candidates=("fraud_detection_app2", "main", "run", "app", "render", "show"))

def render_fraud_detection_legacy():
    _lazy_run("src.pages.fraud_detection",
              func_candidates=("fraud_detection_app", "main", "run", "app", "render", "show"))

# ---------- Presence probes (to hide missing menu items) ----------
def _exists_any(paths):
    for p in paths:
        if Path(p).exists():
            return True
    return False

HAS_TX_PRED = (
    importlib.util.find_spec("src.pages.transaction_predictor") is not None
) or _exists_any([
    ROOT / "src/pages/03_Transaction_Predictor.py",
    ROOT / "pages/03_Transaction_Predictor.py",
    ROOT / "03_Transaction_Predictor.py",
    ROOT / "src/pages/transaction_predictor.py",
    ROOT / "pages/transaction_predictor.py",
])

HAS_APP2 = (
    importlib.util.find_spec("src.pages.fraud_detection_app2") is not None
    or importlib.util.find_spec("src.pages.Fraud_Detection_App2") is not None
) or _exists_any([
    ROOT / "src/pages/fraud_detection_app2.py",
    ROOT / "src/pages/Fraud_Detection_App2.py",
    ROOT / "pages/fraud_detection_app2.py",
    ROOT / "pages/Fraud_Detection_App2.py",
    ROOT / "fraud_detection_app2.py",
    ROOT / "Fraud_Detection_App2.py",
])

HAS_LEGACY = (
    importlib.util.find_spec("src.pages.fraud_detection") is not None
) or _exists_any([
    ROOT / "src/pages/fraud_detection.py",
    ROOT / "pages/fraud_detection.py",
    ROOT / "fraud_detection.py",
])

# ---------- Main ----------
def main():
    try:
        st.set_page_config(page_title="Fraud Detection", page_icon="🛡️", layout="wide")
    except Exception:
        pass

    apply_custom_style()

    # Sidebar brand header
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #FFFFFF; margin-bottom: 0;">Fraud</h2>
            <h2 style="color: #D4AF37; margin-top: 0;">Detection</h2>
            <div style="width: 50px; height: 3px; background: linear-gradient(90deg, #D4AF37, #FFFFFF); margin: 10px auto;"></div>
        </div>
        """, unsafe_allow_html=True)

        # Build menu options dynamically so we don't show dead entries
        options = ["Home"]
        icons   = ["house-fill"]

        if HAS_LEGACY:
            options.append("Fraud Detection")
            icons.append("bar-chart-line-fill")

        if HAS_APP2:
            options.append("Fraud Detection (RAW/PCA)")
            icons.append("graph-up")

        if HAS_TX_PRED:
            options.append("Transaction Predictor")
            icons.append("calculator-fill")

        options.append("About")
        icons.append("info-circle-fill")

        choice = sidebar_menu(
            menu_title=None,
            options=options,
            icons=icons if HAS_MENU else None,
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
            } if HAS_MENU else None,
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
    elif choice == "Fraud Detection" and HAS_LEGACY:
        render_fraud_detection_legacy()
    elif choice == "Fraud Detection (RAW/PCA)" and HAS_APP2:
        render_fraud_detection_app2()
    elif choice == "Transaction Predictor" and HAS_TX_PRED:
        render_transaction_predictor()
    elif choice == "About":
        show_about_page()
    else:
        st.info("This page isn’t available yet.")

if __name__ == "__main__":
    main()
