# import streamlit as st


# # =========================================================
# # PAGE CONFIGURATION
# # =========================================================

# st.set_page_config(
#     page_title="SmartLogix Employee",
#     page_icon="👨‍💼",
#     layout="wide"
# )


# # =========================================================
# # CUSTOM CSS
# # =========================================================

# st.markdown("""
# <style>

# .stApp {
#     background: linear-gradient(
#         135deg,
#         #0f2027,
#         #203a43,
#         #2c5364
#     );
# }

# /* Main container */
# .block-container {
#     padding-top: 2rem;
#     padding-bottom: 2rem;
# }

# /* Hero section */
# .hero {
#     padding: 50px 40px;
#     border-radius: 25px;
#     background: linear-gradient(
#         135deg,
#         rgba(0, 198, 255, 0.95),
#         rgba(0, 114, 255, 0.90),
#         rgba(111, 66, 193, 0.90)
#     );
#     box-shadow: 0px 10px 30px rgba(0,0,0,0.35);
#     margin-bottom: 30px;
# }

# /* Title */
# .hero-title {
#     font-size: 55px;
#     font-weight: 800;
#     color: white;
#     margin-bottom: 10px;
# }

# /* Subtitle */
# .hero-subtitle {
#     font-size: 22px;
#     color: #f1f1f1;
#     line-height: 1.6;
# }

# /* Cards */
# .card {
#     padding: 25px;
#     border-radius: 20px;
#     background: rgba(255,255,255,0.12);
#     border: 1px solid rgba(255,255,255,0.2);
#     box-shadow: 0px 8px 20px rgba(0,0,0,0.25);
#     text-align: center;
#     height: 180px;
# }

# .card h2 {
#     color: white;
# }

# .card p {
#     color: #e5e5e5;
#     font-size: 16px;
# }

# /* Button */
# .stButton > button {
#     width: 100%;
#     border-radius: 12px;
#     height: 50px;
#     font-size: 18px;
#     font-weight: bold;
# }

# /* Footer */
# .footer {
#     text-align: center;
#     color: #cccccc;
#     margin-top: 40px;
#     font-size: 15px;
# }

# </style>
# """, unsafe_allow_html=True)

# # =========================================================
# # CHECK LOGIN
# # =========================================================

# if not st.session_state.get("logged_in", False):

#     st.warning("⚠️ Please login first.")

#     if st.button("🔐 Go to Login"):

#         st.switch_page("app.py")

#     st.stop()


# # =========================================================
# # CHECK ROLE
# # =========================================================

# if st.session_state.get("role") != "Employee":

#     st.error("❌ You are not authorized to access this page.")

#     if st.button("🔐 Go to Login"):

#         st.switch_page("app.py")

#     st.stop()


# # =========================================================
# # EMPLOYEE INFORMATION
# # =========================================================

# username = st.session_state.username


# # =========================================================
# # TITLE
# # =========================================================

# st.title("👨‍💼 SmartLogix Employee Portal")

# st.success(
#     f"Welcome {username}! 👋"
# )

# st.write(
#     "Select a feature below to continue."
# )

# st.divider()


# # =========================================================
# # EMPLOYEE FEATURES
# # =========================================================

# st.markdown("## 🌟 SmartLogix Features")


# # =========================================================
# # FIRST ROW
# # =========================================================

# col1, col2, col3 = st.columns(3)


# # ---------------------------------------------------------
# # ORDER MANAGEMENT
# # ---------------------------------------------------------

# with col1:

#     #st.markdown("### 📦 Order Management")
#     st.markdown("""
#         <div class="card">
    
#         <h2>🚛 Order Management</h2>
    
#         </div>
#         """, unsafe_allow_html=True)

#     st.write(
#         "View and manage customer orders."
#     )

#     if st.button(
#         "Open Order Management",
#         key="order_button",
#         use_container_width=True
#     ):

#         st.switch_page(
#             "pages/orders_page.py"
#         )


# # ---------------------------------------------------------
# # TRANSPORT SELECTION
# # ---------------------------------------------------------

# with col2:

#     st.markdown("### 🚛 Transport Selection")

