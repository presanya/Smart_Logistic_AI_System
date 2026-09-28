
# import streamlit as st
# import pandas as pd
# import numpy as np
# from datetime import datetime, timedelta
# from sqlalchemy import create_engine

# # ============================================================
# # PAGE CONFIG
# # ============================================================

# st.set_page_config(
#     page_title="Delivery Scheduling",
#     page_icon="📅",
#     layout="wide"
# )

# st.title("📅 Delivery Scheduling")
# st.write(
#     "Schedule deliveries based on order priority, promised ETA, "
#     "distance, delivery duration and vehicle availability."
# )

# # ============================================================
# # FILE
# # ============================================================

# ORDERS_FILE = "orders_with_hub.csv"

# # ============================================================
# # LOAD DATA
# # ============================================================

# @st.cache_data
# def load_orders():

#     df = pd.read_csv(ORDERS_FILE)

#     df.columns = (
#         df.columns
#         .str.strip()
#         .str.lower()
#     )

#     return df


# orders = load_orders()

# # ============================================================
# # HELPER FUNCTION
# # ============================================================

# def find_column(df, possible_columns):

#     for col in possible_columns:

#         if col in df.columns:
#             return col

#     return None


# # ============================================================
# # FIND REQUIRED COLUMNS
# # ============================================================

# order_id_col = find_column(
#     orders,
#     [
#         "order_id",
#         "orderid",
#         "order"
#     ]
# )

# order_date_col = find_column(
#     orders,
#     [
#         "order_date",
#         "purchase_date",
#         "created_date"
#     ]
# )

# priority_col = find_column(
#     orders,
#     [
#         "delivery_priority",
#         "priority"
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

# promised_eta_col = find_column(
#     orders,
#     [
#         "promised_eta_hours",
#         "promised_eta",
#         "eta_hours"
#     ]
# )

# actual_delivery_col = find_column(
#     orders,
#     [
#         "actual_delivery_hours",
#         "delivery_hours",
#         "actual_eta_hours"
#     ]
# )

# transport_mode_col = find_column(
#     orders,
#     [
#         "transport_mode",
#         "vehicle_type",
#         "vehicle_mode"
#     ]
# )

# vehicle_id_col = find_column(
#     orders,
#     [
#         "assigned_vehicle_id",
#         "vehicle_id"
#     ]
# )

# origin_col = find_column(
#     orders,
#     [
#         "origin_city",
#         "origin",
#         "origin_hub"
#     ]
# )

# destination_col = find_column(
#     orders,
#     [
#         "destination_city",
#         "destination"
#     ]
# )

# status_col = find_column(
#     orders,
#     [
#         "order_status",
#         "status"
#     ]
# )


# # ============================================================
# # VALIDATION
# # ============================================================

# if order_id_col is None:

#     st.error("Order ID column was not found.")

#     st.write("Available columns:")
#     st.write(list(orders.columns))

#     st.stop()


# # ============================================================
# # CLEAN ORDER ID
# # ============================================================

# orders[order_id_col] = (
#     orders[order_id_col]
#     .astype(str)
#     .str.strip()
#     .str.lower()
# )


# # ============================================================
# # CLEAN PRIORITY
# # ============================================================

# if priority_col is not None:

#     orders[priority_col] = (
#         orders[priority_col]
#         .astype(str)
#         .str.strip()
#         .str.lower()
#     )


# # ============================================================
# # CLEAN DATE
# # ============================================================

# if order_date_col is not None:

#     orders[order_date_col] = pd.to_datetime(
#         orders[order_date_col],
#         format="mixed",
#         dayfirst=True,
#         errors="coerce"
#     )


# # ============================================================
# # SIDEBAR
# # ============================================================

# st.sidebar.header("⚙️ Scheduling Settings")

# working_start_hour = st.sidebar.number_input(
#     "Working Start Hour",
#     min_value=0,
#     max_value=23,
#     value=8
# )

# working_end_hour = st.sidebar.number_input(
#     "Working End Hour",
#     min_value=1,
#     max_value=23,
#     value=20
# )

# buffer_minutes = st.sidebar.slider(
#     "Delivery Buffer (minutes)",
#     min_value=0,
#     max_value=120,
#     value=30,
#     step=10
# )

# max_deliveries_per_vehicle = st.sidebar.number_input(
#     "Maximum Deliveries per Vehicle",
#     min_value=1,
#     max_value=50,
#     value=5
# )


# # ============================================================
# # ORDER SELECTION
# # ============================================================

# st.subheader("1️⃣ Select Order")

# order_ids = sorted(
#     orders[order_id_col].dropna().unique()
# )

# selected_order_id = st.selectbox(
#     "Order ID",
#     order_ids
# )


# # ============================================================
# # SELECT ORDER
# # ============================================================

# selected_order = orders[
#     orders[order_id_col] == selected_order_id
# ].iloc[0]


# # ============================================================
# # ORDER DETAILS
# # ============================================================

# st.subheader("2️⃣ Order Details")

# col1, col2, col3, col4 = st.columns(4)


# with col1:

#     st.metric(
#         "Order ID",
#         selected_order_id.upper()
#     )


# with col2:

#     if priority_col is not None:

#         priority = selected_order[priority_col]

#         st.metric(
#             "Priority",
#             str(priority).title()
#         )

#     else:

#         priority = "normal"

#         st.metric(
#             "Priority",
#             "Normal"
#         )


# with col3:

#     if distance_col is not None:

#         distance = pd.to_numeric(
#             selected_order[distance_col],
#             errors="coerce"
#         )

#         if pd.notna(distance):

#             st.metric(
#                 "Distance",
#                 f"{distance:.2f} km"
#             )

#         else:

#             distance = 0

#             st.metric(
#                 "Distance",
#                 "N/A"
#             )

#     else:

#         distance = 0

#         st.metric(
#             "Distance",
#             "N/A"
#         )


# with col4:

#     if promised_eta_col is not None:

#         promised_eta = pd.to_numeric(
#             selected_order[promised_eta_col],
#             errors="coerce"
#         )

#         if pd.notna(promised_eta):

#             st.metric(
#                 "Promised ETA",
#                 f"{promised_eta:.2f} hrs"
#             )

#         else:

#             promised_eta = 24

#             st.metric(
#                 "Promised ETA",
#                 "N/A"
#             )

#     else:

#         promised_eta = 24

#         st.metric(
#             "Promised ETA",
#             "N/A"
#         )


# # ============================================================
# # ROUTE INFORMATION
# # ============================================================

# st.subheader("3️⃣ Route Information")

# route_col1, route_col2, route_col3 = st.columns(3)


# with route_col1:

#     if origin_col is not None:

#         st.write("**Origin**")
#         st.write(
#             str(selected_order[origin_col]).title()
#         )

#     else:

#         st.write("Origin: N/A")


# with route_col2:

#     if destination_col is not None:

#         st.write("**Destination**")
#         st.write(
#             str(selected_order[destination_col]).title()
#         )

#     else:

#         st.write("Destination: N/A")


# with route_col3:

#     if transport_mode_col is not None:

#         st.write("**Transport Mode**")
#         st.write(
#             str(
#                 selected_order[transport_mode_col]
#             ).title()
#         )

#     else:

#         st.write("Transport Mode: N/A")


# # ============================================================
# # ESTIMATE DELIVERY TIME
# # ============================================================

# st.subheader("4️⃣ Delivery Time Estimation")


# # If actual delivery time exists, use it.
# # Otherwise estimate using distance.

# if actual_delivery_col is not None:

#     actual_hours = pd.to_numeric(
#         selected_order[actual_delivery_col],
#         errors="coerce"
#     )

# else:

#     actual_hours = np.nan


# if pd.notna(actual_hours) and actual_hours > 0:

#     estimated_delivery_hours = actual_hours

# else:

#     # Simple fallback estimation
#     #
#     # Average speed assumption:
#     # 40 km/hour

#     if distance > 0:

#         estimated_delivery_hours = (
#             distance / 40
#         )

#     else:

#         estimated_delivery_hours = 1


# # Add buffer

# estimated_delivery_hours = (
#     estimated_delivery_hours
#     + (buffer_minutes / 60)
# )


# col1, col2, col3 = st.columns(3)


# with col1:

#     st.metric(
#         "Estimated Delivery Time",
#         f"{estimated_delivery_hours:.2f} hrs"
#     )


# with col2:

#     st.metric(
#         "Buffer",
#         f"{buffer_minutes} min"
#     )


# with col3:

#     st.metric(
#         "Total Scheduled Time",
#         f"{estimated_delivery_hours:.2f} hrs"
#     )


# # ============================================================
# # PRIORITY LOGIC
# # ============================================================

# def priority_score(priority):

#     priority = str(priority).lower()

#     if priority in [
#         "urgent",
#         "critical",
#         "high"
#     ]:

#         return 1

#     elif priority in [
#         "medium",
#         "normal"
#     ]:

#         return 2

#     elif priority in [
#         "low"
#     ]:

#         return 3

#     else:

#         return 2


# selected_priority_score = priority_score(
#     priority
# )


# # ============================================================
# # DETERMINE SCHEDULE DATE
# # ============================================================

# if order_date_col is not None:

#     order_date = selected_order[order_date_col]

# else:

#     order_date = pd.Timestamp.now()


# if pd.isna(order_date):

#     order_date = pd.Timestamp.now()


# # ============================================================
# # SCHEDULE TIME INPUT
# # ============================================================

# st.subheader("5️⃣ Schedule Delivery")

# selected_date = st.date_input(
#     "Delivery Date",
#     value=order_date.date()
# )


# start_time = st.time_input(
#     "Preferred Start Time",
#     value=datetime(
#         2026,
#         1,
#         1,
#         working_start_hour,
#         0
#     ).time()
# )


# # ============================================================
# # CREATE START DATETIME
# # ============================================================

# scheduled_start = pd.Timestamp(
#     datetime.combine(
#         selected_date,
#         start_time
#     )
# )


# # ============================================================
# # CREATE END DATETIME
# # ============================================================

# scheduled_end = (
#     scheduled_start
#     + pd.Timedelta(
#         hours=estimated_delivery_hours
#     )
# )


# # ============================================================
# # WORKING HOURS VALIDATION
# # ============================================================

# working_start = scheduled_start.normalize() + pd.Timedelta(
#     hours=working_start_hour
# )

# working_end = scheduled_start.normalize() + pd.Timedelta(
#     hours=working_end_hour
# )


# if scheduled_start < working_start:

#     scheduled_start = working_start

#     scheduled_end = (
#         scheduled_start
#         + pd.Timedelta(
#             hours=estimated_delivery_hours
#         )
#     )


# # ============================================================
# # DISPLAY SCHEDULE
# # ============================================================

# schedule_col1, schedule_col2, schedule_col3 = st.columns(3)


# with schedule_col1:

#     st.metric(
#         "Scheduled Start",
#         scheduled_start.strftime(
#             "%d-%m-%Y %H:%M"
#         )
#     )


# with schedule_col2:

#     st.metric(
#         "Scheduled End",
#         scheduled_end.strftime(
#             "%d-%m-%Y %H:%M"
#         )
#     )


# with schedule_col3:

#     st.metric(
#         "Duration",
#         f"{estimated_delivery_hours:.2f} hrs"
#     )


# # ============================================================
# # WORKING HOURS CHECK
# # ============================================================

# if scheduled_end > working_end:

#     st.warning(
#         "⚠️ Delivery extends beyond the configured "
#         "working hours."
#     )

#     next_day = (
#         scheduled_start.normalize()
#         + pd.Timedelta(days=1)
#         + pd.Timedelta(hours=working_start_hour)
#     )

#     st.info(
#         "Suggested next working-day start: "
#         + next_day.strftime("%d-%m-%Y %H:%M")
#     )


# else:

#     st.success(
#         "✅ Delivery fits within the configured "
#         "working hours."
#     )


# # ============================================================
# # ETA DEADLINE CHECK
# # ============================================================

# if promised_eta_col is not None:

#     if pd.notna(
#         pd.to_numeric(
#             selected_order[promised_eta_col],
#             errors="coerce"
#         )
#     ):

#         promised_hours = float(
#             selected_order[promised_eta_col]
#         )

#         deadline = (
#             scheduled_start
#             + pd.Timedelta(
#                 hours=promised_hours
#             )
#         )

#         if scheduled_end <= deadline:

#             st.success(
#                 "✅ Scheduled delivery is within "
#                 "the promised ETA."
#             )

#         else:

#             st.error(
#                 "⚠️ Scheduled delivery may exceed "
#                 "the promised ETA."
#             )


# # ============================================================
# # VEHICLE INFORMATION
# # ============================================================

# st.subheader("6️⃣ Vehicle Assignment")

# if vehicle_id_col is not None:

#     current_vehicle = str(
#         selected_order[vehicle_id_col]
#     )

# else:

#     current_vehicle = "Not assigned"


# if transport_mode_col is not None:

#     current_transport = str(
#         selected_order[transport_mode_col]
#     ).lower()

# else:

#     current_transport = "Not assigned"


# vehicle_col1, vehicle_col2 = st.columns(2)


# with vehicle_col1:

#     st.write("**Assigned Vehicle**")

#     st.write(
#         current_vehicle.upper()
#         if current_vehicle != "Not assigned"
#         else current_vehicle
#     )


# with vehicle_col2:

#     st.write("**Transport Mode**")

#     st.write(
#         current_transport.title()
#     )


# # ============================================================
# # SCHEDULING PRIORITY
# # ============================================================

