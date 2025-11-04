import streamlit as st
from pathlib import Path

# --- robust asset resolver so st.image never crashes ---
def _resolve_asset(*parts) -> str | None:
    """
    Try to find an asset across common roots so st.image never crashes.
    Looks in (a) project root, (b) current working dir, (c) this file's dir.
    """
    here = Path(__file__).resolve()
    roots = [
        here.parents[2],   # project root (e.g., .../Fraud Detection)
        Path.cwd(),        # current working directory
        here.parent,       # src/pages
    ]
    for root in roots:
        p = root.joinpath(*parts)
        if p.exists():
            return str(p)
    return None


def show_welcome_page():
    # Large premium hero at the top
    st.markdown(
        """
        <div style="
            background:
                radial-gradient(2000px 550px at -10% -60%, rgba(255,255,255,0.06) 20%, transparent 21%) repeat,
                radial-gradient(2000px 550px at 110% 160%, rgba(255,255,255,0.06) 20%, transparent 21%) repeat,
                linear-gradient(135deg, #0F2041 0%, #1E3A8A 100%);
            border-radius: 28px;
            padding: 72px 64px;
            color: #FFFFFF;
            box-shadow: 0 24px 56px rgba(0,0,0,0.18);
            margin: 8px auto 36px auto;
            text-align: center;
            min-height: 260px;">
          <div style="font-size: clamp(2.6rem, 5.6vw, 4rem); font-weight: 800; line-height: 1.1; letter-spacing: .3px;">
            Fraud Detection <span style="color:#D4AF37;">System</span>
          </div>
          <div style="height: 2px; background: rgba(255,255,255,0.70); margin: 18px auto; max-width: 760px;"></div>
          <div style="opacity:.95; font-size: clamp(1.05rem, 1.5vw, 1.25rem); max-width: 900px; margin: 0 auto;">
            Advanced analytics for secure financial transactions
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Premium CSS
    st.markdown(
        """
        <style>
        /* Fix for container issues */
        .element-container { margin: 0 !important; padding: 0 !important; }
        div[data-testid="stElementContainer"] { margin: 0 !important; padding: 0 !important; }
        .stMarkdown div[data-testid="stMarkdownContainer"] { margin: 0 !important; padding: 0 !important; }

        .welcome-header { text-align: center; padding: 20px 0; margin-bottom: 30px; }
        .welcome-title {
            font-size: 3rem; font-weight: 700;
            background: linear-gradient(90deg, #0F2041 0%, #1E3A8A 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px;
        }
        .welcome-subtitle { color: #4B5563; font-size: 1.2rem; font-weight: 400; }
        .gold-accent { color: #D4AF37; }

        .card {
            background-color: #FFFFFF; border-radius: 12px; padding: 30px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.05); height: 100%;
            transition: transform 0.3s ease, box-shadow 0.3s ease; border: 1px solid #F3F4F6;
        }
        .card:hover { transform: translateY(-5px); box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1); }

        .feature-card {
            border-left: 4px solid #1E3A8A; padding-left: 20px; margin-bottom: 25px;
            background-color: #F8FAFC; border-radius: 0 8px 8px 0; padding: 15px 15px 15px 20px;
        }
        .luxury-divider {
            height: 3px; background: linear-gradient(90deg, #D4AF37, #1E3A8A, #D4AF37);
            margin: 40px 0; border-radius: 3px;
        }

        .nav-card {
            background-color: #FFFFFF; border-radius: 12px; padding: 25px; text-align: center;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.05); height: 100%;
            transition: all 0.3s ease; border: 1px solid #F3F4F6; cursor: pointer;
        }
        .nav-card:hover { transform: translateY(-5px); box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1); border-color: #D4AF37; }
        .nav-card h4 { color: #0F2041; font-weight: 600; margin-bottom: 15px; }
        .nav-card p { color: #4B5563; }

        p { color: #4B5563; }
        h1, h2, h3, h4, h5, h6 { color: #0F2041; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --- Banner image with safe fallback ---
    img_path = _resolve_asset("assets", "Fraud.jpg")
    if img_path:
        st.image(img_path, use_column_width=True)
        overlay_margin_top = "-100px"
    else:
        # graceful fallback banner
        st.markdown(
            """
            <div style="
                background:
                    radial-gradient(1600px 400px at -10% -50%, rgba(255,255,255,0.06) 20%, transparent 21%) repeat,
                    radial-gradient(1600px 400px at 110% 150%, rgba(255,255,255,0.06) 20%, transparent 21%) repeat,
                    linear-gradient(135deg, #0F2041 0%, #1E3A8A 100%);
                border-radius: 22px;
                padding: 44px 48px;
                color: #FFFFFF;
                box-shadow: 0 16px 36px rgba(0,0,0,0.14);
                margin-bottom: 0;">
            </div>
            """,
            unsafe_allow_html=True,
        )
        overlay_margin_top = "0"

    # Text overlay on banner / fallback
    st.markdown(
        f"""
        <div style="margin-top: {overlay_margin_top}; margin-bottom: 50px; text-align: center;
                    padding: 20px; background-color: rgba(15, 32, 65, 0.8);
                    border-radius: 0 0 15px 15px;">
            <h2 style="color: white; margin: 0; font-size: 2.5rem; font-weight: 700;">Premium Fraud Detection</h2>
            <p style="color: #D4AF37; margin-top: 15px; font-size: 1.2rem;">Enterprise-grade Transaction Security</p>
            <div style="width: 80px; height: 3px; background: linear-gradient(90deg, #D4AF37, rgba(255,255,255,0.5)); margin: 20px auto;"></div>
            <p style="color: white; font-size: 0.9rem;">Advanced Analytics • Machine Learning • Real-time Protection</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Premium statistics bar
    st.markdown(
        """
        <div style="background: linear-gradient(90deg, #0F2041 0%, #1E3A8A 100%);
                    border-radius: 12px; margin: 30px 0; padding: 20px; display: flex;
                    justify-content: space-around; color: white; text-align: center;">
            <div>
                <h2 style="color: #D4AF37; font-size: 2rem; margin-bottom: 5px;">99.7%</h2>
                <p style="font-size: 0.9rem; margin: 0; color: white;">Detection Accuracy</p>
            </div>
            <div>
                <h2 style="color: #D4AF37; font-size: 2rem; margin-bottom: 5px;">24/7</h2>
                <p style="font-size: 0.9rem; margin: 0; color: white;">Real-time Monitoring</p>
            </div>
            <div>
                <h2 style="color: #D4AF37; font-size: 2rem; margin-bottom: 5px;">R5M+</h2>
                <p style="font-size: 0.9rem; margin: 0; color: white;">Transactions Analyzed</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Features / How-to
    st.markdown('<div class="luxury-divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h2 style="color: #0F2041; margin-bottom: 20px;">Advanced Features</h2>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="feature-card">
                <h4 style="color: #0F2041; display: flex; align-items: center;">
                    <span style="background-color: #1E3A8A; color: white; width: 24px; height: 24px; border-radius: 50%;
                                 display: inline-flex; align-items: center; justify-content: center; margin-right: 10px;
                                 font-weight: bold; font-size: 0.8rem;">ML</span>
                    Comprehensive ML Models
                </h4>
                <p style="color: #4B5563; margin-left: 34px;">Random Forest, Logistic Regression, SVM, and Neural Networks with customizable parameters</p>
            </div>

            <div class="feature-card">
                <h4 style="color: #0F2041; display: flex; align-items: center;">
                    <span style="background-color: #1E3A8A; color: white; width: 24px; height: 24px; border-radius: 50%;
                                 display: inline-flex; align-items: center; justify-content: center; margin-right: 10px;
                                 font-weight: bold; font-size: 0.8rem;">PA</span>
                    Performance Analytics
                </h4>
                <p style="color: #4B5563; margin-left: 34px;">Detailed metrics including ROC curves, Precision-Recall curves, and confusion matrices</p>
            </div>

            <div class="feature-card">
                <h4 style="color: #0F2041; display: flex; align-items: center;">
                    <span style="background-color: #1E3A8A; color: white; width: 24px; height: 24px; border-radius: 50%;
                                 display: inline-flex; align-items: center; justify-content: center; margin-right: 10px;
                                 font-weight: bold; font-size: 0.8rem;">IV</span>
                    Interactive Visualizations
                </h4>
                <p style="color: #4B5563; margin-left: 34px;">Dynamic charts and graphs for feature analysis and distribution exploration</p>
            </div>

            <div class="feature-card">
                <h4 style="color: #0F2041; display: flex; align-items: center;">
                    <span style="background-color: #1E3A8A; color: white; width: 24px; height: 24px; border-radius: 50%;
                                 display: inline-flex; align-items: center; justify-content: center; margin-right: 10px;
                                 font-weight: bold; font-size: 0.8rem;">RT</span>
                    Real-time Prediction
                </h4>
                <p style="color: #4B5563; margin-left: 34px;">Instant transaction verification with confidence scores</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h2 style="color: #0F2041; margin-bottom: 20px;">Premium Experience</h2>', unsafe_allow_html=True)
        st.markdown(
            """
            <p style="color: #4B5563; margin-bottom: 25px;">Our intuitive interface provides seamless navigation through powerful fraud detection tools:</p>

            <div style="margin-bottom: 30px; background-color: #F8FAFC; padding: 15px; border-radius: 8px;">
                <h4 style="color: #1E3A8A; margin-top: 0;">Model Training & Evaluation</h4>
                <p style="color: #4B5563;">Select your preferred classifier, fine-tune parameters, and train models on your dataset. Evaluate with comprehensive metrics and visualizations.</p>
            </div>

            <div style="margin-bottom: 30px; background-color: #F8FAFC; padding: 15px; border-radius: 8px;">
                <h4 style="color: #1E3A8A; margin-top: 0;">Transaction Verification</h4>
                <p style="color: #4B5563;">Test individual transactions with our real-time prediction tool. Get instant fraud assessments with detailed risk analysis.</p>
            </div>

            <div style="text-align: center; margin-top: 40px;">
                <div style="display: inline-block; padding: 12px 24px; background: linear-gradient(90deg, #0F2041, #1E3A8A);
                            color: white; border-radius: 6px; font-weight: 500;">
                    Begin Your Analysis →
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Divider
    st.markdown('<div class="luxury-divider"></div>', unsafe_allow_html=True)

    # Quick navigation
    st.markdown('<h2 style="color: #0F2041; margin-bottom: 30px; text-align: center;">Explore Our Solutions</h2>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="nav-card">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #0F2041 0%, #1E3A8A 100%);
                            color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center;
                            margin: 0 auto 15px; font-size: 1.5rem; font-weight: bold;">FD</div>
                <h4 style="color: #0F2041;">Fraud Detection Suite</h4>
                <p style="color: #4B5563;">Train and evaluate models with comprehensive performance metrics</p>
                <div style="width: 40px; height: 3px; background: linear-gradient(90deg, #D4AF37, #1E3A8A); margin: 15px auto;"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="nav-card">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #0F2041 0%, #1E3A8A 100%);
                            color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center;
                            margin: 0 auto 15px; font-size: 1.5rem; font-weight: bold;">TV</div>
                <h4 style="color: #0F2041;">Transaction Verification</h4>
                <p style="color: #4B5563;">Analyze individual transactions with real-time fraud detection</p>
                <div style="width: 40px; height: 3px; background: linear-gradient(90deg, #D4AF37, #1E3A8A); margin: 15px auto;"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="nav-card">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #0F2041 0%, #1E3A8A 100%);
                            color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center;
                            margin: 0 auto 15px; font-size: 1.5rem; font-weight: bold;">AP</div>
                <h4 style="color: #0F2041;">About Our Platform</h4>
                <p style="color: #4B5563;">Learn about our advanced fraud detection technology</p>
                <div style="width: 40px; height: 3px; background: linear-gradient(90deg, #D4AF37, #1E3A8A); margin: 15px auto;"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Dataset section
    st.markdown('<div class="luxury-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div style="background-color: #FFFFFF; border-radius: 12px; padding: 30px; margin-top: 30px;
                    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.05); border: 1px solid #F3F4F6;">
            <h2 style="color: #0F2041; margin-bottom: 20px; display: flex; align-items: center;">
                <span style="width: 30px; height: 30px; background-color: #D4AF37; color: white; border-radius: 50%;
                       display: inline-flex; align-items: center; justify-content: center; margin-right: 10px;
                       font-weight: bold;">D</span>
                Premium Dataset
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="background-color: #FFFFFF; border-radius: 0 0 12px 12px; padding: 0 30px 30px 30px; margin-top: -20px;
                    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.05); border: 1px solid #F3F4F6; border-top: none;">
            <p style="color: #4B5563; margin-bottom: 25px;">
                Our solution utilizes a high-quality, anonymized credit card transaction dataset
                featuring advanced security measures and comprehensive feature engineering:
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div style="padding: 20px; background-color: #F8FAFC; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);">
                <h4 style="color: #1E3A8A; margin-bottom: 10px;">Time & Amount</h4>
                <p style="color: #4B5563; margin: 0;">Temporal features and transaction values in Rands (R) for contextual analysis</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div style="padding: 20px; background-color: #F8FAFC; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);">
                <h4 style="color: #1E3A8A; margin-bottom: 10px;">Secured Features</h4>
                <p style="color: #4B5563; margin: 0;">28 PCA-transformed features (V1-V28) ensuring privacy and security</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div style="padding: 20px; background-color: #F8FAFC; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);">
                <h4 style="color: #1E3A8A; margin-bottom: 10px;">Classification</h4>
                <p style="color: #4B5563; margin: 0;">Binary labels for transaction legitimacy (0: Normal, 1: Fraudulent)</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div style="margin-top: 25px; padding: 20px; background-color: #FEF9E7; border-radius: 8px; border-left: 4px solid #D4AF37;">
            <p style="color: #4B5563; margin: 0; font-style: italic;">
                <strong style="color: #D4AF37;">Premium Insight:</strong>
                Our dataset maintains the highest standards of privacy while providing the necessary
                information for state-of-the-art fraud detection algorithms.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
