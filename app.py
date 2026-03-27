import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# 1. Page Configuration
st.set_page_config(page_title="Arledge Hub", layout="wide")

# 2. Authentication Setup
# In a production app, move these to a separate 'config.yaml' file
credentials = {
    "usernames": {
        "yahya": {
            "name": "Yahya Ouarach",
            "password": "your_password_1", # Use hashed passwords in production
            "email": "yahya.ouarach@arrow.com"
        },
        "mafernandez": {
            "name": "MA Fernandez",
            "password": "your_password_2",
            "email": "mafernandez@arrow.com"
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "arledge_hub_cookie",
    "signature_key",
    cookie_expiry_days=30
)

# Render the login widget
name, authentication_status, username = authenticator.login("Login", "main")

# 3. Main App Logic (Only runs if logged in)
if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.title("Arledge Hub")
    st.markdown(f"Welcome back, **{name}**! Search for procedures or system codes below.")

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
            "🔍 Select or type a process to view details:", 
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
            st.info("The hub is ready. Use the dropdown above to look up a specific process.")

elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