# st.subheader("7️⃣ Scheduling Priority")

# if selected_priority_score == 1:

#     st.error(
#         "🔴 HIGH PRIORITY — Schedule as early as possible."
#     )

# elif selected_priority_score == 2:

#     st.warning(
#         "🟡 NORMAL PRIORITY — Schedule within normal delivery window."
#     )

# else:

#     st.success(
#         "🟢 LOW PRIORITY — Can be scheduled after higher-priority orders."
#     )


# # ============================================================
# # FINAL SCHEDULE
# # ============================================================

# st.subheader("8️⃣ Final Delivery Schedule")


# schedule_data = {

#     "Order ID": [
#         selected_order_id.upper()
#     ],

#     "Priority": [
#         str(priority).title()
#     ],

#     "Origin": [
#         str(
#             selected_order[origin_col]
#         ).title()
#         if origin_col is not None
#         else "N/A"
#     ],

#     "Destination": [
#         str(
#             selected_order[destination_col]
#         ).title()
#         if destination_col is not None
#         else "N/A"
#     ],

#     "Vehicle ID": [
#         current_vehicle.upper()
#         if current_vehicle != "Not assigned"
#         else "Not assigned"
#     ],

#     "Transport Mode": [
#         current_transport.title()
#     ],

#     "Scheduled Start": [
#         scheduled_start.strftime(
#             "%d-%m-%Y %H:%M"
#         )
#     ],

#     "Scheduled End": [
#         scheduled_end.strftime(
#             "%d-%m-%Y %H:%M"
#         )
#     ],

#     "Estimated Hours": [
#         round(
#             estimated_delivery_hours,
#             2
#         )
#     ]
# }


# schedule_df = pd.DataFrame(
#     schedule_data
# )


# st.dataframe(
#     schedule_df,
#     use_container_width=True,
#     hide_index=True
# )


# # ============================================================
# # DOWNLOAD SCHEDULE
# # ============================================================

# csv_data = schedule_df.to_csv(
#     index=False
# )


# st.download_button(
#     label="⬇️ Download Delivery Schedule",
#     data=csv_data,
#     file_name="delivery_schedule.csv",
#     mime="text/csv"
# )


# # ============================================================
# # FINAL RECOMMENDATION
# # ============================================================

# st.subheader("9️⃣ Scheduling Recommendation")


# if selected_priority_score == 1:

#     recommendation = (
#         "Schedule this order immediately because it has "
#         "high delivery priority."
#     )

# elif selected_priority_score == 2:

#     recommendation = (
#         "Schedule this order within the normal delivery "
#         "window while ensuring the promised ETA is maintained."
#     )

# else:

#     recommendation = (
#         "This order can be scheduled after higher-priority "
#         "orders if vehicle capacity is limited."
#     )


# st.info(
#     recommendation
# )


# # ============================================================
# # FOOTER
# # ============================================================

# st.divider()

# st.caption(
#     "SmartLogix AI — Delivery Scheduling Module"
# )


# if st.button("⬅️ Back to Employee Dashboard"):

#     st.switch_page(
#         "pages/employee_feature_page.py"
#     )


# ============================================================
# SMARTLOGIX - DELIVERY SCHEDULING
# PostgreSQL Version
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np

from datetime import datetime, timedelta

from sqlalchemy import create_engine, text


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SmartLogix - Delivery Scheduling",
    page_icon="🚚",
    layout="wide"
)


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DATABASE = "smartlogistic_db"

DATABASE_URL = (
    f"postgresql://postgres:lavi@localhost:5432/{DATABASE}"
)

ORDERS_TABLE = "orders_with_hub"

SCHEDULE_TABLE = "delivery_schedules"


# ============================================================
# CREATE DATABASE ENGINE
# ============================================================

@st.cache_resource
def get_engine():

    return create_engine(
        DATABASE_URL,
        pool_pre_ping=True
    )


engine = get_engine()


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🚚 SmartLogix Delivery Scheduling")

st.markdown(
    """
    Schedule customer deliveries using order information
    stored in PostgreSQL.
    """
)

st.divider()


# ============================================================
# DATABASE CONNECTION TEST
# ============================================================

try:

    with engine.connect() as connection:

        connection.execute(
            text("SELECT 1")
        )

    db_connected = True

except Exception as e:

    db_connected = False

    st.error(
        f"❌ PostgreSQL connection failed: {e}"
    )

    st.info(
        "Check PostgreSQL service, database name, username, "
        "password and port."
    )

    st.stop()


# ============================================================
# LOAD ORDERS FROM POSTGRESQL
# ============================================================

