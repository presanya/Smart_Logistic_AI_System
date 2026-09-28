# ============================================================
# SMARTLOGIX INTELLIGENT AI CHATBOT
# PostgreSQL + TF-IDF + RAG + Gemini
# ============================================================

import os
import re

import pandas as pd
import streamlit as st

from dotenv import load_dotenv
from google import genai

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sqlalchemy import create_engine


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SmartLogix AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
        radial-gradient(
            circle at 10% 10%,
            rgba(99,102,241,0.15),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(236,72,153,0.12),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #f8fafc,
            #eef2ff
        );
    }

    .chat-title {
        font-size: 38px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    .chat-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .feature-box {
        padding: 15px;
        border-radius: 15px;
        background: rgba(255,255,255,0.75);
        border: 1px solid rgba(148,163,184,0.25);
        text-align: center;
        margin-bottom: 15px;
    }

    .product-card {
        padding: 15px;
        border-radius: 15px;
        background: white;
        border: 1px solid #e2e8f0;
        margin-bottom: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }

    .product-name {
        font-size: 18px;
        font-weight: 700;
    }

    .product-price {
        font-size: 20px;
        font-weight: 700;
    }

    .product-rating {
        color: #f59e0b;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="chat-title">🤖 SmartLogix AI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="chat-subtitle">
    Your intelligent assistant for orders, deliveries, products,
    reviews and FAQs
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not GEMINI_API_KEY:

    st.error(
        "❌ GEMINI_API_KEY was not found in the .env file."
    )

    st.stop()


# ============================================================
# GEMINI CLIENT
# ============================================================

try:

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

except Exception as e:

    st.error(
        f"Gemini client initialization failed: {e}"
    )

    st.stop()


# ============================================================
# POSTGRESQL DATABASE CONFIGURATION
# ============================================================

DATABASE = "smartlogistic_db"

DATABASE_URL = (
    f"postgresql://postgres:lavi@localhost:5432/{DATABASE}"
)


# ============================================================
# CREATE POSTGRESQL ENGINE
# ============================================================

try:

    engine = create_engine(
        DATABASE_URL
    )

    # Test PostgreSQL connection

    with engine.connect() as connection:

        pass

except Exception as e:

    st.error(
        f"""
        ❌ PostgreSQL connection failed.

        Database:
        {DATABASE}

        Error:
        {e}
        """
    )

    st.stop()


# ============================================================
# LOAD PRODUCT DATA
# ============================================================

PRODUCT_FILE = "product.csv"


if not os.path.exists(PRODUCT_FILE):

    st.error(
        f"❌ {PRODUCT_FILE} was not found."
    )

    st.stop()


@st.cache_data
def load_products():

    df = pd.read_csv(
        PRODUCT_FILE
    )

    df.columns = (
        df.columns
        .str.strip()
    )

    return df


df = load_products()


# ============================================================
# CHECK PRODUCT COLUMNS
# ============================================================

required_product_columns = [
    "product_id",
    "product_name",
    "sub_category"
]


missing_columns = [
    col
    for col in required_product_columns
    if col not in df.columns
]


if missing_columns:

    st.error(
        f"Missing product columns: {missing_columns}"
    )

    st.stop()


# ============================================================
# CLEAN PRODUCT DATA
# ============================================================

text_columns = [
    "product_id",
    "product_name",
    "sub_category"
]


for col in text_columns:

    df[col] = (
        df[col]
        .fillna("")
        .astype(str)
        .str.strip()
    )


# ============================================================
# CATEGORY COLUMN
# ============================================================

if "category" not in df.columns:

    df["category"] = ""


df["category"] = (
    df["category"]
    .fillna("")
    .astype(str)
    .str.strip()
)


# ============================================================
# PRICE CLEANING
# ============================================================

if "price.amount" in df.columns:

    df["price.amount"] = (
        df["price.amount"]
        .astype(str)
        .str.replace(
            "₹",
            "",
            regex=False
        )
        .str.replace(
            "Rs.",
            "",
            regex=False
        )
        .str.replace(
            "Rs",
            "",
            regex=False
        )
        .str.replace(
            ",",
            "",
            regex=False
        )
        .str.strip()
    )

    df["price.amount"] = pd.to_numeric(
        df["price.amount"],
        errors="coerce"
    ).fillna(0)

else:

    df["price.amount"] = 0


# ============================================================
# RATING
# ============================================================

if "avg_rating" in df.columns:

    df["avg_rating"] = pd.to_numeric(
        df["avg_rating"],
        errors="coerce"
    ).fillna(0)

else:

    df["avg_rating"] = 0


# ============================================================
# IMAGE MAPPING
# ============================================================

image_mapping = {

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
# PRODUCT SEARCH TEXT
# ============================================================

df["search_text"] = (

    df["product_id"]
    + " "

    + df["product_name"]
    + " "

    + df["category"]
    + " "

    + df["sub_category"]
    + " "

    + "price "

    + df["price.amount"].astype(str)

)


# ============================================================
# TF-IDF
# ============================================================

@st.cache_resource
def create_tfidf_vectors(text_data):

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(
        text_data
    )

    return vectorizer, vectors


vectorizer, product_vectors = (
    create_tfidf_vectors(
        df["search_text"]
    )
)


# ============================================================
# LOAD REVIEWS
# ============================================================

@st.cache_data
def load_reviews():

    if not os.path.exists(
        "reviews.csv"
    ):

        return pd.DataFrame(
            columns=[
                "product_id",
                "review"
            ]
        )


    reviews = pd.read_csv(
        "reviews.csv"
    )

    reviews.columns = (
        reviews.columns
        .str.strip()
    )

    return reviews


reviews_df = load_reviews()


# ============================================================
# LOAD FAQ
# ============================================================

@st.cache_data
def load_faq():

    if not os.path.exists(
        "faq.csv"
    ):

        return pd.DataFrame(
            columns=[
                "question",
                "answer"
            ]
        )


    faq = pd.read_csv(
        "faq.csv"
    )

    faq.columns = (
        faq.columns
        .str.strip()
    )

    return faq


faq_df = load_faq()


# ============================================================
# GET POSTGRESQL DATABASE TABLES
# ============================================================

def get_database_tables():

    try:

        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name
        """


        tables = pd.read_sql(
            query,
            engine
        )


        return tables[
            "table_name"
        ].tolist()


    except Exception as e:

        st.warning(
            f"PostgreSQL table error: {e}"
        )

        return []


# ============================================================
# ORDER ID EXTRACTION
# ============================================================

def extract_order_id(
    question
):

    pattern = (
        r"\b(?:ORD|ORDER)[-_]?\d+\b"
    )


    match = re.search(
        pattern,
        question.upper()
    )


    if match:

        return match.group(0)


    return None


# ============================================================
# PRODUCT ID EXTRACTION
# ============================================================

def extract_product_ids(
    question
):

    pattern = r"\bPRD-\d+\b"


    return re.findall(
        pattern,
        question.upper()
    )


# ============================================================
# PRICE EXTRACTION
# ============================================================

def extract_price(
    question
):

    question_lower = (
        question.lower()
    )


    numbers = re.findall(
        r"\d+(?:,\d+)*(?:\.\d+)?",
        question_lower
    )


    if not numbers:

        return None, None


    try:

        value = float(
            numbers[0].replace(
                ",",
                ""
            )
        )

    except:

        return None, None


    if any(
        word in question_lower
        for word in [
            "under",
            "below",
            "less than",
            "within",
            "upto",
            "up to",
            "maximum",
            "max"
        ]
    ):

        return "max", value


    if any(
        word in question_lower
        for word in [
            "above",
            "over",
            "more than",
            "minimum",
            "min"
        ]
    ):

        return "min", value


    return None, None


# ============================================================
# PRODUCT RETRIEVAL
# ============================================================

def retrieve_products(
    question,
    top_k=6
):

    question_vector = (
        vectorizer.transform(
            [question]
        )
    )


    similarities = (
        cosine_similarity(
            question_vector,
            product_vectors
        )
        .flatten()
    )


    result = df.copy()


    result["similarity"] = (
        similarities
    )


    # --------------------------------------------------------
    # PRICE FILTER
    # --------------------------------------------------------

    price_type, price_value = (
        extract_price(
            question
        )
    )


    if price_type == "max":

        result = result[
            result["price.amount"]
            <= price_value
        ]


    elif price_type == "min":

        result = result[
            result["price.amount"]
            >= price_value
        ]


    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    result = result.sort_values(
        by="similarity",
        ascending=False
    )


    result = result[
        result["similarity"] > 0
    ]


    return result.head(
        top_k
    )


# ============================================================
# GET ORDER INFORMATION FROM POSTGRESQL
# ============================================================

def get_order_information(
    order_id
):

    tables = get_database_tables()


    # --------------------------------------------------------
    # CHECK ORDERS TABLE
    # --------------------------------------------------------

    if "orders" not in tables:

        st.warning(
            """
            ❌ 'orders' table was not found
            in PostgreSQL.
            """
        )

        return None


    try:

        query = """
        SELECT *
        FROM orders
        WHERE UPPER(order_id::text)
              = UPPER(%(order_id)s)
        LIMIT 1
        """


        result = pd.read_sql(
            query,
            engine,
            params={
                "order_id": order_id
            }
        )


        return result


    except Exception as e:

        st.warning(
            f"PostgreSQL SQL error: {e}"
        )

        return None


# ============================================================
# GET DELIVERY INFORMATION
# ============================================================

def get_delivery_information(
    order_id
):

    result = (
        get_order_information(
            order_id
        )
    )


    return result


# ============================================================
# REVIEW RETRIEVAL
# ============================================================

def get_product_reviews(
    product_id
):

    if reviews_df.empty:

        return []


    if "product_id" not in (
        reviews_df.columns
    ):

        return []


    review_column = None


    possible_columns = [

        "review",

        "review_text",

        "reviews",

        "comment",

        "customer_review"

    ]


    for col in possible_columns:

        if col in reviews_df.columns:

            review_column = col

            break


    if review_column is None:

        return []


    result = reviews_df[
        reviews_df[
            "product_id"
        ]
        .astype(str)
        .str.upper()
        ==
        product_id.upper()
    ]


    return result[
        review_column
    ].dropna().astype(str).tolist()


# ============================================================
# FAQ RETRIEVAL
# ============================================================

def retrieve_faq(
    question,
    top_k=3
):

    if faq_df.empty:

        return faq_df


    if "question" not in (
        faq_df.columns
    ):

        return faq_df


    faq_text = (
        faq_df["question"]
        .fillna("")
        .astype(str)
    )


    faq_vectorizer = (
        TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )
    )


    faq_vectors = (
        faq_vectorizer.fit_transform(
            faq_text
        )
    )


    question_vector = (
        faq_vectorizer.transform(
            [question]
        )
    )


    scores = (
        cosine_similarity(
            question_vector,
            faq_vectors
        )
        .flatten()
    )


    result = faq_df.copy()


    result["similarity"] = (
        scores
    )


    result = result.sort_values(
        "similarity",
        ascending=False
    )


    result = result[
        result["similarity"] > 0
    ]


    return result.head(
        top_k
    )


# ============================================================
# COMPARE PRODUCTS
# ============================================================

def compare_products(
    product_ids
):

    if not product_ids:

        return pd.DataFrame()


    result = df[
        df["product_id"].isin(
            product_ids
        )
    ].copy()


    return result


# ============================================================
# BUILD PRODUCT CONTEXT
# ============================================================

def build_product_context(
    products
):

    if products.empty:

        return (
            "No matching products were found."
        )


    context = []


    for _, row in (
        products.iterrows()
    ):

        similarity = row.get(
            "similarity",
            0
        )


        context.append(
            f"""
Product ID: {row['product_id']}
Product Name: {row['product_name']}
Category: {row['category']}
Sub Category: {row['sub_category']}
Price: ₹{row['price.amount']:,.2f}
Rating: {row['avg_rating']:.1f}
Similarity: {similarity:.4f}
"""
        )


    return "\n".join(
        context
    )


# ============================================================
# BUILD ORDER CONTEXT
# ============================================================

def build_order_context(
    order_df
):

    if order_df is None:

        return (
            "No order information was found."
        )


    if order_df.empty:

        return (
            "No order was found "
            "for the given order ID."
        )


    row = order_df.iloc[0]


    context = []


    for column in (
        order_df.columns
    ):

        value = row[column]


        if pd.notna(value):

            context.append(
                f"{column}: {value}"
            )


    return "\n".join(
        context
    )


# ============================================================
# BUILD REVIEW CONTEXT
# ============================================================

def build_review_context(
    product_id
):

    reviews = (
        get_product_reviews(
            product_id
        )
    )


    if not reviews:

        return (
            "No customer reviews were found."
        )


    return "\n".join(
        [
            f"- {review}"
            for review in reviews[:30]
        ]
    )


# ============================================================
# BUILD FAQ CONTEXT
# ============================================================

def build_faq_context(
    question
):

    result = (
        retrieve_faq(
            question
        )
    )


    if result.empty:

        return (
            "No relevant FAQ was found."
        )


    context = []


    for _, row in (
        result.iterrows()
    ):

        context.append(
            f"""
Question: {row['question']}
Answer: {row['answer']}
Similarity: {row['similarity']:.4f}
"""
        )


    return "\n".join(
        context
    )


# ============================================================
# INTENT DETECTION
# ============================================================

def detect_intent(
    question
):

    q = question.lower()


    # --------------------------------------------------------
    # ORDER TRACKING
    # --------------------------------------------------------

    if (
        extract_order_id(
            question
        )

        or any(
            word in q
            for word in [

                "track my order",

                "where is my order",

                "order status",

                "shipment status",

                "delivery status",

                "when will my order arrive",

                "when will my order come"

            ]
        )
    ):

        return "order"


    # --------------------------------------------------------
    # PRODUCT COMPARISON
    # --------------------------------------------------------

    if (
        "compare" in q

        or "comparison" in q

        or "difference between" in q
    ):

        return "compare"


    # --------------------------------------------------------
    # REVIEW
    # --------------------------------------------------------

    if (
        "review" in q

        or "reviews" in q

        or "customer feedback" in q

        or "what customers say" in q
    ):

        return "review"


    # --------------------------------------------------------
    # RECOMMENDATION
    # --------------------------------------------------------

    if (
        "recommend" in q

        or "suggest" in q

        or "show me" in q

        or "looking for" in q

        or "find me" in q

        or "need a" in q

        or "need an" in q
    ):

        return "product"


    # --------------------------------------------------------
    # DELIVERY
    # --------------------------------------------------------

    if (
        "delivery" in q

        or "shipping" in q

        or "shipment" in q

        or "eta" in q
    ):

        if extract_order_id(
            question
        ):

            return "order"


        return "delivery"


    # --------------------------------------------------------
    # FAQ
    # --------------------------------------------------------

    if (
        "policy" in q

        or "return" in q

        or "refund" in q

        or "cancel" in q

        or "faq" in q

        or "how can i" in q

        or "what is" in q
    ):

        return "faq"


    # --------------------------------------------------------
    # DEFAULT
    # --------------------------------------------------------

    return "general"


# ============================================================
# GEMINI RESPONSE
# ============================================================

def ask_gemini(
    question,
    context,
    intent
):

    system_instruction = """
You are SmartLogix AI Assistant.

You help customers with:

1. Order tracking
2. Delivery information
3. Product recommendations
4. Product comparison
5. Customer review summaries
6. FAQs
7. General SmartLogix questions

IMPORTANT RULES:

- Use the supplied context as the primary source.
- Never invent order information.
- Never invent prices.
- Never invent delivery dates.
- Never invent product ratings.
- If information is unavailable, clearly say that it is unavailable.
- For product recommendations, use the retrieved products.
- For order questions, use the PostgreSQL data.
- For FAQs, use the retrieved FAQ information.
- For reviews, summarize only the supplied reviews.
- Keep answers simple and customer-friendly.
- Use bullet points when useful.
- Include product IDs when discussing products.
- Use Indian Rupee formatting for prices.
"""


    prompt = f"""
User Question:

{question}


Detected Intent:

{intent}


Retrieved SmartLogix Context:

{context}


Answer the user's question using
the supplied context.
"""


    try:

        if (
            st.session_state
            .gemini_interaction_id
        ):

            interaction = (
                client.interactions.create(

                    model="gemini-3.6-flash",

                    previous_interaction_id=(
                        st.session_state
                        .gemini_interaction_id
                    ),

                    system_instruction=(
                        system_instruction
                    ),

                    input=prompt
                )
            )


        else:

            interaction = (
                client.interactions.create(

                    model="gemini-3.6-flash",

                    system_instruction=(
                        system_instruction
                    ),

                    input=prompt
                )
            )


        st.session_state.gemini_interaction_id = (
            interaction.id
        )


        return interaction.output_text


    except Exception as e:

        return f"""
❌ Gemini Error

{str(e)}
"""


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in (
    st.session_state
):

    st.session_state.messages = []


if "gemini_interaction_id" not in (
    st.session_state
):

    st.session_state.gemini_interaction_id = None


if "last_products" not in (
    st.session_state
):

    st.session_state.last_products = (
        pd.DataFrame()
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "🤖 SmartLogix AI"
    )


    st.write(
        "Intelligent customer assistant"
    )


    st.divider()


    st.subheader(
        "Capabilities"
    )


    st.write(
        "📦 Order Tracking"
    )


    st.write(
        "🚚 Delivery Questions"
    )


    st.write(
        "🛍️ Product Recommendations"
    )


    st.write(
        "⚖️ Product Comparison"
    )


    st.write(
        "⭐ Review Summarization"
    )


    st.write(
        "🗄️ PostgreSQL Delivery Information"
    )


    st.write(
        "📚 FAQ RAG"
    )


    st.divider()


    st.subheader(
        "Data Sources"
    )


    st.write(
        f"🛍️ Products: {len(df):,}"
    )


    st.write(
        f"⭐ Reviews: {len(reviews_df):,}"
    )


    st.write(
        f"📚 FAQs: {len(faq_df):,}"
    )


    tables = (
        get_database_tables()
    )


    if tables:

        st.write(
            f"🗄️ PostgreSQL Tables: "
            f"{len(tables)}"
        )


        with st.expander(
            "View Tables"
        ):

            for table in tables:

                st.write(
                    f"• {table}"
                )


    else:

        st.write(
            "🗄️ PostgreSQL: No tables found"
        )


    st.divider()


    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.session_state.gemini_interaction_id = (
            None
        )

        st.session_state.last_products = (
            pd.DataFrame()
        )

        st.rerun()


# ============================================================
# FEATURE BOXES
# ============================================================

col1, col2, col3, col4 = (
    st.columns(4)
)


with col1:

    st.markdown(
        """
        <div class="feature-box">
        📦<br>
        <b>Order Tracking</b><br>
        Track your shipment
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="feature-box">
        🛍️<br>
        <b>Product Search</b><br>
        Find suitable products
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="feature-box">
        ⚖️<br>
        <b>Compare Products</b><br>
        Compare product details
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        """
        <div class="feature-box">
        📚<br>
        <b>Smart FAQ</b><br>
        Get instant answers
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CHAT HISTORY
# ============================================================

for message in (
    st.session_state.messages
):

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

user_question = st.chat_input(
    "Ask SmartLogix anything..."
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if user_question:

    # --------------------------------------------------------
    # DISPLAY USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )


    with st.chat_message(
        "user"
    ):

        st.markdown(
            user_question
        )


    # --------------------------------------------------------
    # DETECT INTENT
    # --------------------------------------------------------

    intent = detect_intent(
        user_question
    )


    # --------------------------------------------------------
    # CONTEXT VARIABLES
    # --------------------------------------------------------

    context_parts = []

    retrieved_products = (
        pd.DataFrame()
    )

    order_data = None


    # ========================================================
    # ORDER / DELIVERY
    # ========================================================

    if intent in [
        "order",
        "delivery"
    ]:

        order_id = extract_order_id(
            user_question
        )


        if order_id:

            order_data = (
                get_delivery_information(
                    order_id
                )
            )


            context_parts.append(
                "ORDER / DELIVERY DATA:\n"
                +
                build_order_context(
                    order_data
                )
            )


        else:

            context_parts.append(
                """
No specific order ID was provided.

Ask the customer to provide
their order ID when order-specific
information is required.
"""
            )


    # ========================================================
    # PRODUCT RECOMMENDATION
    # ========================================================

    if intent == "product":

        retrieved_products = (
            retrieve_products(
                user_question,
                top_k=6
            )
        )


        context_parts.append(
            "PRODUCT SEARCH RESULTS:\n"
            +
            build_product_context(
                retrieved_products
            )
        )


        st.session_state.last_products = (
            retrieved_products
        )


    # ========================================================
    # PRODUCT COMPARISON
    # ========================================================

    if intent == "compare":

        product_ids = (
            extract_product_ids(
                user_question
            )
        )


        if product_ids:

            retrieved_products = (
                compare_products(
                    product_ids
                )
            )


            retrieved_products = (
                retrieved_products.copy()
            )


            retrieved_products[
                "similarity"
            ] = 1.0


            context_parts.append(
                "PRODUCT COMPARISON DATA:\n"
                +
                build_product_context(
                    retrieved_products
                )
            )


            st.session_state.last_products = (
                retrieved_products
            )


        else:

            retrieved_products = (
                retrieve_products(
                    user_question,
                    top_k=6
                )
            )


            context_parts.append(
                "POTENTIAL PRODUCTS:\n"
                +
                build_product_context(
                    retrieved_products
                )
            )


            st.session_state.last_products = (
                retrieved_products
            )


    # ========================================================
    # REVIEWS
    # ========================================================

    if intent == "review":

        product_ids = (
            extract_product_ids(
                user_question
            )
        )


        if product_ids:

            for product_id in product_ids:

                review_context = (
                    build_review_context(
                        product_id
                    )
                )


                context_parts.append(
                    f"""
REVIEWS FOR {product_id}:

{review_context}
"""
                )


        else:

            retrieved_products = (
                retrieve_products(
                    user_question,
                    top_k=3
                )
            )


            for _, row in (
                retrieved_products.iterrows()
            ):

                product_id = (
                    row["product_id"]
                )


                review_context = (
                    build_review_context(
                        product_id
                    )
                )


                context_parts.append(
                    f"""
Product: {product_id}

Reviews:
{review_context}
"""
                )


    # ========================================================
    # FAQ RAG
    # ========================================================

    if intent == "faq":

        faq_context = (
            build_faq_context(
                user_question
            )
        )


        context_parts.append(
            "FAQ RAG CONTEXT:\n"
            +
            faq_context
        )


    # ========================================================
    # GENERAL PRODUCT SEARCH
    # ========================================================

    if intent == "general":

        retrieved_products = (
            retrieve_products(
                user_question,
                top_k=4
            )
        )


        if not retrieved_products.empty:

            context_parts.append(
                "RELATED PRODUCT INFORMATION:\n"
                +
                build_product_context(
                    retrieved_products
                )
            )


    # ========================================================
    # COMBINE CONTEXT
    # ========================================================

    if context_parts:

        final_context = (
            "\n\n".join(
                context_parts
            )
        )

    else:

        final_context = (
            "No external context was retrieved."
        )


    # ========================================================
    # GEMINI
    # ========================================================

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "🤖 SmartLogix AI is thinking..."
        ):

            answer = ask_gemini(
                user_question,
                final_context,
                intent
            )


        st.markdown(
            answer
        )


        # ----------------------------------------------------
        # DISPLAY PRODUCTS
        # ----------------------------------------------------

        if (
            not retrieved_products.empty

            and intent in [
                "product",
                "compare",
                "review",
                "general"
            ]
        ):

            st.markdown(
                "### 🛍️ Related Products"
            )


            number_of_columns = min(
                3,
                len(retrieved_products)
            )


            product_columns = (
                st.columns(
                    number_of_columns
                )
            )


            for index, (_, row) in enumerate(
                retrieved_products.iterrows()
            ):

                col = product_columns[
                    index
                    % len(product_columns)
                ]


                with col:

                    st.markdown(
                        '<div class="product-card">',
                        unsafe_allow_html=True
                    )


                    product_id = (
                        row["product_id"]
                    )


                    image_path = (
                        image_mapping.get(
                            product_id
                        )
                    )


                    if (
                        image_path

                        and os.path.exists(
                            image_path
                        )
                    ):

                        st.image(
                            image_path,
                            use_container_width=True
                        )


                    st.markdown(
                        f"""
                        <div class="product-name">
                        {row['product_name']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    st.write(
                        f"🆔 {product_id}"
                    )


                    st.write(
                        f"📂 {row['category']}"
                    )


                    st.markdown(
                        f"""
                        <div class="product-price">
                        ₹{row['price.amount']:,.2f}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    st.markdown(
                        f"""
                        <div class="product-rating">
                        ⭐ {row['avg_rating']:.1f}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    if "similarity" in row:

                        st.caption(
                            f"Similarity: "
                            f"{row['similarity']:.2f}"
                        )


                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )


    # ========================================================
    # SAVE ASSISTANT RESPONSE
    # ========================================================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )