# fraud_detection_app2.py — robust RAW/PCA support + manual class weights + metrics + importance + correlation

import re
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Optional seaborn (fallback to Matplotlib if missing)
try:
    import seaborn as sns
    HAS_SNS = True
except Exception:
    HAS_SNS = False

import streamlit as st

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score,
    confusion_matrix, ConfusionMatrixDisplay,
    RocCurveDisplay, PrecisionRecallDisplay
)
from sklearn.inspection import permutation_importance

# Optional TensorFlow for Shallow NN
HAS_TF = True
try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, InputLayer, BatchNormalization
    from tensorflow.keras.callbacks import ModelCheckpoint
except Exception:
    HAS_TF = False


# -------------------- Page --------------------
# Guard set_page_config so reloads don’t crash
try:
    st.set_page_config(page_title=" Fraud Detection App", page_icon="Fraud_Detection_App", layout="wide")
except Exception:
    pass

# --- Sidebar layout & widget polish (fix cramped multiselect) ---
st.markdown("""
<style>
/* Wider sidebar on desktop */
@media (min-width: 992px){
  section[data-testid="stSidebar"] {width: 360px !important;}
  div[data-testid="stSidebar"] {min-width: 360px !important;}
}

/* Make the sidebar content scroll independently (prevents cut-off) */
section[data-testid="stSidebar"] > div {
  height: 100vh;
  overflow-y: auto;
  padding-right: 8px;
}

/* Multiselect: allow chips to wrap and not be squashed */
[data-testid="stSidebar"] div[data-testid="stMultiSelect"] > div > div {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
  overflow: visible;
}

/* Tag (chip) styling – readable on dark sidebar */
[data-testid="stSidebar"] div[data-testid="stMultiSelect"] [data-baseweb="tag"] {
  border-radius: 8px;
  padding: 2px 8px;
  background: #D94C4C;
  color: #fff;
  border: none;
}
[data-testid="stSidebar"] div[data-testid="stMultiSelect"] [data-baseweb="tag"] svg {
  fill: #fff;
}

/* Inputs: ensure full width and comfortable height */
[data-testid="stSidebar"] .stNumberInput input,
[data-testid="stSidebar"] .stTextInput input {
  height: 38px;
}

/* Dropdown popover should appear over everything in the sidebar */
[data-testid="stSidebar"] div[data-baseweb="select"] {
  z-index: 1000 !important;
}

/* Optional: sidebar background to match your palette
[data-testid="stSidebar"] { background: #0F2041; }
[data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span { color: white; }
*/
</style>
""", unsafe_allow_html=True)

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
        Transaction Fraud  <span style="color:#D4AF37;">App</span>
      </div>
      <div style="height: 1px; background: rgba(255,255,255,0.55); margin: 10px 0 12px 0;"></div>
      <div style="opacity:.9; font-size: 0.98rem;">
        Advanced Algorithms for fraud detection.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# -------------------- Helpers --------------------
@st.cache_data(show_spinner=False)
def load_data(file_or_path):
    """Robust CSV loader: try default engine, fallback to python engine cleanly."""
    try:
        if hasattr(file_or_path, "read"):
            return pd.read_csv(file_or_path)
        return pd.read_csv(file_or_path)
    except Exception:
        try:
            if hasattr(file_or_path, "seek"):
                try:
                    file_or_path.seek(0)
                except Exception:
                    pass
            return pd.read_csv(file_or_path, engine="python")
        except Exception as e2:
            raise e2

def detect_schema(df: pd.DataFrame):
    has_pca = ("Class" in df.columns) and any(re.fullmatch(r"V\d+", c) for c in df.columns)
    has_raw = ("isFraud" in df.columns) and ("type" in df.columns)
    if has_pca:
        return "pca", "Class"
    if has_raw:
        return "raw", "isFraud"
    return None, None

def ensure_engineered_columns(X: pd.DataFrame) -> pd.DataFrame:
    X = X.copy()
    if {"oldbalanceOrg", "newbalanceOrig"}.issubset(X.columns) and "balanceDiffOrig" not in X.columns:
        X["balanceDiffOrig"] = X["oldbalanceOrg"] - X["newbalanceOrig"]
    if {"oldbalanceDest", "newbalanceDest"}.issubset(X.columns) and "balanceDiffDest" not in X.columns:
        X["balanceDiffDest"] = X["oldbalanceDest"] - X["newbalanceDest"]
    return X

def make_ohe_dense():
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)

def build_preprocessor(schema_name: str, X: pd.DataFrame):
    orig_cols = X.columns.tolist()

    if schema_name == "pca":
        v_cols = sorted([c for c in orig_cols if re.fullmatch(r"V\d+", c)])
        extra = [c for c in ["Time", "Amount"] if c in orig_cols]
        numeric = v_cols + extra
        categorical = []
    else:
        numeric_candidates = [
            "amount", "oldbalanceOrg", "newbalanceOrig",
            "oldbalanceDest", "newbalanceDest",
            "balanceDiffOrig", "balanceDiffDest"
        ]
        numeric = [c for c in numeric_candidates if c in orig_cols]
        categorical = ["type"] if "type" in orig_cols else []

    if len(numeric) + len(categorical) == 0:
        cat_auto = X.select_dtypes(include=["object", "category"]).columns.tolist()
        num_auto = X.select_dtypes(include=["number", "bool"]).columns.tolist()
        numeric = num_auto
        categorical = cat_auto
        st.warning(
            "No expected schema columns found. Falling back to dtype-based selection. "
            "Check column names or switch the schema."
        )

    transformers = []
    if len(numeric) > 0:
        transformers.append(("num", StandardScaler(), numeric))
    if len(categorical) > 0:
        transformers.append(("cat", make_ohe_dense(), categorical))

    if not transformers:
        raise ValueError("No usable feature columns were found after schema selection.")

    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder="drop",
        verbose_feature_names_out=False,
    )

    with st.expander("Feature selection (debug)", expanded=False):
        st.write({"schema": schema_name, "numeric_cols": numeric, "categorical_cols": categorical})

    return preprocessor

def plot_confusion(cm, labels):
    fig, ax = plt.subplots(figsize=(4, 4))
    ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels).plot(ax=ax, cmap=plt.cm.Blues, values_format='d')
    st.pyplot(fig); plt.close(fig)

def plot_curves(selected, estimator, X_test, y_test, y_score=None, is_nn=False):
    if "Confusion Matrix" in selected:
        preds = (y_score > 0.5).astype(int) if is_nn and y_score is not None else estimator.predict(X_test)
        cm = confusion_matrix(y_test, preds)
        st.subheader("Confusion Matrix")
        plot_confusion(cm, ["Non-Fraud", "Fraud"])

    if "ROC Curve" in selected:
        st.subheader("ROC Curve")
        fig, ax = plt.subplots(figsize=(6, 4))
        if is_nn and y_score is not None:
            RocCurveDisplay.from_predictions(y_test, y_score, ax=ax)
        else:
            RocCurveDisplay.from_estimator(estimator, X_test, y_test, ax=ax)
        st.pyplot(fig); plt.close(fig)

    if "Precision-Recall Curve" in selected:
        st.subheader("Precision-Recall Curve")
        fig, ax = plt.subplots(figsize=(6, 4))
        if is_nn and y_score is not None:
            PrecisionRecallDisplay.from_predictions(y_test, y_score, ax=ax)
        else:
            PrecisionRecallDisplay.from_estimator(estimator, X_test, y_test, ax=ax)
        st.pyplot(fig); plt.close(fig)

def balanced_class_weights_dict(y: pd.Series) -> dict:
    classes, counts = np.unique(y, return_counts=True)
    if classes.size < 2:
        return {int(classes[0]): 1.0}
    total = counts.sum()
    n_classes = classes.size
    return {int(cls): float(total / (n_classes * cnt)) for cls, cnt in zip(classes, counts)}

# -------------------- NN Wrapper (fixed) --------------------
class _NNWrapper:
    """
    Sklearn-like wrapper around (preprocessor, keras_model).
    Adds classifier markers so sklearn treats it as a classifier
    for scoring/permutation_importance.
    """
    def __init__(self, prep, mdl):
        self.prep = prep
        self.clf = mdl
        self._estimator_type = "classifier"    # tell sklearn it's a classifier
        self.classes_ = np.array([0, 1])       # positive/negative classes

    def fit(self, X, y=None):
        return self  # model already trained

    def predict(self, X):
        X_t = self.prep.transform(X)
        p = self.clf.predict(X_t, verbose=0).flatten()
        return (p > 0.5).astype(int)

    def predict_proba(self, X):
        X_t = self.prep.transform(X)
        p = self.clf.predict(X_t, verbose=0).flatten()
        return np.vstack([1 - p, p]).T

    def decision_function(self, X):
        X_t = self.prep.transform(X)
        p = self.clf.predict(X_t, verbose=0).flatten()
        eps = 1e-9
        return np.log((p + eps) / (1 - p + eps))

    def score(self, X, y):
        y = np.asarray(y)
        yhat = self.predict(X)
        return (yhat == y).mean()

    def get_params(self, deep=False):
        return {}
    def set_params(self, **params):
        return self

    @property
    def named_steps(self):
        return {"prep": self.prep, "clf": self.clf}


def show_feature_importance(pipeline, X, y):
    st.subheader("Feature Importance")
    try:
        prep = getattr(pipeline, "named_steps", {}).get("prep", None)
        clf  = getattr(pipeline, "named_steps", {}).get("clf",  None)
        if prep is None or clf is None:
            st.info("No preprocess/estimator found.")
            return

        try:
            feat_names = prep.get_feature_names_out()
        except Exception:
            n_out = prep.transform(X.head(1)).shape[1]
            feat_names = np.array([f"feat_{i}" for i in range(n_out)])

        importance, method = None, None

        if hasattr(clf, "feature_importances_"):
            importance = clf.feature_importances_
            method = "Tree-based (feature_importances_)"
        elif hasattr(clf, "coef_"):
            try:
                importance = np.abs(clf.coef_).ravel()
                method = "Linear coefficients (|coef|)"
            except Exception:
                importance = None

        if importance is None and hasattr(pipeline, "fit"):
            idx = np.random.choice(len(X), size=min(5000, len(X)), replace=False)
            X_small, y_small = X.iloc[idx], y.iloc[idx]
            perm = permutation_importance(
                pipeline, X_small, y_small,
                n_repeats=5, random_state=42, n_jobs=-1, scoring="roc_auc"
            )
            importance = perm.importances_mean
            method = "Permutation importance (ROC-AUC)"

        if importance is None:
            st.info("Feature importance not available for this estimator.")
            return

        imp_df = pd.DataFrame({"Feature": feat_names, "Importance": importance}).sort_values("Importance", ascending=False)
        st.caption(f"Method: **{method}**")

        if HAS_SNS:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=imp_df.head(30), x="Importance", y="Feature", ax=ax)
            ax.set_title("Top Feature Importance")
            ax.set_xlabel("Importance"); ax.set_ylabel("Feature")
            st.pyplot(fig)
        else:
            fig, ax = plt.subplots(figsize=(10, 6))
            top = imp_df.head(30).iloc[::-1]
            ax.barh(top["Feature"], top["Importance"])
            ax.set_title("Top Feature Importance")
            ax.set_xlabel("Importance"); ax.set_ylabel("Feature")
            st.pyplot(fig)
        plt.close('all')

        with st.expander("Show full importance table"):
            st.dataframe(imp_df.reset_index(drop=True), use_container_width=True)

    except Exception as e:
        st.info("Could not compute feature importance.")
        st.exception(e)

