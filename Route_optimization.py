
# import streamlit as st
# import pandas as pd
# import folium

# from streamlit_folium import st_folium

# from math import (
#     radians,
#     sin,
#     cos,
#     sqrt,
#     atan2
# )


# # ============================================================
# # PAGE CONFIGURATION
# # ============================================================

# st.set_page_config(
#     page_title="SmartLogix Route Optimization",
#     page_icon="🚚",
#     layout="wide"
# )


# # ============================================================
# # LOAD ORDERS DATASET
# # ============================================================

# orders = pd.read_csv("orders_with_hub.csv")


# # ============================================================
# # CONVERT COORDINATE COLUMNS TO NUMERIC
# # ============================================================

# coordinate_columns = [
#     "destination_lat",
#     "destination_lon",
#     "hub_lat",
#     "hub_lon"
# ]

# for column in coordinate_columns:

#     orders[column] = pd.to_numeric(
#         orders[column],
#         errors="coerce"
#     )


# # ============================================================
# # REMOVE MISSING COORDINATES
# # ============================================================

# orders = orders.dropna(
#     subset=[
#         "destination_lat",
#         "destination_lon",
#         "hub_lat",
#         "hub_lon"
#     ]
# )


# # ============================================================
# # TITLE
# # ============================================================

# st.title("🚚 SmartLogix Route Optimization")

# st.write(
#     "Select a hub to find the closest delivery orders "
#     "and generate an optimized delivery route."
# )


# # ============================================================
# # HAVERSINE DISTANCE FUNCTION
# # ============================================================

# def calculate_distance(
#     lat1,
#     lon1,
#     lat2,
#     lon2
# ):

#     # Earth radius in kilometers
#     R = 6371

#     # Convert degrees to radians
#     lat1 = radians(lat1)
#     lon1 = radians(lon1)

#     lat2 = radians(lat2)
#     lon2 = radians(lon2)

#     # Difference between coordinates
#     dlat = lat2 - lat1
#     dlon = lon2 - lon1

#     # Haversine formula
#     a = (
#         sin(dlat / 2) ** 2
#         +
#         cos(lat1)
#         *
#         cos(lat2)
#         *
#         sin(dlon / 2) ** 2
#     )

#     c = 2 * atan2(
#         sqrt(a),
#         sqrt(1 - a)
#     )

#     distance = R * c

#     return distance


# # ============================================================
# # ROUTE OPTIMIZATION FUNCTION
# # ============================================================

# def optimize_route(
#     df,
#     hub_lat,
#     hub_lon
# ):

#     # Make a copy
#     remaining = df.copy()

#     # Current location starts at the hub
#     current_lat = hub_lat
#     current_lon = hub_lon

#     # Store optimized orders
#     optimized_rows = []

#     # Total route distance
#     total_distance = 0


#     # --------------------------------------------------------
#     # FIND THE NEXT NEAREST DELIVERY
#     # --------------------------------------------------------

#     while len(remaining) > 0:

#         # Calculate distance from current location
#         remaining["distance_from_current"] = remaining.apply(
#             lambda row: calculate_distance(
#                 current_lat,
#                 current_lon,
#                 row["destination_lat"],
#                 row["destination_lon"]
#             ),
#             axis=1
#         )


#         # Find the nearest delivery
#         nearest_index = (
#             remaining["distance_from_current"]
#             .idxmin()
#         )


#         # Get nearest order
#         nearest_order = remaining.loc[
#             nearest_index
#         ].copy()


#         # Distance to nearest order
#         distance = nearest_order[
#             "distance_from_current"
#         ]


#         # Add distance to total
#         total_distance += distance


#         # Add order to optimized route
#         optimized_rows.append(
#             nearest_order
#         )


#         # Update current location
#         current_lat = nearest_order[
#             "destination_lat"
#         ]

#         current_lon = nearest_order[
#             "destination_lon"
#         ]


#         # Remove visited order
#         remaining = remaining.drop(
#             nearest_index
#         )


#     # --------------------------------------------------------
#     # RETURN FROM LAST DELIVERY TO HUB
#     # --------------------------------------------------------

#     return_distance = calculate_distance(
#         current_lat,
#         current_lon,
#         hub_lat,
#         hub_lon
#     )


#     # Add return distance
#     total_distance += return_distance


#     # --------------------------------------------------------
#     # CREATE OPTIMIZED DATAFRAME
#     # --------------------------------------------------------

#     optimized_route = pd.DataFrame(
#         optimized_rows
#     )


#     optimized_route = optimized_route.reset_index(
#         drop=True
#     )


#     # Add stop number
#     optimized_route["stop_number"] = (
#         optimized_route.index + 1
#     )


#     return (
#         optimized_route,
#         total_distance,
#         return_distance
#     )


# # ============================================================
# # SELECT HUB
# # ============================================================

# hub_list = (
#     orders["origin_hub"]
#     .dropna()
#     .unique()
# )


# hub = st.selectbox(
#     "📍 Select Hub",
#     hub_list
# )


# # ============================================================
# # GET ALL ORDERS FOR SELECTED HUB
# # ============================================================

# hub_orders = orders[
#     orders["origin_hub"] == hub
# ].copy()


# # ============================================================
# # CHECK WHETHER ORDERS ARE AVAILABLE
# # ============================================================

# if len(hub_orders) == 0:

#     st.warning(
#         "No delivery orders are available for this hub."
#     )

#     st.stop()


# # ============================================================
# # GET HUB COORDINATES
# # ============================================================

# hub_lat = hub_orders[
#     "hub_lat"
# ].iloc[0]


# hub_lon = hub_orders[
#     "hub_lon"
# ].iloc[0]


# # Starting point = hub
# start_point = [
#     hub_lat,
#     hub_lon
# ]


# # ============================================================
# # DISPLAY HUB INFORMATION
# # ============================================================

# st.subheader("🏭 Selected Hub")

# col1, col2, col3 = st.columns(3)


# with col1:

#     st.write(
#         f"**Hub:** {hub}"
#     )


# with col2:

#     st.write(
#         f"**Hub Latitude:** {hub_lat}"
#     )


# with col3:

#     st.write(
#         f"**Hub Longitude:** {hub_lon}"
#     )


# # ============================================================
# # SELECT NUMBER OF DELIVERY ORDERS
# # ============================================================

# max_available = min(
#     20,
#     len(hub_orders)
# )


# if max_available >= 2:

#     number_of_orders = st.slider(
#         "📦 Number of closest deliveries",
#         min_value=2,
#         max_value=max_available,
#         value=min(10, max_available)
#     )

# else:

#     st.error(
#         "At least 2 delivery locations are required."
#     )

#     st.stop()


# # ============================================================
# # CALCULATE DISTANCE FROM HUB TO EVERY ORDER
# # ============================================================

# hub_orders["distance_from_hub"] = hub_orders.apply(
#     lambda row: calculate_distance(
#         hub_lat,
#         hub_lon,
#         row["destination_lat"],
#         row["destination_lon"]
#     ),
#     axis=1
# )


# # ============================================================
# # SORT ORDERS BY DISTANCE FROM HUB
# # ============================================================

# hub_orders = hub_orders.sort_values(
#     by="distance_from_hub",
#     ascending=True
# )


# # ============================================================
# # SELECT CLOSEST ORDERS
# # ============================================================

# closest_orders = hub_orders.head(
#     number_of_orders
# ).copy()


# # ============================================================
# # RESET INDEX
# # ============================================================

# closest_orders = closest_orders.reset_index(
#     drop=True
# )


# # ============================================================
# # DISPLAY CLOSEST ORDERS
# # ============================================================

# st.subheader(
#     f"📍 {number_of_orders} Closest Delivery Locations"
# )


