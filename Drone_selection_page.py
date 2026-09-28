import streamlit as st
import pandas as pd
import numpy as np


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Drone Selection",
    page_icon="🚁",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🚁 Drone Selection Based on Order")
st.write(
    "Enter an Order ID to find the most suitable drone "
    "based on order details and drone telemetry."
)


# ============================================================
# FILE PATHS
# ============================================================

ORDERS_FILE = "orders_with_hub.csv"
TELEMETRY_FILE = "drone_telemetry.csv"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    orders = pd.read_csv(ORDERS_FILE)

    telemetry = pd.read_csv(TELEMETRY_FILE)

    return orders, telemetry


orders, telemetry = load_data()


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

orders.columns = (
    orders.columns
    .str.strip()
    .str.lower()
)

telemetry.columns = (
    telemetry.columns
    .str.strip()
    .str.lower()
)


# ============================================================
# CLEAN ORDER DATA
# ============================================================

orders["order_id"] = (
    orders["order_id"]
    .astype(str)
    .str.strip()
    .str.lower()
)


# Package weight
orders["package_weight_kg"] = pd.to_numeric(
    orders["package_weight"],
    errors="coerce"
)


# Coordinates
coordinate_columns = [
    "hub_lat",
    "hub_lon",
    "destination_lat",
    "destination_lon"
]

for col in coordinate_columns:

    orders[col] = pd.to_numeric(
        orders[col],
        errors="coerce"
    )


# ============================================================
# HAVERSINE DISTANCE
# ============================================================

def haversine_distance(
    lat1,
    lon1,
    lat2,
    lon2
):

    R = 6371.0

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)

    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2
        +
        np.cos(lat1)
        *
        np.cos(lat2)
        *
        np.sin(dlon / 2) ** 2
    )

    c = 2 * np.arcsin(
        np.sqrt(a)
    )

    return R * c


# ============================================================
# CALCULATE ORDER DISTANCE
# # ============================================================

orders["hub_destination_distance_km"] = (
    haversine_distance(
        orders["hub_lat"],
        orders["hub_lon"],
        orders["destination_lat"],
        orders["destination_lon"]
    )
)


# # ============================================================
# # CLEAN TELEMETRY
# # ============================================================

telemetry["drone_id"] = (
    telemetry["drone_id"]
    .astype(str)
    .str.strip()
    .str.lower()
)


# # Timestamp
telemetry["flight_timestamp"] = pd.to_datetime(
    telemetry["flight_timestamp"],
    errors="coerce"
)


# # Numeric columns
numeric_columns = [
    "battery_start_pct",
    "battery_end_pct",
    "battery_health_pct",
    "motor_temp_c",
    "vibration_rms",
    "payload_kg",
    "max_altitude_m",
    "wind_speed_kmph",
    "rotor_rpm_avg",
    "route_deviation_m",
    "maintenance_required"
]


for col in numeric_columns:

    telemetry[col] = pd.to_numeric(
        telemetry[col],
        errors="coerce"
    )


# # GPS
telemetry["gps_signal_quality"] = (
    telemetry["gps_signal_quality"]
    .astype(str)
    .str.strip()
    .str.lower()
)


# ============================================================
# GET LATEST TELEMETRY FOR EACH DRONE
# ============================================================

latest_telemetry = (
    telemetry
    .sort_values("flight_timestamp")
    .drop_duplicates(
        subset=["drone_id"],
        keep="last"
    )
    .reset_index(drop=True)
)


# ============================================================
# DRONE CONSTRAINTS
# ============================================================

MAX_PAYLOAD_KG = 5.0

MAX_RANGE_KM = 50.0

MIN_BATTERY_PCT = 50.0

MIN_BATTERY_HEALTH_PCT = 70.0

MAX_WIND_KMPH = 30.0

MAX_MOTOR_TEMP_C = 85.0

MAX_VIBRATION_RMS = 5.0

MAX_ROUTE_DEVIATION_M = 50.0


# ============================================================
# FUNCTION TO CHECK DRONE
# ============================================================