def show_correlation_matrix(schema_name: str, X: pd.DataFrame):
    st.subheader("Correlation Matrix (original numeric columns)")
    if schema_name == "pca":
        num_cols = sorted([c for c in X.columns if re.fullmatch(r"V\d+", c)] + [c for c in ["Time", "Amount"] if c in X.columns])
    else:
        num_cols = [c for c in [
            "amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest", "newbalanceDest",
            "balanceDiffOrig", "balanceDiffDest"
        ] if c in X.columns]
        if not num_cols:
            num_cols = X.select_dtypes(include=["number", "bool"]).columns.tolist()

    if not num_cols:
        st.info("No numeric columns available for correlation.")
        return

    corr = X[num_cols].corr().round(2)
    fig, ax = plt.subplots(figsize=(12, 8))
    if HAS_SNS:
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    else:
        cax = ax.imshow(corr, cmap="coolwarm")
        ax.set_xticks(range(len(num_cols))); ax.set_yticks(range(len(num_cols)))
        ax.set_xticklabels(num_cols, rotation=90); ax.set_yticklabels(num_cols)
        fig.colorbar(cax)
    ax.set_title("Correlation Matrix")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# -------------------- SIDEBAR: Data & Settings --------------------
st.sidebar.header("Data")
uploaded = st.sidebar.file_uploader("Upload CSV (optional)", type=["csv"])
data_path = st.sidebar.text_input("…or CSV Path", value="")
test_size = st.sidebar.slider("Test set fraction", 0.05, 0.5, 0.2, 0.05)
random_state = int(st.sidebar.number_input("Random seed", 0, 9999, value=42))

st.sidebar.header("Model")
model_options = ["Random Forest", "Logistic Regression", "SVM"]
if HAS_TF:
    model_options.append("Shallow Neural Network")
classifier = st.sidebar.selectbox("Estimator", tuple(model_options))

metrics_to_plot = st.sidebar.multiselect(
    "Curves to plot", ("Confusion Matrix", "ROC Curve", "Precision-Recall Curve"),
    default=("Confusion Matrix", "ROC Curve", "Precision-Recall Curve")
)

st.sidebar.header("Estimator Hyperparams")
if classifier == "Random Forest":
    n_estimators = st.sidebar.number_input("n_estimators", 10, 2000, value=300, step=10)
    max_depth = st.sidebar.number_input("max_depth (0=None)", 0, 300, value=0, step=1)
elif classifier == "Logistic Regression":
    C = st.sidebar.number_input("C (inverse regularization)", 1e-4, 100.0, value=1.0, step=0.1, format="%.4f")
    max_iter = st.sidebar.number_input("max_iter", 50, 5000, value=400, step=50)
    solver = st.sidebar.selectbox("solver", ["lbfgs", "saga", "liblinear"])
elif classifier == "SVM":
    C_svm = st.sidebar.number_input("C", 1e-4, 100.0, value=1.0, step=0.1, format="%.4f")
    kernel = st.sidebar.selectbox("kernel", ("rbf", "linear"))
    gamma = st.sidebar.selectbox("gamma", ("scale", "auto"))

train_btn = st.sidebar.button("Train model")


# -------------------- Load data --------------------
try:
    with st.spinner("Loading data…"):
        if uploaded is not None:
            df = load_data(uploaded)
        elif data_path.strip():
            df = load_data(data_path.strip())
        else:
            st.warning("Upload a CSV or provide a CSV path in the sidebar.")
            st.stop()
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

st.success("Data loaded")
with st.expander("Data preview", expanded=False):
    st.dataframe(df.head(10), use_container_width=True)
    try:
        st.write(df.describe(include="all").transpose())
    except Exception:
        st.write(df.describe().transpose())

# Detect/override schema
schema_name, target_col = detect_schema(df)
schema_override = None
if schema_name is None:
    st.warning("Could not detect schema automatically.")
    schema_override = st.radio("Select schema to use:", ["raw", "pca"], horizontal=True, index=0)
