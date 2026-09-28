# import streamlit as st
# from sqlalchemy import create_engine, text


# # =========================================================
# # PAGE CONFIGURATION
# # =========================================================

# st.set_page_config(
#     page_title="SmartLogix Login",
#     page_icon="🚚",
#     layout="centered"
# )


# # =========================================================
# # POSTGRESQL DATABASE CONNECTION
# # =========================================================

# database = "smartlogistic_db"

# connection = (
#     "postgresql://postgres:lavi@localhost:5432/"
#     f"{database}"
# )

# engine = create_engine(connection)


# # =========================================================
# # SESSION STATE
# # =========================================================

# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# if "username" not in st.session_state:
#     st.session_state.username = ""

# if "role" not in st.session_state:
#     st.session_state.role = ""


# # =========================================================
# # LOGIN FUNCTION
# # =========================================================

# def login_user(username, password, selected_role):

#     try:

#         # =================================================
#         # EMPLOYEE LOGIN
#         # =================================================

#         if selected_role == "Employee":

#             query = text("""
#                 SELECT *
#                 FROM logistic_employee
#                 WHERE username = :username
#                 AND password = :password
#                 LIMIT 1
#             """)

#             with engine.connect() as conn:

#                 result = conn.execute(
#                     query,
#                     {
#                         "username": username,
#                         "password": password
#                     }
#                 )

#                 user = result.fetchone()


#             if user:

#                 return True, "Login successful."

#             else:

#                 return False, "Invalid employee username or password."


#         # =================================================
#         # CUSTOMER LOGIN
#         # =================================================

#         elif selected_role == "Customer":

#             query = text("""
#                 SELECT *
#                 FROM customers
#                 WHERE customer_id = :customer_id
#                 AND phone = :phone
#                 LIMIT 1
#             """)

#             with engine.connect() as conn:

#                 result = conn.execute(
#                     query,
#                     {
#                         "customer_id": username,
#                         "phone": password
#                     }
#                 )

#                 user = result.fetchone()


#             if user:

#                 return True, "Login successful."

#             else:

#                 return False, "Invalid customer username or password."


#     except Exception as e:

#         return False, f"Database connection error: {e}"


# # =========================================================
# # LOGOUT FUNCTION
# # =========================================================

# def logout():

#     st.session_state.logged_in = False

#     st.session_state.username = ""

#     st.session_state.role = ""

#     st.switch_page("app.py")


# # =========================================================
# # LOGIN PAGE
# # =========================================================

# if not st.session_state.logged_in:

#     # -----------------------------------------------------
#     # TITLE
#     # -----------------------------------------------------

#     st.title("🚚    Smart Logistics Management System")

   

#     st.write(
#         "Please login to continue."
#     )

#     st.divider()


#     # -----------------------------------------------------
#     # USERNAME
#     # -----------------------------------------------------

#     username = st.text_input(

#         "👤 Username",

#         placeholder="Enter your username"

#     )


#     # -----------------------------------------------------
#     # PASSWORD
#     # -----------------------------------------------------

#     password = st.text_input(

#         "🔑 Password",

#         type="password",

#         placeholder="Enter your password"

#     )


#     # -----------------------------------------------------
#     # ROLE
#     # -----------------------------------------------------

#     selected_role = st.selectbox(

#         "👥 Select Role",

#         [
#             "Employee",
#             "Customer"
#         ]

#     )


#     st.write("")


#     # =====================================================
#     # LOGIN BUTTON
#     # =====================================================

#     if st.button(

#         "🔐 Login",

#         use_container_width=True

#     ):

#         # -------------------------------------------------
#         # REMOVE SPACES
#         # -------------------------------------------------

#         username = username.strip()


#         # -------------------------------------------------
#         # CHECK EMPTY FIELDS
#         # -------------------------------------------------

#         if username == "" or password == "":

#             st.warning(
#                 "⚠️ Please enter username and password."
#             )


#         else:

#             # -------------------------------------------------
#             # VALIDATE LOGIN FROM POSTGRESQL
#             # -------------------------------------------------

