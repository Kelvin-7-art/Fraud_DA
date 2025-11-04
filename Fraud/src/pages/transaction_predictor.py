# pages/03_Transaction_Predictor.py
# RAW/PCA predictor with slider toggle + unified fraud score
# Now auto-restricts RAW "type" to categories learned by the loaded pipeline.
# Robust path resolution + file-uploader fallback to avoid [Errno 2].

from pathlib import Path
from typing import List, Optional, Union
import io
import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st

# ---- shim for old sklearn pickles that reference a private class ----
try:
    from sklearn.compose import _column_transformer as _ct
    class _RemainderColsList(list): ...
    if not hasattr(_ct, "_RemainderColsList"):
        _ct._RemainderColsList = _RemainderColsList
except Exception:
    pass
# ---------------------------------------------------------------------


# ---------- Robust path resolution helpers ----------
def _resolve_any(rel_path: str) -> Optional[str]:
    """
    Try to find a relative path across common project roots.
    Returns absolute string path if found, else None.
    """
    here = Path(__file__).resolve()
    candidates_roots = [
        here.parents[2] if len(here.parents) >= 3 else here.parent,  # project root (e.g., .../Fraud Detection)
        here.parents[1] if len(here.parents) >= 2 else here.parent,  # src/
        here.parent,                                                 # src/pages
        Path.cwd(),                                                  # current working dir
        Path.cwd().parent,                                           # parent of CWD
        Path.cwd() / "Fraud Detection",                              # common folder name variant
    ]
    candidates = []
    for root in candidates_roots:
        candidates.append(root / rel_path)
        # also try with backslash-friendly variant automatically covered by Path

    for p in candidates:
        try:
            if p.exists():
                return str(p)
        except Exception:
            pass
    return None


def _first_existing(paths: list[str]) -> Optional[str]:
    """Return the first existing path from a list (absolute or relative)."""
    for p in paths:
        if not p:
            continue
        # absolute allowed
        pp = Path(p)
        if pp.is_absolute() and pp.exists():
            return str(pp)
        # try as relative via resolver
        hit = _resolve_any(p)
        if hit:
            return hit
    return None


# ---------- Loading helpers ----------
@st.cache_resource(show_spinner=False)
def _load_pipeline_from_path(path: str):
    return joblib.load(path)

def _load_pipeline(src: Union[str, io.BufferedReader, io.BytesIO]):
    """
    Load from a path or a file-like object (for uploaded files).
    Not cached for file-like objects (they are not hashable).
    """
    if isinstance(src, (io.BufferedReader, io.BytesIO)):
        return joblib.load(src)
    return _load_pipeline_from_path(str(src))


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + np.exp(-x))


def _get_allowed_types_from_pipeline(pipeline) -> Optional[List[str]]:
    """
    Try to extract the list of categories the OneHotEncoder learned for the 'type' column.
    Returns None if it can’t be detected.
    """
    try:
        # Expecting Pipeline([('prep', ColumnTransformer([...('cat', OneHotEncoder, ['type'])...])), ('clf', ...)])
        prep = getattr(pipeline, "named_steps", {}).get("prep")
        if prep is None:
            return None

        from sklearn.preprocessing import OneHotEncoder

        # Walk ColumnTransformer's fitted transformers
        for _, transformer, columns in getattr(prep, "transformers_", []):
            ohe = None
            if isinstance(transformer, OneHotEncoder):
                ohe = transformer
            else:
                inner = getattr(transformer, "steps", None)
                if inner:
                    for _, step_obj in inner:
                        if isinstance(step_obj, OneHotEncoder):
                            ohe = step_obj
                            break

            if ohe is not None and columns is not None:
                cols = [columns] if isinstance(columns, str) else list(columns)
                if ("type" in cols) and hasattr(ohe, "categories_") and len(ohe.categories_) >= 1:
                    return list(map(str, ohe.categories_[0]))
        return None
    except Exception:
        return None