schema_used = schema_name or schema_override
if schema_used is None:
    st.error("Please select a schema."); st.stop()

st.info(f" Using schema: **{schema_used.upper()}**")

# Build X, y
if schema_used == "pca":
    if "Class" not in df.columns:
        st.error("PCA schema requires a 'Class' column."); st.stop()
    y = df["Class"].astype(int)
    v_cols = sorted([c for c in df.columns if re.fullmatch(r"V\d+", c)])
    extras = [c for c in ["Time", "Amount"] if c in df.columns]
    used_cols = v_cols + extras
    if not used_cols:
        st.error("No PCA features (V1..V28/Time/Amount) found."); st.stop()
    X = df[used_cols].copy()
else:
    if "isFraud" not in df.columns:
        st.error("RAW schema requires an 'isFraud' column."); st.stop()
    y = df["isFraud"].astype(int)
    candidate_cols = [
        "type", "amount", "oldbalanceOrg", "newbalanceOrig",
        "oldbalanceDest", "newbalanceDest",
        "balanceDiffOrig", "balanceDiffDest"
    ]
    existing = [c for c in candidate_cols if c in df.columns]
    if not existing:
        drop_cols = {"isFraud", "isFlaggedFraud", "nameOrig", "nameDest", "step"}
        existing = [c for c in df.columns if c not in drop_cols]
    X = df[existing].copy()
    X = ensure_engineered_columns(X)

# Split (guard against single-class training)
if y.nunique() < 2:
    st.error("Your dataset contains only a single class. Add examples of both classes to train a classifier.")
    st.stop()

stratify = y if y.nunique() == 2 else None
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=float(test_size), random_state=int(random_state), stratify=stratify
)

st.sidebar.markdown("### Class distribution (train)")
st.sidebar.write(y_train.value_counts())

# Build preprocessor and sanity check
preprocessor = build_preprocessor(schema_used, X)
try:
    preprocessor.fit(X_train)
    out_shape = preprocessor.transform(X_train[:5]).shape[1]
    if out_shape == 0:
        st.error("Preprocessor produced 0 features. Adjust schema/columns.")
        st.stop()
except Exception as e:
    st.error("Preprocessor failed to fit/transform.")
    st.exception(e)
    st.stop()

# -------------------- Train --------------------
if not train_btn:
    st.info("Choose your settings in the sidebar, then click **Train model**.")
    st.stop()

st.write(f"### Training **{classifier}** …")

# Manual balanced weights
cw = balanced_class_weights_dict(y_train)

if classifier == "Random Forest":
    clf = RandomForestClassifier(
        n_estimators=int(n_estimators),
        max_depth=(None if int(max_depth) == 0 else int(max_depth)),
        random_state=random_state,
        class_weight=cw,
        n_jobs=-1
    )

elif classifier == "Logistic Regression":
    lr_kwargs = dict(C=float(C), max_iter=int(max_iter), class_weight=cw, solver=solver)
    # n_jobs supported for liblinear and saga
    if solver in ("saga", "liblinear"):
        lr_kwargs["n_jobs"] = -1
    clf = LogisticRegression(**lr_kwargs)

elif classifier == "SVM":
    clf = SVC(
        C=float(C_svm), kernel=kernel, gamma=gamma,
        probability=True, class_weight=cw,
        random_state=random_state
    )
    if len(X_train) > 300_000:
        st.warning("SVM on very large datasets can be slow. Consider subsampling or using RF/LR.")

else:  # Shallow NN
    if not HAS_TF:
        st.error("TensorFlow is not available. Install it to use the Shallow NN."); st.stop()
    clf = None

