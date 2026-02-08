import streamlit as st
import pandas as pd
import numpy as np

# 1. CORE ARCHITECTURE
st.set_page_config(page_title="Arrow Ops Masterclass", layout="wide", page_icon="🏹")

# 2. ELITE DARK THEME (Graphite & High-Contrast Blue)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&family=Inter:wght@400;700&display=swap');

    .stApp {
        background-color: #0B0E14; /* Midnight Graphite */
        color: #D1D5DB;
        font-family: 'Inter', sans-serif;
    }

    /* Professional Glass Cards */
    .sop-card {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 30px;
        margin-bottom: 20px;
    }
    
    /* Search Bar Professionalism */
    .stTextInput input {
        background-color: #0B0E14 !important;
        border: 1px solid #58A6FF !important;
        color: #58A6FF !important;
        font-family: 'Roboto Mono', monospace;
    }

    /* Terminal-style Link Buttons */
    .app-link {
        display: inline-block;
        padding: 10px 20px;
        margin-right: 10px;
        border: 1px solid #30363D;
        border-radius: 5px;
        color: #8B949E;
        text-decoration: none;
        font-size: 12px;
        font-weight: bold;
        transition: 0.3s;
    }
    .app-link:hover {
        border-color: #58A6FF;
        color: #58A6FF;
        background: rgba(88, 166, 255, 0.1);
    }

    /* Strategic Labeling */
    .strat-header {
        color: #58A6FF;
        text-transform: uppercase;
        font-size: 0.8em;
        letter