#             success, message = login_user(

#                 username,

#                 password,

#                 selected_role

#             )


#             # =================================================
#             # SUCCESSFUL LOGIN
#             # =================================================

#             if success:

#                 # Save login information

#                 st.session_state.logged_in = True

#                 st.session_state.username = username

#                 st.session_state.role = selected_role


#                 # -------------------------------------------------
#                 # EMPLOYEE
#                 # -------------------------------------------------

#                 if selected_role == "Employee":

#                     st.switch_page(
#                         "pages/employee_feature_page.py"
#                     )


#                 # -------------------------------------------------
#                 # CUSTOMER
#                 # -------------------------------------------------

#                 elif selected_role == "Customer":

#                     st.switch_page(
#                         "pages/customer_page.py"
#                     )


#             # =================================================
#             # LOGIN FAILED
#             # =================================================

#             else:

#                 st.error(
#                     f"❌ {message}"
#                 )
import streamlit as st
from sqlalchemy import create_engine, text


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SmartLogix Login",
    page_icon="🚚",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =========================================================
# POSTGRESQL DATABASE CONNECTION
# =========================================================

DATABASE = "smartlogistic_db"

DATABASE_URL = (
    f"postgresql://postgres:lavi@localhost:5432/{DATABASE}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       PAGE BACKGROUND
       ===================================================== */

    .stApp {
        background:
            linear-gradient(
                135deg,
                #eef6ff 0%,
                #f7f9fc 50%,
                #effcf9 100%
            );

        min-height: 100vh;
    }


    /* =====================================================
       HIDE STREAMLIT DEFAULT UI
       ===================================================== */

    #MainMenu {
        display: none !important;
    }

    header {
        display: none !important;
    }

    footer {
        display: none !important;
    }


    /* =====================================================
       REMOVE ALL TOP SPACE
       ===================================================== */

    html,
    body {
        margin: 0 !important;
        padding: 0 !important;
    }


    [data-testid="stAppViewContainer"] {
        margin: 0 !important;
        padding: 0 !important;
    }


    [data-testid="stAppViewContainer"] > .main {
        margin: 0 !important;
        padding: 0 !important;
    }


    [data-testid="stMain"] {
        margin: 0 !important;
        padding: 0 !important;
    }


    [data-testid="stMainBlockContainer"] {
        margin: 0 !important;

        padding-top: 0px !important;
        padding-bottom: 20px !important;

        padding-left: 20px !important;
        padding-right: 20px !important;
    }


    .block-container {
        max-width: 600px !important;

        margin-top: 0px !important;
        margin-bottom: 0px !important;

        padding-top: 0px !important;
        padding-bottom: 20px !important;

        padding-left: 20px !important;
        padding-right: 20px !important;
    }


    /* =====================================================
       LOGIN CARD
       ===================================================== */

    .login-card {
        width: 100%;

        box-sizing: border-box;

        background: #ffffff;

        border-radius: 24px;

        padding:
            30px 42px 28px 42px;

        margin-top: 0px !important;
        margin-bottom: 0px !important;

        box-shadow:
            0 15px 45px
            rgba(15, 23, 42, 0.12);

        border:
            1px solid #e2e8f0;
    }


    /* =====================================================
       SMARTLOGIX LOGO
       ===================================================== */

    .login-logo {
        text-align: center;

        font-size: 42px;

        font-weight: 900;

        letter-spacing: -1.5px;

        color: #123b7a;

        margin-top: 0px;

        margin-bottom: 5px;
    }


    .login-logo span {
        color: #08b39f;
    }


    /* =====================================================
       TITLE
       ===================================================== */

    .login-title {
        text-align: center;

        font-size: 20px;

        font-weight: 800;

        color: #1e293b;

        margin-top: 0px;

        margin-bottom: 5px;
    }


    /* =====================================================
       DESCRIPTION
       ===================================================== */

    .login-description {
        text-align: center;

        font-size: 14px;

        color: #64748b;

        margin-top: 0px;

        margin-bottom: 22px;
    }


    /* =====================================================
       LABELS
       ===================================================== */

    label {
        font-weight: 700 !important;

        color: #334155 !important;
    }


    /* =====================================================
       TEXT INPUT
       ===================================================== */

    div[data-baseweb="input"] {

        background: #ffffff !important;

        border:
            1px solid #cbd5e1 !important;

        border-radius: 12px !important;

        min-height: 48px !important;
    }


    div[data-baseweb="input"]:focus-within {

        border:
            1px solid #2563eb !important;

        box-shadow:
            0 0 0 3px
            rgba(37, 99, 235, 0.10) !important;
    }


    input {
        font-size: 15px !important;
    }


    /* =====================================================
       SELECT BOX
       ===================================================== */

    div[data-baseweb="select"] > div {

        background: #ffffff !important;

        border:
            1px solid #cbd5e1 !important;

        border-radius: 12px !important;

        min-height: 48px !important;
    }


    /* =====================================================
       LOGIN BUTTON
       ===================================================== */

    .stButton > button {

        width: 100% !important;

        height: 52px !important;

        border: none !important;

        border-radius: 12px !important;

        background:
            linear-gradient(
                90deg,
                #174ea6,
                #1479d1,
                #08a995
            ) !important;

        color: #ffffff !important;

        font-size: 16px !important;

        font-weight: 800 !important;

        box-shadow:
            0 8px 20px
            rgba(23, 78, 166, 0.22) !important;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }


    .stButton > button:hover {

        color: #ffffff !important;

        transform: translateY(-2px);

        box-shadow:
            0 12px 25px
            rgba(23, 78, 166, 0.30) !important;
    }


    /* =====================================================
       REMOVE EXTRA SPACE CREATED BY STREAMLIT ELEMENTS
       ===================================================== */

    div[data-testid="stTextInput"] {
        margin-bottom: 0px !important;
    }


    div[data-testid="stSelectbox"] {
        margin-bottom: 0px !important;
    }


    /* =====================================================
       DIVIDER
       ===================================================== */

    .login-divider {

        width: 100%;

        border-top:
            1px solid #e2e8f0;

        margin-top: 22px;

        margin-bottom: 15px;
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .login-footer {

        text-align: center;

        color: #64748b;

        font-size: 13px;

        line-height: 1.6;

        margin: 0px;
    }


    .priority-text {

        color: #087f8c;

        font-size: 17px;

        font-weight: 800;

        margin-bottom: 3px;
    }


    /* =====================================================
       ALERTS
       ===================================================== */

    div[data-testid="stAlert"] {

        border-radius: 12px !important;

        margin-top: 10px !important;
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media screen and (max-width: 600px) {

        [data-testid="stMainBlockContainer"] {

            padding-top: 0px !important;

            padding-left: 12px !important;

            padding-right: 12px !important;
        }


        .block-container {

            padding-top: 0px !important;

            padding-left: 12px !important;

            padding-right: 12px !important;
        }


        .login-card {

            padding:
                25px 20px 24px 20px;

            border-radius: 20px;
        }


        .login-logo {

            font-size: 36px;
        }


        .login-title {

            font-size: 18px;
        }


        .login-description {

            font-size: 13px;

            margin-bottom: 20px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOGIN FUNCTION
# =========================================================

def login_user(username, password, selected_role):

    try:

        # =================================================
        # EMPLOYEE LOGIN
        # =================================================

        if selected_role == "Employee":

            query = text(
                """
                SELECT *
                FROM logistic_employee
                WHERE username = :username
                AND password = :password
                LIMIT 1
                """
            )

            with engine.connect() as conn:

                result = conn.execute(
                    query,
                    {
                        "username": username,
                        "password": password
                    }
                )

                user = result.fetchone()


            if user is not None:

                return True, "Login successful."


            return (
                False,
                "Invalid employee username or password."
            )


        # =================================================
        # CUSTOMER LOGIN
        # =================================================

        elif selected_role == "Customer":

            query = text(
                """
                SELECT *
                FROM customers
                WHERE customer_id = :customer_id
                AND phone = :phone
                LIMIT 1
                """
            )

            with engine.connect() as conn:

                result = conn.execute(
                    query,
                    {
                        "customer_id": username,
                        "phone": password
                    }
                )

                user = result.fetchone()


            if user is not None:

                return True, "Login successful."


            return (
                False,
                "Invalid customer ID or phone number."
            )


        return False, "Please select a valid role."


    except Exception as e:

        return (
            False,
            f"Database connection error: {str(e)}"
        )


# =========================================================
# LOGOUT FUNCTION
# =========================================================

def logout():

    st.session_state.logged_in = False

    st.session_state.username = ""

    st.session_state.role = ""

    st.switch_page("app.py")


# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state.logged_in:

    # =====================================================
    # LOGIN CARD START
    # =====================================================

    st.markdown(
        '<div class="login-card">',
        unsafe_allow_html=True
    )


    # =====================================================
    # LOGO
    # =====================================================

    st.markdown(
        """
        <div class="login-logo">
            Smart<span>Logix</span>
        </div>

        <div class="login-title">
            Logistics Management System
        </div>

        <div class="login-description">
            Sign in to access your SmartLogix account
        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # USERNAME
    # =====================================================

    username = st.text_input(
        "👤 Username",
        placeholder="Enter username or customer ID",
        key="login_username"
    )


    # =====================================================
    # PASSWORD
    # =====================================================

    password = st.text_input(
        "🔐 Password",
        type="password",
        placeholder="Enter password or phone number",
        key="login_password"
    )


    # =====================================================
    # ROLE
    # =====================================================

    selected_role = st.selectbox(
        "👥 Login as",
        [
            "Employee",
            "Customer"
        ],
        key="login_role"
    )


    # =====================================================
    # SMALL SPACE
    # =====================================================

    st.markdown(
        "<div style='height:8px;'></div>",
        unsafe_allow_html=True
    )


    # =====================================================
    # LOGIN BUTTON
    # =====================================================

    if st.button(
        "🔐  Sign In",
        use_container_width=True
    ):

        username = username.strip()

        password = password.strip()


        # =================================================
        # EMPTY FIELD CHECK
        # =================================================

        if not username or not password:

            st.warning(
                "⚠️ Please enter username and password."
            )


        else:

            # =============================================
            # LOGIN VALIDATION
            # =============================================

            success, message = login_user(
                username,
                password,
                selected_role
            )


            # =============================================
            # LOGIN SUCCESS
            # =============================================

            if success:

                st.session_state.logged_in = True

                st.session_state.username = username

                st.session_state.role = selected_role


                # =========================================
                # EMPLOYEE
                # =========================================

                if selected_role == "Employee":

                    st.switch_page(
                        "pages/employee_feature_page.py"
                    )


                # =========================================
                # CUSTOMER
                # =========================================

                elif selected_role == "Customer":

                    st.switch_page(
                        "pages/customer_page.py"
                    )


            # =============================================
            # LOGIN FAILED
            # =============================================

            else:

                st.error(
                    f"❌ {message}"
                )


    # =====================================================
    # FOOTER
    # =====================================================

    st.markdown(
        """
        

        <div class="login-footer">

            

            Secure • Smart • Reliable Logistics

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # LOGIN CARD END
    # =====================================================

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# LOGGED-IN STATE
# =========================================================

else:
     st.markdown(
    """
    

    <div style="
        text-align: center;
        color: #64748b;
        font-size: 13px;
        line-height: 1.6;
    ">

        <div style="
            color: #087f8c;
            font-size: 17px;
            font-weight: 800;
            margin-bottom: 3px;
        ">
            
        </div>

        Secure • Smart • Reliable Logistics

    </div>
    """,
         unsafe_allow_html=True
)


    # =====================================================
    # WELCOME
    # =====================================================

     st.success(
        f"Welcome, {st.session_state.username}!"
    )


     st.info(
        f"Logged in as: {st.session_state.role}"
    )


    # =====================================================
    # LOGOUT
    # =====================================================

     if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout()