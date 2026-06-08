import streamlit as st
import pandas as pd
import os

# ==============================================================================
# PAGE CONFIG
# ==============================================================================
st.set_page_config(
    page_title="Arledge Hub",
    layout="wide"
)

# ==============================================================================
# SESSION STATE
# ==============================================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_role" not in st.session_state:
    st.session_state.user_role = "User"

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# ==============================================================================
# LOGIN
# ==============================================================================
def render_login():

    st.title("🛡️ ARLEDGE HUB")
    st.caption("Operations & Logistics Management Platform")

    with st.form("login_form"):

        email = st.text_input(
            "Corporate Email",
            placeholder="user@arrow.com"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        submit = st.form_submit_button(
            "Login",
            use_container_width=True
        )

        if submit:

            users = {
                "yahya.ouarach@arrow.com": {
                    "password": "Arrow2026!",
                    "role": "Admin"
                },
                "mafernandez@arrow.com": {
                    "password": "Arrow2026!",
                    "role": "User"
                }
            }

            user = users.get(email.lower())

            if user and password == user["password"]:

                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.user_role = user["role"]

                st.rerun()

            else:
                st.error("Invalid credentials")


# ==============================================================================
# DATA LOADER
# ==============================================================================
@st.cache_data
def load_data():

    if not os.path.exists("data.csv"):
        return pd.DataFrame()

    try:

        df = pd.read_csv("data.csv")

        if "Process" in df.columns:
            df["Process"] = (
                df["Process"]
                .astype(str)
                .str.strip()
            )

        return df

    except Exception as e:

        st.error(f"Error loading CSV: {e}")
        return pd.DataFrame()


# ==============================================================================
# LOGIN PAGE
# ==============================================================================
if not st.session_state.logged_in:
    render_login()
    st.stop()

# ==============================================================================
# SIDEBAR
# ==============================================================================
st.sidebar.title("💎 Arledge Hub")
st.sidebar.caption(
    f"Connected: {st.session_state.user_email}"
)

pages = ["📋 Knowledge Base"]

if st.session_state.user_role == "Admin":
    pages.append("🛠️ Admin")

page = st.sidebar.radio(
    "Navigation",
    pages
)

if st.sidebar.button("Logout", use_container_width=True):

    st.session_state.logged_in = False
    st.session_state.user_role = "User"
    st.session_state.user_email = ""

    st.rerun()

# ==============================================================================
# LOAD DATA
# ==============================================================================
df = load_data()

# ==============================================================================
# KNOWLEDGE BASE
# ==============================================================================
if page == "📋 Knowledge Base":

    st.title("Knowledge Base")

    if df.empty:

        st.warning(
            "No data.csv file found or file is empty."
        )

    else:

        col1, col2 = st.columns(2)

        with col1:

            if "Process" in df.columns:
                st.metric(
                    "Processes",
                    len(df["Process"].unique())
                )

        with col2:
            st.metric(
                "Status",
                "Online"
            )

        search = st.text_input(
            "Search",
            placeholder="Type keyword..."
        )

        filtered_df = df.copy()

        if search:

            mask = filtered_df.fillna("").apply(
                lambda row: row.astype(str)
                .str.contains(
                    search,
                    case=False,
                    na=False
                )
                .any(),
                axis=1
            )

            filtered_df = filtered_df[mask]

        if (
            "Process" in filtered_df.columns
            and not filtered_df.empty
        ):

            options = sorted(
                filtered_df["Process"].unique()
            )

            selected = st.selectbox(
                "Select Process",
                [""] + options
            )

            if selected:

                matches = df[
                    df["Process"] == selected
                ]

                if not matches.empty:

                    process = matches.iloc[0]

                    st.subheader(selected)

                    c1, c2 = st.columns(2)

                    with c1:

                        st.info(
                            process.get(
                                "System",
                                "N/A"
                            )
                        )

                        st.success(
                            process.get(
                                "Rationale",
                                "N/A"
                            )
                        )

                    with c2:

                        st.warning(
                            process.get(
                                "Instructions",
                                "N/A"
                            )
                        )

                        st.caption(
                            process.get(
                                "File_Source",
                                "N/A"
                            )
                        )

# ==============================================================================
# ADMIN
# ==============================================================================
elif page == "🛠️ Admin":

    st.title("Admin Panel")

    uploaded_csv = st.file_uploader(
        "Upload data.csv",
        type="csv"
    )

    if uploaded_csv is not None:

        try:

            df_new = pd.read_csv(uploaded_csv)

            df_new.to_csv(
                "data.csv",
                index=False
            )

            load_data.clear()

            st.success(
                "Database updated successfully."
            )

        except Exception as e:

            st.error(str(e))

    uploaded_pdf = st.file_uploader(
        "Upload SOP PDF",
        type="pdf"
    )

    if uploaded_pdf is not None:

        os.makedirs(
            "sops",
            exist_ok=True
        )

        path = os.path.join(
            "sops",
            uploaded_pdf.name
        )

        with open(path, "wb") as f:
            f.write(uploaded_pdf.getbuffer())

        st.success(
            f"Uploaded {uploaded_pdf.name}"
        )
