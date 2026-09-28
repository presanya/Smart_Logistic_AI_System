# # # import streamlit as st
# # # import pandas as pd


# # # # =========================================================
# # # # PAGE CONFIG
# # # # =========================================================

# # # st.set_page_config(
# # #     page_title="SmartLogix Customer",
# # #     page_icon="🛒",
# # #     layout="wide"
# # # )


# # # # =========================================================
# # # # LOAD DATA
# # # # =========================================================

# # # df = pd.read_csv("product.csv")


# # # # =========================================================
# # # # IMAGE MAPPING
# # # # =========================================================

# # # image_mapping = {

# # #     "PRD-00453": "images/zenitha_saree.jpeg",

# # #     "PRD-00517": "images/shoe.jpeg",

# # #     "PRD-00079": "images/head_phone.jpeg",

# # #     "PRD-00377": "images/dry_fruits.jpeg",

# # #     "PRD-00635": "images/phamorchy.jpeg",
# # #     "PRD-00071": "images/smart_phone.jpeg",
# # #     "PRD-00190": "images/microwave.jpeg",
# # #     "PRD-00524": "images/saree_01.jpeg",
# # #     "PRD-00395":"images/spices.jpeg",
# # #     "PRD-00115":"images/air_purifier.jpeg",
# # #     "PRD-00336":"images/rice_bag.jpeg",
# # #     "PRD-00391":"images/cooking_oil.jpeg",
# # #     "PRD-00036":"images/laptop.jpeg",
# # #     "PRD-00506":"images/saree_02.jpeg",
# # #     "PRD-00466":"images/saree_03.jpeg"
# # # }


# # # # =========================================================
# # # # TITLE
# # # # =========================================================

# # # st.title("🛒 SmartLogix Customer")


# # # # =========================================================
# # # # SEARCH
# # # # =========================================================

# # # search = st.text_input(
# # #     "🔍 Search Product"
# # # )


# # # # =========================================================
# # # # FILTER
# # # # =========================================================

# # # if search:

# # #     filtered_df = df[
# # #         df["product_name"]
# # #         .str.contains(
# # #             search,
# # #             case=False,
# # #             na=False
# # #         )
# # #     ]

# # # else:

# # #     filtered_df = df


# # # # =========================================================
# # # # PRODUCT DISPLAY
# # # # =========================================================

# # # cols = st.columns(4)


# # # for index, row in filtered_df.iterrows():

# # #     with cols[index % 4]:

# # #         product_id = row["product_id"]

# # #         # Get image path
# # #         image_path = image_mapping.get(product_id)


# # #         # -----------------------------------------
# # #         # PRODUCT IMAGE
# # #         # -----------------------------------------

# # #         if image_path:

# # #             st.image(
# # #                 image_path,
# # #                 use_container_width=True
# # #             )

# # #         else:

# # #             st.warning(
# # #                 "Image not available"
# # #             )


# # #         # -----------------------------------------
# # #         # PRODUCT DETAILS
# # #         # -----------------------------------------

# # #         st.subheader(
# # #             row["product_name"]
# # #         )

# # #         st.write(
# # #             f"Product ID: {product_id}"
# # #         )

# # #         st.write(
# # #             f"Category: {row['sub_category']}"
# # #         )

# # #         st.write(
# # #             f"⭐ Rating: {row['avg_rating']}")

# # #         price = float(str(row["price.amount"]).replace(",", ""))

# # #         st.write(f"₹{price:.2f}")
        


# # #         # -----------------------------------------
# # #         # ADD TO CART
# # #         # -----------------------------------------

# # #         if st.button(
# # #             "🛒 Add to Cart",
# # #             key=f"cart_{product_id}"
# # #         ):

# # #             st.success(
# # #                 f"{row['product_name']} added to cart!"
# # #             )


# # import streamlit as st
# # import pandas as pd
# # import os


# # # =========================================================
# # # PAGE CONFIGURATION
# # # =========================================================

# # st.set_page_config(
# #     page_title="SmartLogix Customer",
# #     page_icon="🛍️",
# #     layout="wide"
# # )


# # # =========================================================
# # # TITLE
# # # =========================================================

# # st.title("🛍️ SmartLogix Customer Portal")
# # st.subheader("Browse Products")


# # # =========================================================
# # # LOAD PRODUCT DATA
# # # =========================================================

# # df = pd.read_csv("product.csv")


# # # =========================================================
# # # IMAGE MAPPING
# # # =========================================================

# # image_mapping = {

# #     "PRD-00453": "images/zenitha_saree.jpeg",

# #     "PRD-00517": "images/shoe.jpeg",

# #     "PRD-00079": "images/head_phone.jpeg",

# #     "PRD-00377": "images/dry_fruits.jpeg",

# #     "PRD-00635": "images/phamorchy.jpeg",
# #     "PRD-00071": "images/smart_phone.jpeg",
# #     "PRD-00190": "images/microwave.jpeg",
# #     "PRD-00524": "images/saree_01.jpeg",
# #     "PRD-00395":"images/spices.jpeg",
# #     "PRD-00115":"images/air_purifier.jpeg",
# #     "PRD-00336":"images/rice_bag.jpeg",
# #     "PRD-00391":"images/cooking_oil.jpeg",
# #     "PRD-00036":"images/laptop.jpeg",
# #     "PRD-00506":"images/saree_02.jpeg",
# #     "PRD-00466":"images/saree_03.jpeg"
# # }


# # # =========================================================
# # # SHOW ONLY 8 PRODUCTS
# # # =========================================================

# # display_df = df.head(8).copy()


# # # =========================================================
# # # PRODUCT GRID
# # # =========================================================

# # st.markdown("### 🛒 Available Products")


# # # Create 4 columns
# # cols = st.columns(4)


# # for index, (_, product) in enumerate(display_df.iterrows()):

# #     col = cols[index % 4]

# #     with col:

# #         product_id = product["product_id"]

# #         # ---------------------------------------------
# #         # GET IMAGE
# #         # ---------------------------------------------

# #         image_path = image_mapping.get(product_id)


# #         if image_path and os.path.exists(image_path):

# #             st.image(
# #                 image_path,
# #                 use_container_width=True
# #             )

# #         else:

# #             st.warning(
# #                 f"Image not found for {product_id}"
# #             )


# #         # ---------------------------------------------
# #         # PRODUCT NAME
# #         # ---------------------------------------------

# #         st.markdown(
# #             f"### {product['product_name']}"
# #         )


# #         # ---------------------------------------------
# #         # CATEGORY
# #         # ---------------------------------------------

# #         if "category" in product:

# #             st.write(
# #                 f"📂 Category: {product['sub_category']}"
# #             )


# #         # ---------------------------------------------
# #         # PRICE
# #         # ---------------------------------------------

# #         price = float(
# #             str(product["price.amount"]).replace(",", "")
# #         )

# #         st.write(
# #             f"💰 **₹{price:,.2f}**"
# #         )


# #         # ---------------------------------------------
# #         # RATING
# #         # ---------------------------------------------

# #         if "rating" in product:

# #             rating = float(product["avg_rating"])

# #             st.write(
# #                 f"⭐ {rating:.1f}"
# #             )


# #         # ---------------------------------------------
# #         # ADD TO CART
# #         # ---------------------------------------------

# #         if st.button(
# #             "🛒 Add to Cart",
# #             key=f"cart_{product_id}"
# #         ):

# #             st.success(
# #                 f"{product['product_name']} added to cart!"
# #             )


# #         st.divider()


# # # =========================================================
# # # CUSTOMER CHAT BOX
# # # =========================================================

# # st.markdown("---")

# # st.header("💬 Customer Support")


# # st.write(
# #     "Have a question about products, orders, delivery or payment?"
# # )


# # # Initialize chat history
# # if "messages" not in st.session_state:

# #     st.session_state.messages = []


# # # Display previous messages
# # for message in st.session_state.messages:

# #     with st.chat_message(message["role"]):

# #         st.write(message["content"])


# # # Chat input
# # user_question = st.chat_input(
# #     "Type your question here..."
# # )


# # if user_question:

# #     # ---------------------------------------------
# #     # STORE CUSTOMER QUESTION
# #     # ---------------------------------------------

# #     st.session_state.messages.append(
# #         {
# #             "role": "user",
# #             "content": user_question
# #         }
# #     )


# #     # ---------------------------------------------
# #     # SIMPLE CUSTOMER SUPPORT RESPONSE
# #     # ---------------------------------------------

# #     question = user_question.lower()


# #     if "price" in question:

# #         answer = (
# #             "You can check the product price directly "
# #             "below each product image."
# #         )


# #     elif "delivery" in question:

# #         answer = (
# #             "Our delivery team will process your order "
# #             "and provide delivery details after checkout."
# #         )


# #     elif "order" in question:

# #         answer = (
# #             "Please provide your Order ID so that "
# #             "we can check your order details."
# #         )


# #     elif "return" in question:

# #         answer = (
# #             "For return-related questions, please provide "
# #             "your Order ID and the reason for return."
# #         )


# #     elif "payment" in question:

# #         answer = (
# #             "We support standard online payment methods. "
# #             "Please contact support if your payment has failed."
# #         )


# #     else:

# #         answer = (
# #             "Thank you for your question! "
# #             "Our customer support team will help you."
# #         )


# #     # ---------------------------------------------
# #     # STORE RESPONSE
# #     # ---------------------------------------------

# #     st.session_state.messages.append(
# #         {
# #             "role": "assistant",
# #             "content": answer
# #         }
# #     )


# #     # Refresh page
# #     st.rerun()



# import streamlit as st
# import pandas as pd
# import os

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity


# # =========================================================
# # PAGE CONFIGURATION
# # =========================================================

# st.set_page_config(
#     page_title="SmartLogix Customer",
#     page_icon="🛍️",
#     layout="wide"
# )


# # =========================================================
# # LOAD DATA
# # =========================================================

# df = pd.read_csv("product.csv")


# # =========================================================
# # CLEAN DATA
# # =========================================================

# df["product_id"] = df["product_id"].astype(str)

# df["product_name"] = (
#     df["product_name"]
#     .fillna("")
#     .astype(str)
# )

# df["category"] = (
#     df["category"]
#     .fillna("")
#     .astype(str)
# )

# df["sub_category"] = (
#     df["sub_category"]
#     .fillna("")
#     .astype(str)
# )


# # =========================================================
# # IMAGE MAPPING
# # =========================================================
# image_mapping = {

#     "PRD-00453": "images/zenitha_saree.jpeg",

#     "PRD-00517": "images/shoe.jpeg",

#     "PRD-00079": "images/head_phone.jpeg",

#     "PRD-00377": "images/dry_fruits.jpeg",

#     "PRD-00635": "images/phamorchy.jpeg",
#     "PRD-00071": "images/smart_phone.jpeg",
#     "PRD-00190": "images/microwave.jpeg",
#     "PRD-00524": "images/saree_01.jpeg",
#     "PRD-00395":"images/spices.jpeg",
#     "PRD-00115":"images/air_purifier.jpeg",
#     "PRD-00336":"images/rice_bag.jpeg",
#     "PRD-00391":"images/cooking_oil.jpeg",
#     "PRD-00036":"images/laptop.jpeg",
#     "PRD-00506":"images/saree_02.jpeg",
#     "PRD-00466":"images/saree_03.jpeg",
#     "PRD-00794":"images/book.jpeg",
#     "PRD-00107": "images/smart_phone_01.jpeg",
#     "PRD-00063": "images/head_phone_01.jpeg",
# }


# # =========================================================
# # PAGE TITLE
# # =========================================================

# st.title("🛍️ SmartLogix Customer Page")

# st.write(
#     "Welcome! Search products or ask our customer support."
# )


# # =========================================================
# # CUSTOMER CHAT - TOP OF PAGE
# # =========================================================

# st.subheader("💬 Customer Support")


# # Create message history
# if "messages" not in st.session_state:

#     st.session_state.messages = []


# # Display previous messages
# for message in st.session_state.messages:

#     with st.chat_message(message["role"]):

#         st.write(message["content"])


# # Chat input
# customer_question = st.chat_input(
#     "Ask your question..."
# )


# # Process customer question
# if customer_question:

#     # Store customer message
#     st.session_state.messages.append({

#         "role": "user",

#         "content": customer_question

#     })


#     # Convert question to lowercase
#     question = customer_question.lower()


#     # -----------------------------------------------------
#     # CUSTOMER SUPPORT RESPONSES
#     # -----------------------------------------------------

#     if "price" in question:

#         response = (
#             "💰 You can see the price below each product."
#         )

#     elif "delivery" in question:

#         response = (
#             "🚚 Delivery time depends on your "
#             "location and selected product."
#         )

#     elif "order" in question:

#         response = (
#             "📦 Please provide your Order ID "
#             "to check your order."
#         )

#     elif "return" in question:

#         response = (
#             "🔄 Please provide your Order ID "
#             "and the reason for the return."
#         )

#     elif "payment" in question:

#         response = (
#             "💳 Available payment options will "
#             "be displayed during checkout."
#         )

#     elif "product" in question:

#         response = (
#             "🛍️ You can search for products "
#             "using the search box below."
#         )

#     elif "hello" in question or "hi" in question:

#         response = (
#             "👋 Hello! How can I help you today?"
#         )

#     else:

#         response = (
#             "😊 Thank you for your question. "
#             "Please provide more details."
#         )


#     # Store assistant response
#     st.session_state.messages.append({

#         "role": "assistant",

#         "content": response

#     })


#     # Refresh page
#     st.rerun()


# # =========================================================
# # SEPARATOR
# # =========================================================

# st.divider()


# # =========================================================
# # PRODUCT SEARCH
# # =========================================================

# st.subheader("🔎 Search Products")


# search_text = st.text_input(
#     "🔎 Search by product name, category, sub-category or price",
#     placeholder="Example: running shoes, saree, laptop, 2000..."
# )

# # =========================================================
# # CREATE SEARCH TEXT
# # =========================================================

# df["search_text"] = (

#     df["product_name"] + " "

#     + df["sub_category"] + " "
#     + df["price.amount"].astype(str)

# )


# # =========================================================
# # TF-IDF
# # =========================================================

# vectorizer = TfidfVectorizer(
#     stop_words="english"
# )


# product_vectors = vectorizer.fit_transform(
#     df["search_text"]
# )


# # =========================================================
# # PRODUCT SELECTION
# # =========================================================

# if search_text.strip() == "":

#     # -----------------------------------------------------
#     # NO SEARCH
#     # SHOW FIRST 8 PRODUCTS
#     # -----------------------------------------------------

#     st.subheader("🛒 Featured Products")

#     display_df = df.head(8).copy()


# else:

#     # -----------------------------------------------------
#     # SEARCH ENTERED
#     # COSINE SIMILARITY
#     # -----------------------------------------------------

#     search_vector = vectorizer.transform(
#         [search_text]
#     )


#     similarity_scores = cosine_similarity(

#         search_vector,

#         product_vectors

#     ).flatten()


#     search_results = df.copy()


#     search_results["similarity_score"] = (
#         similarity_scores
#     )


#     # Highest similarity first
#     search_results = search_results.sort_values(

#         by="similarity_score",

#         ascending=False

#     )


#     # Remove zero similarity products
#     search_results = search_results[
#         search_results["similarity_score"] > 0
#     ]


#     # -----------------------------------------------------
#     # TOP 6 PRODUCTS
#     # -----------------------------------------------------

#     display_df = search_results.head(6).copy()


#     st.subheader("🔎 Top 6 Similar Products")


#     if display_df.empty:

#         st.warning(
#             "No similar products found. "
#             "Please try another search."
#         )


# # =========================================================
# # DISPLAY PRODUCTS
# # =========================================================

# if not display_df.empty:

#     # 4 products in each row
#     cols = st.columns(4)


#     for index, (_, product) in enumerate(
#         display_df.iterrows()
#     ):

#         with cols[index % 4]:

#             # -------------------------------------------------
#             # IMAGE
#             # -------------------------------------------------

#             product_id = product["product_id"]


#             image_path = image_mapping.get(
#                 product_id
#             )


#             if image_path and os.path.exists(
#                 image_path
#             ):

#                 st.image(
#                     image_path,
#                     use_container_width=True
#                 )

#             else:

#                 st.info(
#                     "Image not available"
#                 )


#             # -------------------------------------------------
#             # PRODUCT NAME
#             # -------------------------------------------------

#             st.markdown(
#                 f"### {product['product_name']}"
#             )


#             # -------------------------------------------------
#             # PRODUCT ID
#             # -------------------------------------------------

#             st.write(
#                 f"🆔 {product_id}"
#             )


#             # -------------------------------------------------
#             # CATEGORY
#             # -------------------------------------------------

#             # st.write(
#             #     f"📂 {product['category']}"
#             # )


#             # -------------------------------------------------
#             # SUB CATEGORY
#             # -------------------------------------------------

#             st.write(
#                 f"📁 {product['sub_category']}"
#             )


#             # -------------------------------------------------
#             # PRICE
#             # -------------------------------------------------

#             try:

#                 price = float(

#                     str(product["price.amount"])
#                     .replace(",", "")
#                     .replace("₹", "")
#                     .strip()

#                 )

#                 st.write(
#                     f"💰 **₹{price:,.2f}**"
#                 )

#             except:

#                 st.write(
#                     f"💰 **{product['price.amount']}**"
#                 )


#             # -------------------------------------------------
#             # RATING
#             # -------------------------------------------------

#             try:

#                 rating = float(
#                     product["avg_rating"]
#                 )

#                 st.write(
#                     f"⭐ {rating:.1f} / 5"
#                 )

#             except:

#                 st.write(
#                     f"⭐ {product['avg_rating']}"
#                 )


#             # -------------------------------------------------
#             # ADD TO CART
#             # -------------------------------------------------

#             if st.button(

#                 "🛒 Add to Cart",

#                 key=f"cart_{product_id}_{index}"

#             ):

#                 if "cart" not in st.session_state:

#                     st.session_state.cart = []


#                 st.session_state.cart.append({

#                     "product_id": product_id,

#                     "product_name":
#                         product["product_name"],

#                     "price":
#                         product["price.amount"]

#                 })


#                 st.success(
#                     "Added to cart!"
#                 )


# # =========================================================
# # SHOPPING CART
# # =========================================================

# st.divider()

# st.subheader("🛒 Shopping Cart")


# if "cart" not in st.session_state:

#     st.session_state.cart = []


# if len(st.session_state.cart) == 0:

#     st.info(
#         "Your cart is empty."
#     )


# else:

#     for item in st.session_state.cart:

#         st.write(

#             f"**{item['product_name']}** "
#             f"- ₹{item['price']}"

#         )


