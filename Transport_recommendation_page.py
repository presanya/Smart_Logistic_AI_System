import streamlit as st
import pandas as pd
import pickle

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Transport Recommendation",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 Transport Recommendation")
st.write("Enter the order details to recommend the best transport mode.")

# --------------------------------------------------
# Load Model
# --------------------------------------------------

@st.cache_resource
def load_model():
    with open("transport_mode_Random_forest_classifier_model.pkl", "rb") as file:
        model = pickle.load(file)
    return model

model = load_model()

# --------------------------------------------------
# User Input
# --------------------------------------------------

st.subheader("📦 Order Details")

col1, col2 = st.columns(2)

with col1:

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=5
    )

    distance_km = st.number_input(
        "Distance (km)",
        min_value=0.0,
        value=400.78
    )

    package_weight = st.number_input(
        "Package Weight (kg)",
        min_value=0.0,
        value=300.0
    )

    is_fragile = st.selectbox(
        "Is Fragile?",
        [0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No"
    )

    is_hazmat = st.selectbox(
        "Is Hazmat?",
        [0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No"
    )

    cold_chain_required = st.selectbox(
        "Cold Chain Required?",
        [0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No"
    )

    destination_city = st.text_input(
            "Destination City",
            value="chennai"
        ).lower()

with col2:

    delivery_priority = st.selectbox(
        "Delivery Priority",
        [
            "standard",
            "express",
            "urgent"
        ]
    )

    order_value_inr = st.number_input(
        "Order Value (INR)",
        min_value=0.0,
        value=20000.0
    )

    weather_condition_at_dest = st.selectbox(
        "Weather Condition",
        [
            "clear",
            "cloudy",
            "rain",
            "heavy rain",
            "storm",
            "fog"
        ]
    )

    promised_eta_hours = st.number_input(
        "Promised ETA (Hours)",
        min_value=0.0,
        value=12.0
    )

    actual_delivery_hours = st.number_input(
        "Actual Delivery Hours",
        min_value=0.0,
        value=17.5
    )

    origin_city = st.text_input(
        "Origin City",
        value="chennai"
    ).lower()

    destination_state = st.text_input(
        "Destination State",
        value="tn"
    ).lower()

# --------------------------------------------------
# Prediction Button
# --------------------------------------------------

st.divider()

if st.button(
    "🚀 Recommend Transport",
    use_container_width=True
):

    # Create input dictionary

    user_input = {

        "quantity": quantity,

        "distance_km": distance_km,

        "package_weight": package_weight,

        "is_fragile": is_fragile,

        "is_hazmat": is_hazmat,

        "cold_chain_required": cold_chain_required,

        "delivery_priority": delivery_priority,

        "order_value_inr": order_value_inr,

        "weather_condition_at_dest":
            weather_condition_at_dest,

        "promised_eta_hours":
            promised_eta_hours,

        "origin_city":
            origin_city,

        "destination_city":
            destination_city,

        "destination_state":
            destination_state,

        "actual_delivery_hours":
            actual_delivery_hours
    }

    # Convert dictionary to DataFrame

    user_in = pd.DataFrame([user_input])

    # Display input

    st.subheader("📋 Input Details")

    st.dataframe(
        user_in,
        use_container_width=True
    )

    # --------------------------------------------------
    # Prediction
    # --------------------------------------------------

    try:

        prediction = model.predict(user_in)

        recommended_transport = prediction[0]

        st.success(
            f"Recommended Transport: **{recommended_transport}**"
        )

    except Exception as e:

        st.error(
            "Prediction failed."
        )

        st.exception(e)

if st.button("⬅️ Back to Employee Dashboard"):

    st.switch_page(
        "pages/employee_feature_page.py"
    )