# closest_display_columns = [
#     "order_id",
#     "destination_city",
#     "destination_lat",
#     "destination_lon",
#     "distance_from_hub",
#     "delivery_priority",
#     "package_weight"
# ]


# # Keep only columns that actually exist
# closest_display_columns = [
#     column
#     for column in closest_display_columns
#     if column in closest_orders.columns
# ]


# st.dataframe(
#     closest_orders[
#         closest_display_columns
#     ],
#     use_container_width=True
# )


# # ============================================================
# # RUN ROUTE OPTIMIZATION
# # ============================================================

# optimized_route, total_distance, return_distance = (
#     optimize_route(
#         closest_orders,
#         hub_lat,
#         hub_lon
#     )
# )


# # ============================================================
# # ROUTE SUMMARY
# # ============================================================

# st.subheader("📊 Route Summary")


# col1, col2, col3 = st.columns(3)


# with col1:

#     st.metric(
#         "Total Deliveries",
#         len(optimized_route)
#     )


# with col2:

#     st.metric(
#         "Total Route Distance",
#         f"{total_distance:.2f} km"
#     )


# with col3:

#     st.metric(
#         "Return Distance",
#         f"{return_distance:.2f} km"
#     )


# # ============================================================
# # CREATE FOLIUM MAP
# # ============================================================

# m = folium.Map(
#     location=start_point,
#     zoom_start=12
# )


# # ============================================================
# # ADD HUB MARKER
# # ============================================================

# folium.Marker(
#     location=start_point,

#     popup=f"""
#     <b>Starting Hub</b><br>
#     Hub: {hub}<br>
#     Latitude: {hub_lat}<br>
#     Longitude: {hub_lon}
#     """,

#     tooltip="🏭 Starting Hub",

#     icon=folium.Icon(
#         color="red",
#         icon="home",
#         prefix="fa"
#     )

# ).add_to(m)


# # ============================================================
# # CREATE ROUTE POINTS
# # ============================================================

# route_points = []


# # Start route from hub
# route_points.append(
#     [hub_lat, hub_lon]
# )


# # ============================================================
# # ADD DELIVERY MARKERS
# # ============================================================

# for _, row in optimized_route.iterrows():

#     lat = row[
#         "destination_lat"
#     ]

#     lon = row[
#         "destination_lon"
#     ]


#     # Add delivery location to route
#     route_points.append(
#         [lat, lon]
#     )


#     # Create popup
#     popup_text = f"""
#     <b>Stop:</b> {row['stop_number']}<br>
#     <b>Order:</b> {row['order_id']}<br>
#     <b>City:</b> {row['destination_city']}<br>
#     <b>Priority:</b> {row['delivery_priority']}<br>
#     <b>Weight:</b> {row['package_weight']}<br>
#     <b>Distance from Hub:</b>
#     {row['distance_from_hub']:.2f} km
#     """


#     # Add marker
#     folium.Marker(

#         location=[lat, lon],

#         popup=popup_text,

#         tooltip=(
#             f"Stop {row['stop_number']} - "
#             f"{row['order_id']}"
#         ),

#         icon=folium.Icon(
#             color="blue",
#             icon="truck",
#             prefix="fa"
#         )

#     ).add_to(m)


# # ============================================================
# # RETURN TO HUB
# # ============================================================

# route_points.append(
#     [hub_lat, hub_lon]
# )


# # ============================================================
# # DRAW OPTIMIZED ROUTE
# # ============================================================

# folium.PolyLine(

#     locations=route_points,

#     weight=5,

#     opacity=0.8,

#     tooltip="🚚 Optimized Delivery Route"

# ).add_to(m)


# # ============================================================
# # FIT MAP TO ROUTE
# # ============================================================

# m.fit_bounds(
#     route_points
# )


# # ============================================================
# # DISPLAY MAP
# # ============================================================

# st.subheader(
#     "🗺️ Optimized Delivery Route"
# )


# st_folium(
#     m,
#     width=1200,
#     height=650
# )


