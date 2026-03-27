import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Arledge Hub", layout="wide")

# 2. Simple Login Logic
def check_password():
    """Returns True if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        # Update these with your preferred login/pass
        if (
            st.session_state["username"] in ["yahya.ouarach@arrow.com", "mafernandez@arrow.com"]
            and st.session_state["password"] == "Arrow2026!"
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username and password.
        st.title("Arledge Hub Login")
        st.text_input("Email", on_change=password_entered, key="username")
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error.
        st.title("Arledge Hub Login")
        st.text_input("Email", on_change=password_entered, key="username")
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

# 3. App Execution
if check_password():
    # --- Everything below only shows AFTER login ---
    
    st.sidebar.button("Log out", on_click=lambda: st.session_state.update({"password_correct": None}))
    
    st.title("Arledge Hub")
    st.markdown("Search for procedures or system codes below.")

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
        # Dropdown Search
        options = [""] + list(df["Process"].unique())
        selected_process = st.selectbox(
            "🔍 Select a process to view details:", 
            options=options,
            index=0,
            placeholder="Choose an option..."
        )

        if selected_process != "":
            detail = df[df["Process"] == selected_process].iloc[0]

            st.subheader(f"Details for: {selected_process}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**System:** {detail.get('System', 'N/A')}")
                st.success(f"**Rationale:** {detail.get('Rationale', 'N/A')}")
            with col2:
                st.warning(f"**Instructions:**\n{detail.get('Instructions', 'N/A')}")
                st.write(f"*Source: {detail.get('File_Source', 'Unknown')}*")
        else:
            st.divider()
            st.info("Please select a process from the dropdown to see its information.")