@st.cache_data(ttl=60)
def load_orders():

    query = text(
        f"""
        SELECT *
        FROM {ORDERS_TABLE}
        """
    )

    df = pd.read_sql(
        query,
        engine
    )

    # --------------------------------------------------------
    # CLEAN COLUMN NAMES
    # --------------------------------------------------------

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    return df


# ============================================================
# LOAD DATA
# ============================================================

try:

    orders_df = load_orders()

except Exception as e:

    st.error(
        f"❌ Unable to load orders from PostgreSQL: {e}"
    )

    st.stop()


# ============================================================
# CHECK DATA
# ============================================================

if orders_df.empty:

    st.warning(
        f"⚠️ No orders found in PostgreSQL table "
        f"`{ORDERS_TABLE}`."
    )

    st.stop()


# ============================================================
# HELPER FUNCTION
# ============================================================

def find_column(df, possible_columns):

    for column in possible_columns:

        if column in df.columns:

            return column

    return None


# ============================================================
# DETECT COLUMNS
# ============================================================

order_id_col = find_column(
    orders_df,
    [
        "order_id",
        "orderid",
        "order_number"
    ]
)

order_date_col = find_column(
    orders_df,
    [
        "order_date",
        "orderdate",
        "created_date",
        "created_at"
    ]
)

priority_col = find_column(
    orders_df,
    [
        "delivery_priority",
        "priority",
        "deliverypriority"
    ]
)

distance_col = find_column(
    orders_df,
    [
        "distance_km",
        "distance",
        "delivery_distance_km"
    ]
)

promised_eta_col = find_column(
    orders_df,
    [
        "promised_eta_hours",
        "promised_eta",
        "promised_delivery_hours"
    ]
)

actual_delivery_col = find_column(
    orders_df,
    [
        "actual_delivery_hours",
        "actual_delivery_time",
        "delivery_hours"
    ]
)

transport_col = find_column(
    orders_df,
    [
        "transport_mode",
        "transport",
        "vehicle_type"
    ]
)

vehicle_col = find_column(
    orders_df,
    [
        "assigned_vehicle_id",
        "vehicle_id",
        "assigned_vehicle"
    ]
)

origin_col = find_column(
    orders_df,
    [
        "origin_city",
        "origin",
        "origin_hub",
        "source_city"
    ]
)

destination_col = find_column(
    orders_df,
    [
        "destination_city",
        "destination",
        "destination_hub",
        "dest_city"
    ]
)

status_col = find_column(
    orders_df,
    [
        "order_status",
        "status",
        "delivery_status"
    ]
)


# ============================================================
# CHECK ORDER ID COLUMN
# ============================================================

if order_id_col is None:

    st.error(
        "❌ Order ID column was not found in "
        f"`{ORDERS_TABLE}`."
    )

    st.write(
        "Available columns:"
    )

    st.write(
        list(orders_df.columns)
    )

    st.stop()


# ============================================================
# CLEAN ORDER ID
# ============================================================

orders_df[order_id_col] = (
    orders_df[order_id_col]
    .astype(str)
    .str.strip()
)


orders_df = orders_df[
    orders_df[order_id_col].notna()
]


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Scheduling Settings")


working_start_hour = st.sidebar.number_input(
    "Working Start Hour",
    min_value=0,
    max_value=23,
    value=8
)


working_end_hour = st.sidebar.number_input(
    "Working End Hour",
    min_value=1,
    max_value=23,
    value=20
)


buffer_minutes = st.sidebar.number_input(
    "Delivery Buffer (Minutes)",
    min_value=0,
    max_value=240,
    value=30
)


max_deliveries_per_vehicle = st.sidebar.number_input(
    "Max Deliveries per Vehicle",
    min_value=1,
    max_value=100,
    value=5
)


# ============================================================
# SIDEBAR DATABASE INFORMATION
# ============================================================

st.sidebar.divider()

st.sidebar.success(
    "🟢 PostgreSQL Connected"
)

st.sidebar.write(
    f"**Database:** {DATABASE}"
)

st.sidebar.write(
    f"**Orders Table:** {ORDERS_TABLE}"
)

st.sidebar.write(
    f"**Schedule Table:** {SCHEDULE_TABLE}"
)


# ============================================================
# ORDER SELECTION
# ============================================================

st.subheader("1️⃣ Select Order")


