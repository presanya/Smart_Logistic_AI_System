
import streamlit as st
import pandas as pd
import pickle


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Prediction ETA & Maintenance",
    page_icon="🔮",
    layout="wide"
)


# =========================================================
# PAGE TITLE
# =========================================================

st.title("🔮 SmartLogix Prediction Center")

st.write(
    "Select a prediction type below."
)


# =========================================================
# LOAD ETA MODEL
# =========================================================

with open(
    "delivery_edt_linearRegression_model.pkl",
    "rb"
) as file:

    eta_model = pickle.load(file)


# =========================================================
# LOAD MAINTENANCE MODEL
# =========================================================

with open(
    "maintance_required_randomforest_classifier_model.pkl",
    "rb"
) as file:

    maintenance_model = pickle.load(file)


# =========================================================
# LOAD DATA
# =========================================================

eta_df = pd.read_csv(
    "eda_df.csv"
)

maintenance_df = pd.read_csv(
    "cleaned_maintance_vechile_df.csv"
)


# =========================================================
# SELECT PREDICTION TYPE
# =========================================================

prediction_type = st.radio(

    "Select Prediction Type",

    [
        "⏱️ ETA Prediction",
        "🔧 Vehicle Maintenance Prediction"
    ],

    horizontal=True
)


# =========================================================
# ETA PREDICTION
# =========================================================

if prediction_type == "⏱️ ETA Prediction":

    st.header("⏱️ Delivery ETA Prediction")

    st.write(
        "Enter the delivery details to predict actual delivery hours."
    )


    # -----------------------------------------------------
    # CREATE COLUMNS
    # -----------------------------------------------------

    col1, col2 = st.columns(2)


    # -----------------------------------------------------
    # TRANSPORT MODE
    # -----------------------------------------------------

    with col1:

        transport_mode = st.selectbox(

            "Transport Mode",

            sorted(
                eta_df["transport_mode"]
                .dropna()
                .unique()
            )
        )


    # -----------------------------------------------------
    # DELIVERY PRIORITY
    # -----------------------------------------------------

    with col2:

        delivery_priority = st.selectbox(

            "Delivery Priority",

            sorted(
                eta_df["delivery_priority"]
                .dropna()
                .unique()
            )
        )


    # -----------------------------------------------------
    # WEATHER
    # -----------------------------------------------------

    with col1:

        weather_condition = st.selectbox(

            "Weather Condition",

            sorted(
                eta_df["weather_condition_at_dest"]
                .dropna()
                .unique()
            )
        )


    # -----------------------------------------------------
    # DISTANCE
    # -----------------------------------------------------

    with col2:

        distance_km = st.number_input(

            "Distance (KM)",

            min_value=0.0,

            value=100.0,

            step=1.0
        )


    # -----------------------------------------------------
    # ORIGIN CITY
    # -----------------------------------------------------

    with col1:

        origin_city = st.selectbox(

            "Origin City",

            sorted(
                eta_df["origin_city"]
                .dropna()
                .unique()
            )
        )


    # -----------------------------------------------------
    # DESTINATION CITY
    # -----------------------------------------------------

    with col2:

        destination_city = st.selectbox(

            "Destination City",

            sorted(
                eta_df["destination_city"]
                .dropna()
                .unique()
            )
        )


    # -----------------------------------------------------
    # ORDER VALUE
    # -----------------------------------------------------

    with col1:

        order_value_inr = st.number_input(

            "Order Value (₹)",

            min_value=0.0,

            value=5000.0,

            step=500.0
        )


    # -----------------------------------------------------
    # PROMISED ETA
    # -----------------------------------------------------

    with col2:

        promised_eta_hours = st.number_input(

            "Promised ETA (Hours)",

            min_value=0.0,

            value=12.0,

            step=1.0
        )


    # -----------------------------------------------------
    # PREDICT BUTTON
    # -----------------------------------------------------

    if st.button(
        "🚚 Predict Delivery ETA",
        use_container_width=True
    ):

        # ---------------------------------------------
        # CREATE INPUT DATAFRAME
        # ---------------------------------------------

        eta_input = pd.DataFrame({

            "transport_mode": [
                transport_mode
            ],

            "delivery_priority": [
                delivery_priority
            ],

            "weather_condition_at_dest": [
                weather_condition
            ],

            "distance_km": [
                distance_km
            ],

            "origin_city": [
                origin_city
            ],

            "destination_city": [
                destination_city
            ],

            "order_value_inr": [
                order_value_inr
            ],

            "promised_eta_hours": [
                promised_eta_hours
            ]

        })


        # ---------------------------------------------
        # DISPLAY INPUT
        # ---------------------------------------------

        st.subheader("Input Values")

        st.dataframe(
            eta_input,
            use_container_width=True
        )


        # ---------------------------------------------
        # PREDICTION
        # ---------------------------------------------

        prediction = eta_model.predict(
            eta_input
        )[0]


        prediction = max(
            0,
            prediction
        )


        # ---------------------------------------------
        # DISPLAY RESULT
        # ---------------------------------------------

        st.success(
            f"Predicted Actual Delivery Time: "
            f"{prediction:.2f} hours"
        )


        # ---------------------------------------------
        # COMPARE WITH PROMISED ETA
        # ---------------------------------------------

        difference = (
            prediction -
            promised_eta_hours
        )


        if difference > 0:

            st.warning(
                f"⚠️ Possible delay: "
                f"{difference:.2f} hours"
            )

        elif difference < 0:

            st.info(
                f"✅ Possible early delivery: "
                f"{abs(difference):.2f} hours"
            )

        else:

            st.success(
                "✅ Delivery is expected around the promised ETA."
            )


