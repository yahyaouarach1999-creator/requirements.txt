import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Operations Knowledge Base", layout="wide")

st.title("Line Operations & Logistics Lookup")
st.markdown("Search for procedures, system codes, or contact emails below.")

# Load the data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv")
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        st.info("Make sure your CSV file is named 'data.csv' and is in the same folder as this script.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # Search bar
    search_query = st.text_input("🔍 Search by System, Process, or Keyword (e.g., 'Unity', 'Reno', 'Email')", "")

    # Logic: Only process and display if there is a search query
    if search_query:
        # Filter logic: search across all columns
        mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
        filtered_df = df[mask]

        # Display results count
        st.subheader(f"Found {len(filtered_df)} Results")
        
        if not filtered_df.empty:
            # Using a dataframe display for a clean UI
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)

            # Detailed view if a user wants to see specific instructions clearly
            st.divider()
            st.subheader("Detail View")
            
            # Ensure "Process" column exists before using unique()
            process_options = filtered_df["Process"].unique()
            selected_process = st.selectbox("Select a process to see full instructions:", process_options)
            
            # Get data for the selected process
            detail = filtered_df[filtered_df["Process"] == selected_process].iloc[0]
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**System:** {detail.get('System', 'N/A')}")
                st.success(f"**Rationale:** {detail.get('Rationale', 'N/A')}")
            with col2:
                st.warning(f"**Instructions:**\n{detail.get('Instructions', 'N/A')}")
                st.write(f"*Source: {detail.get('File_Source', 'Unknown')}*")
        else:
            st.warning("No matches found. Please try a different keyword.")
    else:
        # What the user sees when they first land on the page
        st.info("Welcome! Please enter a search term above to begin browsing the database.")
        
        # Optional: You can show a small tip or a list of common search terms here
        st.write("---")
        st.caption("Common searches: Unity, Logistics, SOP, Contact")