order_list = (
    orders_df[order_id_col]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


order_list = sorted(
    order_list
)


if not order_list:

    st.warning(
        "No valid orders available."
    )

    st.stop()


selected_order_id = st.selectbox(
    "Select Order ID",
    order_list
)


# ============================================================
# GET SELECTED ORDER
# ============================================================

selected_rows = orders_df[
    orders_df[order_id_col].astype(str)
    == str(selected_order_id)
]


if selected_rows.empty:

    st.error(
        "❌ Selected order was not found."
    )

    st.stop()


selected_order = (
    selected_rows
    .iloc[0]
)


# ============================================================
# EXTRACT ORDER VALUES
# ============================================================

def get_value(column, default="Not Available"):

    if column is None:

        return default

    value = selected_order.get(
        column,
        default
    )

    if pd.isna(value):

        return default

    return value


# ============================================================
# ORDER DETAILS
# ============================================================

priority = get_value(
    priority_col,
    "normal"
)

origin_value = get_value(
    origin_col,
    "Not Available"
)

destination_value = get_value(
    destination_col,
    "Not Available"
)

current_transport = get_value(
    transport_col,
    "Not Assigned"
)

current_vehicle = get_value(
    vehicle_col,
    "Not assigned"
)

order_status = get_value(
    status_col,
    "Not Available"
)

distance_value = get_value(
    distance_col,
    0
)

promised_eta_value = get_value(
    promised_eta_col,
    0
)

actual_delivery_value = get_value(
    actual_delivery_col,
    np.nan
)

order_date_value = get_value(
    order_date_col,
    None
)


# ============================================================
# CONVERT NUMERIC VALUES
# ============================================================

try:

    distance_value = float(
        distance_value
    )

except:

    distance_value = 0.0


try:

    promised_eta_value = float(
        promised_eta_value
    )

except:

    promised_eta_value = 0.0


try:

    actual_delivery_value = float(
        actual_delivery_value
    )

except:

    actual_delivery_value = np.nan


# ============================================================
# DISPLAY ORDER DETAILS
# ============================================================

st.subheader("2️⃣ Order Details")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Order ID",
        str(selected_order_id)
    )


with col2:

    st.metric(
        "Priority",
        str(priority).title()
    )


with col3:

    st.metric(
        "Distance",
        f"{distance_value:.2f} km"
    )


with col4:

    st.metric(
        "Status",
        str(order_status).title()
    )


# ============================================================
# ROUTE INFORMATION
# ============================================================

st.subheader("3️⃣ Route Information")


route_col1, route_col2 = st.columns(2)


with route_col1:

    st.write(
        f"**Origin:** {origin_value}"
    )


with route_col2:

    st.write(
        f"**Destination:** {destination_value}"
    )


st.write(
    f"**Transport Mode:** {current_transport}"
)


st.write(
    f"**Assigned Vehicle:** {current_vehicle}"
)


# ============================================================
# DELIVERY TIME ESTIMATION
# ============================================================

st.subheader("4️⃣ Delivery Time Estimation")


if not np.isnan(actual_delivery_value):

    estimated_delivery_hours = (
        actual_delivery_value
    )

    estimation_method = (
        "Based on historical actual delivery hours"
    )

else:

    if distance_value > 0:

        # Average assumed speed
        average_speed = 40

        estimated_delivery_hours = (
            distance_value /
            average_speed
        )

    else:

        estimated_delivery_hours = 1.0

    estimation_method = (
        "Estimated using distance"
    )


# Add buffer

buffer_hours = (
    buffer_minutes / 60
)


estimated_total_hours = (
    estimated_delivery_hours
    + buffer_hours
)


st.info(
    f"""
    **Estimated Delivery Time:** 
    {estimated_delivery_hours:.2f} hours

    **Buffer:** 
    {buffer_minutes} minutes

    **Total Scheduling Time:** 
    {estimated_total_hours:.2f} hours

    **Method:** 
    {estimation_method}
    """
)


# ============================================================
# PRIORITY SCORE
# ============================================================

def get_priority_score(value):

    value = str(value).strip().lower()

    if value in [
        "urgent",
        "critical",
        "high"
    ]:

        return 1

    elif value in [
        "medium",
        "normal"
    ]:

        return 2

    elif value == "low":

        return 3

    return 2


selected_priority_score = get_priority_score(
    priority
)


# ============================================================
# PRIORITY DISPLAY
# ============================================================

st.subheader("5️⃣ Priority Information")


priority_col1, priority_col2 = st.columns(2)


with priority_col1:

    st.metric(
        "Priority",
        str(priority).title()
    )


with priority_col2:

    st.metric(
        "Priority Score",
        selected_priority_score
    )


# ============================================================
# SCHEDULE DATE
# ============================================================

st.subheader("6️⃣ Schedule Delivery")


default_date = datetime.today().date()


