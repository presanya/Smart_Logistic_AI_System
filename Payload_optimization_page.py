
# import streamlit as st
# import pandas as pd
# import numpy as np

# # ============================================================
# # PAGE CONFIGURATION
# # ============================================================

# st.set_page_config(
#     page_title="Payload Optimization",
#     page_icon="📦",
#     layout="wide"
# )

# st.title("📦 Payload Optimization")
# st.write(
#     "Select an Order ID to find the most suitable vehicle based on "
#     "payload capacity and vehicle constraints."
# )

# # ============================================================
# # FILE PATHS
# # ============================================================

# ORDERS_FILE = "orders_with_hub.csv"
# FLEET_FILE = "fleet_vehicles_cl.csv"
# DRONE_TELEMETRY_FILE = "drone_telemetry_cl.csv"

# # ============================================================
# # LOAD DATA
# # ============================================================

# @st.cache_data
# def load_data():

#     orders = pd.read_csv(ORDERS_FILE)
#     fleet = pd.read_csv(FLEET_FILE)

#     # Drone telemetry is optional
#     try:
#         drone_telemetry = pd.read_csv(DRONE_TELEMETRY_FILE)
#     except:
#         drone_telemetry = pd.DataFrame()

#     return orders, fleet, drone_telemetry


# orders, fleet, drone_telemetry = load_data()

# # ============================================================
# # STANDARDIZE COLUMN NAMES
# # ============================================================

# orders.columns = orders.columns.str.strip().str.lower()
# fleet.columns = fleet.columns.str.strip().str.lower()

# if not drone_telemetry.empty:
#     drone_telemetry.columns = (
#         drone_telemetry.columns.str.strip().str.lower()
#     )

# # ============================================================
# # HELPER FUNCTION
# # ============================================================

# def find_column(df, possible_columns):

#     for col in possible_columns:
#         if col in df.columns:
#             return col

#     return None


# # ============================================================
# # IDENTIFY IMPORTANT ORDER COLUMNS
# # ============================================================

# order_id_col = find_column(
#     orders,
#     [
#         "order_id",
#         "orderid",
#         "order"
#     ]
# )

# payload_col = find_column(
#     orders,
#     [
#         "package_weight_kg",
#         "package_weight",
#         "weight_kg",
#         "weight",
#         "payload_kg",
#         "package_weight_kgs"
#     ]
# )

# quantity_col = find_column(
#     orders,
#     [
#         "quantity",
#         "qty"
#     ]
# )

# distance_col = find_column(
#     orders,
#     [
#         "distance_km",
#         "distance",
#         "delivery_distance_km"
#     ]
# )

# priority_col = find_column(
#     orders,
#     [
#         "delivery_priority",
#         "priority"
#     ]
# )

# origin_col = find_column(
#     orders,
#     [
#         "origin_city",
#         "origin",
#         "origin_hub",
#         "origin_city_name"
#     ]
# )

# destination_col = find_column(
#     orders,
#     [
#         "destination_city",
#         "destination",
#         "destination_city_name"
#     ]
# )

# # ============================================================
# # VALIDATION
# # ============================================================

# if order_id_col is None:

#     st.error(
#         "Order ID column was not found in the orders dataset."
#     )

#     st.write("Available columns:")
#     st.write(list(orders.columns))

#     st.stop()


# if payload_col is None:

#     st.error(
#         "Package weight / payload column was not found."
#     )

#     st.write("Expected one of:")
#     st.write(
#         [
#             "package_weight_kg",
#             "package_weight",
#             "weight_kg",
#             "payload_kg"
#         ]
#     )

#     st.write("Available columns:")
#     st.write(list(orders.columns))

#     st.stop()


# # ============================================================
# # CLEAN ORDER DATA
# # ============================================================

# orders[order_id_col] = (
#     orders[order_id_col]
#     .astype(str)
#     .str.strip()
#     .str.lower()
# )

# orders[payload_col] = pd.to_numeric(
#     orders[payload_col],
#     errors="coerce"
# )

# orders = orders.dropna(
#     subset=[order_id_col, payload_col]
# )

# orders = orders[
#     orders[payload_col] > 0
# ]


# # ============================================================
# # CLEAN FLEET DATA
# # ============================================================

# fleet.columns = fleet.columns.str.strip().str.lower()

# vehicle_id_col = find_column(
#     fleet,
#     [
#         "vehicle_id",
#         "vehicleid",
#         "vehicle"
#     ]
# )

# vehicle_type_col = find_column(
#     fleet,
#     [
#         "vehicle_type",
#         "veh_type",
#         "type"
#     ]
# )

# capacity_col = find_column(
#     fleet,
#     [
#         "payload_capacity_kg",
#         "payload_capacity",
#         "capacity_kg",
#         "capacity",
#         "max_payload_kg",
#         "max_payload"
#     ]
# )

# if vehicle_id_col is None:

#     st.error(
#         "Vehicle ID column was not found in fleet dataset."
#     )

#     st.write(list(fleet.columns))

#     st.stop()


# if vehicle_type_col is None:

#     st.error(
#         "Vehicle type column was not found in fleet dataset."
#     )

#     st.write(list(fleet.columns))

#     st.stop()


# # ============================================================
# # VEHICLE TYPE STANDARDIZATION
# # ============================================================

# fleet[vehicle_type_col] = (
#     fleet[vehicle_type_col]
#     .astype(str)
#     .str.strip()
#     .str.lower()
# )

# fleet[vehicle_id_col] = (
#     fleet[vehicle_id_col]
#     .astype(str)
#     .str.strip()
#     .str.lower()
# )


# # ============================================================
# # STANDARD VEHICLE TYPE MAPPING
# # ============================================================

# def standardize_vehicle_type(value):

#     value = str(value).lower().strip()

#     if value in ["truck", "trucks"]:
#         return "truck"

#     elif value in ["bike", "bikes", "motorbike", "motorcycle"]:
#         return "bike"

#     elif value in ["van", "vans"]:
#         return "van"

#     elif value in ["drone", "drones"]:
#         return "drone"

#     elif value in [
#         "air cargo",
#         "air_cargo",
#         "aircargo",
#         "air-cargo"
#     ]:
#         return "air cargo"

#     elif value in [
#         "ship",
#         "ships",
#         "sea",
#         "boat"
#     ]:
#         return "ship"

#     else:
#         return value


# fleet["vehicle_type_standard"] = (
#     fleet[vehicle_type_col]
#     .apply(standardize_vehicle_type)
# )


# # ============================================================
# # DEFAULT PAYLOAD CAPACITIES
# # ============================================================
# #
# # IMPORTANT:
# # If your fleet dataset already contains a payload capacity
# # column, that value will be used.
# #
# # Otherwise these default values are used.
# #
# # You can change these values according to your project.
# # ============================================================