def check_drone(order, drone):

    reasons = []


    # --------------------------------------------------------
    # 1. PACKAGE WEIGHT
    # --------------------------------------------------------

    if pd.isna(order["package_weight_kg"]):

        reasons.append(
            "Package weight missing"
        )

    elif order["package_weight_kg"] > MAX_PAYLOAD_KG:

        reasons.append(
            "Package weight exceeds drone payload capacity"
        )


    # --------------------------------------------------------
    # 2. DISTANCE
    # --------------------------------------------------------

    if pd.isna(
        order["hub_destination_distance_km"]
    ):

        reasons.append(
            "Destination distance unavailable"
        )

    elif (
        order["hub_destination_distance_km"]
        > MAX_RANGE_KM
    ):

        reasons.append(
            "Destination is beyond drone range"
        )


    # --------------------------------------------------------
    # 3. BATTERY
    # --------------------------------------------------------

    if pd.isna(
        drone["battery_start_pct"]
    ):

        reasons.append(
            "Battery information unavailable"
        )

    elif (
        drone["battery_start_pct"]
        < MIN_BATTERY_PCT
    ):

        reasons.append(
            "Battery too low"
        )


    # --------------------------------------------------------
    # 4. BATTERY HEALTH
    # --------------------------------------------------------

    if pd.isna(
        drone["battery_health_pct"]
    ):

        reasons.append(
            "Battery health unavailable"
        )

    elif (
        drone["battery_health_pct"]
        < MIN_BATTERY_HEALTH_PCT
    ):

        reasons.append(
            "Battery health too low"
        )


    # --------------------------------------------------------
    # 5. WIND
    # --------------------------------------------------------

    if pd.isna(
        drone["wind_speed_kmph"]
    ):

        reasons.append(
            "Wind information unavailable"
        )

    elif (
        drone["wind_speed_kmph"]
        > MAX_WIND_KMPH
    ):

        reasons.append(
            "Wind speed too high"
        )


    # --------------------------------------------------------
    # 6. GPS
    # --------------------------------------------------------

    if (
        drone["gps_signal_quality"]
        not in ["good", "fair"]
    ):

        reasons.append(
            "GPS signal is poor"
        )


    # --------------------------------------------------------
    # 7. MAINTENANCE
    # --------------------------------------------------------

    if (
        drone["maintenance_required"]
        != 0
    ):

        reasons.append(
            "Drone requires maintenance"
        )


    # --------------------------------------------------------
    # 8. ERROR CODE
    # --------------------------------------------------------

    error_code = drone["error_codes"]

    if pd.notna(error_code):

        error_code = str(
            error_code
        ).strip().lower()

        if error_code not in [
            "",
            "nan",
            "none"
        ]:

            reasons.append(
                "Drone has error codes"
            )


    # --------------------------------------------------------
    # 9. MOTOR TEMPERATURE
    # --------------------------------------------------------

    if pd.isna(
        drone["motor_temp_c"]
    ):

        reasons.append(
            "Motor temperature unavailable"
        )

    elif (
        drone["motor_temp_c"]
        > MAX_MOTOR_TEMP_C
    ):

        reasons.append(
            "Motor temperature too high"
        )


    # --------------------------------------------------------
    # 10. VIBRATION
    # --------------------------------------------------------

    if pd.isna(
        drone["vibration_rms"]
    ):

        reasons.append(
            "Vibration information unavailable"
        )

    elif (
        drone["vibration_rms"]
        > MAX_VIBRATION_RMS
    ):

        reasons.append(
            "Vibration too high"
        )


    # --------------------------------------------------------
    # 11. ROUTE DEVIATION
    # --------------------------------------------------------

    if pd.isna(
        drone["route_deviation_m"]
    ):

        reasons.append(
            "Route deviation unavailable"
        )

    elif (
        drone["route_deviation_m"]
        > MAX_ROUTE_DEVIATION_M
    ):

        reasons.append(
            "Route deviation too high"
        )


    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    if len(reasons) == 0:

        return True, "All constraints satisfied"

    else:

        return False, "; ".join(reasons)