# # ============================================================
# # DISPLAY OPTIMIZED DELIVERY SEQUENCE
# # ============================================================

# st.subheader(
#     "📦 Optimized Delivery Sequence"
# )


# route_display_columns = [
#     "stop_number",
#     "order_id",
#     "destination_city",
#     "destination_lat",
#     "destination_lon",
#     "distance_from_hub",
#     "delivery_priority",
#     "package_weight"
# ]


# # Keep only existing columns
# route_display_columns = [
#     column
#     for column in route_display_columns
#     if column in optimized_route.columns
# ]


# st.dataframe(
#     optimized_route[
#         route_display_columns
#     ],
#     use_container_width=True
# )


# # ============================================================
# # DOWNLOAD OPTIMIZED ROUTE
# # ============================================================

# csv_data = optimized_route[
#     route_display_columns
# ].to_csv(
#     index=False
# )


# st.download_button(

#     label="⬇️ Download Optimized Route",

#     data=csv_data,

#     file_name="optimized_route.csv",

#     mime="text/csv"

# )



# ============================================================
# SMARTLOGIX ROUTE OPTIMIZATION
# POSTGRESQL VERSION
# ============================================================

import streamlit as st
import pandas as pd
import folium

from streamlit_folium import st_folium

from sqlalchemy import create_engine, text

from math import (
    radians,
    sin,
    cos,
    sqrt,
    atan2
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SmartLogix Route Optimization",
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


# ============================================================
# CREATE POSTGRESQL ENGINE
# ============================================================

@st.cache_resource
def get_database_engine():

    try:

        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True
        )

        return engine

    except Exception as e:

        st.error(
            f"❌ PostgreSQL connection failed: {e}"
        )

        st.stop()


engine = get_database_engine()


# ============================================================
# TEST DATABASE CONNECTION
# ============================================================

def test_database_connection():

    try:

        with engine.connect() as connection:

            connection.execute(
                text("SELECT 1")
            )

        return True

    except Exception as e:

        st.error(
            f"❌ Unable to connect to PostgreSQL: {e}"
        )

        return False


if not test_database_connection():

    st.stop()


# ============================================================
# LOAD ORDERS FROM POSTGRESQL
# ============================================================

@st.cache_data(ttl=300)
def load_orders_from_postgresql():

    query = """
        SELECT *
        FROM orders_with_hub
    """

    try:

        orders = pd.read_sql(
            query,
            engine
        )

        return orders

    except Exception as e:

        st.error(
            f"❌ Error loading orders_with_hub table: {e}"
        )

        return pd.DataFrame()


orders = load_orders_from_postgresql()


# ============================================================
# CHECK DATA
# ============================================================

if orders.empty:

    st.error(
        "❌ No data found in PostgreSQL table: orders_with_hub"
    )

    st.stop()


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [

    "origin_hub",

    "destination_lat",
    "destination_lon",

    "hub_lat",
    "hub_lon"
]


missing_columns = [

    column
    for column in required_columns
    if column not in orders.columns

]


if missing_columns:

    st.error(
        "❌ Missing required columns in PostgreSQL table:"
    )

    st.write(missing_columns)

    st.info(
        "Please check the columns in your orders_with_hub table."
    )

    st.stop()


# ============================================================
# CONVERT COORDINATE COLUMNS TO NUMERIC
# ============================================================

coordinate_columns = [

    "destination_lat",
    "destination_lon",
    "hub_lat",
    "hub_lon"

]


for column in coordinate_columns:

    orders[column] = pd.to_numeric(
        orders[column],
        errors="coerce"
    )


# ============================================================
# REMOVE MISSING COORDINATES
# ============================================================

orders = orders.dropna(
    subset=[
        "destination_lat",
        "destination_lon",
        "hub_lat",
        "hub_lon"
    ]
)


# ============================================================
# TITLE
# ============================================================

st.title(
    "🚚 SmartLogix Route Optimization"
)