if order_date_value is not None:

    try:

        converted_date = pd.to_datetime(
            order_date_value
        )

        if not pd.isna(converted_date):

            default_date = (
                converted_date.date()
            )

    except:

        pass


schedule_date = st.date_input(
    "Delivery Date",
    value=default_date
)


# ============================================================
# SCHEDULE TIME
# ============================================================

default_time = datetime.strptime(
    f"{working_start_hour}:00",
    "%H:%M"
).time()


schedule_time = st.time_input(
    "Delivery Start Time",
    value=default_time
)


# ============================================================
# COMBINE DATE + TIME
# ============================================================

scheduled_start = datetime.combine(
    schedule_date,
    schedule_time
)


# ============================================================
# VALIDATE WORKING HOURS
# ============================================================

working_start = datetime.strptime(
    f"{working_start_hour}:00",
    "%H:%M"
).time()


working_end = datetime.strptime(
    f"{working_end_hour}:00",
    "%H:%M"
).time()


time_valid = True


if schedule_time < working_start:

    st.warning(
        f"⚠️ Delivery starts before working hours "
        f"({working_start_hour}:00)."
    )

    time_valid = False


if schedule_time >= working_end:

    st.warning(
        f"⚠️ Delivery starts after working hours "
        f"({working_end_hour}:00)."
    )

    time_valid = False


# ============================================================
# CALCULATE END TIME
# ============================================================

scheduled_end = (
    scheduled_start
    + timedelta(
        hours=estimated_delivery_hours,
        minutes=buffer_minutes
    )
)


# ============================================================
# PROMISED ETA CHECK
# ============================================================

st.subheader("7️⃣ ETA Validation")


if promised_eta_value > 0:

    estimated_finish_hours = (
        estimated_delivery_hours
        + buffer_hours
    )

    if estimated_finish_hours <= promised_eta_value:

        st.success(
            f"""
            ✅ Estimated delivery time is within
            the promised ETA of
            {promised_eta_value:.2f} hours.
            """
        )

    else:

        delay = (
            estimated_finish_hours
            - promised_eta_value
        )

        st.warning(
            f"""
            ⚠️ Estimated delivery may exceed
            promised ETA by
            {delay:.2f} hours.
            """
        )

else:

    st.info(
        "No promised ETA information available."
    )


# ============================================================
# SCHEDULE PREVIEW
# ============================================================

st.subheader("8️⃣ Schedule Preview")


schedule_preview = pd.DataFrame(
    {
        "Order ID": [
            selected_order_id
        ],

        "Priority": [
            priority
        ],

        "Origin": [
            origin_value
        ],

        "Destination": [
            destination_value
        ],

        "Transport Mode": [
            current_transport
        ],

        "Vehicle ID": [
            current_vehicle
        ],

        "Scheduled Start": [
            scheduled_start
        ],

        "Scheduled End": [
            scheduled_end
        ],

        "Estimated Hours": [
            round(
                estimated_delivery_hours,
                2
            )
        ],

        "Buffer Minutes": [
            buffer_minutes
        ]
    }
)