# DEFAULT_CAPACITY = {

#     "bike": 20,

#     "drone": 10,

#     "van": 1000,

#     "truck": 10000,

#     "air cargo": 5000,

#     "ship": 50000

# }


# # ============================================================
# # CREATE CAPACITY COLUMN
# # ============================================================

# if capacity_col is not None:

#     fleet["payload_capacity_kg"] = pd.to_numeric(
#         fleet[capacity_col],
#         errors="coerce"
#     )

# else:

#     fleet["payload_capacity_kg"] = np.nan


# # Fill missing capacities using default values

# fleet["payload_capacity_kg"] = fleet[
#     "payload_capacity_kg"
# ].fillna(
#     fleet["vehicle_type_standard"].map(DEFAULT_CAPACITY)
# )


# # Remove invalid capacities

# fleet = fleet[
#     fleet["payload_capacity_kg"] > 0
# ]


# # ============================================================
# # OPTIONAL DRONE TELEMETRY
# # ============================================================

# if not drone_telemetry.empty:

#     telemetry_vehicle_col = find_column(
#         drone_telemetry,
#         [
#             "vehicle_id",
#             "drone_id",
#             "vehicleid"
#         ]
#     )

#     if telemetry_vehicle_col is not None:

#         drone_telemetry[telemetry_vehicle_col] = (
#             drone_telemetry[telemetry_vehicle_col]
#             .astype(str)
#             .str.strip()
#             .str.lower()
#         )


# # ============================================================
# # SIDEBAR
# # ============================================================

# st.sidebar.header("⚙️ Payload Settings")

# utilization_limit = st.sidebar.slider(
#     "Maximum Payload Utilization (%)",
#     min_value=50,
#     max_value=100,
#     value=90,
#     step=5
# )

# utilization_limit_decimal = utilization_limit / 100


# st.sidebar.write(
#     "A vehicle will be considered suitable only when the "
#     "required payload is within the selected utilization limit."
# )


# # ============================================================
# # ORDER SELECTION
# # ============================================================cd 

# st.subheader("1️⃣ Select Order")

# order_ids = sorted(
#     orders[order_id_col].unique()
# )

# selected_order_id = st.selectbox(
#     "Select Order ID",
#     order_ids
# )


# # ============================================================
# # GET SELECTED ORDER
# # ============================================================

# selected_order = orders[
#     orders[order_id_col] == selected_order_id
# ].iloc[0]


# required_payload = float(
#     selected_order[payload_col]
# )


# # ============================================================
# # ORDER INFORMATION
# # ============================================================

# st.subheader("2️⃣ Order Details")

# col1, col2, col3, col4 = st.columns(4)

# with col1:

#     st.metric(
#         "Order ID",
#         selected_order_id
#     )

# with col2:

#     st.metric(
#         "Required Payload",
#         f"{required_payload:.2f} kg"
#     )

# with col3:

#     if distance_col is not None:

#         distance_value = pd.to_numeric(
#             selected_order[distance_col],
#             errors="coerce"
#         )

#         if pd.notna(distance_value):

#             st.metric(
#                 "Distance",
#                 f"{distance_value:.2f} km"
#             )

#         else:

#             st.metric(
#                 "Distance",
#                 "N/A"
#             )

#     else:

#         st.metric(
#             "Distance",
#             "N/A"
#         )


# with col4:

#     if priority_col is not None:

#         st.metric(
#             "Priority",
#             str(selected_order[priority_col])
#         )

#     else:

#         st.metric(
#             "Priority",
#             "N/A"
#         )


# # ============================================================
# # MORE ORDER DETAILS
# # ============================================================

# detail_data = {}

# if quantity_col is not None:
#     detail_data["Quantity"] = selected_order[quantity_col]

# if origin_col is not None:
#     detail_data["Origin"] = selected_order[origin_col]

# if destination_col is not None:
#     detail_data["Destination"] = selected_order[destination_col]

# if distance_col is not None:
#     detail_data["Distance (km)"] = selected_order[distance_col]

# if priority_col is not None:
#     detail_data["Priority"] = selected_order[priority_col]


# if len(detail_data) > 0:

#     st.dataframe(
#         pd.DataFrame(
#             [detail_data]
#         ),
#         use_container_width=True,
#         hide_index=True
#     )


# # ============================================================
# # PAYLOAD OPTIMIZATION
# # ============================================================

# st.subheader("3️⃣ Vehicle Payload Analysis")


# # ------------------------------------------------------------
# # Calculate maximum usable payload
# # ------------------------------------------------------------

# fleet["maximum_usable_payload_kg"] = (
#     fleet["payload_capacity_kg"]
#     * utilization_limit_decimal
# )


# # ------------------------------------------------------------
# # Calculate payload remaining
# # ------------------------------------------------------------

# fleet["remaining_payload_kg"] = (
#     fleet["maximum_usable_payload_kg"]
#     - required_payload
# )


# # ------------------------------------------------------------
# # Calculate utilization
# # ------------------------------------------------------------

# fleet["payload_utilization_pct"] = (
#     required_payload
#     / fleet["payload_capacity_kg"]
# ) * 100


# # ------------------------------------------------------------
# # Determine suitability
# # ------------------------------------------------------------

# fleet["suitable"] = (
#     required_payload
#     <= fleet["maximum_usable_payload_kg"]
# )


# # ============================================================
# # SORT VEHICLES
# # ============================================================

# suitable_vehicles = fleet[
#     fleet["suitable"] == True
# ].copy()


# # ============================================================
# # VEHICLE TYPE PRIORITY
# # ============================================================

# vehicle_type_priority = {

#     "bike": 1,

#     "drone": 2,

#     "van": 3,

#     "truck": 4,

#     "air cargo": 5,

#     "ship": 6
# }


# suitable_vehicles["type_priority"] = (
#     suitable_vehicles["vehicle_type_standard"]
#     .map(vehicle_type_priority)
#     .fillna(99)
# )


# # ============================================================
# # SORT BY:
# # 1. Lowest payload utilization
# # 2. Smaller capacity
# # 3. Vehicle type
# # ============================================================

# suitable_vehicles = suitable_vehicles.sort_values(
#     by=[
#         "payload_utilization_pct",
#         "payload_capacity_kg",
#         "type_priority"
#     ],
#     ascending=[
#         True,
#         True,
#         True
#     ]
# )


# # ============================================================
# # BEST VEHICLE
# # ============================================================

# if len(suitable_vehicles) > 0:

#     best_vehicle = suitable_vehicles.iloc[0]

