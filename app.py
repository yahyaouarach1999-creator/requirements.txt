import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Operations Knowledge Base", layout="wide")

st.title("Line Operations & Logistics Lookup")
st.markdown("Search for procedures, system codes, or contact emails below.")

# Load the data
@st.cache_data
def load_data():
    # We use 'header=0' because your data has a clear header row
    df = pd.read_csv("data.csv")
    return df

try:
    df = load_data()

    # Search bar
    search_query = st.text_input("🔍 Search by System, Process, or Keyword (e.g., 'Unity', 'Reno', 'Email')", "")

    if search_query:
        # Filter logic: search across all columns
        mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
        filtered_df = df[mask]
    else:
        filtered_df = df

    # Display results
    st.subheader(f"Found {len(filtered_df)} Results")
    
    # Using a dataframe display for a clean UI
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    # Detailed view if a user wants to see specific instructions clearly
    if len(filtered_df) > 0:
        st.divider()
        st.subheader("Detail View")
        selected_process = st.selectbox("Select a process to see full instructions:", filtered_df["Process"].unique())
        
        detail = filtered_df[filtered_df["Process"] == selected_process].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**System:** {detail['System']}")
            st.success(f"**Rationale:** {detail['Rationale']}")
        with col2:
            st.warning(f"**Instructions:**\n{detail['Instructions']}")
            st.write(f"*Source: {detail['File_Source']}*")

except Exception as e:
    st.error(f"Error loading CSV: {e}")
    st.info("Make sure your CSV file is named 'data.csv' and is in the same folder as this script.")