st.dataframe(
    schedule_preview,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# CREATE DELIVERY SCHEDULE TABLE
# ============================================================

def create_delivery_schedule_table():

    query = text(
        f"""
        CREATE TABLE IF NOT EXISTS {SCHEDULE_TABLE} (

            id SERIAL PRIMARY KEY,

            order_id VARCHAR(100) NOT NULL,

            priority VARCHAR(50),

            origin VARCHAR(255),

            destination VARCHAR(255),

            vehicle_id VARCHAR(100),

            transport_mode VARCHAR(100),

            scheduled_start TIMESTAMP,

            scheduled_end TIMESTAMP,

            estimated_hours DOUBLE PRECISION,

            buffer_minutes INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )

    with engine.begin() as connection:

        connection.execute(
            query
        )


# ============================================================
# SAVE SCHEDULE
# ============================================================

st.subheader("9️⃣ Save Schedule")


if not time_valid:

    st.warning(
        "⚠️ Please select a valid delivery time "
        "within working hours."
    )


if st.button(
    "💾 Save Schedule to PostgreSQL",
    type="primary",
    use_container_width=True
):

    if not time_valid:

        st.error(
            "❌ Schedule cannot be saved because "
            "the selected time is outside working hours."
        )

    else:

        try:

            # ------------------------------------------------
            # CREATE TABLE
            # ------------------------------------------------

            create_delivery_schedule_table()


            # ------------------------------------------------
            # CHECK EXISTING ORDER
            # ------------------------------------------------

            check_query = text(
                f"""
                SELECT COUNT(*)
                FROM {SCHEDULE_TABLE}
                WHERE order_id = :order_id
                """
            )


            with engine.connect() as connection:

                existing_count = connection.execute(
                    check_query,
                    {
                        "order_id":
                            str(selected_order_id)
                    }
                ).scalar()


            # ------------------------------------------------
            # INSERT NEW SCHEDULE
            # ------------------------------------------------

            if existing_count == 0:

                insert_query = text(
                    f"""
                    INSERT INTO {SCHEDULE_TABLE}
                    (

                        order_id,

                        priority,

                        origin,

                        destination,

                        vehicle_id,

                        transport_mode,

                        scheduled_start,

                        scheduled_end,

                        estimated_hours,

                        buffer_minutes

                    )

                    VALUES
                    (

                        :order_id,

                        :priority,

                        :origin,

                        :destination,

                        :vehicle_id,

                        :transport_mode,

                        :scheduled_start,

                        :scheduled_end,

                        :estimated_hours,

                        :buffer_minutes

                    )
                    """
                )


                with engine.begin() as connection:

                    connection.execute(
                        insert_query,
                        {
                            "order_id":
                                str(
                                    selected_order_id
                                ),

                            "priority":
                                str(
                                    priority
                                ),

                            "origin":
                                str(
                                    origin_value
                                ),

                            "destination":
                                str(
                                    destination_value
                                ),

                            "vehicle_id":
                                (
                                    None
                                    if str(
                                        current_vehicle
                                    ).lower()
                                    in [
                                        "not assigned",
                                        "not available",
                                        "nan"
                                    ]
                                    else str(
                                        current_vehicle
                                    )
                                ),

                            "transport_mode":
                                str(
                                    current_transport
                                ),

                            "scheduled_start":
                                scheduled_start,

                            "scheduled_end":
                                scheduled_end,

                            "estimated_hours":
                                float(
                                    estimated_delivery_hours
                                ),

                            "buffer_minutes":
                                int(
                                    buffer_minutes
                                )
                        }
                    )


                st.success(
                    "✅ Delivery schedule saved "
                    "successfully to PostgreSQL."
                )


            # ------------------------------------------------
            # EXISTING SCHEDULE
            # ------------------------------------------------

            else:

                st.warning(
                    "⚠️ A schedule already exists "
                    f"for order {selected_order_id}."
                )


                update_existing = st.checkbox(
                    "🔄 Update the existing schedule",
                    key=f"update_{selected_order_id}"
                )


                if update_existing:

                    update_query = text(
                        f"""
                        UPDATE {SCHEDULE_TABLE}

                        SET

                            priority = :priority,

                            origin = :origin,

                            destination = :destination,

                            vehicle_id = :vehicle_id,

                            transport_mode = :transport_mode,

                            scheduled_start = :scheduled_start,

                            scheduled_end = :scheduled_end,

                            estimated_hours = :estimated_hours,

                            buffer_minutes = :buffer_minutes,

                            created_at = CURRENT_TIMESTAMP

                        WHERE order_id = :order_id
                        """
                    )


                    with engine.begin() as connection:

                        connection.execute(
                            update_query,
                            {
                                "order_id":
                                    str(
                                        selected_order_id
                                    ),

                                "priority":
                                    str(
                                        priority
                                    ),

                                "origin":
                                    str(
                                        origin_value
                                    ),

                                "destination":
                                    str(
                                        destination_value
                                    ),

                                "vehicle_id":
                                    (
                                        None
                                        if str(
                                            current_vehicle
                                        ).lower()
                                        in [
                                            "not assigned",
                                            "not available",
                                            "nan"
                                        ]
                                        else str(
                                            current_vehicle
                                        )
                                    ),

                                "transport_mode":
                                    str(
                                        current_transport
                                    ),

                                "scheduled_start":
                                    scheduled_start,

                                "scheduled_end":
                                    scheduled_end,

                                "estimated_hours":
                                    float(
                                        estimated_delivery_hours
                                    ),

                                "buffer_minutes":
                                    int(
                                        buffer_minutes
                                    )
                            }
                        )


                    st.success(
                        "✅ Existing delivery schedule "
                        "updated successfully."
                    )


        except Exception as e:

            st.error(
                "❌ Unable to save delivery schedule."
            )

            st.exception(e)




# ============================================================
# BACK TO EMPLOYEE DASHBOARD
# ============================================================

if st.button(
    "⬅️ Back to Employee Dashboard",
    use_container_width=True
):

    st.switch_page(
        "pages/employee_feature_page.py"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🚚 SmartLogix AI — Delivery Scheduling "
    "Module"
)

