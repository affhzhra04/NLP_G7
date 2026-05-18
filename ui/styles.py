import streamlit as st


def inject_premium_css():
    """Injects sleek glassmorphism CSS aesthetics mimicking production platforms."""
    st.markdown("""
        <style>
        /* Forces the web page grid body to use the full available device width space */
        .block-container {
            max-width: 100% !important;
            padding-left: 5rem !important;
            padding-right: 5rem !important;
        }
        
        .stApp {
            background-color: #0b0f19;
            color: #94a3b8;
            font-family: 'Inter', system-ui, sans-serif;
        }
        
        /* Logo Identity Layout styling */
        .brand-container {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: -10px;
        }
        .nav-logo {
            font-size: 2.2rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.5px;
        }
        .nav-logo span {
            background: linear-gradient(135deg, #6366f1, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Interface Form Panels */
        .search-container {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 25px;
            backdrop-filter: blur(12px);
        }
        
        /* Interactive Premium Recommendation Cards */
        .premium-card {
            background: linear-gradient(180deg, rgba(20, 26, 43, 0.7) 0%, rgba(12, 16, 28, 0.8) 100%);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 16px;
            display: flex;
            gap: 24px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .premium-card:hover {
            transform: translateY(-2px);
            border-color: rgba(168, 85, 247, 0.4);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.5), 0 0 20px rgba(168, 85, 247, 0.08);
        }
        
        /* Dynamic Cover Arts */
        .cover-frame {
            width: 100px;
            height: 145px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            background: #111524;
            flex-shrink: 0;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .cover-frame img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        /* Tag Chips */
        .pill-metadata {
            background: rgba(99, 102, 241, 0.1);
            color: #818cf8;
            padding: 3px 9px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 500;
            border: 1px solid rgba(99, 102, 241, 0.18);
            display: inline-block;
            margin-right: 6px;
        }
        .score-indicator {
            font-size: 1rem;
            font-weight: 700;
            color: #c084fc;
            background: rgba(192, 132, 252, 0.08);
            padding: 4px 12px;
            border-radius: 8px;
            border: 1px solid rgba(192, 132, 252, 0.2);
        }
        </style>
    """, unsafe_allow_html=True)