# Pipeline or NN
if classifier != "Shallow Neural Network":
    pipe = Pipeline([("prep", preprocessor), ("clf", clf)])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    if hasattr(pipe.named_steps["clf"], "predict_proba"):
        y_score = pipe.predict_proba(X_test)[:, 1]
    elif hasattr(pipe.named_steps["clf"], "decision_function"):
        decision = pipe.decision_function(X_test)
        y_score = (decision - decision.min()) / (decision.max() - decision.min() + 1e-9)
    else:
        y_score = None
else:
    X_train_t = preprocessor.transform(X_train)
    X_test_t = preprocessor.transform(X_test)
    model = Sequential([
        InputLayer(input_shape=(X_train_t.shape[1],)),
        Dense(32, activation='relu'),
        BatchNormalization(),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    checkpoint = ModelCheckpoint('shallow_nn.keras', save_best_only=True, monitor='val_loss', mode='min')
    with st.spinner("Training shallow neural network…"):
        model.fit(X_train_t, y_train, validation_split=0.1, epochs=12, callbacks=[checkpoint], verbose=0)
    y_score = model.predict(X_test_t).flatten()
    y_pred = (y_score > 0.5).astype(int)

    # Wrap to look like sklearn for downstream utilities (incl. permutation_importance)
    pipe = _NNWrapper(preprocessor, model)

# -------------------- Metrics --------------------
acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred, zero_division=0)
rec = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)
roc_auc = roc_auc_score(y_test, y_score) if y_score is not None else float("nan")
avg_prec = average_precision_score(y_test, y_score) if y_score is not None else float("nan")

st.subheader("Results")
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Accuracy", f"{acc:.4f}")
k2.metric("Precision", f"{prec:.4f}")
k3.metric("Recall", f"{rec:.4f}")
k4.metric("F1-score", f"{f1:.4f}")
k5.metric("ROC AUC", "—" if np.isnan(roc_auc) else f"{roc_auc:.4f}")
k6.metric("PR AUC",  "—" if np.isnan(avg_prec) else f"{avg_prec:.4f}")

plot_curves(metrics_to_plot, pipe, X_test, y_test, y_score=y_score, is_nn=(classifier == "Shallow Neural Network"))

st.divider()
show_feature_importance(pipe, X, y)
st.divider()
show_correlation_matrix(schema_used, X)

with st.expander("Quick EDA (sampled)", expanded=False):
    st.caption("Small sampled plots for speed.")
    sample = X.copy()
    sample["__label__"] = y.values
    take = min(10_000, len(sample))
    sample = sample.sample(take, random_state=42)

    num_cols = sample.select_dtypes(include=["number", "bool"]).columns.tolist()
    if "__label__" in num_cols:
        num_cols.remove("__label__")
    for col in num_cols[:12]:
        fig, ax = plt.subplots(figsize=(6, 4))
        try:
            if HAS_SNS:
                sns.histplot(data=sample, x=col, hue="__label__", bins=60, stat="density", common_norm=False, ax=ax)
            else:
                a = sample[sample["__label__"] == 0][col].dropna()
                b = sample[sample["__label__"] == 1][col].dropna()
                ax.hist(a, bins=60, alpha=0.6, label="0")
                ax.hist(b, bins=60, alpha=0.6, label="1")
                ax.legend(title="Class")
            ax.set_title(f"Distribution: {col} by class")
            st.pyplot(fig); plt.close(fig)
        except Exception:
            plt.close(fig)
            continue

    if schema_used == "pca" and all(c in sample.columns for c in ["V1", "V2"]):
        fig, ax = plt.subplots(figsize=(6, 4))
        if HAS_SNS:
            sns.scatterplot(data=sample, x="V1", y="V2", hue="__label__", ax=ax, s=12)
        else:
            c0 = sample[sample["__label__"] == 0]
            c1 = sample[sample["__label__"] == 1]
            ax.scatter(c0["V1"], c0["V2"], s=6, label="0")
            ax.scatter(c1["V1"], c1["V2"], s=6, label="1")
            ax.legend()
        ax.set_title("V1 vs V2 (sample)")
        st.pyplot(fig); plt.close(fig)