#     best_vehicle_id = best_vehicle[
#         vehicle_id_col
#     ]

#     best_vehicle_type = best_vehicle[
#         "vehicle_type_standard"
#     ]

#     best_capacity = best_vehicle[
#         "payload_capacity_kg"
#     ]

#     best_utilization = best_vehicle[
#         "payload_utilization_pct"
#     ]

#     best_remaining = best_vehicle[
#         "remaining_payload_kg"
#     ]


#     # ========================================================
#     # RECOMMENDATION
#     # ========================================================

#     st.success(
#         f"✅ Recommended Vehicle: {best_vehicle_id.upper()}"
#     )


#     col1, col2, col3, col4 = st.columns(4)

#     with col1:

#         st.metric(
#             "Vehicle ID",
#             best_vehicle_id.upper()
#         )

#     with col2:

#         st.metric(
#             "Vehicle Type",
#             best_vehicle_type.title()
#         )

#     with col3:

#         st.metric(
#             "Payload Capacity",
#             f"{best_capacity:.2f} kg"
#         )

#     with col4:

#         st.metric(
#             "Payload Utilization",
#             f"{best_utilization:.2f}%"
#         )


#     # ========================================================
#     # PAYLOAD PROGRESS
#     # ========================================================

#     st.write("### Payload Utilization")

#     progress_value = min(
#         best_utilization / 100,
#         1.0
#     )

#     st.progress(
#         progress_value
#     )

#     st.write(
#         f"Required Payload: "
#         f"**{required_payload:.2f} kg**"
#     )

#     st.write(
#         f"Vehicle Capacity: "
#         f"**{best_capacity:.2f} kg**"
#     )

#     st.write(
#         f"Remaining Capacity: "
#         f"**{best_remaining:.2f} kg**"
#     )


# else:

#     st.error(
#         "❌ No vehicle can safely carry this payload."
#     )


# # ============================================================
# # ALL SUITABLE VEHICLES
# # ============================================================

# st.subheader("4️⃣ Suitable Vehicles")

# if len(suitable_vehicles) > 0:

#     display_columns = [
#         vehicle_id_col,
#         "vehicle_type_standard",
#         "payload_capacity_kg",
#         "maximum_usable_payload_kg",
#         "remaining_payload_kg",
#         "payload_utilization_pct"
#     ]

#     display_df = suitable_vehicles[
#         display_columns
#     ].copy()

#     display_df.columns = [
#         "Vehicle ID",
#         "Vehicle Type",
#         "Capacity (kg)",
#         "Usable Capacity (kg)",
#         "Remaining Capacity (kg)",
#         "Payload Utilization (%)"
#     ]

#     display_df["Payload Utilization (%)"] = (
#         display_df["Payload Utilization (%)"]
#         .round(2)
#     )

#     display_df["Capacity (kg)"] = (
#         display_df["Capacity (kg)"]
#         .round(2)
#     )

#     display_df["Usable Capacity (kg)"] = (
#         display_df["Usable Capacity (kg)"]
#         .round(2)
#     )

#     display_df["Remaining Capacity (kg)"] = (
#         display_df["Remaining Capacity (kg)"]
#         .round(2)
#     )

#     st.dataframe(
#         display_df,
#         use_container_width=True,
#         hide_index=True
#     )


# # ============================================================
# # VEHICLE TYPE SUMMARY
# # ============================================================

# st.subheader("5️⃣ Vehicle Type Comparison")


# vehicle_summary = (
#     suitable_vehicles
#     .groupby("vehicle_type_standard")
#     .agg(
#         vehicles_available=(
#             vehicle_id_col,
#             "count"
#         ),

#         minimum_capacity_kg=(
#             "payload_capacity_kg",
#             "min"
#         ),

#         average_capacity_kg=(
#             "payload_capacity_kg",
#             "mean"
#         ),

#         best_utilization_pct=(
#             "payload_utilization_pct",
#             "min"
#         )
#     )
#     .reset_index()
# )


# if len(vehicle_summary) > 0:

#     vehicle_summary.columns = [
#         "Vehicle Type",
#         "Vehicles Available",
#         "Minimum Capacity (kg)",
#         "Average Capacity (kg)",
#         "Best Utilization (%)"
#     ]

#     vehicle_summary[
#         "Minimum Capacity (kg)"
#     ] = vehicle_summary[
#         "Minimum Capacity (kg)"
#     ].round(2)

#     vehicle_summary[
#         "Average Capacity (kg)"
#     ] = vehicle_summary[
#         "Average Capacity (kg)"
#     ].round(2)

#     vehicle_summary[
#         "Best Utilization (%)"
#     ] = vehicle_summary[
#         "Best Utilization (%)"
#     ].round(2)

#     st.dataframe(
#         vehicle_summary,
#         use_container_width=True,
#         hide_index=True
#     )

# else:

#     st.warning(
#         "No vehicle type can handle this payload."
#     )


# # ============================================================
# # ALL 6 VEHICLE TYPES
# # ============================================================

# st.subheader("6️⃣ All Vehicle Types")

# all_vehicle_types = pd.DataFrame({

#     "Vehicle Type": [
#         "Bike",
#         "Drone",
#         "Van",
#         "Truck",
#         "Air Cargo",
#         "Ship"
#     ],

#     "Default Capacity (kg)": [
#         DEFAULT_CAPACITY["bike"],
#         DEFAULT_CAPACITY["drone"],
#         DEFAULT_CAPACITY["van"],
#         DEFAULT_CAPACITY["truck"],
#         DEFAULT_CAPACITY["air cargo"],
#         DEFAULT_CAPACITY["ship"]
#     ]
# })


# # Add actual fleet counts

# fleet_counts = (
#     fleet["vehicle_type_standard"]
#     .value_counts()
# )


# all_vehicle_types[
#     "Vehicles in Fleet"
# ] = all_vehicle_types[
#     "Vehicle Type"
# ].str.lower().map(
#     fleet_counts
# ).fillna(0).astype(int)


# # Check suitability

# all_vehicle_types[
#     "Suitable for Order"
# ] = all_vehicle_types[
#     "Default Capacity (kg)"
# ].apply(
#     lambda x:
#     "Yes"
#     if required_payload <= x * utilization_limit_decimal
#     else "No"
# )


# st.dataframe(
#     all_vehicle_types,
#     use_container_width=True,
#     hide_index=True
# )


# # ============================================================
# # VEHICLE TYPE FILTER
# # ============================================================

# st.subheader("7️⃣ Analyze Vehicle Type")

# selected_vehicle_type = st.selectbox(
#     "Select Vehicle Type",
#     [
#         "truck",
#         "bike",
#         "van",
#         "drone",
#         "air cargo",
#         "ship"
#     ]
# )


# type_vehicles = fleet[
#     fleet["vehicle_type_standard"]
#     == selected_vehicle_type
# ].copy()


# if len(type_vehicles) == 0:

#     st.warning(
#         f"No {selected_vehicle_type.title()} vehicles "
#         "are available in the fleet."
#     )

# else:

#     type_vehicles[
#         "remaining_payload_kg"
#     ] = (
#         type_vehicles[
#             "maximum_usable_payload_kg"
#         ]
#         - required_payload
#     )

#     type_vehicles[
#         "payload_utilization_pct"
#     ] = (
#         required_payload
#         / type_vehicles[
#             "payload_capacity_kg"
#         ]
#     ) * 100


#     type_vehicles[
#         "suitable"
#     ] = (
#         required_payload
#         <= type_vehicles[
#             "maximum_usable_payload_kg"
#         ]
#     )


#     type_display = type_vehicles[
#         [
#             vehicle_id_col,
#             "payload_capacity_kg",
#             "maximum_usable_payload_kg",
#             "remaining_payload_kg",
#             "payload_utilization_pct",
#             "suitable"
#         ]
#     ].copy()


#     type_display.columns = [
#         "Vehicle ID",
#         "Capacity (kg)",
#         "Usable Capacity (kg)",
#         "Remaining Capacity (kg)",
#         "Utilization (%)",
#         "Suitable"
#     ]


#     type_display[
#         "Utilization (%)"
#     ] = type_display[
#         "Utilization (%)"
#     ].round(2)


#     type_display = type_display.sort_values(
#         by="Utilization (%)"
#     )


#     st.dataframe(
#         type_display,
#         use_container_width=True,
#         hide_index=True
#     )


# # ============================================================
# # DRONE-SPECIFIC TELEMETRY CHECK
# # ============================================================

# if (
#     selected_vehicle_type == "drone"
#     and not drone_telemetry.empty
# ):

#     st.subheader(
#         "🚁 Drone Payload & Telemetry Check"
#     )

#     telemetry_vehicle_col = find_column(
#         drone_telemetry,
#         [
#             "vehicle_id",
#             "drone_id",
#             "vehicleid"
#         ]
#     )


#     if telemetry_vehicle_col is not None:

#         drone_vehicles = type_vehicles.copy()

#         drone_vehicles = drone_vehicles[
#             drone_vehicles["suitable"] == True
#         ]


#         if len(drone_vehicles) > 0:

#             telemetry_ids = set(
#                 drone_telemetry[
#                     telemetry_vehicle_col
#                 ]
#                 .astype(str)
#                 .str.lower()
#             )


#             drone_vehicles[
#                 "telemetry_available"
#             ] = drone_vehicles[
#                 vehicle_id_col
#             ].isin(
#                 telemetry_ids
#             )


#             st.dataframe(
#                 drone_vehicles[
#                     [
#                         vehicle_id_col,
#                         "payload_capacity_kg",
#                         "remaining_payload_kg",
#                         "payload_utilization_pct",
#                         "telemetry_available"
#                     ]
#                 ],
#                 use_container_width=True,
#                 hide_index=True
#             )

#         else:

#             st.warning(
#                 "No drone can carry this payload."
#             )


# # ============================================================
# # BUSINESS LOGIC SUMMARY
# # ============================================================

# st.subheader("8️⃣ Optimization Result")

# if len(suitable_vehicles) > 0:

#     st.write(
#         f"""
#         **Order:** `{selected_order_id.upper()}`

#         **Required Payload:** `{required_payload:.2f} kg`

#         **Recommended Vehicle:** `{best_vehicle_id.upper()}`

#         **Vehicle Type:** `{best_vehicle_type.title()}`

#         **Vehicle Capacity:** `{best_capacity:.2f} kg`

#         **Payload Utilization:** `{best_utilization:.2f}%`

#         **Remaining Capacity:** `{best_remaining:.2f} kg`
#         """
#     )

#     st.info(
#         "The recommendation selects a vehicle that can safely "
#         "carry the order payload while minimizing unnecessary "
#         "payload capacity."
#     )

# else:

#     st.error(
#         "No suitable vehicle was found for this order."
#     )


# # ============================================================
# # FOOTER
# # ============================================================

# st.divider()

# st.caption(
#     "Payload Optimization | SmartLogix AI Intelligent "
#     "Multi-Modal Logistics"
# )



# ============================================================
# SMARTLOGIX - PAYLOAD OPTIMIZATION
# PostgreSQL Version
# ============================================================
import streamlit as st
import pandas as pd
import numpy as np

from sqlalchemy import create_engine, text


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SmartLogix Payload Optimization",
    page_icon="📦",
    layout="wide"
)


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DATABASE = "smartlogistic_db"

DATABASE_URL = (
    f"postgresql://postgres:lavi@localhost:5432/{DATABASE}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


# ============================================================
# POSTGRESQL TABLE NAMES
# ============================================================

ORDERS_TABLE = "orders_with_hub"
FLEET_TABLE = "fleet_vehicles"
DRONE_TELEMETRY_TABLE = "drone_telemetry"


# ============================================================
# PAGE TITLE
# ============================================================

st.title("📦 SmartLogix Payload Optimization")

st.write(
    "Select an Order ID to find the most suitable vehicle "
    "based on payload capacity and vehicle constraints."
)


# ============================================================
# LOAD DATA FROM POSTGRESQL
# ============================================================

@st.cache_data(ttl=300)
def load_data():

    # --------------------------------------------------------
    # ORDERS
    # --------------------------------------------------------

    orders_query = text(
        f"""
        SELECT *
        FROM {ORDERS_TABLE}
        """
    )

    orders = pd.read_sql(
        orders_query,
        engine
    )

    # --------------------------------------------------------
    # FLEET
    # --------------------------------------------------------

    fleet_query = text(
        f"""
        SELECT *
        FROM {FLEET_TABLE}
        """
    )

    fleet = pd.read_sql(
        fleet_query,
        engine
    )

    # --------------------------------------------------------
    # DRONE TELEMETRY
    # --------------------------------------------------------

    try:

        drone_query = text(
            f"""
            SELECT *
            FROM {DRONE_TELEMETRY_TABLE}
            """
        )

        drone_telemetry = pd.read_sql(
            drone_query,
            engine
        )

    except Exception:

        drone_telemetry = pd.DataFrame()

    return (
        orders,
        fleet,
        drone_telemetry
    )


# ============================================================
# DATABASE CONNECTION / DATA LOADING
# ============================================================

try:

    orders, fleet, drone_telemetry = load_data()

except Exception as e:

    st.error(
        "❌ Unable to connect to PostgreSQL."
    )

    st.error(
        f"Database error: {e}"
    )

    st.stop()


# ============================================================
# DATABASE STATUS
# ============================================================

st.success(
    f"✅ PostgreSQL connected successfully: {DATABASE}"
)


# ============================================================
# SHOW DATA COUNTS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Orders",
        f"{len(orders):,}"
    )

with col2:

    st.metric(
        "Fleet Vehicles",
        f"{len(fleet):,}"
    )

with col3:

    st.metric(
        "Drone Telemetry",
        f"{len(drone_telemetry):,}"
    )


# ============================================================
# STANDARDIZE COLUMN NAMES
# ============================================================

orders.columns = (
    orders.columns
    .str.strip()
    .str.lower()
)

fleet.columns = (
    fleet.columns
    .str.strip()
    .str.lower()
)

if not drone_telemetry.empty:

    drone_telemetry.columns = (
        drone_telemetry.columns
        .str.strip()
        .str.lower()
    )


# ============================================================
# HELPER FUNCTION
# ============================================================

def find_column(df, possible_columns):

    for col in possible_columns:

        if col in df.columns:

            return col

    return None


# ============================================================
# IDENTIFY ORDER COLUMNS
# ============================================================

order_id_col = find_column(
    orders,
    [
        "order_id",
        "orderid",
        "order"
    ]
)


payload_col = find_column(
    orders,
    [
        "package_weight_kg",
        "package_weight",
        "weight_kg",
        "weight",
        "payload_kg",
        "package_weight_kgs"
    ]
)


quantity_col = find_column(
    orders,
    [
        "quantity",
        "qty"
    ]
)


distance_col = find_column(
    orders,
    [
        "distance_km",
        "distance",
        "delivery_distance_km"
    ]
)


priority_col = find_column(
    orders,
    [
        "delivery_priority",
        "priority"
    ]
)


origin_col = find_column(
    orders,
    [
        "origin_city",
        "origin",
        "origin_hub",
        "origin_city_name"
    ]
)


destination_col = find_column(
    orders,
    [
        "destination_city",
        "destination",
        "destination_city_name"
    ]
)


# ============================================================
# VALIDATE ORDER COLUMNS
# ============================================================

if order_id_col is None:

    st.error(
        "❌ Order ID column was not found in "
        f"PostgreSQL table `{ORDERS_TABLE}`."
    )

    st.write(
        "Available columns:"
    )

    st.write(
        list(orders.columns)
    )

    st.stop()


if payload_col is None:

    st.error(
        "❌ Package weight / payload column was not found "
        f"in PostgreSQL table `{ORDERS_TABLE}`."
    )

    st.write(
        "Expected one of:"
    )

    st.write(
        [
            "package_weight_kg",
            "package_weight",
            "weight_kg",
            "weight",
            "payload_kg"
        ]
    )

    st.write(
        "Available columns:"
    )

    st.write(
        list(orders.columns)
    )

    st.stop()


# ============================================================
# CLEAN ORDER DATA
# ============================================================

orders[order_id_col] = (
    orders[order_id_col]
    .astype(str)
    .str.strip()
    .str.lower()
)

orders[payload_col] = pd.to_numeric(
    orders[payload_col],
    errors="coerce"
)

orders = orders.dropna(
    subset=[
        order_id_col,
        payload_col
    ]
)

orders = orders[
    orders[payload_col] > 0
].copy()


# ============================================================
# IDENTIFY FLEET COLUMNS
# ============================================================

vehicle_id_col = find_column(
    fleet,
    [
        "vehicle_id",
        "vehicleid",
        "vehicle"
    ]
)


vehicle_type_col = find_column(
    fleet,
    [
        "vehicle_type",
        "veh_type",
        "type"
    ]
)


capacity_col = find_column(
    fleet,
    [
        "payload_capacity_kg",
        "payload_capacity",
        "capacity_kg",
        "capacity",
        "max_payload_kg",
        "max_payload"
    ]
)


# ============================================================
# VALIDATE FLEET COLUMNS
# ============================================================

if vehicle_id_col is None:

    st.error(
        "❌ Vehicle ID column was not found in "
        f"PostgreSQL table `{FLEET_TABLE}`."
    )

    st.write(
        list(fleet.columns)
    )

    st.stop()


if vehicle_type_col is None:

    st.error(
        "❌ Vehicle type column was not found in "
        f"PostgreSQL table `{FLEET_TABLE}`."
    )

    st.write(
        list(fleet.columns)
    )

    st.stop()


# ============================================================
# CLEAN FLEET DATA
# ============================================================

fleet[vehicle_type_col] = (
    fleet[vehicle_type_col]
    .astype(str)
    .str.strip()
    .str.lower()
)


fleet[vehicle_id_col] = (
    fleet[vehicle_id_col]
    .astype(str)
    .str.strip()
    .str.lower()
)


# ============================================================
# STANDARDIZE VEHICLE TYPE
# ============================================================

def standardize_vehicle_type(value):

    value = str(value).lower().strip()

    if value in [
        "truck",
        "trucks"
    ]:

        return "truck"

    elif value in [
        "bike",
        "bikes",
        "motorbike",
        "motorcycle"
    ]:

        return "bike"

    elif value in [
        "van",
        "vans"
    ]:

        return "van"

    elif value in [
        "drone",
        "drones"
    ]:

        return "drone"

    elif value in [
        "air cargo",
        "air_cargo",
        "aircargo",
        "air-cargo"
    ]:

        return "air cargo"

    elif value in [
        "ship",
        "ships",
        "sea",
        "boat"
    ]:

        return "ship"

    else:

        return value


fleet["vehicle_type_standard"] = (
    fleet[vehicle_type_col]
    .apply(standardize_vehicle_type)
)


# ============================================================
# DEFAULT PAYLOAD CAPACITY
# ============================================================

DEFAULT_CAPACITY = {

    "bike": 20,

    "drone": 10,

    "van": 1000,

    "truck": 10000,

    "air cargo": 5000,

    "ship": 50000

}


# ============================================================
# CREATE CAPACITY COLUMN
# ============================================================

if capacity_col is not None:

    fleet["payload_capacity_kg"] = pd.to_numeric(
        fleet[capacity_col],
        errors="coerce"
    )

else:

    fleet["payload_capacity_kg"] = np.nan


# ============================================================
# FILL MISSING CAPACITY
# ============================================================

fleet["payload_capacity_kg"] = (
    fleet["payload_capacity_kg"]
    .fillna(
        fleet["vehicle_type_standard"]
        .map(DEFAULT_CAPACITY)
    )
)