def _compute_fraud_score(model, X, schema: str) -> dict:
    """
    Returns a dict with:
      - pred_label: 0/1 fraud label (after any mapping)
      - score: unified [0,1] fraud score (always present)
      - extras: how the score was computed
      - proba/decision/anomaly if available
    """
    out = {"proba": None, "decision": None, "anomaly": None, "extras": ""}

    raw_pred = model.predict(X)

    if hasattr(model, "predict_proba"):
        try:
            out["proba"] = float(np.asarray(model.predict_proba(X))[:, -1][0])
        except Exception:
            out["proba"] = None

    if hasattr(model, "decision_function"):
        try:
            out["decision"] = float(np.asarray(model.decision_function(X))[0])
        except Exception:
            out["decision"] = None

    if hasattr(model, "score_samples"):
        try:
            out["anomaly"] = float(np.asarray(model.score_samples(X))[0])
        except Exception:
            out["anomaly"] = None

    if schema == "pca":
        # IsolationForest: -1=outlier → 1 (fraud), 1=inlier → 0
        pred_label = 1 if int(raw_pred[0]) == -1 else 0
    else:
        pred_label = int(raw_pred[0])

    if out["proba"] is not None:
        score = out["proba"]; out["extras"] = "from predict_proba"
    elif out["decision"] is not None:
        score = _sigmoid(out["decision"]); out["extras"] = "sigmoid(decision_function)"
    elif out["anomaly"] is not None:
        score = _sigmoid(-out["anomaly"]); out["extras"] = "sigmoid(-score_samples)"
    else:
        score = float(pred_label); out["extras"] = "fallback from predicted label"

    out["pred_label"] = pred_label
    out["score"] = float(np.clip(score, 0.0, 1.0))
    return out


