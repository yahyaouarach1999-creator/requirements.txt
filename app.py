import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Operations Knowledge Base", layout="wide")

st.title("Line Operations & Logistics Lookup")
st.markdown("Select a process below to view system codes, instructions, and rationales.")

# Load the data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv")
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # 1. Dropdown Search (The primary interaction)
    # We add an empty string at the start so the page starts "blank"
    options = [""] + list(df["Process"].unique())
    selected_process = st.selectbox(
        "🔍 Select or type a process to view details:", 
        options=options,
        index=0,
        placeholder="Choose an option..."
    )

    # 2. Conditional Display: Only show data if a process is selected
    if selected_process != "":
        # Filter the dataframe for the specific selection
        detail = df[df["Process"] == selected_process].iloc[0]

        st.subheader(f"Details for: {selected_process}")
        
        # Main Info Cards
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**System:** {detail.get('System', 'N/A')}")
            st.success(f"**Rationale:** {detail.get('Rationale', 'N/A')}")
        with col2:
            st.warning(f"**Instructions:**\n{detail.get('Instructions', 'N/A')}")
            st.write(f"*Source: {detail.get('File_Source', 'Unknown')}*")
        
        # Optional: Show the raw row data in a small table below
        with st.expander("View Raw Data Row"):
            st.table(pd.DataFrame(detail).T)

    else:
        # Initial Landing State
        st.divider()
        st.info("The dashboard is ready. Use the dropdown above to look up a specific process.")
        st.caption("Tip: You can click the dropdown and start typing to filter the list instantly.")

else:
    st.warning("No data found. Please check your 'data.csv' file.")