# ============================================================
# REMOVE INVALID CAPACITY
# ============================================================

fleet = fleet[
    fleet["payload_capacity_kg"] > 0
].copy()


# ============================================================
# DRONE TELEMETRY STANDARDIZATION
# ============================================================

if not drone_telemetry.empty:

    telemetry_vehicle_col = find_column(
        drone_telemetry,
        [
            "vehicle_id",
            "drone_id",
            "vehicleid"
        ]
    )

    if telemetry_vehicle_col is not None:

        drone_telemetry[
            telemetry_vehicle_col
        ] = (
            drone_telemetry[
                telemetry_vehicle_col
            ]
            .astype(str)
            .str.strip()
            .str.lower()
        )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header(
    "⚙️ Payload Settings"
)


utilization_limit = st.sidebar.slider(
    "Maximum Payload Utilization (%)",
    min_value=50,
    max_value=100,
    value=90,
    step=5
)


utilization_limit_decimal = (
    utilization_limit / 100
)


st.sidebar.write(
    "A vehicle is suitable only when the "
    "required payload is within the selected "
    "utilization limit."
)


# ============================================================
# REFRESH DATABASE DATA
# ============================================================

if st.sidebar.button(
    "🔄 Refresh PostgreSQL Data"
):

    st.cache_data.clear()

    st.rerun()


# ============================================================
# ORDER SELECTION
# ============================================================

st.subheader(
    "1️⃣ Select Order"
)


order_ids = sorted(
    orders[order_id_col]
    .unique()
)


if len(order_ids) == 0:

    st.error(
        "❌ No valid orders available."
    )

    st.stop()


selected_order_id = st.selectbox(
    "Select Order ID",
    order_ids
)


# ============================================================
# GET SELECTED ORDER
# ============================================================

selected_order = orders[
    orders[order_id_col]
    == selected_order_id
].iloc[0]


required_payload = float(
    selected_order[payload_col]
)


# ============================================================
# ORDER INFORMATION
# ============================================================

st.subheader(
    "2️⃣ Order Details"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Order ID",
        selected_order_id.upper()
    )


with col2:

    st.metric(
        "Required Payload",
        f"{required_payload:.2f} kg"
    )


with col3:

    if distance_col is not None:

        distance_value = pd.to_numeric(
            selected_order[distance_col],
            errors="coerce"
        )

        if pd.notna(distance_value):

            st.metric(
                "Distance",
                f"{distance_value:.2f} km"
            )

        else:

            st.metric(
                "Distance",
                "N/A"
            )

    else:

        st.metric(
            "Distance",
            "N/A"
        )


with col4:

    if priority_col is not None:

        st.metric(
            "Priority",
            str(
                selected_order[
                    priority_col
                ]
            )
        )

    else:

        st.metric(
            "Priority",
            "N/A"
        )


# ============================================================
# MORE ORDER DETAILS
# ============================================================

detail_data = {}


if quantity_col is not None:

    detail_data["Quantity"] = (
        selected_order[quantity_col]
    )


if origin_col is not None:

    detail_data["Origin"] = (
        selected_order[origin_col]
    )


if destination_col is not None:

    detail_data["Destination"] = (
        selected_order[destination_col]
    )


if distance_col is not None:

    detail_data["Distance (km)"] = (
        selected_order[distance_col]
    )


if priority_col is not None:

    detail_data["Priority"] = (
        selected_order[priority_col]
    )


