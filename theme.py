import streamlit as st

def apply_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&family=Playfair+Display:wght@500&display=swap');
        * { font-family: 'Poppins', sans-serif !important; color: #16314a !important; }
        .stApp { background: linear-gradient(180deg, #f7fbff 0%, #ffffff 100%); }
        .title-container h1 { font-family: 'Playfair Display', serif !important; color: #10293f !important; font-size: 2.2rem; margin: 0; }
        .title-sub { color: #3b556e !important; margin-top: 6px; margin-bottom: 18px; }
        [data-testid="stSidebar"] { background: linear-gradient(180deg, #1f3a6b 0%, #153056 100%) !important; color: #ffffff !important; }
        [data-testid="stSidebar"] * { color: #ffffff !important; }
        .card { background: #ffffff; border-radius: 14px; padding: 16px; margin-bottom: 12px;
                box-shadow: 0 8px 24px rgba(17,36,59,0.06); border: 1px solid #eef4fb; }
        .stButton>button { background: linear-gradient(90deg, #5c84d6, #89aef5) !important; color: white !important;
                           border: none !important; border-radius: 10px !important; padding: 8px 14px !important;
                           font-weight: 600 !important; box-shadow: 0 6px 16px rgba(92,132,214,0.18) !important; }
        .stButton>button:hover { transform: translateY(-2px); }
        @media (max-width: 800px) {
            .title-container h1 { font-size: 1.6rem !important; }
            .card { padding: 12px !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )