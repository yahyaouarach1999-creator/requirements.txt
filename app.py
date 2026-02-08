import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Sales Ops Portal", layout="wide")

try:
    # This 'sep=None' is the magic fix for the 'nan' issue
    df = pd.read_csv("sop_data.csv", sep=None, engine='python')
    
    # Remove hidden spaces from column names
    df.columns = df.columns.str.strip()
    
    # Replace any empty/missing data with a clean message instead of 'nan'
    df = df.fillna("Information pending")

    st.title("🛡️ Sales Ops Knowledge Hub")
    
    search = st.text_input("🔍 Search (e.g., Refund, Venlo, Email)")

    if search:
        # Search across all columns
        mask = df.apply(lambda x: x.astype(str).str.contains(search, case=False)).any(axis=1)
        filtered = df[mask]
        
        for _, row in filtered.iterrows():
            # Using .get ensures we find the column even if it's slightly misspelled
            p_name = row.get('Process', 'Process')
            with st.expander(f"📖 {p_name}"):
                st.write(f"**System:** {row.get('System', 'N/A')}")
                st.write(f"**Instructions:** {row.get('Instructions', 'No instructions found')}")
                
                pic = row.get('Screenshot_URL', '')
                if str(pic).startswith('http'):
                    st.image(pic)
    else:
        st.info("Search for a task above.")

except Exception as e:
    st.error(f"Data Error: {e}")