#     st.write(

#         f"Total Items: "
#         f"{len(st.session_state.cart)}"

#     )

    
#     if st.button("🗑️ Clear Cart"):

#         st.session_state.cart = []

#         st.rerun()


# ============================================================
# SMARTLOGIX CUSTOMER PAGE
# ============================================================

import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SmartLogix Customer",
    page_icon="🛍️",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = True

if "messages" not in st.session_state:
    st.session_state.messages = []

if "cart" not in st.session_state:
    st.session_state.cart = []

if "wishlist" not in st.session_state:
    st.session_state.wishlist = []

if "orders" not in st.session_state:
    st.session_state.orders = []

if "customer_location" not in st.session_state:
    st.session_state.customer_location = "Chennai"

if "account_option" not in st.session_state:
    st.session_state.account_option = "Select an option"


# ============================================================
# POSTGRESQL DATABASE
# ============================================================

DATABASE = "smartlogistic_db"

DATABASE_URL = (
    f"postgresql://postgres:lavi@localhost:5432/{DATABASE}"
)

engine = create_engine(DATABASE_URL)


# ============================================================
# GET CUSTOMER DETAILS FROM POSTGRESQL
# ============================================================

def get_customer_details(customer_id):
    query = text("""
        SELECT
            customer_id,
            customer_name,
            email,
            phone
        FROM customers
        WHERE customer_id = :customer_id
        LIMIT 1
    """)

    try:
        with engine.connect() as conn:
            result = conn.execute(
                query,
                {"customer_id": customer_id}
            ).mappings().first()
        return result
    except Exception as e:
        st.error(f"❌ Unable to fetch customer details: {e}")
        return None


# ============================================================
# CUSTOMER INFORMATION
# ============================================================

customer_id = st.session_state.get("username", "")

customer_data = get_customer_details(customer_id)

if customer_data:
    customer_id = str(customer_data.get("customer_id", customer_id))
    customer_name = str(customer_data.get("customer_name", ""))
    customer_email = str(customer_data.get("email", ""))
    customer_phone = str(customer_data.get("phone", ""))
else:
    customer_name = ""
    customer_email = ""
    customer_phone = ""


# ============================================================
# PRODUCT FILE

# ============================================================

PRODUCT_FILE = "product.csv"


# ============================================================
# LOAD PRODUCT DATA
# ============================================================

try:

    df = pd.read_csv(PRODUCT_FILE)

except FileNotFoundError:

    st.error(
        f"❌ Product file not found: {PRODUCT_FILE}"
    )

    st.stop()

except Exception as e:

    st.error(
        f"❌ Error loading product.csv: {e}"
    )

    st.stop()


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [
    "product_id",
    "product_name"
]

missing_columns = [
    col
    for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(
        f"❌ Missing columns in product.csv: {missing_columns}"
    )

    st.stop()


# ============================================================
# CREATE OPTIONAL COLUMNS IF NOT AVAILABLE
# ============================================================

optional_columns = [
    "category",
    "sub_category",
    "price.amount",
    "rating",
    "tags",
    "specs"
]

for col in optional_columns:

    if col not in df.columns:

        if col == "price.amount":
            df[col] = 0

        elif col == "rating":
            df[col] = 0

        else:
            df[col] = ""


# ============================================================
# CLEAN DATA
# ============================================================

text_columns = [
    "product_id",
    "product_name",
    "category",
    "sub_category",
    "tags",
    "specs"
]

for col in text_columns:

    df[col] = (
        df[col]
        .fillna("")
        .astype(str)
    )


df["price.amount"] = pd.to_numeric(
    df["price.amount"],
    errors="coerce"
).fillna(0)


df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
).fillna(0)


# ============================================================
# PRODUCT IMAGE MAPPING
# ============================================================

