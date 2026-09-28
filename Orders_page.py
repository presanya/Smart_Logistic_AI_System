import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Order Management",
    page_icon="📦",
    layout="wide"
)




# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

orders = pd.read_csv(
    "orders_cl_df.csv"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📦 Order Management")

st.write(
    f"Welcome **{st.session_state.username}**"
)

st.divider()


# --------------------------------------------------
# ORDER COUNT
# --------------------------------------------------

st.metric(
    "Total Orders",
    f"{len(orders):,}"
)


# --------------------------------------------------
# SEARCH ORDER
# --------------------------------------------------

st.subheader("🔎 Search Order")

order_id = st.text_input(
    "Enter Order ID",
    placeholder="Example: ord-001245"
)


# --------------------------------------------------
# SEARCH
# --------------------------------------------------

if order_id:

    order_id = order_id.strip()

    # Find order
    selected_order = orders[
        orders["order_id"]
        .astype(str)
        .str.lower()
        == order_id.lower()
    ]


    # ------------------------------------------------
    # ORDER FOUND
    # ------------------------------------------------

    if not selected_order.empty:

        st.success(
            f"✅ Order {order_id} found"
        )

        order = selected_order.iloc[0]


        # --------------------------------------------
        # ORDER INFORMATION
        # --------------------------------------------

        st.subheader("📦 Order Information")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.write("**Order ID**")
            st.write(order["order_id"])

        with col2:
            st.write("**Customer ID**")
            st.write(order["customer_id"])

        with col3:
            st.write("**Product ID**")
            st.write(order["product_id"])

        with col4:
            st.write("**Quantity**")
            st.write(order["quantity"])


        # --------------------------------------------
        # SHOW COMPLETE ORDER
        # --------------------------------------------

        st.subheader("📋 Complete Order Information")

        st.dataframe(
            selected_order,
            use_container_width=True
        )


    # ------------------------------------------------
    # ORDER NOT FOUND
    # ------------------------------------------------

    else:

        st.error(
            f"❌ Order ID '{order_id}' not found."
        )


# --------------------------------------------------
# SHOW ALL ORDERS
# --------------------------------------------------

else:

    st.subheader("📋 All Orders")

    st.dataframe(
        orders,
        use_container_width=True,
        height=600
    )


# --------------------------------------------------
# BACK BUTTON
# --------------------------------------------------

st.divider()

if st.button("⬅️ Back to Employee Dashboard"):

    st.switch_page(
        "pages/employee_feature_page.py"
    )