# ============================================================
# ORDER ID INPUT
# ============================================================

st.subheader("🔎 Enter Order ID")


order_id = st.text_input(
    "Order ID",
    placeholder="Example: ord-005123"
)


# ============================================================
# SEARCH BUTTON
# ============================================================

if st.button(
    "🚁 Find Suitable Drone",
    type="primary"
):

    if order_id.strip() == "":

        st.warning(
            "Please enter an Order ID."
        )

        st.stop()


    # Clean input
    order_id = (
        order_id
        .strip()
        .lower()
    )


    # ========================================================
    # FIND ORDER
    # ========================================================

    order = orders[
        orders["order_id"] == order_id
    ]


    if order.empty:

        st.error(
            f"Order ID '{order_id}' was not found."
        )

        st.stop()


    # Take first matching order
    order = order.iloc[0]


    # ========================================================
    # DISPLAY ORDER DETAILS
    # ========================================================

    st.subheader("📦 Order Details")


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Order ID",
        order["order_id"]
    )


    col2.metric(
        "Package Weight",
        f"{order['package_weight_kg']:.2f} kg"
        if pd.notna(order["package_weight_kg"])
        else "N/A"
    )


    col3.metric(
        "Distance",
        f"{order['hub_destination_distance_km']:.2f} km"
        if pd.notna(
            order["hub_destination_distance_km"]
        )
        else "N/A"
    )


    col4.metric(
        "Priority",
        str(
            order.get(
                "delivery_priority",
                "N/A"
            )
        )
    )


    # ========================================================
    # MORE ORDER DETAILS
    # ========================================================

    detail_col1, detail_col2 = st.columns(2)


    with detail_col1:

        st.write("**Origin Hub:**")

        st.write(
            order.get(
                "origin_hub",
                "N/A"
            )
        )


        st.write("**Destination City:**")

        st.write(
            order.get(
                "destination_city",
                "N/A"
            )
        )


        st.write("**Destination State:**")

        st.write(
            order.get(
                "destination_state",
                "N/A"
            )
        )


    with detail_col2:

        st.write("**Weather:**")

        st.write(
            order.get(
                "weather_condition_at_dest",
                "N/A"
            )
        )


        st.write("**Destination Latitude:**")

        st.write(
            order["destination_lat"]
        )


        st.write("**Destination Longitude:**")

        st.write(
            order["destination_lon"]
        )


    # ========================================================
    # CHECK EVERY DRONE
    # ========================================================

    results = []


    for _, drone in latest_telemetry.iterrows():

        eligible, reason = check_drone(
            order,
            drone
        )


        # Calculate score
        score = 0


        if eligible:

            score += 1


        # Better battery health
        if (
            pd.notna(drone["battery_health_pct"])
        ):

            score += (
                drone["battery_health_pct"]
                / 100
            )


        # Better battery level
        if (
            pd.notna(drone["battery_start_pct"])
        ):

            score += (
                drone["battery_start_pct"]
                / 100
            )


        # Lower temperature is better
        if (
            pd.notna(drone["motor_temp_c"])
        ):

            score += max(
                0,
                (
                    MAX_MOTOR_TEMP_C
                    - drone["motor_temp_c"]
                )
                / MAX_MOTOR_TEMP_C
            )


        results.append({

            "drone_id":
                drone["drone_id"],

            "battery_start_pct":
                drone["battery_start_pct"],

            "battery_health_pct":
                drone["battery_health_pct"],

            "motor_temp_c":
                drone["motor_temp_c"],

            "vibration_rms":
                drone["vibration_rms"],

            "wind_speed_kmph":
                drone["wind_speed_kmph"],

            "gps_signal_quality":
                drone["gps_signal_quality"],

            "maintenance_required":
                drone["maintenance_required"],

            "error_codes":
                drone["error_codes"],

            "route_deviation_m":
                drone["route_deviation_m"],

            "eligible":
                eligible,

            "reason":
                reason,

            "score":
                score

        })


    # ========================================================
    # CREATE RESULTS DATAFRAME
    # ========================================================

    results_df = pd.DataFrame(
        results
    )


    # ========================================================
    # ELIGIBLE DRONES
    # ========================================================

    eligible_drones = results_df[
        results_df["eligible"] == True
    ].copy()


    # ========================================================
    # BEST DRONE
    # ========================================================

    if eligible_drones.empty:

        st.error(
            "❌ No suitable drone is available "
            "for this order."
        )


        st.subheader(
            "Why are the drones not suitable?"
        )


        st.dataframe(
            results_df[
                [
                    "drone_id",
                    "eligible",
                    "reason"
                ]
            ],
            use_container_width=True
        )


    else:

        # Sort by score
        eligible_drones = (
            eligible_drones
            .sort_values(
                by="score",
                ascending=False
            )
            .reset_index(drop=True)
        )


        best_drone = (
            eligible_drones
            .iloc[0]
        )


        # ====================================================
        # FINAL VEHICLE ID
        # ====================================================

        st.success(
            "✅ Suitable drone found!"
        )


        st.subheader(
            "🚁 Recommended Vehicle"
        )


        st.markdown(
            f"""
            ## Vehicle ID: `{best_drone["drone_id"]}`
            """
        )


        # ====================================================
        # DRONE DETAILS
        # ====================================================

        col1, col2, col3, col4 = st.columns(4)


        col1.metric(
            "Vehicle ID",
            best_drone["drone_id"]
        )


        col2.metric(
            "Battery",
            f"{best_drone['battery_start_pct']:.1f}%"
        )


        col3.metric(
            "Battery Health",
            f"{best_drone['battery_health_pct']:.1f}%"
        )


        col4.metric(
            "GPS",
            best_drone["gps_signal_quality"]
        )


        # ====================================================
        # OTHER TELEMETRY
        # ====================================================

        st.subheader(
            "Drone Telemetry"
        )


        telemetry_display = pd.DataFrame({

            "Parameter": [
                "Vehicle ID",
                "Battery Start",
                "Battery Health",
                "Motor Temperature",
                "Vibration RMS",
                "Wind Speed",
                "GPS Signal",
                "Maintenance Required",
                "Error Codes",
                "Route Deviation"
            ],

            "Value": [
                best_drone["drone_id"],
                f"{best_drone['battery_start_pct']:.2f}%",
                f"{best_drone['battery_health_pct']:.2f}%",
                f"{best_drone['motor_temp_c']:.2f} °C",
                f"{best_drone['vibration_rms']:.2f}",
                f"{best_drone['wind_speed_kmph']:.2f} km/h",
                best_drone["gps_signal_quality"],
                best_drone["maintenance_required"],
                best_drone["error_codes"]
                if pd.notna(
                    best_drone["error_codes"]
                )
                else "None",
                f"{best_drone['route_deviation_m']:.2f} m"
            ]

        })


        st.dataframe(
            telemetry_display,
            use_container_width=True,
            hide_index=True
        )


        # ====================================================
        # ALL ELIGIBLE DRONES
        # ====================================================

        st.subheader(
            "Other Suitable Drones"
        )


        st.dataframe(
            eligible_drones[
                [
                    "drone_id",
                    "battery_start_pct",
                    "battery_health_pct",
                    "motor_temp_c",
                    "vibration_rms",
                    "wind_speed_kmph",
                    "gps_signal_quality",
                    "score"
                ]
            ],
            use_container_width=True
        )


        # ====================================================
        # DOWNLOAD
        # ====================================================

        csv = results_df.to_csv(
            index=False
        ).encode("utf-8")


        st.download_button(
            "⬇️ Download Drone Analysis",
            data=csv,
            file_name=f"{order_id}_drone_analysis.csv",
            mime="text/csv"
        )
if st.button("⬅️ Back to Employee Dashboard"):

    st.switch_page(
        "pages/employee_feature_page.py"
    )
