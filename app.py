import streamlit as st
import pandas as pd
import numpy as np

# 1. THE ACADEMY CONFIGURATION
st.set_page_config(page_title="Arrow Ops Academy", layout="wide", page_icon="🎓")

# 2. MASTERCLASS STYLING (Coursera/LinkedIn Learning Aesthetic)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .stApp { background-color: #FFFFFF; font-family: 'Inter', sans-serif; }
    
    /* Sidebar: Professional Navigation */
    section[data-testid="stSidebar"] { 
        background-color: #002147 !important; /* Oxford Blue */
    }
    section[data-testid="stSidebar"] * { color: white !important; }

    /* Learning Card Architecture */
    .learning-card {
        background: #FFFFFF;
        padding: 40px;
        border-radius: 20px;
        border: 1px solid #F3F4F6;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05);
        margin-bottom: 30px;
    }

    /* Scenario Badge */
    .scenario-badge {
        background-color: #EBF5FF;
        color: #0056D2; /* Coursera Blue */
        padding: 8px 16px;
        border-radius: 100px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
    }

    /* Premium Buttons */
    .stButton>button {
        background: #0056D2;
        color: white;
        border-radius: 12px;
        font-weight: 600;
        height:
