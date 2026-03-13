import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import re
import os

st.set_page_config(page_title="Arledge", page_icon="🏹", layout="wide")

# -------------------------
# LOAD USERS
# -------------------------
with open("users.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

name, auth_status, username = authenticator.login("Login", "main")

if auth_status is False:
    st.error("Incorrect username or password")

if auth_status is None:
    st.warning("Please enter your credentials")

if auth_status:

    authenticator.logout("Logout", "sidebar")

    st.sidebar.title("🏹 Arledge")
    st.sidebar.write(f"Welcome **{name}**")

    page = st.sidebar.radio(
        "Navigation",
        ["Knowledge Base", "Admin Dashboard"]
    )

    # -------------------------
    # LOAD DATABASE
    # -------------------------
    @st.cache_data
    def load_data():
        if os.path.exists("master_ops_database.csv"):
            return pd.read_csv("master_ops_database.csv").fillna("")
        return pd.DataFrame(columns=["System","Process","Instructions","Rationale","File_Source"])

    df = load_data()

    # -------------------------
    # RULE FORMATTER
    # -------------------------
    def format_rules(text):

        steps = re.split(r'(?:\d+\.|\n-|\n\*)', text)

        formatted = ""

        count = 1

        for s in steps:

            s = s.strip()

            if s:
                formatted += f"**Rule {count}:** {s}\n\n"
                count += 1

        return formatted

    # -------------------------
    # SEARCH FUNCTION
    # -------------------------
    def search(query):

        keywords = query.lower().split()

        mask = df.apply(
            lambda row: all(
                k in str(row).lower() for k in keywords
            ),
            axis=1
        )

        return df[mask]

    # -------------------------
    # KNOWLEDGE BASE
    # -------------------------
    if page == "Knowledge Base":

        st.title("Knowledge Base")

        query = st.text_input(
            "Search process",
            placeholder="ex: credit venlo partial"
        )

        if query:

            results = search(query)

            st.write(f"{len(results)} results found")

            if not results.empty:

                for _, row in results.iterrows():

                    with st.expander(
                        f"{row['System']} ▸ {row['Process']}"
                    ):

                        st.markdown("### Instructions")

                        st.markdown(
                            format_rules(row["Instructions"])
                        )

            else:

                st.warning("No results found")

        else:

            st.info("Enter keywords to search")

    # -------------------------
    # ADMIN DASHBOARD
    # -------------------------
    if page == "Admin Dashboard":

        st.title("Admin Dashboard")

        edited_df = st.data_editor(
            df,
            use_container_width=True,
            num_rows="dynamic"
        )

        if st.button("Save Changes"):

            edited_df.to_csv(
                "master_ops_database.csv",
                index=False
            )

            st.success("Database Updated")

        st.divider()

        uploaded = st.file_uploader(
            "Upload new database CSV"
        )

        if uploaded:

            new_df = pd.read_csv(uploaded)

            st.dataframe(new_df)

            if st.button("Import Database"):

                new_df.to_csv(
                    "master_ops_database.csv",
                    index=False
                )

                st.success("New database imported")