# =========================================================
# MAINTENANCE PREDICTION
# =========================================================

else:

    st.header("🔧 Vehicle Maintenance Prediction")

    st.write(
        "Enter the vehicle details to predict whether "
        "maintenance/failure is likely to be reported."
    )


    # -----------------------------------------------------
    # CREATE COLUMNS
    # -----------------------------------------------------

    col1, col2 = st.columns(2)


    # -----------------------------------------------------
    # SERVICE TYPE
    # -----------------------------------------------------

    with col1:

        service_type = st.selectbox(

            "Service Type",

            sorted(
                maintenance_df["service_type"]
                .dropna()
                .unique()
            )
        )


    # -----------------------------------------------------
    # PARTS REPLACED
    # -----------------------------------------------------

    with col2:

        parts_replaced = st.selectbox(

            "Parts Replaced",

            sorted(
                maintenance_df["parts_replaced"]
                .dropna()
                .unique()
            )
        )


    # -----------------------------------------------------
    # MODEL NAME
    # -----------------------------------------------------

    with col1:

        model_name = st.selectbox(

            "Model Name",

            sorted(
                maintenance_df["model_name"]
                .dropna()
                .unique()
            )
        )


    # -----------------------------------------------------
    # VEHICLE TYPE
    # -----------------------------------------------------

    with col2:

        vehicle_type = st.selectbox(

            "Vehicle Type",

            sorted(
                maintenance_df["vehicle_type"]
                .dropna()
                .unique()
            )
        )


    # -----------------------------------------------------
    # HUB CODE
    # -----------------------------------------------------

    with col1:

        hub_code = st.selectbox(

            "Hub Code",

            sorted(
                maintenance_df["hub_code"]
                .dropna()
                .unique()
            )
        )


    # -----------------------------------------------------
    # FLEET STATUS
    # -----------------------------------------------------

    with col2:

        fleet_status = st.selectbox(

            "Fleet Status",

            sorted(
                maintenance_df["fleet_status"]
                .dropna()
                .unique()
            )
        )


    # -----------------------------------------------------
    # CAPACITY
    # -----------------------------------------------------

    with col1:

        capacity_kg = st.number_input(

            "Capacity (KG)",

            min_value=0.0,

            value=300.0,

            step=10.0
        )


    # -----------------------------------------------------
    # MAX RANGE
    # -----------------------------------------------------

    with col2:

        max_range_km = st.number_input(

            "Maximum Range (KM)",

            min_value=0.0,

            value=800.0,

            step=10.0
        )


    # -----------------------------------------------------
    # AVERAGE SPEED
    # -----------------------------------------------------

    with col1:

        avg_speed_kmph = st.number_input(

            "Average Speed (KM/H)",

            min_value=0.0,

            value=70.0,

            step=5.0
        )


    # -----------------------------------------------------
    # ODOMETER
    # -----------------------------------------------------

    with col2:

        odometer_km = st.number_input(

            "Odometer (KM)",

            min_value=0.0,

            value=15000.0,

            step=500.0
        )


    # -----------------------------------------------------
    # VEHICLE AGE
    # -----------------------------------------------------

    with col1:

        vehicle_age_years = st.number_input(

            "Vehicle Age (Years)",

            min_value=0.0,

            value=2.5,

            step=0.5
        )


    # -----------------------------------------------------
    # DAYS SINCE LAST SERVICE
    # -----------------------------------------------------

    # with col2:

    #     days_since_last_service = st.number_input(

    #         "Days Since Last Service",

    #         min_value=0,

    #         value=45,

    #         step=1
    #     )


    # -----------------------------------------------------
    # PREDICT BUTTON
    # -----------------------------------------------------

    if st.button(
        "🔧 Predict Maintenance",
        use_container_width=True
    ):

        # ---------------------------------------------
        # CREATE INPUT DATAFRAME
        # ---------------------------------------------

        maintenance_input = pd.DataFrame({

            "service_type": [
                service_type
            ],

            "parts_replaced": [
                parts_replaced
            ],

            "model_name": [
                model_name
            ],

            "vehicle_type": [
                vehicle_type
            ],

            "capacity_kg": [
                capacity_kg
            ],

            "max_range_km": [
                max_range_km
            ],

            "avg_speed_kmph": [
                avg_speed_kmph
            ],

            "hub_code": [
                hub_code
            ],

            "odometer_km": [
                odometer_km
            ],

            "fleet_status": [
                fleet_status
            ],

            "vehicle_age_years": [
                vehicle_age_years
            ],

            # "days_since_last_service": [
            #     days_since_last_service
            # ]

        })


        # ---------------------------------------------
        # DISPLAY INPUT
        # ---------------------------------------------

        st.subheader("Vehicle Input Values")

        st.dataframe(
            maintenance_input,
            use_container_width=True
        )


        # ---------------------------------------------
        # PREDICTION
        # ---------------------------------------------

        prediction = maintenance_model.predict(
            maintenance_input
        )[0]


        # ---------------------------------------------
        # PROBABILITY
        # ---------------------------------------------

        probability = maintenance_model.predict_proba(
            maintenance_input
        )[0]


        # ---------------------------------------------
        # GET CLASS NAMES
        # ---------------------------------------------

        classes = maintenance_model.classes_


        # ---------------------------------------------
        # DISPLAY PREDICTION
        # ---------------------------------------------

        st.subheader("Prediction Result")


        if prediction == 1 or str(prediction).lower() == "yes":

            st.error(
                "🔴 Maintenance Needed"
            )

        else:

            st.success(
                "🟢 No Maintenance"
            )



if st.button("⬅️ Back to Employee Dashboard"):

      st.switch_page(
        "pages/employee_feature_page.py"
    )        


        # ---------------------------------------------
        # DISPLAY PROBABILITY
        # ---------------------------------------------

        # st.subheader("Prediction Probability")


        # probability_df = pd.DataFrame({

        #     "Class": classes,

        #     "Probability": probability

        # })


        # probability_df["Probability"] = (
        #     probability_df["Probability"] * 100
        # ).round(2)


        # probability_df = probability_df.rename(

        #     columns={
        #         "Probability": "Probability (%)"
        #     }

        # )


        # st.dataframe(
        #     probability_df,
        #     use_container_width=True
        # )