IMAGE_MAP = {

    "PRD-00453": "images/zenitha_saree.jpeg",

    "PRD-00517": "images/shoe.jpeg",

    "PRD-00079": "images/head_phone.jpeg",

    "PRD-00377": "images/dry_fruits.jpeg",

    "PRD-00635": "images/phamorchy.jpeg",

    "PRD-00071": "images/smart_phone.jpeg",

    "PRD-00190": "images/microwave.jpeg",

    "PRD-00524": "images/saree_01.jpeg",

    "PRD-00395": "images/spices.jpeg",

    "PRD-00115": "images/air_purifier.jpeg",

    "PRD-00336": "images/rice_bag.jpeg",

    "PRD-00391": "images/cooking_oil.jpeg",

    "PRD-00036": "images/laptop.jpeg",

    "PRD-00506": "images/saree_02.jpeg",

    "PRD-00466": "images/saree_03.jpeg",

    "PRD-00794": "images/book.jpeg",

    "PRD-00107": "images/smart_phone_01.jpeg",

    "PRD-00063": "images/head_phone_01.jpeg"
}


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 32px;
        font-weight: 700;
        color: #262936;
    }

    .sub-title {
        font-size: 16px;
        color: #666666;
        margin-bottom: 15px;
    }

    .product-name {
        font-size: 18px;
        font-weight: 600;
        margin-top: 8px;
    }

    .price-text {
        font-size: 20px;
        font-weight: 700;
    }

    .account-box {
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #dddddd;
        background-color: #fafafa;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

header_col1, header_col2, header_col3 = st.columns(
    [6, 2, 2]
)


with header_col1:

    st.markdown(
        '<div class="main-title">🛍️ SmartLogix Customer Page</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Shop smart. Deliver smarter.</div>',
        unsafe_allow_html=True
    )


# ============================================================
# MY ACCOUNT DROPDOWN
# ============================================================

with header_col2:

    account_option = st.selectbox(
        "👤 My Account",
        [
    
            "👤 My Profile",
            "📦 My Orders",
            "❤️ Wishlist",
            "🚪 Logout"
        ],
        key="account_option",
        label_visibility="collapsed"
    )


# ============================================================
# LOCATION
# ============================================================

with header_col3:

    st.info(
        f"📍 {st.session_state.customer_location}"
    )


# ============================================================
# MY PROFILE
# ============================================================

if account_option == "👤 My Profile":

    st.markdown("---")

    st.subheader("👤 My Profile")

    profile_col1, profile_col2 = st.columns(2)

    with profile_col1:

        st.write(
            f"**Customer ID:** {customer_id}"
        )

        st.write(
            f"**Name:** {customer_name}"
        )

        st.write(
            f"**Email:** {customer_email}"
        )

        st.write(
            f"**Phone Number:** {customer_phone}"
        )

    with profile_col2:

        st.subheader("📍 Delivery Location")

        location_options = [
            "Chennai",
            "Coimbatore",
            "Madurai",
            "Trichy",
            "Salem",
            "Tirunelveli",
            "Erode",
            "Tiruppur",
            "Karaikudi",
            "Bangalore",
            "Hyderabad",
            "Mumbai",
            "Delhi",
            "Kolkata",
            "Pune"
        ]

        current_location = (
            st.session_state.customer_location
        )

        if current_location not in location_options:

            location_options.insert(
                0,
                current_location
            )

        selected_location = st.selectbox(
            "Choose delivery location",
            location_options,
            index=location_options.index(
                current_location
            )
        )

        if st.button(
            "💾 Save Location",
            use_container_width=True
        ):

            st.session_state.customer_location = (
                selected_location
            )

            st.success(
                "✅ Delivery location updated successfully."
            )

            st.rerun()


# ============================================================
# MY ORDERS
# ============================================================

elif account_option == "📦 My Orders":

    st.markdown("---")

    st.subheader("📦 My Orders")

    if len(st.session_state.orders) == 0:

        st.info(
            "You have no orders yet."
        )

    else:

        for order in st.session_state.orders:

            with st.container(border=True):

                st.write(
                    f"### 🧾 {order.get('order_id', 'N/A')}"
                )

                st.write(
                    f"**Product:** "
                    f"{order.get('product_name', 'N/A')}"
                )

                st.write(
                    f"**Product ID:** "
                    f"{order.get('product_id', 'N/A')}"
                )

                order_price = float(
                    order.get(
                        "price",
                        0
                    )
                )

                st.write(
                    f"**Price:** ₹{order_price:,.2f}"
                )

                st.write(
                    f"**Location:** "
                    f"{order.get('location', 'N/A')}"
                )

                st.write(
                    f"**Status:** "
                    f"{order.get('status', 'Order Placed')}"
                )


# ============================================================
# WISHLIST
# ============================================================

elif account_option == "❤️ Wishlist":

    st.markdown("---")

    st.subheader("❤️ My Wishlist")

    if len(st.session_state.wishlist) == 0:

        st.info(
            "Your wishlist is empty."
        )

    else:

        wishlist_columns = st.columns(4)

        for index, item in enumerate(
            st.session_state.wishlist
        ):

            with wishlist_columns[index % 4]:

                with st.container(border=True):

                    product_id = item.get(
                        "product_id",
                        ""
                    )

                    product_name = item.get(
                        "product_name",
                        "Product"
                    )

                    price = float(
                        item.get(
                            "price",
                            0
                        )
                    )

                    image_path = IMAGE_MAP.get(
                        product_id
                    )

                    if (
                        image_path
                        and os.path.exists(image_path)
                    ):

                        st.image(
                            image_path,
                            use_container_width=True
                        )

                    else:

                        st.info(
                            "🛍️ Image not available"
                        )

                    st.write(
                        f"**{product_name}**"
                    )

                    st.caption(
                        f"Product ID: {product_id}"
                    )

                    st.write(
                        f"₹{price:,.2f}"
                    )

                    if st.button(
                        "❌ Remove",
                        key=f"remove_wishlist_{index}",
                        use_container_width=True
                    ):

                        st.session_state.wishlist.pop(
                            index
                        )

                        st.rerun()


# ============================================================
# LOGOUT
# ============================================================

elif account_option == "🚪 Logout":

    st.markdown("---")

    st.warning(
        "Are you sure you want to logout?"
    )

    logout_col1, logout_col2 = st.columns(2)

    with logout_col1:

        if st.button(
            "✅ Yes, Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False

            st.session_state.messages = []

            st.session_state.cart = []

            st.session_state.wishlist = []

            st.session_state.orders = []

            if "username" in st.session_state:
                del st.session_state["username"]

            if "customer_id" in st.session_state:
                del st.session_state["customer_id"]

            if "customer_name" in st.session_state:
                del st.session_state["customer_name"]

            if "email" in st.session_state:
                del st.session_state["email"]

            if "phone" in st.session_state:
                del st.session_state["phone"]

            st.switch_page("app.py")


    with logout_col2:

        if st.button(
            "❌ Cancel",
            use_container_width=True
        ):

            st.session_state.account_option = (
                "Select an option"
            )

            st.rerun()


# ============================================================
# CURRENT LOCATION
# ============================================================

st.markdown("---")

st.success(
    f"📍 Current delivery location: "
    f"{st.session_state.customer_location}"
)


# ============================================================
# PRODUCT SEARCH
# ============================================================

st.header("🛍️ Products")

search_query = st.text_input(
    "🔎 Search products",
    placeholder=(
        "Search by product name, category, "
        "sub-category or price..."
    )
)


# ============================================================
# SEARCH TEXT
# ============================================================

df["search_text"] = (
    df["product_name"]
    + " "
    + df["category"]
    + " "
    + df["sub_category"]
    + " "
    + df["price.amount"].astype(str)
    + " "
    + df["tags"]
    + " "
    + df["specs"]
)


# ============================================================
# PRODUCT SEARCH
# ============================================================

if search_query.strip() == "":

    display_df = df.head(8).copy()

else:

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        tfidf_matrix = vectorizer.fit_transform(
            df["search_text"]
        )

        query_vector = vectorizer.transform(
            [search_query]
        )

        similarity_scores = cosine_similarity(
            query_vector,
            tfidf_matrix
        ).flatten()

        df["similarity"] = similarity_scores

        display_df = (
            df[
                df["similarity"] > 0
            ]
            .sort_values(
                by="similarity",
                ascending=False
            )
            .head(6)
            .copy()
        )

    except Exception as e:

        st.error(
            f"❌ Search error: {e}"
        )

        display_df = df.head(8).copy()


# ============================================================
# SEARCH RESULT
# ============================================================

if search_query.strip() != "":

    if len(display_df) == 0:

        st.warning(
            "❌ No matching products found."
        )

    else:

        st.success(
            f"🔎 {len(display_df)} matching products found."
        )


# ============================================================
# DISPLAY PRODUCTS
# ============================================================

if len(display_df) == 0:

    st.info(
        "No products available."
    )

else:

    product_columns = st.columns(4)

    for index, (_, product) in enumerate(
        display_df.iterrows()
    ):

        with product_columns[index % 4]:

            # IMPORTANT:
            # Use Streamlit container instead of
            # opening HTML div tags.

            with st.container(border=True):

                product_id = str(
                    product["product_id"]
                )

                product_name = str(
                    product["product_name"]
                )

                category = str(
                    product["category"]
                )

                sub_category = str(
                    product["sub_category"]
                )

                price = float(
                    product["price.amount"]
                )

                rating = float(
                    product["rating"]
                )

                image_path = IMAGE_MAP.get(
                    product_id
                )


                # --------------------------------------------
                # IMAGE
                # --------------------------------------------

                if (
                    image_path
                    and os.path.exists(image_path)
                ):

                    st.image(
                        image_path,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "🛍️ Product image not available"
                    )


                # --------------------------------------------
                # PRODUCT NAME
                # --------------------------------------------

                st.markdown(
                    f"### {product_name}"
                )


                # --------------------------------------------
                # PRODUCT ID
                # --------------------------------------------

                st.caption(
                    f"Product ID: {product_id}"
                )


                # --------------------------------------------
                # CATEGORY
                # --------------------------------------------

                st.write(
                    f"**Category:** {category}"
                )


                st.write(
                    f"**Sub-category:** {sub_category}"
                )


                # --------------------------------------------
                # PRICE
                # --------------------------------------------

                st.markdown(
                    f"### ₹{price:,.2f}"
                )


                # --------------------------------------------
                # RATING
                # --------------------------------------------

                st.write(
                    f"⭐ {rating:.1f}"
                )


                # --------------------------------------------
                # ADD TO CART
                # --------------------------------------------

                if st.button(
                    "🛒 Add to Cart",
                    key=f"cart_{product_id}_{index}",
                    use_container_width=True
                ):

                    existing_cart_ids = [
                        item.get("product_id")
                        for item in st.session_state.cart
                    ]

                    if product_id in existing_cart_ids:

                        st.warning(
                            "Product is already in your cart."
                        )

                    else:

                        cart_item = {

                            "product_id":
                                product_id,

                            "product_name":
                                product_name,

                            "price":
                                price,

                            "location":
                                st.session_state.customer_location
                        }

                        st.session_state.cart.append(
                            cart_item
                        )

                        st.success(
                            "✅ Added to cart."
                        )


                # --------------------------------------------
                # ADD TO WISHLIST
                # --------------------------------------------

                if st.button(
                    "❤️ Add to Wishlist",
                    key=f"wishlist_{product_id}_{index}",
                    use_container_width=True
                ):

                    existing_wishlist_ids = [
                        item.get("product_id")
                        for item in st.session_state.wishlist
                    ]

                    if product_id in existing_wishlist_ids:

                        st.warning(
                            "Product is already in wishlist."
                        )

                    else:

                        wishlist_item = {

                            "product_id":
                                product_id,

                            "product_name":
                                product_name,

                            "price":
                                price
                        }

                        st.session_state.wishlist.append(
                            wishlist_item
                        )

                        st.success(
                            "❤️ Added to wishlist."
                        )


# ============================================================
# SHOPPING CART
# ============================================================

st.markdown("---")

st.header("🛒 Shopping Cart")


if len(st.session_state.cart) == 0:

    st.info(
        "Your cart is empty."
    )

else:

    total_amount = 0.0


    for index, item in enumerate(
        st.session_state.cart
    ):

        item_product_id = item.get(
            "product_id",
            ""
        )

        item_product_name = item.get(
            "product_name",
            "Product"
        )

        item_price = float(
            item.get(
                "price",
                0
            )
        )

        item_location = item.get(
            "location",
            st.session_state.customer_location
        )


        with st.container(border=True):

            cart_col1, cart_col2, cart_col3 = st.columns(
                [5, 2, 2]
            )


            with cart_col1:

                st.write(
                    f"### 🛍️ {item_product_name}"
                )

                st.write(
                    f"Product ID: {item_product_id}"
                )

                st.write(
                    f"📍 {item_location}"
                )


            with cart_col2:

                st.write(
                    f"₹{item_price:,.2f}"
                )


            with cart_col3:

                if st.button(
                    "❌ Remove",
                    key=f"remove_cart_{index}",
                    use_container_width=True
                ):

                    st.session_state.cart.pop(
                        index
                    )

                    st.rerun()


        total_amount += item_price


    # ========================================================
    # TOTAL
    # ========================================================

    st.subheader(
        f"💰 Total Amount: ₹{total_amount:,.2f}"
    )


    # ========================================================
    # PLACE ORDER
    # ========================================================

    if st.button(
        "📦 Place Order",
        use_container_width=True
    ):

        starting_order_number = (
            len(st.session_state.orders) + 1
        )


        for item_index, item in enumerate(
            st.session_state.cart
        ):

            order_number = (
                starting_order_number
                + item_index
            )

            new_order = {

                "order_id":
                    f"ORD-{order_number:05d}",

                "product_id":
                    item.get(
                        "product_id",
                        ""
                    ),

                "product_name":
                    item.get(
                        "product_name",
                        "Product"
                    ),

                "price":
                    float(
                        item.get(
                            "price",
                            0
                        )
                    ),

                "location":
                    item.get(
                        "location",
                        st.session_state.customer_location
                    ),

                "status":
                    "Order Placed"
            }

            st.session_state.orders.append(
                new_order
            )


        st.session_state.cart = []

        st.success(
            "🎉 Order placed successfully!"
        )

        st.balloons()

        st.rerun()


    # ========================================================
    # CLEAR CART
    # ========================================================

    if st.button(
        "🗑️ Clear Cart",
        use_container_width=True
    ):

        st.session_state.cart = []

        st.success(
            "Cart cleared successfully."
        )

        st.rerun()


# ============================================================
# SUMMARY
# ============================================================

st.markdown("---")

summary_col1, summary_col2, summary_col3 = st.columns(3)


with summary_col1:

    st.metric(
        "🛒 Cart Items",
        len(st.session_state.cart)
    )


with summary_col2:

    st.metric(
        "❤️ Wishlist",
        len(st.session_state.wishlist)
    )


with summary_col3:

    st.metric(
        "📦 Orders",
        len(st.session_state.orders)
    )



