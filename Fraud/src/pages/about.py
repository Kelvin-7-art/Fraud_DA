import streamlit as st

def show_about_page():
    # Custom CSS for premium about page
    st.markdown("""
    <style>
    /* Fix for container issues */
    .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }
    div[data-testid="stElementContainer"] {
        margin: 0 !important;
        padding: 0 !important;
    }
    .stMarkdown div[data-testid="stMarkdownContainer"] {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .premium-header {
        background: linear-gradient(90deg, #0F2041 0%, #1E3A8A 100%);
        padding: 40px;
        border-radius: 15px;
        margin-bottom: 40px;
        color: white;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .premium-header::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" stroke="rgba(255,255,255,0.05)" stroke-width="1.5" fill="none"/></svg>') repeat;
        opacity: 0.4;
    }
    .elegant-divider {
        height: 2px;
        background: linear-gradient(90deg, rgba(30, 58, 138, 0.1), rgba(30, 58, 138, 0.5), rgba(30, 58, 138, 0.1));
        margin: 30px 0;
        border: none;
    }
    .section-title {
        text-align: center;
        color: #1E3A8A;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 30px;
        position: relative;
        padding-bottom: 15px;
    }
    .section-title::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 3px;
        background: linear-gradient(90deg, #D4AF37, #FBE173);
        border-radius: 2px;
    }
    .premium-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 10px;
        position: relative;
        z-index: 10;
    }
    .premium-subtitle {
        font-size: 1.1rem;
        font-weight: 400;
        opacity: 0.8;
        position: relative;
        z-index: 10;
    }
    .premium-gold {
        color: #D4AF37;
    }
    .premium-card {
        background-color: white;
        border-radius: 12px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.05);
        border: 1px solid #F3F4F6;
        position: relative;
        overflow: hidden;
    }
    .feature-icon {
        font-size: 1.5rem;
        margin-right: 10px;
        color: #D4AF37;
    }
    .premium-info-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.05);
        border: 1px solid #F3F4F6;
    }
    .team-card {
        background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFC 100%);
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.03);
        border: 1px solid #F3F4F6;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .team-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.06);
    }
    .team-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background-color: #E5E7EB;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 15px auto;
        border: 3px solid #F3F4F6;
        font-size: 2rem;
        color: #64748B;
    }
    .team-name {
        color: #0F2041;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .team-role {
        color: #D4AF37;
        font-weight: 500;
        font-size: 0.9rem;
        margin-bottom: 10px;
    }
    .premium-badge {
        display: inline-block;
        padding: 3px 10px;
        background: linear-gradient(90deg, #D4AF37 0%, #FBE173 100%);
        color: #0F2041;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-left: 8px;
        vertical-align: middle;
    }
    .feature-item {
        display: flex;
        align-items: flex-start;
        margin-bottom: 20px;
    }
    .feature-content {
        flex-grow: 1;
    }
    .feature-title {
        color: #0F2041;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .feature-desc {
        color: #64748B;
        font-size: 0.9rem;
        margin: 0;
    }
    .premium-card p {
        color: #0F2041;
        font-weight: 500;
    }
    .premium-info-card p {
        color: #0F2041;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Premium header
    st.markdown("""
    <div class="premium-header">
        <h1 class="premium-title">Fraud Detection <span class="premium-gold">Suite</span></h1>
        <p class="premium-subtitle">Enterprise-grade solution for secure transaction processing</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Overview and features in a premium layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.container():
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            
            # Header with title and badge
            st.markdown('<div style="display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">', unsafe_allow_html=True)
            st.markdown('<h2 class="section-title" style="margin-bottom: 0;">Platform Overview</h2>', unsafe_allow_html=True)
            st.markdown('<span class="premium-badge" style="margin-left: 10px;">ENTERPRISE</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Elegant divider
            st.markdown('<hr class="elegant-divider">', unsafe_allow_html=True)
            
            # Overview text with improved visibility
            st.markdown("""
            <div style="color: #0F2041; font-size: 1rem; font-weight: 500; line-height: 1.6; margin-bottom: 20px; padding: 5px 0;">
                Our premium fraud detection solution offers state-of-the-art security for financial institutions
                and payment processors. Built with advanced machine learning algorithms, our platform
                delivers exceptional accuracy in identifying fraudulent transactions while minimizing false positives.
            </div>
            """, unsafe_allow_html=True)
            
            # Premium features header
            st.markdown('<h3 style="color: #1E3A8A; margin-top: 25px; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid rgba(30, 58, 138, 0.2);">Premium Features</h3>', unsafe_allow_html=True)
            
            # Feature items with improved visibility
            feature_items = [
                {
                    "icon": "ML",
                    "title": "Multiple ML Models",
                    "desc": "Train and compare different algorithms including Random Forest, SVM, Logistic Regression, and Neural Networks"
                },
                {
                    "icon": "PM",
                    "title": "Comprehensive Performance Metrics",
                    "desc": "Evaluate model performance with accuracy, precision, recall, F1-score, ROC AUC, and PR AUC metrics"
                },
                {
                    "icon": "IV",
                    "title": "Interactive Visualizations",
                    "desc": "Explore data with dynamic, interactive charts for better understanding of feature distributions"
                },
                {
                    "icon": "RT",
                    "title": "Real-time Transaction Verification",
                    "desc": "Test individual transactions with instant fraud detection and comprehensive risk assessment"
                }
            ]
            
            # Display each feature item with enhanced visibility
            for item in feature_items:
                cols = st.columns([1, 5])
                with cols[0]:
                    st.markdown(
                        f'<div style="width: 40px; height: 40px; background-color: #1E3A8A; '
                        f'color: white; border-radius: 50%; display: flex; align-items: center; '
                        f'justify-content: center; font-weight: bold; font-size: 0.9rem;">{item["icon"]}</div>',
                        unsafe_allow_html=True
                    )
                with cols[1]:
                    # Title with improved visibility
                    st.markdown(f'<div style="color: #0F2041; font-weight: 600; font-size: 1.05rem; margin-bottom: 8px;">{item["title"]}</div>', unsafe_allow_html=True)
                    # Description with improved visibility
                    st.markdown(f'<div style="color: #0F2041; font-weight: 500; font-size: 0.9rem; line-height: 1.4;">{item["desc"]}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Dataset information in a premium card
        with st.container():
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            
            # Dataset Intelligence header with section-title style
            st.markdown('<h2 class="section-title">Dataset Intelligence</h2>', unsafe_allow_html=True)
            
            # Elegant divider
            st.markdown('<hr class="elegant-divider">', unsafe_allow_html=True)
            
            # Description
            st.markdown("""
            Our platform leverages highly secure, anonymized credit card transaction data engineered 
            for optimal fraud detection performance:
            """)
            
            # Feature grid with 2x2 layout
            col1, col2 = st.columns(2)
            
            with col1:
                with st.container():
                    st.markdown("""
                    <div style="background-color: #F8FAFC; padding: 20px; border-radius: 8px;">
                        <h4 style="color: #1E3A8A; margin-top: 0;">Temporal Features</h4>
                        <p style="color: #0F2041; margin-bottom: 0; font-size: 0.9rem; font-weight: 600;">Time elapsed between transactions for pattern analysis</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                
                with st.container():
                    st.markdown("""
                    <div style="background-color: #F8FAFC; padding: 20px; border-radius: 8px;">
                        <h4 style="color: #1E3A8A; margin-top: 0;">PCA Features (V1-V28)</h4>
                        <p style="color: #0F2041; margin-bottom: 0; font-size: 0.9rem; font-weight: 600;">Privacy-protected transformed features</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                with st.container():
                    st.markdown("""
                    <div style="background-color: #F8FAFC; padding: 20px; border-radius: 8px;">
                        <h4 style="color: #1E3A8A; margin-top: 0;">Transaction Amount</h4>
                        <p style="color: #0F2041; margin-bottom: 0; font-size: 0.9rem; font-weight: 600;">Rand (R) value of each transaction</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                
                with st.container():
                    st.markdown("""
                    <div style="background-color: #F8FAFC; padding: 20px; border-radius: 8px;">
                        <h4 style="color: #1E3A8A; margin-top: 0;">Classification</h4>
                        <p style="color: #0F2041; margin-bottom: 0; font-size: 0.9rem; font-weight: 600;">Binary labels for legitimate (0) vs fraudulent (1) transactions</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Security note
            st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
            with st.container():
                st.markdown("""
                <div style="background-color: #0F2041; color: white; padding: 20px; border-radius: 8px;">
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="font-size: 1.5rem; margin-right: 15px;">🔒</div>
                        <div style="font-weight: 600;">Enterprise-Grade Security</div>
                    </div>
                    <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">
                        All data is anonymized using advanced PCA transformation techniques to ensure
                        privacy compliance while maintaining detection accuracy.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        # Project information card
        with st.container():
            st.markdown('<div class="premium-info-card">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: #0F2041; margin-top: 0; padding-bottom: 10px; border-bottom: 2px solid rgba(30, 58, 138, 0.2);">Project Details</h3>', unsafe_allow_html=True)
            
            # Project details as a table for better layout
            project_details = [
                {"label": "Version", "value": "1.0.0"},
                {"label": "Last Updated", "value": "October 2025"},
                {"label": "Status", "value": '<span style="color: #10B981; display: flex; align-items: center;"><span style="width: 8px; height: 8px; background-color: #10B981; border-radius: 50%; margin-right: 6px;"></span>Active</span>'}
            ]
            
            for detail in project_details:
                col_label, col_value = st.columns([1, 1])
                with col_label:
                    st.markdown(f'<span style="color: #344054; font-weight: 500;">{detail["label"]}</span>', unsafe_allow_html=True)
                with col_value:
                    st.markdown(f'<span style="font-weight: 500; color: #0F2041;">{detail["value"]}</span>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Technology stack
        with st.container():
            st.markdown('<div class="premium-info-card">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: #0F2041; margin-top: 0; padding-bottom: 10px; border-bottom: 2px solid rgba(30, 58, 138, 0.2);">Technology Stack</h3>', unsafe_allow_html=True)
            
            # Tech stack items
            tech_stack = [
                {"icon": "Py", "color": "#3B82F6", "name": "Python", "description": "Core programming language"},
                {"icon": "St", "color": "#FF4B4B", "name": "Streamlit", "description": "UI framework"},
                {"icon": "Sk", "color": "#F59E0B", "name": "scikit-learn", "description": "Machine learning library"}
            ]
            
            for tech in tech_stack:
                cols = st.columns([1, 3])
                with cols[0]:
                    st.markdown(f"""
                    <div style="width: 40px; height: 40px; background-color: #F8FAFC; border-radius: 8px; 
                    display: flex; align-items: center; justify-content: center;">
                        <span style="color: {tech['color']};">{tech['icon']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with cols[1]:
                    st.markdown(f"""
                    <div style="font-weight: 500; color: #0F2041;">{tech['name']}</div>
                    <div style="font-size: 0.8rem; color: #0F2041; font-weight: 600;">{tech['description']}</div>
                    """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Data source
        with st.container():
            st.markdown('<div class="premium-info-card">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: #0F2041; margin-top: 0; padding-bottom: 10px; border-bottom: 2px solid rgba(30, 58, 138, 0.2);">Data Source</h3>', unsafe_allow_html=True)
            
            # Improved text visibility with explicit styling
            st.markdown("""
            <div style="color: #0F2041; font-weight: 500; margin-bottom: 15px; font-size: 0.95rem;">
                This platform utilizes the renowned Credit Card Fraud Detection dataset, 
                recognized as the industry standard for fraud detection research and development.
            </div>
            """, unsafe_allow_html=True)
            
            # Custom warning with better visibility
            st.markdown("""
            <div style="background-color: #FFF8E1; border-left: 4px solid #FFA000; padding: 12px 15px; margin: 15px 0; border-radius: 4px;">
                <strong style="color: #B45309;">Note:</strong>
                <span style="color: #0F2041; font-weight: 500;"> All data has been anonymized to protect customer privacy while maintaining analytical value.</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Technical implementation with premium styling
    with st.container():
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        
        # Technical Architecture header with section-title style
        st.markdown('<h2 class="section-title">Technical Architecture</h2>', unsafe_allow_html=True)
        
        # Elegant divider
        st.markdown('<hr class="elegant-divider">', unsafe_allow_html=True)
        
        # Description with improved visibility - making sure text color is clearly visible
        st.markdown("""
        <div style="color: #0F2041; font-size: 1rem; font-weight: 500; margin-bottom: 25px; line-height: 1.5;">
            Our enterprise-grade fraud detection platform implements a comprehensive suite of machine learning 
            algorithms and evaluation metrics to provide the highest level of transaction security.
        </div>
        """, unsafe_allow_html=True)
        
        # Algorithm cards in a grid with section-style header
        st.markdown('<h3 style="color: #1E3A8A; margin-top: 20px; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid rgba(30, 58, 138, 0.2);">Machine Learning Algorithms</h3>', unsafe_allow_html=True)
        
        # Define the algorithms
        algorithms = [
            {
                "icon": "RF",
                "name": "Random Forest",
                "description": """
                An ensemble learning method that constructs multiple decision trees during training 
                and outputs the class that is the mode of the classes of the individual trees.
                """,
                "tags": ["Ensemble", "High Accuracy"]
            },
            {
                "icon": "SVM", 
                "name": "Support Vector Machine",
                "description": """
                A supervised learning model that analyzes data for classification by finding the optimal hyperplane 
                that separates classes in high-dimensional space.
                """,
                "tags": ["Kernel Methods", "Margin Maximization"]
            },
            {
                "icon": "LR",
                "name": "Logistic Regression",
                "description": """
                A statistical model that uses a logistic function to model a binary dependent variable, 
                estimating probabilities using a logistic function.
                """,
                "tags": ["Probabilistic", "Interpretable"]
            },
            {
                "icon": "NN",
                "name": "Neural Network",
                "description": """
                A deep learning approach inspired by biological neural networks, capable of capturing 
                complex non-linear relationships in data.
                """,
                "tags": ["Deep Learning", "Pattern Recognition"]
            }
        ]
        
        # Create a 2x2 grid for the algorithms
        col1, col2 = st.columns(2)
        
        # First row
        with col1:
            with st.container():
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%); 
                            border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">
                    <div style="width: 50px; height: 50px; background-color: #1E3A8A; color: white; 
                                border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                                margin-bottom: 15px; font-weight: bold; font-size: 1.2rem;">{algorithms[0]["icon"]}</div>
                    <h3 style="color: #0F2041; margin-top: 0;">{algorithms[0]["name"]}</h3>
                    <p style="color: #0F2041; font-size: 0.9rem; font-weight: 600;">{algorithms[0]["description"]}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            with st.container():
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%); 
                            border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">
                    <div style="width: 50px; height: 50px; background-color: #1E3A8A; color: white; 
                                border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                                margin-bottom: 15px; font-weight: bold; font-size: 1.2rem;">{algorithms[1]["icon"]}</div>
                    <h3 style="color: #0F2041; margin-top: 0;">{algorithms[1]["name"]}</h3>
                    <p style="color: #0F2041; font-size: 0.9rem; font-weight: 600;">{algorithms[1]["description"]}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Second row
        col3, col4 = st.columns(2)
        
        with col3:
            with st.container():
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%); 
                            border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">
                    <div style="width: 50px; height: 50px; background-color: #1E3A8A; color: white; 
                                border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                                margin-bottom: 15px; font-weight: bold; font-size: 1.2rem;">{algorithms[2]["icon"]}</div>
                    <h3 style="color: #0F2041; margin-top: 0;">{algorithms[2]["name"]}</h3>
                    <p style="color: #0F2041; font-size: 0.9rem; font-weight: 600;">{algorithms[2]["description"]}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col4:
            with st.container():
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%); 
                            border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">
                    <div style="width: 50px; height: 50px; background-color: #1E3A8A; color: white; 
                                border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                                margin-bottom: 15px; font-weight: bold; font-size: 1.2rem;">{algorithms[3]["icon"]}</div>
                    <h3 style="color: #0F2041; margin-top: 0;">{algorithms[3]["name"]}</h3>
                    <p style="color: #0F2041; font-size: 0.9rem; font-weight: 600;">{algorithms[3]["description"]}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Performance metrics section with light background for better visibility
        st.markdown("""
        <div style="background-color: #F8FAFC; border-radius: 12px; padding: 25px; color: #0F2041; margin-top: 30px; border: 1px solid #E5E7EB;">
            <h3 style="margin-top: 0; color: #1E3A8A; padding-bottom: 15px; border-bottom: 1px solid rgba(30, 58, 138, 0.2);">Performance Metrics</h3>
            <p style="color: #0F2041; margin-bottom: 20px; font-weight: 500;">
                Our platform provides comprehensive evaluation metrics for model performance assessment.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Metrics categories in a grid
        metric_categories = [
            {
                "title": "Classification Metrics",
                "items": ["Accuracy", "Precision", "Recall", "F1-score"]
            },
            {
                "title": "Probability Metrics",
                "items": ["ROC AUC", "PR AUC", "Log Loss", "Brier Score"]
            },
            {
                "title": "Visualizations",
                "items": ["Confusion Matrix", "ROC Curve", "Precision-Recall Curve", "Feature Importance"]
            }
        ]
        
        metric_cols = st.columns(3)
        for i, category in enumerate(metric_categories):
            with metric_cols[i]:
                st.markdown(f"""
                <div style="background-color: #FFFFFF; padding: 20px; border-radius: 8px; 
                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); border: 1px solid #E5E7EB;">
                    <h4 style="margin-top: 0; color: #1E3A8A; font-weight: 600;">{category['title']}</h4>
                    <ul style="color: #0F2041; padding-left: 20px; margin-bottom: 0; font-weight: 500;">
                        {"".join([f'<li style="margin-bottom: 8px;">{item}</li>' for item in category['items'][:-1]])}
                        <li>{category['items'][-1]}</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        # Add Fraud Detection footer with improved visibility
        st.markdown("""
        <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #E5E7EB;">
            <p style="color: #1E3A8A; font-size: 0.9rem; font-weight: 600;">Fraud Detection Suite © 2025</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Development team
    with st.container():
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        
        # Team section title
        st.markdown('<h2 class="section-title">Our Team</h2>', unsafe_allow_html=True)
        
        # Elegant divider
        st.markdown('<hr class="elegant-divider">', unsafe_allow_html=True)
        
        # Team members in a grid
        team_members = [
            {
                "initials": "KK",
                "name": "Kelvin Kgarudi"
            },
            {
                "initials": "DB",
                "name": "Dylan Badenhorst"
            },
            {
                "initials": "KM",
                "name": "Karabo Matlhoi"
            },
            {
                "initials": "MM",
                "name": "Moshoeshoe Mokhachane"
            }
        ]
        
        # Create a 4-column layout for team members
        team_cols = st.columns(4)
        for i, member in enumerate(team_members):
            with team_cols[i]:
                st.markdown(f"""
                <div style="background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFC 100%); 
                            border-radius: 12px; padding: 25px; text-align: center; 
                            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.03); border: 1px solid #F3F4F6;">
                    <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #1E3A8A 0%, #0F2041 100%); 
                                color: white; border-radius: 50%; display: flex; align-items: center; 
                                justify-content: center; margin: 0 auto 15px; font-size: 1.5rem; 
                                font-weight: bold; border: 2px solid #D4AF37;">{member["initials"]}</div>
                    <div style="font-weight: bold; color: #0F2041; font-size: 1.1rem; margin-bottom: 5px;">{member["name"]}</div>
                    <div style="width: 40px; height: 2px; background: linear-gradient(90deg, #D4AF37, #FBE173); margin: 10px auto;"></div>
                </div>
                """, unsafe_allow_html=True)
        
        # Add Fraud Detection footer
        st.markdown("""
        <div style="text-align: center; margin-top: 20px;">
            <p style="color: #1E3A8A; font-size: 0.9rem; font-weight: 600;">Fraud Detection Suite © 2025</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Resources and Documentation section
    with st.container():
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        
        # Header as section title
        st.markdown('<h2 class="section-title">Resources & Documentation</h2>', unsafe_allow_html=True)
        
        # Elegant divider
        st.markdown('<hr class="elegant-divider">', unsafe_allow_html=True)
        
        # First row
        col1, col2 = st.columns(2)
        
        # Data Sources
        with col1:
            with st.container():
                st.markdown("""
                <div style="padding: 10px 0;">
                    <h3 style="color: #1E3A8A; margin-top: 0; padding-bottom: 10px; border-bottom: 2px solid rgba(30, 58, 138, 0.2);">Data Sources</h3>
                    <ul style="color: #0F2041; padding-left: 20px; font-weight: 600;">
                        <li style="margin-bottom: 8px;">
                            <strong>Credit Card Fraud Detection Dataset</strong>
                            <div style="font-size: 0.85rem; margin-top: 3px; color: #344054; font-weight: 500;">Industry standard for fraud detection research</div>
                        </li>
                        <li style="margin-bottom: 8px;">
                            <strong>Anonymized Financial Transaction Data</strong>
                            <div style="font-size: 0.85rem; margin-top: 3px; color: #344054; font-weight: 500;">Privacy-protected transaction records</div>
                        </li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        # Documentation
        with col2:
            with st.container():
                st.markdown("""
                <div style="padding: 10px 0;">
                    <h3 style="color: #1E3A8A; margin-top: 0; padding-bottom: 10px; border-bottom: 2px solid rgba(30, 58, 138, 0.2);">Documentation</h3>
                    <ul style="color: #0F2041; padding-left: 20px; font-weight: 600;">
                        <li style="margin-bottom: 8px;">
                            <strong>scikit-learn Documentation</strong>
                            <div style="font-size: 0.85rem; margin-top: 3px; color: #344054; font-weight: 500;">Machine learning framework reference</div>
                        </li>
                        <li style="margin-bottom: 8px;">
                            <strong>Streamlit Documentation</strong>
                            <div style="font-size: 0.85rem; margin-top: 3px; color: #344054; font-weight: 500;">UI framework implementation guide</div>
                        </li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        # Second row
        col3, col4 = st.columns(2)
        
        # Research Papers
        with col3:
            with st.container():
                st.markdown("""
                <div style="padding: 10px 0;">
                    <h3 style="color: #1E3A8A; margin-top: 0; padding-bottom: 10px; border-bottom: 2px solid rgba(30, 58, 138, 0.2);">Research Papers</h3>
                    <ul style="color: #0F2041; padding-left: 20px; font-weight: 600;">
                        <li style="margin-bottom: 8px;">
                            <strong>"Machine Learning for Fraud Detection"</strong>
                            <div style="font-size: 0.85rem; margin-top: 3px; color: #344054; font-weight: 500;">Academic research on financial security</div>
                        </li>
                        <li style="margin-bottom: 8px;">
                            <strong>"Deep Learning Approaches in Finance"</strong>
                            <div style="font-size: 0.85rem; margin-top: 3px; color: #344054; font-weight: 500;">Neural network applications in fraud detection</div>
                        </li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        # Industry Standards
        with col4:
            with st.container():
                st.markdown("""
                <div style="padding: 10px 0;">
                    <h3 style="color: #1E3A8A; margin-top: 0; padding-bottom: 10px; border-bottom: 2px solid rgba(30, 58, 138, 0.2);">Industry Standards</h3>
                    <ul style="color: #0F2041; padding-left: 20px; font-weight: 600;">
                        <li style="margin-bottom: 8px;">
                            <strong>PCI DSS Compliance</strong>
                            <div style="font-size: 0.85rem; margin-top: 3px; color: #344054; font-weight: 500;">Payment Card Industry Data Security Standard</div>
                        </li>
                        <li style="margin-bottom: 8px;">
                            <strong>ISO 27001</strong>
                            <div style="font-size: 0.85rem; margin-top: 3px; color: #344054; font-weight: 500;">Information security management standards</div>
                        </li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        # Add Fraud Detection footer
        st.markdown("""
        <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #E5E7EB;">
            <p style="color: #1E3A8A; font-size: 0.9rem; font-weight: 600;">Fraud Detection Suite © 2025</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    