st.write(
    "Select a hub to find the closest delivery orders "
    "and generate an optimized delivery route using "
    "PostgreSQL order data."
)


# ============================================================
# HAVERSINE DISTANCE FUNCTION
# ============================================================

def calculate_distance(
    lat1,
    lon1,
    lat2,
    lon2
):

    # Earth radius in kilometers
    R = 6371

    # Convert degrees to radians

    lat1 = radians(lat1)
    lon1 = radians(lon1)

    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Difference between coordinates

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula

    a = (

        sin(dlat / 2) ** 2

        +

        cos(lat1)
        *
        cos(lat2)
        *
        sin(dlon / 2) ** 2

    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    distance = R * c

    return distance


# ============================================================
# ROUTE OPTIMIZATION FUNCTION
# ============================================================

def optimize_route(
    df,
    hub_lat,
    hub_lon
):

    # Make a copy

    remaining = df.copy()

    # Current location starts at hub

    current_lat = hub_lat
    current_lon = hub_lon

    # Store optimized orders

    optimized_rows = []

    # Total route distance

    total_distance = 0


    # --------------------------------------------------------
    # FIND THE NEXT NEAREST DELIVERY
    # --------------------------------------------------------

    while len(remaining) > 0:

        # Calculate distance from current location

        remaining["distance_from_current"] = remaining.apply(

            lambda row:

            calculate_distance(

                current_lat,
                current_lon,

                row["destination_lat"],
                row["destination_lon"]

            ),

            axis=1

        )


        # Find nearest delivery

        nearest_index = (

            remaining[
                "distance_from_current"
            ].idxmin()

        )


        # Get nearest order

        nearest_order = remaining.loc[
            nearest_index
        ].copy()


        # Distance to nearest order

        distance = nearest_order[
            "distance_from_current"
        ]


        # Add distance to total

        total_distance += distance


        # Add order to optimized route

        optimized_rows.append(
            nearest_order
        )


        # Update current location

        current_lat = nearest_order[
            "destination_lat"
        ]

        current_lon = nearest_order[
            "destination_lon"
        ]


        # Remove visited order

        remaining = remaining.drop(
            nearest_index
        )


    # --------------------------------------------------------
    # RETURN FROM LAST DELIVERY TO HUB
    # --------------------------------------------------------

    return_distance = calculate_distance(

        current_lat,
        current_lon,

        hub_lat,
        hub_lon

    )


    # Add return distance

    total_distance += return_distance


    # --------------------------------------------------------
    # CREATE OPTIMIZED DATAFRAME
    # --------------------------------------------------------

    optimized_route = pd.DataFrame(
        optimized_rows
    )


    optimized_route = optimized_route.reset_index(
        drop=True
    )


    # Add stop number

    optimized_route["stop_number"] = (
        optimized_route.index + 1
    )


    return (
        optimized_route,
        total_distance,
        return_distance
    )


# ============================================================
# SELECT HUB
# ============================================================

hub_list = (

    orders[
        "origin_hub"
    ]

    .dropna()

    .unique()

)


# Sort hubs

hub_list = sorted(
    hub_list,
    key=lambda x: str(x)
)


# ============================================================
# HUB SELECTBOX
# ============================================================

hub = st.selectbox(
    "📍 Select Hub",
    hub_list
)


# ============================================================
# GET ALL ORDERS FOR SELECTED HUB
# ============================================================

hub_orders = orders[
    orders["origin_hub"] == hub
].copy()


# ============================================================
# CHECK WHETHER ORDERS ARE AVAILABLE
# ============================================================

if len(hub_orders) == 0:

    st.warning(
        "No delivery orders are available for this hub."
    )

    st.stop()


# ============================================================
# GET HUB COORDINATES
# ============================================================

hub_lat = hub_orders[
    "hub_lat"
].iloc[0]


hub_lon = hub_orders[
    "hub_lon"
].iloc[0]


# ============================================================
# STARTING POINT
# ============================================================

start_point = [

    hub_lat,
    hub_lon

]


# ============================================================
# DISPLAY HUB INFORMATION
# ============================================================

st.subheader(
    "🏭 Selected Hub"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.write(
        f"**Hub:** {hub}"
    )


with col2:

    st.write(
        f"**Hub Latitude:** {hub_lat}"
    )


with col3:

    st.write(
        f"**Hub Longitude:** {hub_lon}"
    )


# ============================================================
# HUB ORDER COUNT
# ============================================================

st.info(
    f"📦 Total orders available from {hub}: "
    f"{len(hub_orders):,}"
)


# ============================================================
# SELECT NUMBER OF DELIVERY ORDERS
# ============================================================

max_available = min(
    20,
    len(hub_orders)
)


if max_available >= 2:

    number_of_orders = st.slider(

        "📦 Number of closest deliveries",

        min_value=2,

        max_value=max_available,

        value=min(10, max_available)

    )

else:

    st.error(
        "At least 2 delivery locations are required."
    )

    st.stop()


# ============================================================
# CALCULATE DISTANCE FROM HUB TO EVERY ORDER
# ============================================================

hub_orders["distance_from_hub"] = hub_orders.apply(

    lambda row:

    calculate_distance(

        hub_lat,
        hub_lon,

        row["destination_lat"],
        row["destination_lon"]

    ),

    axis=1

)


# ============================================================
# SORT ORDERS BY DISTANCE FROM HUB
# ============================================================

hub_orders = hub_orders.sort_values(

    by="distance_from_hub",

    ascending=True

)


# ============================================================
# SELECT CLOSEST ORDERS
# ============================================================

closest_orders = hub_orders.head(
    number_of_orders
).copy()


# ============================================================
# RESET INDEX
# ============================================================

closest_orders = closest_orders.reset_index(
    drop=True
)


# ============================================================
# DISPLAY CLOSEST ORDERS
# ============================================================

st.subheader(
    f"📍 {number_of_orders} Closest Delivery Locations"
)


closest_display_columns = [

    "order_id",

    "destination_city",

    "destination_lat",

    "destination_lon",

    "distance_from_hub",

    "delivery_priority",

    "package_weight"

]


# Keep only columns that exist

closest_display_columns = [

    column

    for column in closest_display_columns

    if column in closest_orders.columns

]


# Round distance

display_closest = closest_orders[
    closest_display_columns
].copy()


if "distance_from_hub" in display_closest.columns:

    display_closest[
        "distance_from_hub"
    ] = display_closest[
        "distance_from_hub"
    ].round(2)


st.dataframe(

    display_closest,

    use_container_width=True,

    hide_index=True

)


# ============================================================
# RUN ROUTE OPTIMIZATION
# ============================================================

optimized_route, total_distance, return_distance = (

    optimize_route(

        closest_orders,

        hub_lat,

        hub_lon

    )

)


# ============================================================
# ROUTE SUMMARY
# ============================================================

st.subheader(
    "📊 Route Summary"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(

        "Total Deliveries",

        len(optimized_route)

    )


with col2:

    st.metric(

        "Total Route Distance",

        f"{total_distance:.2f} km"

    )


with col3:

    st.metric(

        "Return Distance",

        f"{return_distance:.2f} km"

    )


# ============================================================
# CREATE FOLIUM MAP
# ============================================================

m = folium.Map(

    location=start_point,

    zoom_start=12

)


# ============================================================
# ADD HUB MARKER
# ============================================================

folium.Marker(

    location=start_point,

    popup=f"""

        <b>Starting Hub</b><br>

        Hub: {hub}<br>

        Latitude: {hub_lat}<br>

        Longitude: {hub_lon}

    """,

    tooltip="🏭 Starting Hub",

    icon=folium.Icon(

        color="red",

        icon="home",

        prefix="fa"

    )

).add_to(m)


# ============================================================
# CREATE ROUTE POINTS
# ============================================================

route_points = []


# Start route from hub

route_points.append(

    [
        hub_lat,
        hub_lon
    ]

)


# ============================================================
# ADD DELIVERY MARKERS
# ============================================================

for _, row in optimized_route.iterrows():

    lat = row[
        "destination_lat"
    ]

    lon = row[
        "destination_lon"
    ]


    # Add delivery location

    route_points.append(

        [
            lat,
            lon
        ]

    )


    # --------------------------------------------------------
    # SAFE VALUES FOR POPUP
    # --------------------------------------------------------

    order_id = row.get(
        "order_id",
        "N/A"
    )

    destination_city = row.get(
        "destination_city",
        "N/A"
    )

    delivery_priority = row.get(
        "delivery_priority",
        "N/A"
    )

    package_weight = row.get(
        "package_weight",
        "N/A"
    )

    distance_from_hub = row.get(
        "distance_from_hub",
        0
    )


    # ========================================================
    # CREATE POPUP
    # ========================================================

    popup_text = f"""

        <b>Stop:</b>
        {row['stop_number']}
        <br>

        <b>Order:</b>
        {order_id}
        <br>

        <b>City:</b>
        {destination_city}
        <br>

        <b>Priority:</b>
        {delivery_priority}
        <br>

        <b>Weight:</b>
        {package_weight}
        <br>

        <b>Distance from Hub:</b>
        {distance_from_hub:.2f} km

    """


    # ========================================================
    # ADD MARKER
    # ========================================================

    folium.Marker(

        location=[
            lat,
            lon
        ],

        popup=popup_text,

        tooltip=(

            f"Stop {row['stop_number']} - "
            f"{order_id}"

        ),

        icon=folium.Icon(

            color="blue",

            icon="truck",

            prefix="fa"

        )

    ).add_to(m)


# ============================================================
# RETURN TO HUB
# ============================================================

route_points.append(

    [
        hub_lat,
        hub_lon
    ]

)


# ============================================================
# DRAW OPTIMIZED ROUTE
# ============================================================

folium.PolyLine(

    locations=route_points,

    weight=5,

    opacity=0.8,

    tooltip="🚚 Optimized Delivery Route"

).add_to(m)


# ============================================================
# FIT MAP TO ROUTE
# ============================================================

m.fit_bounds(
    route_points
)


# ============================================================
# DISPLAY MAP
# ============================================================

st.subheader(
    "🗺️ Optimized Delivery Route"
)


st_folium(

    m,

    width=1200,

    height=650

)


# ============================================================
# DISPLAY OPTIMIZED DELIVERY SEQUENCE
# ============================================================

st.subheader(
    "📦 Optimized Delivery Sequence"
)


route_display_columns = [

    "stop_number",

    "order_id",

    "destination_city",

    "destination_lat",

    "destination_lon",

    "distance_from_hub",

    "delivery_priority",

    "package_weight"

]


# Keep only existing columns

route_display_columns = [

    column

    for column in route_display_columns

    if column in optimized_route.columns

]


# Create display dataframe

display_route = optimized_route[
    route_display_columns
].copy()


# Round distance

if "distance_from_hub" in display_route.columns:

    display_route[
        "distance_from_hub"
    ] = display_route[
        "distance_from_hub"
    ].round(2)


st.dataframe(

    display_route,

    use_container_width=True,

    hide_index=True

)


# ============================================================
# DOWNLOAD OPTIMIZED ROUTE
# ============================================================

csv_data = optimized_route[
    route_display_columns
].to_csv(

    index=False

)


st.download_button(

    label="⬇️ Download Optimized Route",

    data=csv_data,

    file_name="optimized_route.csv",

    mime="text/csv"

)

# --------------------------------------------------
# BACK BUTTON
# --------------------------------------------------

st.divider()

if st.button("⬅️ Back to Employee Dashboard"):

    st.switch_page(
        "pages/employee_feature_page.py"
    )