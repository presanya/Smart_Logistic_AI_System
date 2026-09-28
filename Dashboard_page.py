# ============================================================
# SMARTLOGIX AI
# OVERALL LOGISTICS DASHBOARD
#
# PostgreSQL + Streamlit + Plotly
# NO CUSTOM HTML
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np

from sqlalchemy import create_engine, text

import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SmartLogix Logistics Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DATABASE = "smartlogistic_db"

DATABASE_URL = (
    f"postgresql://postgres:lavi@localhost:5432/{DATABASE}"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

@st.cache_resource
def get_engine():

    try:

        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True
        )

        return engine

    except Exception as e:

        st.error(
            f"Database connection failed: {e}"
        )

        return None


engine = get_engine()


# ============================================================
# DATABASE QUERY FUNCTION
# ============================================================

def run_query(query, params=None):

    if engine is None:
        return pd.DataFrame()

    try:

        with engine.connect() as connection:

            df = pd.read_sql(
                text(query),
                connection,
                params=params
            )

        return df

    except Exception as e:

        st.warning(
            f"Query error: {e}"
        )

        return pd.DataFrame()


# ============================================================
# GET DATABASE TABLES
# ============================================================

@st.cache_data(ttl=300)
def get_database_tables():

    query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name
    """

    return run_query(query)


# ============================================================
# CHECK TABLE EXISTS
# ============================================================

def table_exists(table_name):

    tables = get_database_tables()

    if tables.empty:

        return False

    available_tables = (
        tables["table_name"]
        .astype(str)
        .str.lower()
        .tolist()
    )

    return table_name.lower() in available_tables


# ============================================================
# FIND COLUMN
# ============================================================

def find_column(
    columns,
    possible_names
):

    column_dictionary = {
        str(column).lower(): column
        for column in columns
    }

    for name in possible_names:

        if name.lower() in column_dictionary:

            return column_dictionary[
                name.lower()
            ]

    return None


# ============================================================
# FORMAT NUMBER
# ============================================================

def format_number(value):

    try:

        value = float(value)

    except:

        return "0"

    if value >= 10000000:

        return f"{value / 10000000:.2f} Cr"

    elif value >= 100000:

        return f"{value / 100000:.2f} L"

    elif value >= 1000:

        return f"{value / 1000:.2f} K"

    else:

        return f"{value:,.0f}"


# ============================================================
# MAIN TITLE
# ============================================================

st.title(
    "📊 Logistics Dashboard"
)

st.caption(
    "🚚 SmartLogix AI — Intelligent Multi-Modal Logistics Operations Dashboard"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title(
        "🚚 SmartLogix"
    )

    st.subheader(
        "Operations Control Center"
    )

    st.divider()

    st.write(
        "### 🗄️ PostgreSQL"
    )

    st.code(
        DATABASE,
        language="text"
    )

    if engine is not None:

        st.success(
            "🟢 Database Connected"
        )

    else:

        st.error(
            "🔴 Database Connection Failed"
        )

    st.divider()

    if st.button(
        "🔄 Refresh Dashboard",
        use_container_width=True
    ):

        st.cache_data.clear()

        st.rerun()

    st.divider()

    st.write(
        "### 📌 Dashboard Modules"
    )

    st.write(
        """
        📦 Order Management

        🚚 Transport Selection

        🛣️ Route Optimization

        ⏱️ ETA Prediction

        🔧 Predictive Maintenance

        🚁 Drone Monitoring

        📅 Delivery Scheduling

        📦 Payload Optimization
        """
    )


# ============================================================
# STOP IF DATABASE FAILED
# ============================================================

if engine is None:

    st.error(
        "Please check your PostgreSQL connection."
    )

    st.stop()


# ============================================================
# GET TABLES
# ============================================================

tables_df = get_database_tables()

if tables_df.empty:

    st.error(
        "No tables found in smartlogistic_db."
    )

    st.stop()


# ============================================================
# TABLE NAMES
# ============================================================

ORDERS_TABLE = "orders_with_hub"

FLEET_TABLE = "fleet_vehicles"

DRONE_TABLE = "drone_telemetry"

DELIVERY_TABLE = "orders"


# ============================================================
# LOAD ORDERS
# ============================================================

orders_df = pd.DataFrame()

if table_exists(ORDERS_TABLE):

    orders_df = run_query(
        f'SELECT * FROM "{ORDERS_TABLE}"'
    )


# ============================================================
# LOAD FLEET
# ============================================================

fleet_df = pd.DataFrame()

if table_exists(FLEET_TABLE):

    fleet_df = run_query(
        f'SELECT * FROM "{FLEET_TABLE}"'
    )


# ============================================================
# LOAD DRONE TELEMETRY
# ============================================================

drone_df = pd.DataFrame()

if table_exists(DRONE_TABLE):

    drone_df = run_query(
        f'SELECT * FROM "{DRONE_TABLE}"'
    )


# ============================================================
# LOAD DELIVERY LOG
# ============================================================

delivery_df = pd.DataFrame()

if table_exists(DELIVERY_TABLE):

    delivery_df = run_query(
        f'SELECT * FROM "{DELIVERY_TABLE}"'
    )


# ============================================================
# ORDER COLUMNS
# ============================================================

order_columns = list(
    orders_df.columns
)


order_id_col = find_column(
    order_columns,
    [
        "order_id",
        "orderid",
        "id"
    ]
)


transport_col = find_column(
    order_columns,
    [
        "transport_mode",
        "transport",
        "vehicle_type",
        "mode"
    ]
)


origin_col = find_column(
    order_columns,
    [
        "origin_city",
        "origin",
        "source_city"
    ]
)


destination_col = find_column(
    order_columns,
    [
        "destination_city",
        "destination",
        "dest_city"
    ]
)


order_value_col = find_column(
    order_columns,
    [
        "order_value_inr",
        "order_value",
        "total_amount",
        "price",
        "amount"
    ]
)


distance_col = find_column(
    order_columns,
    [
        "distance_km",
        "distance"
    ]
)


priority_col = find_column(
    order_columns,
    [
        "delivery_priority",
        "priority"
    ]
)


status_col = find_column(
    order_columns,
    [
        "delivery_status",
        "status",
        "order_status"
    ]
)


# ============================================================
# DELIVERY COLUMNS
# ============================================================

delivery_columns = list(
    delivery_df.columns
)


delivery_status_col = find_column(
    delivery_columns,
    [
        "delivery_status",
        "status",
        "delivery_result"
    ]
)


actual_hours_col = find_column(
    delivery_columns,
    [
        "actual_delivery_hours",
        "delivery_hours",
        "actual_hours"
    ]
)


# ============================================================
# TOTAL ORDERS
# ============================================================

if not orders_df.empty:

    if order_id_col:

        total_orders = (
            orders_df[
                order_id_col
            ]
            .nunique()
        )

    else:

        total_orders = len(
            orders_df
        )

else:

    total_orders = 0


# ============================================================
# TOTAL VEHICLES
# ============================================================

vehicle_id_col = find_column(
    list(fleet_df.columns),
    [
        "vehicle_id",
        "vehicleid",
        "id"
    ]
)


if not fleet_df.empty:

    if vehicle_id_col:

        total_vehicles = (
            fleet_df[
                vehicle_id_col
            ]
            .nunique()
        )

    else:

        total_vehicles = len(
            fleet_df
        )

else:

    total_vehicles = 0


# ============================================================
# TOTAL DRONE FLIGHTS
# ============================================================

flight_id_col = find_column(
    list(drone_df.columns),
    [
        "flight_id",
        "flightid"
    ]
)


if not drone_df.empty:

    if flight_id_col:

        total_drone_flights = (
            drone_df[
                flight_id_col
            ]
            .nunique()
        )

    else:

        total_drone_flights = len(
            drone_df
        )

else:

    total_drone_flights = 0


# ============================================================
# TOTAL ORDER VALUE
# ============================================================

total_order_value = 0


if (
    not orders_df.empty
    and order_value_col
):

    order_values = pd.to_numeric(
        orders_df[
            order_value_col
        ],
        errors="coerce"
    )

    total_order_value = (
        order_values
        .fillna(0)
        .sum()
    )


# ============================================================
# TOTAL DISTANCE
# ============================================================

total_distance = 0


if (
    not orders_df.empty
    and distance_col
):

    distance_values = pd.to_numeric(
        orders_df[
            distance_col
        ],
        errors="coerce"
    )

    total_distance = (
        distance_values
        .fillna(0)
        .sum()
    )


# ============================================================
# DELIVERY STATUS SOURCE
# ============================================================

status_source = None

status_source_col = None


if (
    not delivery_df.empty
    and delivery_status_col
):

    status_source = delivery_df

    status_source_col = (
        delivery_status_col
    )

elif (
    not orders_df.empty
    and status_col
):

    status_source = orders_df

    status_source_col = status_col


# ============================================================
# DELIVERY COUNTS
# ============================================================

delivered_orders = 0

pending_orders = 0

delayed_orders = 0

cancelled_orders = 0


if status_source is not None:

    status_series = (
        status_source[
            status_source_col
        ]
        .astype(str)
        .str.lower()
        .str.strip()
    )


    delivered_orders = (
        status_series
        .isin(
            [
                "delivered",
                "completed",
                "success",
                "successful"
            ]
        )
        .sum()
    )


    pending_orders = (
        status_series
        .isin(
            [
                "pending",
                "processing",
                "in transit",
                "in_transit"
            ]
        )
        .sum()
    )


    delayed_orders = (
        status_series
        .isin(
            [
                "delayed",
                "late"
            ]
        )
        .sum()
    )


    cancelled_orders = (
        status_series
        .isin(
            [
                "cancelled",
                "canceled"
            ]
        )
        .sum()
    )


# ============================================================
# AVERAGE DELIVERY TIME
# ============================================================

average_delivery_hours = 0


if (
    not delivery_df.empty
    and actual_hours_col
):

    delivery_hours = pd.to_numeric(
        delivery_df[
            actual_hours_col
        ],
        errors="coerce"
    ).dropna()


    if not delivery_hours.empty:

        average_delivery_hours = (
            delivery_hours.mean()
        )


# ============================================================
# FLEET FAILURE
# ============================================================

failure_col = find_column(
    list(fleet_df.columns),
    [
        "failure_reported",
        "maintenance_required",
        "failure"
    ]
)


maintenance_col = find_column(
    list(fleet_df.columns),
    [
        "maintenance_required",
        "maintenance_status"
    ]
)


failure_count = 0

maintenance_count = 0


if (
    not fleet_df.empty
    and failure_col
):

    failure_values = (
        fleet_df[
            failure_col
        ]
        .astype(str)
        .str.lower()
        .str.strip()
    )


    failure_count = (
        failure_values
        .isin(
            [
                "1",
                "true",
                "yes",
                "failure",
                "failed"
            ]
        )
        .sum()
    )


if (
    not fleet_df.empty
    and maintenance_col
):

    maintenance_values = (
        fleet_df[
            maintenance_col
        ]
        .astype(str)
        .str.lower()
        .str.strip()
    )


    maintenance_count = (
        maintenance_values
        .isin(
            [
                "1",
                "true",
                "yes",
                "required",
                "maintenance"
            ]
        )
        .sum()
    )


# ============================================================
# DELIVERY RATE
# ============================================================

delivery_rate = 0


if total_orders > 0:

    delivery_rate = (
        delivered_orders /
        total_orders
    ) * 100


# ============================================================
# MAIN KPI SECTION
# ============================================================

st.subheader(
    "📊 Logistics Overview"
)


# ============================================================
# KPI ROW 1
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    with st.container(border=True):

        st.metric(
            label="📦 Total Orders",
            value=format_number(
                total_orders
            ),
            help="Total orders available in PostgreSQL"
        )

        st.caption(
            "Orders in PostgreSQL"
        )


with col2:

    with st.container(border=True):

        st.metric(
            label="🚚 Total Vehicles",
            value=format_number(
                total_vehicles
            ),
            help="Total vehicles in fleet"
        )

        st.caption(
            "Fleet vehicles"
        )


with col3:

    with st.container(border=True):

        st.metric(
            label="🚁 Drone Flights",
            value=format_number(
                total_drone_flights
            ),
            help="Unique drone flights / telemetry records"
        )

        st.caption(
            "Telemetry records"
        )


with col4:

    with st.container(border=True):

        st.metric(
            label="💰 Order Value",
            value=f"₹{format_number(total_order_value)}",
            help="Total order value"
        )

        st.caption(
            "Total order value"
        )


# ============================================================
# KPI ROW 2
# ============================================================

col5, col6, col7, col8 = st.columns(4)


with col5:

    with st.container(border=True):

        st.metric(
            label="✅ Delivered",
            value=format_number(
                delivered_orders
            )
        )

        st.caption(
            "Successfully delivered"
        )


with col6:

    with st.container(border=True):

        st.metric(
            label="⏳ Pending",
            value=format_number(
                pending_orders
            )
        )

        st.caption(
            "Pending / in transit"
        )


with col7:

    with st.container(border=True):

        st.metric(
            label="🚨 Delayed",
            value=format_number(
                delayed_orders
            )
        )

        st.caption(
            "Delayed deliveries"
        )


with col8:

    with st.container(border=True):

        st.metric(
            label="⏱️ Avg Delivery",
            value=f"{average_delivery_hours:.2f} hrs"
        )

        st.caption(
            "Actual delivery time"
        )


# ============================================================
# ADDITIONAL METRICS
# ============================================================

st.subheader(
    "📌 Additional Operations Metrics"
)


col9, col10, col11, col12 = st.columns(4)


with col9:

    st.metric(
        "📍 Total Distance",
        f"{total_distance:,.0f} km"
    )


with col10:

    st.metric(
        "🔧 Maintenance",
        format_number(
            maintenance_count
        )
    )


with col11:

    st.metric(
        "⚠️ Vehicle Failures",
        format_number(
            failure_count
        )
    )


with col12:

    st.metric(
        "📈 Delivery Rate",
        f"{delivery_rate:.2f}%"
    )


# ============================================================
# ANALYTICS
# ============================================================

st.divider()

st.header(
    "📈 Logistics Analytics"
)


# ============================================================
# TRANSPORT MODE + DELIVERY STATUS
# ============================================================

chart1, chart2 = st.columns(2)


# ============================================================
# TRANSPORT MODE
# ============================================================

with chart1:

    st.subheader(
        "🚚 Transport Mode Distribution"
    )

    if (
        not orders_df.empty
        and transport_col
    ):

        transport_data = (
            orders_df[
                transport_col
            ]
            .astype(str)
            .str.strip()
            .replace(
                "",
                "Unknown"
            )
            .value_counts()
            .reset_index()
        )


        transport_data.columns = [
            "Transport Mode",
            "Orders"
        ]


        fig = px.pie(
            transport_data,
            names="Transport Mode",
            values="Orders",
            hole=0.45
        )


        fig.update_layout(
            height=430
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "Transport mode data not available."
        )


# ============================================================
# DELIVERY STATUS
# ============================================================

with chart2:

    st.subheader(
        "📦 Delivery Status"
    )

    if (
        status_source is not None
        and status_source_col
    ):

        status_data = (
            status_source[
                status_source_col
            ]
            .astype(str)
            .str.strip()
            .replace(
                "",
                "Unknown"
            )
            .value_counts()
            .reset_index()
        )


        status_data.columns = [
            "Status",
            "Orders"
        ]


        fig = px.bar(
            status_data,
            x="Status",
            y="Orders",
            text="Orders"
        )


        fig.update_traces(
            textposition="outside"
        )


        fig.update_layout(
            height=430
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "Delivery status data not available."
        )


# ============================================================
# CITY ANALYSIS
# ============================================================

chart3, chart4 = st.columns(2)


# ============================================================
# ORIGIN CITY
# ============================================================

with chart3:

    st.subheader(
        "📍 Orders by Origin City"
    )

    if (
        not orders_df.empty
        and origin_col
    ):

        origin_data = (
            orders_df[
                origin_col
            ]
            .astype(str)
            .str.strip()
            .replace(
                "",
                "Unknown"
            )
            .value_counts()
            .head(15)
            .reset_index()
        )


        origin_data.columns = [
            "Origin City",
            "Orders"
        ]


        fig = px.bar(
            origin_data,
            x="Orders",
            y="Origin City",
            orientation="h",
            text="Orders"
        )


        fig.update_traces(
            textposition="outside"
        )


        fig.update_layout(
            height=480,
            yaxis={
                "categoryorder":
                "total ascending"
            }
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "Origin city data not available."
        )


# ============================================================
# DESTINATION CITY
# ============================================================

with chart4:

    st.subheader(
        "🎯 Orders by Destination City"
    )

    if (
        not orders_df.empty
        and destination_col
    ):

        destination_data = (
            orders_df[
                destination_col
            ]
            .astype(str)
            .str.strip()
            .replace(
                "",
                "Unknown"
            )
            .value_counts()
            .head(15)
            .reset_index()
        )


        destination_data.columns = [
            "Destination City",
            "Orders"
        ]


        fig = px.bar(
            destination_data,
            x="Orders",
            y="Destination City",
            orientation="h",
            text="Orders"
        )


        fig.update_traces(
            textposition="outside"
        )


        fig.update_layout(
            height=480,
            yaxis={
                "categoryorder":
                "total ascending"
            }
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "Destination city data not available."
        )


# ============================================================
# PRIORITY ANALYSIS
# ============================================================

if (
    not orders_df.empty
    and priority_col
):

    st.subheader(
        "⚡ Delivery Priority Analysis"
    )


    priority_data = (
        orders_df[
            priority_col
        ]
        .astype(str)
        .str.strip()
        .replace(
            "",
            "Unknown"
        )
        .value_counts()
        .reset_index()
    )


    priority_data.columns = [
        "Priority",
        "Orders"
    ]


    fig = px.bar(
        priority_data,
        x="Priority",
        y="Orders",
        text="Orders"
    )


    fig.update_traces(
        textposition="outside"
    )


    fig.update_layout(
        height=400
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# ORDER VALUE DISTRIBUTION
# ============================================================

if (
    not orders_df.empty
    and order_value_col
):

    st.subheader(
        "💰 Order Value Distribution"
    )


    value_data = pd.to_numeric(
        orders_df[
            order_value_col
        ],
        errors="coerce"
    ).dropna()


    if not value_data.empty:

        fig = px.histogram(
            value_data,
            nbins=40
        )


        fig.update_layout(
            height=400,
            xaxis_title="Order Value (₹)",
            yaxis_title="Number of Orders"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# DISTANCE DISTRIBUTION
# ============================================================

if (
    not orders_df.empty
    and distance_col
):

    st.subheader(
        "🛣️ Delivery Distance Distribution"
    )


    distance_data = pd.to_numeric(
        orders_df[
            distance_col
        ],
        errors="coerce"
    ).dropna()


    if not distance_data.empty:

        fig = px.histogram(
            distance_data,
            nbins=40
        )


        fig.update_layout(
            height=400,
            xaxis_title="Distance (km)",
            yaxis_title="Number of Orders"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# FLEET ANALYTICS
# ============================================================

if not fleet_df.empty:

    st.divider()

    st.header(
        "🚚 Fleet Analytics"
    )


    fleet_chart1, fleet_chart2 = st.columns(2)


    # ========================================================
    # VEHICLE TYPE
    # ========================================================

    with fleet_chart1:

        vehicle_type_col = find_column(
            list(fleet_df.columns),
            [
                "vehicle_type",
                "type"
            ]
        )


        st.subheader(
            "🚚 Fleet by Vehicle Type"
        )


        if vehicle_type_col:

            vehicle_type_data = (
                fleet_df[
                    vehicle_type_col
                ]
                .astype(str)
                .str.strip()
                .replace(
                    "",
                    "Unknown"
                )
                .value_counts()
                .reset_index()
            )


            vehicle_type_data.columns = [
                "Vehicle Type",
                "Vehicles"
            ]


            fig = px.pie(
                vehicle_type_data,
                names="Vehicle Type",
                values="Vehicles",
                hole=0.4
            )


            fig.update_layout(
                height=430
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Vehicle type data not available."
            )


    # ========================================================
    # FLEET STATUS
    # ========================================================

    with fleet_chart2:

        fleet_status_col = find_column(
            list(fleet_df.columns),
            [
                "fleet_status",
                "status",
                "vehicle_status"
            ]
        )


        st.subheader(
            "🔧 Fleet Status"
        )


        if fleet_status_col:

            fleet_status_data = (
                fleet_df[
                    fleet_status_col
                ]
                .astype(str)
                .str.lower()
                .str.strip()
                .replace(
                    "",
                    "unknown"
                )
                .value_counts()
                .reset_index()
            )


            fleet_status_data.columns = [
                "Fleet Status",
                "Vehicles"
            ]


            fig = px.bar(
                fleet_status_data,
                x="Fleet Status",
                y="Vehicles",
                text="Vehicles"
            )


            fig.update_traces(
                textposition="outside"
            )


            fig.update_layout(
                height=430
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Fleet status data not available."
            )


# ============================================================
# MAINTENANCE ANALYSIS
# ============================================================

if (
    not fleet_df.empty
    and failure_col
):

    st.subheader(
        "🔧 Predictive Maintenance Overview"
    )


    maintenance_data = (
        fleet_df[
            failure_col
        ]
        .astype(str)
        .str.lower()
        .str.strip()
        .replace(
            "",
            "unknown"
        )
        .value_counts()
        .reset_index()
    )


    maintenance_data.columns = [
        "Failure Status",
        "Vehicles"
    ]


    fig = px.pie(
        maintenance_data,
        names="Failure Status",
        values="Vehicles",
        hole=0.45
    )


    fig.update_layout(
        height=420
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# RECENT ORDERS
# ============================================================

if not orders_df.empty:

    st.divider()

    st.header(
        "📦 Recent Orders"
    )


    display_columns = []


    possible_columns = [
        order_id_col,
        origin_col,
        destination_col,
        transport_col,
        priority_col,
        order_value_col,
        distance_col,
        status_col
    ]


    for column in possible_columns:

        if (
            column
            and column not in display_columns
        ):

            display_columns.append(
                column
            )


    if display_columns:

        recent_orders = (
            orders_df[
                display_columns
            ]
            .tail(15)
            .copy()
        )


        st.dataframe(
            recent_orders,
            use_container_width=True,
            hide_index=True
        )




# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🚚 SmartLogix AI | Intelligent Multi-Modal Logistics"
)