if len(detail_data) > 0:

    st.dataframe(
        pd.DataFrame(
            [detail_data]
        ),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PAYLOAD OPTIMIZATION
# ============================================================

st.subheader(
    "3️⃣ Vehicle Payload Analysis"
)


# ============================================================
# MAXIMUM USABLE PAYLOAD
# ============================================================

fleet[
    "maximum_usable_payload_kg"
] = (
    fleet[
        "payload_capacity_kg"
    ]
    * utilization_limit_decimal
)


# ============================================================
# REMAINING PAYLOAD
# ============================================================

fleet[
    "remaining_payload_kg"
] = (
    fleet[
        "maximum_usable_payload_kg"
    ]
    - required_payload
)


# ============================================================
# PAYLOAD UTILIZATION
# ============================================================

fleet[
    "payload_utilization_pct"
] = (
    required_payload
    / fleet[
        "payload_capacity_kg"
    ]
) * 100


# ============================================================
# SUITABILITY
# ============================================================

fleet["suitable"] = (
    required_payload
    <= fleet[
        "maximum_usable_payload_kg"
    ]
)


# ============================================================
# SUITABLE VEHICLES
# ============================================================

suitable_vehicles = fleet[
    fleet["suitable"] == True
].copy()


# ============================================================
# VEHICLE TYPE PRIORITY
# ============================================================

vehicle_type_priority = {

    "bike": 1,

    "drone": 2,

    "van": 3,

    "truck": 4,

    "air cargo": 5,

    "ship": 6

}


suitable_vehicles[
    "type_priority"
] = (
    suitable_vehicles[
        "vehicle_type_standard"
    ]
    .map(vehicle_type_priority)
    .fillna(99)
)


# ============================================================
# IMPORTANT:
# BEST-FIT PAYLOAD OPTIMIZATION
# ============================================================

if len(suitable_vehicles) > 0:

    # --------------------------------------------------------
    # Calculate actual unused capacity
    # --------------------------------------------------------

    suitable_vehicles[
        "unused_capacity_kg"
    ] = (
        suitable_vehicles[
            "payload_capacity_kg"
        ]
        - required_payload
    )

    # --------------------------------------------------------
    # Sort by smallest unused capacity
    #
    # This prevents large vehicles such as Ship from being
    # selected when a smaller vehicle can safely carry the
    # order.
    # --------------------------------------------------------

    suitable_vehicles = (
        suitable_vehicles
        .sort_values(
            by=[
                "unused_capacity_kg",
                "payload_capacity_kg",
                "type_priority"
            ],
            ascending=[
                True,
                True,
                True
            ]
        )
        .reset_index(drop=True)
    )


# ============================================================
# BEST VEHICLE
# ============================================================

if len(suitable_vehicles) > 0:

    best_vehicle = (
        suitable_vehicles.iloc[0]
    )

    best_vehicle_id = (
        best_vehicle[
            vehicle_id_col
        ]
    )

    best_vehicle_type = (
        best_vehicle[
            "vehicle_type_standard"
        ]
    )

    best_capacity = float(
        best_vehicle[
            "payload_capacity_kg"
        ]
    )

    best_utilization = float(
        best_vehicle[
            "payload_utilization_pct"
        ]
    )

    best_remaining = float(
        best_vehicle[
            "remaining_payload_kg"
        ]
    )

    best_unused_capacity = float(
        best_vehicle[
            "unused_capacity_kg"
        ]
    )


    # ========================================================
    # RECOMMENDATION
    # ========================================================

    st.success(
        f"✅ Recommended Vehicle: "
        f"{str(best_vehicle_id).upper()}"
    )


    col1, col2, col3, col4, col5 = st.columns(5)


    with col1:

        st.metric(
            "Vehicle ID",
            str(
                best_vehicle_id
            ).upper()
        )


    with col2:

        st.metric(
            "Vehicle Type",
            best_vehicle_type.title()
        )


    with col3:

        st.metric(
            "Payload Capacity",
            f"{best_capacity:.2f} kg"
        )


    with col4:

        st.metric(
            "Payload Utilization",
            f"{best_utilization:.2f}%"
        )


    with col5:

        st.metric(
            "Unused Capacity",
            f"{best_unused_capacity:.2f} kg"
        )


    # ========================================================
    # PAYLOAD PROGRESS
    # ========================================================

    st.write(
        "### Payload Utilization"
    )


    progress_value = min(
        best_utilization / 100,
        1.0
    )


    st.progress(
        progress_value
    )


    st.write(
        f"Required Payload: "
        f"**{required_payload:.2f} kg**"
    )


    st.write(
        f"Vehicle Capacity: "
        f"**{best_capacity:.2f} kg**"
    )


    st.write(
        f"Remaining Usable Capacity: "
        f"**{best_remaining:.2f} kg**"
    )


    st.write(
        f"Unused Total Capacity: "
        f"**{best_unused_capacity:.2f} kg**"
    )


else:

    st.error(
        "❌ No vehicle can safely carry this payload."
    )


# ============================================================
# ALL SUITABLE VEHICLES
# ============================================================

st.subheader(
    "4️⃣ Suitable Vehicles"
)


if len(suitable_vehicles) > 0:

    display_columns = [

        vehicle_id_col,

        "vehicle_type_standard",

        "payload_capacity_kg",

        "maximum_usable_payload_kg",

        "remaining_payload_kg",

        "unused_capacity_kg",

        "payload_utilization_pct"

    ]


    display_df = (
        suitable_vehicles[
            display_columns
        ].copy()
    )


    display_df.columns = [

        "Vehicle ID",

        "Vehicle Type",

        "Capacity (kg)",

        "Usable Capacity (kg)",

        "Remaining Capacity (kg)",

        "Unused Capacity (kg)",

        "Payload Utilization (%)"

    ]


    display_df[
        "Payload Utilization (%)"
    ] = (
        display_df[
            "Payload Utilization (%)"
        ].round(2)
    )


    display_df[
        "Capacity (kg)"
    ] = (
        display_df[
            "Capacity (kg)"
        ].round(2)
    )


    display_df[
        "Usable Capacity (kg)"
    ] = (
        display_df[
            "Usable Capacity (kg)"
        ].round(2)
    )


    display_df[
        "Remaining Capacity (kg)"
    ] = (
        display_df[
            "Remaining Capacity (kg)"
        ].round(2)
    )


    display_df[
        "Unused Capacity (kg)"
    ] = (
        display_df[
            "Unused Capacity (kg)"
        ].round(2)
    )


    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


else:

    st.warning(
        "No suitable vehicles found."
    )


# ============================================================
# VEHICLE TYPE SUMMARY
# ============================================================

st.subheader(
    "5️⃣ Vehicle Type Comparison"
)


if len(suitable_vehicles) > 0:

    vehicle_summary = (
        suitable_vehicles
        .groupby(
            "vehicle_type_standard"
        )
        .agg(

            vehicles_available=(
                vehicle_id_col,
                "count"
            ),

            minimum_capacity_kg=(
                "payload_capacity_kg",
                "min"
            ),

            average_capacity_kg=(
                "payload_capacity_kg",
                "mean"
            ),

            minimum_unused_capacity_kg=(
                "unused_capacity_kg",
                "min"
            ),

            best_utilization_pct=(
                "payload_utilization_pct",
                "min"
            )

        )
        .reset_index()
    )


    if len(vehicle_summary) > 0:

        vehicle_summary.columns = [

            "Vehicle Type",

            "Vehicles Available",

            "Minimum Capacity (kg)",

            "Average Capacity (kg)",

            "Minimum Unused Capacity (kg)",

            "Best Utilization (%)"

        ]


        vehicle_summary[
            "Minimum Capacity (kg)"
        ] = (
            vehicle_summary[
                "Minimum Capacity (kg)"
            ].round(2)
        )


        vehicle_summary[
            "Average Capacity (kg)"
        ] = (
            vehicle_summary[
                "Average Capacity (kg)"
            ].round(2)
        )


        vehicle_summary[
            "Minimum Unused Capacity (kg)"
        ] = (
            vehicle_summary[
                "Minimum Unused Capacity (kg)"
            ].round(2)
        )


        vehicle_summary[
            "Best Utilization (%)"
        ] = (
            vehicle_summary[
                "Best Utilization (%)"
            ].round(2)
        )


        st.dataframe(
            vehicle_summary,
            use_container_width=True,
            hide_index=True
        )


else:

    st.warning(
        "No vehicle type can handle this payload."
    )


# ============================================================
# ALL 6 VEHICLE TYPES
# ============================================================

st.subheader(
    "6️⃣ All Vehicle Types"
)


all_vehicle_types = pd.DataFrame({

    "Vehicle Type": [

        "Bike",

        "Drone",

        "Van",

        "Truck",

        "Air Cargo",

        "Ship"

    ],

    "Default Capacity (kg)": [

        DEFAULT_CAPACITY["bike"],

        DEFAULT_CAPACITY["drone"],

        DEFAULT_CAPACITY["van"],

        DEFAULT_CAPACITY["truck"],

        DEFAULT_CAPACITY["air cargo"],

        DEFAULT_CAPACITY["ship"]

    ]

})


# ============================================================
# FLEET COUNTS
# ============================================================

fleet_counts = (
    fleet[
        "vehicle_type_standard"
    ]
    .value_counts()
)


all_vehicle_types[
    "Vehicles in Fleet"
] = (
    all_vehicle_types[
        "Vehicle Type"
    ]
    .str.lower()
    .map(fleet_counts)
    .fillna(0)
    .astype(int)
)


# ============================================================
# SUITABILITY USING DEFAULT CAPACITY
# ============================================================

all_vehicle_types[
    "Suitable for Order"
] = (
    all_vehicle_types[
        "Default Capacity (kg)"
    ]
    .apply(
        lambda x:
        "Yes"
        if (
            required_payload
            <= x * utilization_limit_decimal
        )
        else "No"
    )
)


st.dataframe(
    all_vehicle_types,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# VEHICLE TYPE FILTER
# ============================================================

st.subheader(
    "7️⃣ Analyze Vehicle Type"
)


selected_vehicle_type = st.selectbox(
    "Select Vehicle Type",
    [
        "truck",
        "bike",
        "van",
        "drone",
        "air cargo",
        "ship"
    ]
)


# ============================================================
# FILTER VEHICLES
# ============================================================

type_vehicles = fleet[
    fleet[
        "vehicle_type_standard"
    ]
    == selected_vehicle_type
].copy()


if len(type_vehicles) == 0:

    st.warning(
        f"No {selected_vehicle_type.title()} "
        "vehicles are available in the fleet."
    )

else:

    # --------------------------------------------------------
    # REMAINING CAPACITY
    # --------------------------------------------------------

    type_vehicles[
        "remaining_payload_kg"
    ] = (
        type_vehicles[
            "maximum_usable_payload_kg"
        ]
        - required_payload
    )


    # --------------------------------------------------------
    # UNUSED CAPACITY
    # --------------------------------------------------------

    type_vehicles[
        "unused_capacity_kg"
    ] = (
        type_vehicles[
            "payload_capacity_kg"
        ]
        - required_payload
    )


    # --------------------------------------------------------
    # UTILIZATION
    # --------------------------------------------------------

    type_vehicles[
        "payload_utilization_pct"
    ] = (
        required_payload
        / type_vehicles[
            "payload_capacity_kg"
        ]
    ) * 100


    # --------------------------------------------------------
    # SUITABLE
    # --------------------------------------------------------

    type_vehicles[
        "suitable"
    ] = (
        required_payload
        <= type_vehicles[
            "maximum_usable_payload_kg"
        ]
    )


    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    type_display = (
        type_vehicles[
            [
                vehicle_id_col,

                "payload_capacity_kg",

                "maximum_usable_payload_kg",

                "remaining_payload_kg",

                "unused_capacity_kg",

                "payload_utilization_pct",

                "suitable"

            ]
        ]
        .copy()
    )


    type_display.columns = [

        "Vehicle ID",

        "Capacity (kg)",

        "Usable Capacity (kg)",

        "Remaining Capacity (kg)",

        "Unused Capacity (kg)",

        "Utilization (%)",

        "Suitable"

    ]


    type_display[
        "Utilization (%)"
    ] = (
        type_display[
            "Utilization (%)"
        ].round(2)
    )


    type_display[
        "Capacity (kg)"
    ] = (
        type_display[
            "Capacity (kg)"
        ].round(2)
    )


    type_display[
        "Usable Capacity (kg)"
    ] = (
        type_display[
            "Usable Capacity (kg)"
        ].round(2)
    )


    type_display[
        "Remaining Capacity (kg)"
    ] = (
        type_display[
            "Remaining Capacity (kg)"
        ].round(2)
    )


    type_display[
        "Unused Capacity (kg)"
    ] = (
        type_display[
            "Unused Capacity (kg)"
        ].round(2)
    )


    type_display = (
        type_display
        .sort_values(
            by=[
                "Suitable",
                "Unused Capacity (kg)"
            ],
            ascending=[
                False,
                True
            ]
        )
    )


    st.dataframe(
        type_display,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# DRONE-SPECIFIC TELEMETRY CHECK
# ============================================================

if (
    selected_vehicle_type == "drone"
    and not drone_telemetry.empty
):

    st.subheader(
        "🚁 Drone Payload & Telemetry Check"
    )


    telemetry_vehicle_col = find_column(
        drone_telemetry,
        [
            "vehicle_id",
            "drone_id",
            "vehicleid"
        ]
    )


    if telemetry_vehicle_col is not None:

        drone_vehicles = (
            type_vehicles.copy()
        )


        drone_vehicles = (
            drone_vehicles[
                drone_vehicles[
                    "suitable"
                ] == True
            ]
        )


        if len(drone_vehicles) > 0:

            telemetry_ids = set(
                drone_telemetry[
                    telemetry_vehicle_col
                ]
                .astype(str)
                .str.lower()
            )


            drone_vehicles[
                "telemetry_available"
            ] = (
                drone_vehicles[
                    vehicle_id_col
                ]
                .astype(str)
                .str.lower()
                .isin(
                    telemetry_ids
                )
            )


            telemetry_display = (
                drone_vehicles[
                    [
                        vehicle_id_col,

                        "payload_capacity_kg",

                        "remaining_payload_kg",

                        "payload_utilization_pct",

                        "telemetry_available"

                    ]
                ]
                .copy()
            )


            telemetry_display.columns = [

                "Vehicle ID",

                "Payload Capacity (kg)",

                "Remaining Capacity (kg)",

                "Payload Utilization (%)",

                "Telemetry Available"

            ]


            telemetry_display[
                "Payload Utilization (%)"
            ] = (
                telemetry_display[
                    "Payload Utilization (%)"
                ].round(2)
            )


            st.dataframe(
                telemetry_display,
                use_container_width=True,
                hide_index=True
            )


        else:

            st.warning(
                "No drone can carry this payload."
            )


    else:

        st.warning(
            "Vehicle ID column was not found "
            "in drone telemetry table."
        )


# ============================================================
# BUSINESS LOGIC SUMMARY
# ============================================================

st.subheader(
    "8️⃣ Optimization Result"
)


if len(suitable_vehicles) > 0:

    st.write(
        f"""
        **Order:** `{selected_order_id.upper()}`

        **Required Payload:** `{required_payload:.2f} kg`

        **Recommended Vehicle:** `{str(best_vehicle_id).upper()}`

        **Vehicle Type:** `{best_vehicle_type.title()}`

        **Vehicle Capacity:** `{best_capacity:.2f} kg`

        **Payload Utilization:** `{best_utilization:.2f}%`

        **Remaining Usable Capacity:** `{best_remaining:.2f} kg`

        **Unused Total Capacity:** `{best_unused_capacity:.2f} kg`
        """
    )


    st.info(
        "The recommendation uses a best-fit payload strategy: "
        "among vehicles that can safely carry the order, "
        "the vehicle with the smallest unused capacity is selected."
    )

else:

    st.error(
        "No suitable vehicle was found for this order."
    )



# ============================================================
# BACK BUTTON
# ============================================================

st.divider()


if st.button(
    "⬅️ Back to Employee Dashboard"
):

    st.switch_page(
        "pages/employee_feature_page.py"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.caption(
    "SmartLogix AI Intelligent Multi-Modal Logistics | "
    "Payload Optimization"
)