#     st.write(
#         "Select the suitable transport mode."
#     )

#     if st.button(
#         "Open Transport Selection",
#         key="transport_button",
#         use_container_width=True
#     ):

#         st.switch_page(
#             "pages/Transport_recommendation_page.py"
#         )


# # ---------------------------------------------------------
# # ROUTE OPTIMIZATION
# # ---------------------------------------------------------

# with col3:

#     st.markdown("### 📍 Route Optimization")

#     st.write(
#         "Optimize delivery routes."
#     )

#     if st.button(
#         "Open Route Optimization",
#         key="route_button",
#         use_container_width=True
#     ):

#         st.switch_page(
#             "pages/route_optimization.py"
#         )


# # =========================================================
# # SECOND ROW
# # =========================================================

# st.write("")

# col4, col5, col6 = st.columns(3)


# # ---------------------------------------------------------
# # PAYLOAD OPTIMIZATION
# # ---------------------------------------------------------

# with col4:

#     st.markdown("### 📦 Payload Optimization")

#     st.write(
#         "Find the suitable vehicle for an order."
#     )

#     if st.button(
#         "Open Payload Optimization",
#         key="payload_button",
#         use_container_width=True
#     ):

#         st.switch_page(
#             "pages/payload_optimization_page.py"
#         )


# # ---------------------------------------------------------
# # PREDICTIVE MAINTENANCE
# # ---------------------------------------------------------

# with col5:

#     st.markdown("### 🔧 Predictive Maintenance & ETA")

#     st.write(
#         "Predict vehicle failure and maintenance."
#     )

#     if st.button(
#         "Open Predictive Maintenance",
#         key="maintenance_button",
#         use_container_width=True
#     ):

#         st.switch_page(
#             "pages/Prediction_ETA&Maintance.py"
#         )


# # ---------------------------------------------------------
# # DELIVERY SCHEDULING
# # ---------------------------------------------------------

# with col6:

#     st.markdown("### ⏱️ Delivery Scheduling")

#     st.write(
#         "Schedule and manage deliveries."
#     )

#     if st.button(
#         "Open Delivery Scheduling",
#         key="delivery_button",
#         use_container_width=True
#     ):

#         st.switch_page(
#             "pages/Delivery_scheduling_page.py"
#         )


# # =========================================================
# # LOGOUT
# # =========================================================

# st.divider()

# if st.button(
#     "🚪 Logout",
#     use_container_width=True
# ):

#     st.session_state.logged_in = False

#     st.session_state.username = ""

#     st.session_state.role = ""

#     st.switch_page("app.py")


import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SmartLogix Employee",
    page_icon="👨‍💼",
    layout="wide"
)


# =========================================================
# CUSTOM CSS (GREEN CARDS, WHITE BUTTONS, BLUE TEXT)
# =========================================================

