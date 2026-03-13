import streamlit as st
import pandas as pd
import sqlite3
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import re

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Arledge",
    page_icon="🏹",
    layout="wide"
)

# --------------------------------
# DATABASE CONNECTION
# --------------------------------
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS ops (
System TEXT,
Process TEXT,
Instructions TEXT,
Rationale TEXT,
File_Source TEXT
)
""")
conn.commit()

# --------------------------------
# LOAD USERS
# --------------------------------
with open("users.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

name, auth_status, username = authenticator.login("Login", "main")

# --------------------------------
# LOGIN CHECK
# --------------------------------
if auth_status is False:
    st.error("Invalid username or password")

if auth_status is None:
    st.warning("Enter login credentials")

if auth_status:

    authenticator.logout("Logout", "sidebar")

    # --------------------------------
    # SIDEBAR
    # --------------------------------
    st.sidebar.title("🏹 Arledge")

    page = st.sidebar.radio(
        "Navigation",
        ["Knowledge Base", "Admin Dashboard"]
    )

    st.sidebar.divider()

    st.sidebar.markdown(f"**User:** {name}")

    # --------------------------------
    # LOAD DATABASE
    # --------------------------------
    def load_data():
        df = pd.read_sql("SELECT * FROM ops", conn)
        return df.fillna("")

    df = load_data()

    # --------------------------------
    # RULE FORMATTER
    # --------------------------------
    def format_rules(text):

        rules = re.split(r'\d+\.', text)

        formatted = ""

        for i, r in enumerate(rules):
            r = r.strip()

            if r:
                formatted += f"**Rule {i}:** {r}\n\n"

        return formatted if formatted else text

    # --------------------------------
    # SEARCH ENGINE
    # --------------------------------
    def search_db(query):

        keywords = query.lower().split()

        df_lower = df.astype(str).apply(lambda x: x.str.lower())

        mask = df_lower.apply(
            lambda row: all(k in " ".join(row) for k in keywords),
            axis=1
        )

        return df[mask]

    # --------------------------------
    # KNOWLEDGE BASE
    # --------------------------------
    if page == "Knowledge Base":

        st.title("Knowledge Base")

        query = st.text_input(
            "🔎 Search Processes",
            placeholder="ex: credit venlo partial"
        )

        if query:

            results = search_db(query)

            st.write(f"{len(results)} results found")

            if len(results) > 0:

                for _, row in results.iterrows():

                    with st.expander(
                        f"⚙️ {row['System']} ▸ {row['Process']}"
                    ):

                        st.markdown("### Instructions")

                        st.markdown(
                            format_rules(row["Instructions"])
                        )

            else:

                st.warning("No matches found")

        else:

            st.info("Type keywords to search")

    # --------------------------------
    # ADMIN DASHBOARD
    # --------------------------------
    if page == "Admin Dashboard":

        st.title("Admin Dashboard")

        tab1, tab2, tab3 = st.tabs([
            "Database Editor",
            "Upload Data",
            "Analytics"
        ])

        # --------------------------------
        # DATABASE EDITOR
        # --------------------------------
        with tab1:

            edited_df = st.data_editor(
                df,
                num_rows="dynamic",
                use_container_width=True
            )

            if st.button("Save Database"):

                cursor.execute("DELETE FROM ops")

                for _, r in edited_df.iterrows():

                    cursor.execute(
                        "INSERT INTO ops VALUES (?,?,?,?,?)",
                        (
                            r["System"],
                            r["Process"],
                            r["Instructions"],
                            r["Rationale"],
                            r["File_Source"]
                        )
                    )

                conn.commit()

                st.success("Database Updated")

        # --------------------------------
        # CSV UPLOAD
        # --------------------------------
        with tab2:

            uploaded = st.file_uploader(
                "Upload CSV Database"
            )

            if uploaded:

                new_df = pd.read_csv(uploaded)

                st.dataframe(new_df)

                if st.button("Import Data"):

                    cursor.execute("DELETE FROM ops")

                    for _, r in new_df.iterrows():

                        cursor.execute(
                            "INSERT INTO ops VALUES (?,?,?,?,?)",
                            (
                                r["System"],
                                r["Process"],
                                r["Instructions"],
                                r["Rationale"],
                                r["File_Source"]
                            )
                        )

                    conn.commit()

                    st.success("New Database Imported")

        # --------------------------------
        # ANALYTICS
        # --------------------------------
        with tab3:

            st.subheader("Database Statistics")

            col1, col2 = st.columns(2)

            col1.metric("Total Processes", len(df))

            col2.metric(
                "Systems",
                df["System"].nunique()
            )

            st.bar_chart(
                df["System"].value_counts()
            )