def transaction_predictor():
    # Title/intro (unchanged, just premium)
    st.markdown(
        """
        <div style="
            background: radial-gradient(1200px 300px at -10% -50%, rgba(255,255,255,0.06) 20%, transparent 21%) repeat,
                        radial-gradient(1200px 300px at 110% 150%, rgba(255,255,255,0.06) 20%, transparent 21%) repeat,
                        linear-gradient(135deg, #0F2041 0%, #1E3A8A 100%);
            border-radius: 18px;
            padding: 28px 32px;
            color: #FFFFFF;
            box-shadow: 0 12px 28px rgba(0,0,0,0.12);
            margin-bottom: 22px;">
          <div style="font-size: 2rem; font-weight: 800; line-height: 1.2; letter-spacing: .2px;">
            Transaction Fraud  <span style="color:#D4AF37;">Predictor</span>
          </div>
          <div style="height: 1px; background: rgba(255,255,255,0.55); margin: 10px 0 12px 0;"></div>
          <div style="opacity:.9; font-size: 0.98rem;">
            Pick one of the two trained pipelines, then enter inputs that match it.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Tabs (⭐ Premium Interface | 🔬 Advanced Analysis)
    tab1, tab2 = st.tabs(["⭐ Premium Interface", "🔬 Advanced Analysis"])

    # ------------------------------------------------------------------
    # PREMIUM INTERFACE (visual UI only)
    # ------------------------------------------------------------------
    with tab1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)

        # Transaction details with premium styling
        st.markdown('<div class="premium-section-title">Transaction Information</div>', unsafe_allow_html=True)

        # Card number input
        st.markdown(
            """
            <div style="margin-bottom: 20px;">
                <label style="font-weight: 500; color: #1E3A8A; display: block; margin-bottom: 8px;">Card Information (optional)</label>
                <div style="display: flex; gap: 10px; margin-bottom: 10px; align-items: center;">
                    <div style="background-color: #F8FAFC; border-radius: 6px; padding: 10px 15px; flex-grow: 1; color: #64748B;">
                        •••• •••• •••• 1234
                    </div>
                    <div style="color: #64748B; font-size: 1.5rem;">💳</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Transaction details
        col1, col2 = st.columns(2)
        with col1:
            time_input = st.number_input(
                "Transaction Time (seconds)",
                min_value=0,
                value=0,
                step=1000,
                help="Time elapsed since first transaction in seconds",
            )
        with col2:
            amount_input = st.number_input(
                "Transaction Amount (R)",
                min_value=0.0,
                value=100.0,
                step=10.0,
                help="Rand amount of the transaction",
            )

        # Risk factor assessment with premium styling
        st.markdown(
            """
            <div style="margin: 25px 0 15px 0;">
                <div class="premium-section-title">Risk Assessment</div>
                <p style="color: #64748B; margin-bottom: 20px;">
                    Adjust the risk factors to simulate different transaction scenarios
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Risk score with premium slider
        risk_score = st.slider(
            "Transaction Risk Score",
            min_value=-10.0,
            max_value=10.0,
            value=0.0,
            step=0.5,
            help="Higher values indicate higher risk based on transaction patterns",
        )

        # Risk factors as toggles with premium styling
        col1, col2 = st.columns(2)

        with col1:
            location_match = st.checkbox(
                "Location matches billing address",
                value=True,
                help="Whether the transaction location matches the billing address",
            )
            device_recognized = st.checkbox(
                "Recognized device",
                value=True,
                help="Whether the transaction is from a previously used device",
            )

        with col2:
            unusual_time = st.checkbox(
                "Unusual transaction time",
                value=False,
                help="Whether the transaction occurred at an unusual hour",
            )
            international = st.checkbox(
                "International transaction",
                value=False,
                help="Whether the transaction occurred in a different country",
            )

        # Convert simplified inputs to feature values (more accurate approximation)
        pca_features = [0.0] * 28

        # Update features based on risk factors - enhance the impact
        if unusual_time:
            pca_features[0] = -2.5
            pca_features[6] = -1.0
            pca_features[12] = -1.5
        if not location_match:
            pca_features[1] = -3.5
            pca_features[7] = -1.5
            pca_features[13] = -2.0
        if not device_recognized:
            pca_features[4] = -3.0
            pca_features[9] = -1.5
            pca_features[15] = -1.0
        if international:
            pca_features[5] = -2.5
            pca_features[8] = -2.0
            pca_features[14] = -1.5

        # Add risk score influence across multiple features for more realistic patterns
        risk_multiplier = risk_score / 10.0  # Normalize to -1.0 to 1.0 range
        for i in range(28):
            # Distribute risk effect across all features with varying weights
            if i % 3 == 0:  # Every 3rd feature gets stronger influence
                pca_features[i] += risk_multiplier * 2.0
            elif i % 2 == 0:  # Every 2nd feature gets medium influence
                pca_features[i] += risk_multiplier * 1.5
            else:  # Others get lower influence
                pca_features[i] += risk_multiplier * 0.8

        # Apply stronger influence to key features
        pca_features[2] += risk_score * 0.4
        pca_features[3] += risk_score * 0.3
        pca_features[10] += risk_score * 0.35
        pca_features[17] += risk_score * 0.25

        st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # ADVANCED ANALYSIS (original logic inside tab2) + robust model loading
    # ------------------------------------------------------------------
    with tab2:
        # Environment-variable overrides if you want (optional)
        env_raw = os.getenv("FRAUD_RAW_PIPE")
        env_pca = os.getenv("FRAUD_PCA_PIPE")

        # Candidates for both
        RAW_PIPE = _first_existing(
            [
                env_raw,
                "assets/fraud_detection_pipeline.pkl",
                "models/fraud_detection_pipeline.pkl",
                "Fraud Detection/assets/fraud_detection_pipeline.pkl",
                "Fraud Detection/models/fraud_detection_pipeline.pkl",
                # absolute from this file's grandparent
                str(Path(__file__).resolve().parents[2] / "assets" / "fraud_detection_pipeline.pkl"),
                str(Path(__file__).resolve().parents[2] / "models" / "fraud_detection_pipeline.pkl"),
            ]
        )
        PCA_PIPE = _first_existing(
            [
                env_pca,
                "assets/iforest_pipeline.joblib",
                "models/iforest_pipeline.joblib",
                "Fraud Detection/assets/iforest_pipeline.joblib",
                "Fraud Detection/models/iforest_pipeline.joblib",
                str(Path(__file__).resolve().parents[2] / "assets" / "iforest_pipeline.joblib"),
                str(Path(__file__).resolve().parents[2] / "models" / "iforest_pipeline.joblib"),
            ]
        )

        RAW_LABEL = "RAW"
        PCA_LABEL = "PCA"

        choice_label = st.radio(
            " Choose a trained pipeline",
            options=[RAW_LABEL, PCA_LABEL],
            horizontal=True,
            index=0,
        )
        # Decide schema + default path
        default_path = RAW_PIPE if choice_label == RAW_LABEL else PCA_PIPE
        schema = "raw" if choice_label == RAW_LABEL else "pca"

        st.markdown(
            "<small>Tip: If you get UI lag from many sliders, switch to numeric inputs.</small>",
            unsafe_allow_html=True,
        )
        use_sliders = st.toggle("Use sliders (instead of numeric inputs)", value=False)

        # If no file found on disk, allow upload
        uploaded = None
        if default_path is None:
            st.warning(
                "Could not find the selected trained pipeline on disk. "
                "Upload the correct **.pkl** (RAW) or **.joblib** (PCA) bundle below."
            )
            uploaded = st.file_uploader(
                f"Upload {choice_label} pipeline file",
                type=["pkl", "joblib"],
                accept_multiple_files=False,
                key=f"upl_{choice_label.lower()}",
                help="Pickle/joblib bundle of your trained pipeline",
            )

        # Load the pipeline (from disk or uploaded file)
        try:
            if uploaded is not None:
                pipe = _load_pipeline(uploaded)
                st.success(f"Using **uploaded {choice_label} pipeline** → schema **{schema.upper()}**.")
            else:
                if default_path is None:
                    st.error(
                        "No pipeline provided. Please place your model under `assets/` or `models/` "
                        "or use the uploader above."
                    )
                    st.stop()
                pipe = _load_pipeline(default_path)
                st.success(f"Using **{Path(default_path).name}** → schema **{schema.upper()}**.")
        except Exception as e:
            st.exception(e)
            st.error(
                "Failed to load the pipeline. Ensure the file matches the selected schema "
                "(RAW expects `fraud_detection_pipeline.pkl`; PCA expects `iforest_pipeline.joblib`)."
            )
            st.stop()

        with st.expander(" Debug: expected input", expanded=False):
            names_in = getattr(pipe, "feature_names_in_", None)
            st.write(
                list(names_in)
                if names_in is not None
                else "feature_names_in_ not present (normal for many pickles)."
            )

        # ---------- helpers ----------
        def ui_number_or_slider(label, *, value, min_value, max_value, step, format="%.2f", key=None):
            if use_sliders:
                v = st.slider(
                    label,
                    min_value=float(min_value),
                    max_value=float(max_value),
                    value=float(value),
                    step=float(step),
                    key=key,
                )
                return float(v)
            else:
                return float(
                    st.number_input(
                        label,
                        min_value=float(min_value),
                        max_value=float(max_value),
                        value=float(value),
                        step=float(step),
                        format=format,
                        key=key,
                    )
                )

        # ------------------------------- Forms ---------------------------------
        st.markdown("---")
        if schema == "raw":
            st.subheader("RAW Transaction Fields")

            # Default menu if we can’t read from the model
            default_types = ["PAYMENT", "TRANSFER", "CASH_OUT", "CASH_IN", "DEBIT"]
            allowed_types = _get_allowed_types_from_pipeline(pipe) or default_types

            # If your trained model didn’t see DEPOSIT, it won’t be offered.
            tx_type = st.selectbox("Transaction Type", options=allowed_types)

            amount = ui_number_or_slider(
                "Amount", value=1000.0, min_value=0.0, max_value=1_000_000.0, step=10.0
            )
            old_org = ui_number_or_slider(
                "Old Balance (Sender)", value=10_000.0, min_value=0.0, max_value=10_000_000.0, step=10.0
            )
            new_org = ui_number_or_slider(
                "New Balance (Sender)", value=9_000.0, min_value=0.0, max_value=10_000_000.0, step=10.0
            )
            old_dst = ui_number_or_slider(
                "Old Balance (Receiver)", value=0.0, min_value=0.0, max_value=10_000_000.0, step=10.0
            )
            new_dst = ui_number_or_slider(
                "New Balance (Receiver)", value=0.0, min_value=0.0, max_value=10_000_000.0, step=10.0
            )

            X_input = pd.DataFrame(
                [
                    {
                        "type": tx_type,
                        "amount": amount,
                        "oldbalanceOrg": old_org,
                        "newbalanceOrig": new_org,
                        "oldbalanceDest": old_dst,
                        "newbalanceDest": new_dst,
                    }
                ]
            )

            # Safety: if someone manages to submit an unseen category, coerce to first allowed
            if "type" in X_input and allowed_types and X_input.loc[0, "type"] not in allowed_types:
                st.warning(
                    f"'{X_input.loc[0, 'type']}' was not seen during training – using '{allowed_types[0]}' instead."
                )
                X_input.loc[0, "type"] = allowed_types[0]

        else:
            st.subheader("PCA Features (V1..V28) + Time + Amount")

            pca_min, pca_max, pca_step = -20.0, 20.0, 0.01
            vals = {}
            cols = st.columns(4)
            for i in range(1, 29):
                with cols[(i - 1) % 4]:
                    vals[f"V{i}"] = ui_number_or_slider(
                        f"V{i}",
                        value=0.0,
                        min_value=pca_min,
                        max_value=pca_max,
                        step=pca_step,
                        key=f"V{i}",
                    )

            time_val = ui_number_or_slider(
                "Time (sec since start)", value=0.0, min_value=0.0, max_value=2_000_000.0, step=1.0, key="Time"
            )
            amt_val = ui_number_or_slider(
                "Amount", value=0.0, min_value=0.0, max_value=50_000.0, step=1.0, key="Amount"
            )

            vals["Time"] = time_val
            vals["Amount"] = amt_val

            names_in = getattr(pipe, "feature_names_in_", None)
            ordered = list(names_in) if names_in is not None else [f"V{i}" for i in range(1, 29)] + ["Time", "Amount"]
            X_input = pd.DataFrame([[vals.get(k, 0.0) for k in ordered]], columns=ordered)

        st.markdown("---")
        if st.button("Predict"):
            try:
                result = _compute_fraud_score(pipe, X_input, schema)

                st.subheader(f"Prediction: {result['pred_label']}")
                st.metric("Fraud score (0–1)", f"{result['score']:.3f}", help=f"Computed {result['extras']}")

                if result["proba"] is not None:
                    st.write(f"Model probability (predict_proba): **{result['proba']:.3f}**")
                if result["decision"] is not None and result["proba"] is None:
                    st.write(f"Decision function: **{result['decision']:.4f}**")
                if result["anomaly"] is not None:
                    st.write(f"Anomaly score (raw): **{result['anomaly']:.4f}**")

                if result["pred_label"] == 1:
                    st.error("This transaction may be **fraudulent**.")
                else:
                    st.success("This transaction looks **non-fraudulent**.")

                with st.expander("Show model inputs"):
                    st.dataframe(X_input)

            except Exception as e:
                st.exception(e)
                st.warning(
                    "The input columns (names & dtypes) must match those used to train this pipeline. "
                    "Make sure your selection (RAW vs PCA) matches the bundle you chose."
                )


# Aliases so your loader can call it
def main():
    transaction_predictor()


if __name__ == "__main__":
    main()