st.markdown("""
<style>

/* Plain background */
.stApp {
    background-color: #ffffff !important;
}

/* Force standard text, headings, and labels to blue */
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp p, .stApp label, .stApp span {
    color: #1E40AF !important; /* Deep Blue Text */
}

/* Main container spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Green Cards */
.card {
    padding: 25px;
    border-radius: 12px;
    background-color: #15803D !important; /* Dark Green Card */
    border: 1px solid #166534;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.15);
    text-align: center;
    margin-bottom: 15px;
}

/* Text inside the Green Cards */
.card h2 {
    color: #FFFFFF !important; /* White text inside green card for contrast */
    margin: 0;
    font-size: 22px;
}

/* White Buttons */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 48px;
    font-size: 16px;
    font-weight: bold;
    color: #1E40AF !important; /* Blue text on white button */
    background-color: #FFFFFF !important; /* White button */
    border: 2px solid #1E40AF !important; /* Blue border */
}

.stButton > button:hover {
    background-color: #1E40AF !important; /* Blue background on hover */
    color: #FFFFFF !important; /* White text on hover */
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# CHECK LOGIN
# =========================================================

if not st.session_state.get("logged_in", False):
    st.warning("⚠️ Please login first.")
    if st.button("🔐 Go to Login"):
        st.switch_page("app.py")
    st.stop()


# =========================================================
# CHECK ROLE
# =========================================================

if st.session_state.get("role") != "Employee":
    st.error("❌ You are not authorized to access this page.")
    if st.button("🔐 Go to Login"):
        st.switch_page("app.py")
    st.stop()


# =========================================================
# EMPLOYEE INFORMATION
# =========================================================

username = st.session_state.get("username", "Employee")


# =========================================================
# TITLE
# =========================================================

st.title("👨‍💼 SmartLogix Employee Portal")

st.write("""
<div class="hero">
Optimize transportation, predict vehicle failures,
manage deliveries and find intelligent routes using
Artificial Intelligence and Machine Learning.
</div>

</div>
""", unsafe_allow_html=True)
st.success(f"Welcome {username}! 👋")

st.header("Select a feature below to continue.")

st.divider()


# =========================================================
# EMPLOYEE FEATURES
# =========================================================

st.markdown("## 🌟 SmartLogix Features")


# =========================================================
# FIRST ROW
# =========================================================

col1, col2, col3 = st.columns(3)


# ---------------------------------------------------------
# ORDER MANAGEMENT
# ---------------------------------------------------------

with col1:
    st.markdown("""
        <div class="card">
            <h2>🚛 Order Management</h2>
        </div>
        """, unsafe_allow_html=True)

    st.write("View and manage customer orders.")

    if st.button(
        "Open Order Management",
        key="order_button",
        use_container_width=True
    ):
        st.switch_page("pages/orders_page.py")


# ---------------------------------------------------------
# TRANSPORT SELECTION
# ---------------------------------------------------------

with col2:
    st.markdown("""
        <div class="card">
            <h2>🚚 Transport Selection</h2>
        </div>
        """, unsafe_allow_html=True)

    st.write("Select the suitable transport mode.")

    if st.button(
        "Open Transport Selection",
        key="transport_button",
        use_container_width=True
    ):
        st.switch_page("pages/Transport_recommendation_page.py")


# ---------------------------------------------------------
# ROUTE OPTIMIZATION
# ---------------------------------------------------------

with col3:
    st.markdown("""
        <div class="card">
            <h2>📍 Route Optimization</h2>
        </div>
        """, unsafe_allow_html=True)

    st.write("Optimize delivery routes.")

    if st.button(
        "Open Route Optimization",
        key="route_button",
        use_container_width=True
    ):
        st.switch_page("pages/route_optimization.py")


# =========================================================
# SECOND ROW
# =========================================================

st.write("")

col4, col5, col6 = st.columns(3)


# ---------------------------------------------------------
# PAYLOAD OPTIMIZATION
# ---------------------------------------------------------

with col4:
    st.markdown("""
        <div class="card">
            <h2>📦 Payload Optimization</h2>
        </div>
        """, unsafe_allow_html=True)

    st.write("Find the suitable vehicle for an order.")

    if st.button(
        "Open Payload Optimization",
        key="payload_button",
        use_container_width=True
    ):
        st.switch_page("pages/payload_optimization_page.py")


# ---------------------------------------------------------
# PREDICTIVE MAINTENANCE
# ---------------------------------------------------------

with col5:
    st.markdown("""
        <div class="card">
            <h2>🔧Predictive Maintenance&ETA</h2>
        </div>
        """, unsafe_allow_html=True)

    st.write("Predict maintenance and vehicle failure")

    if st.button(
        "Open Predictive Maintenance",
        key="maintenance_button",
        use_container_width=True
    ):
        st.switch_page("pages/Prediction_ETA&Maintance.py")


# ---------------------------------------------------------
# DELIVERY SCHEDULING
# ---------------------------------------------------------

with col6:
    st.markdown("""
        <div class="card">
            <h2>⏱️ Delivery Scheduling</h2>
        </div>
        """, unsafe_allow_html=True)

    st.write("Schedule and manage deliveries.")

    if st.button(
        "Open Delivery Scheduling",
        key="delivery_button",
        use_container_width=True
    ):
        st.switch_page("pages/Delivery_scheduling_page.py")


# =========================================================
# LOGOUT
# =========================================================

st.divider()

if st.button("Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.switch_page("app.py")