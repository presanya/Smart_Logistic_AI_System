# ============================================================
# SMARTLOGIX - DRONE DAMAGE CLASSIFICATION
# YOLO CLASSIFICATION + STREAMLIT
# ============================================================

import os
import tempfile
import streamlit as st
from PIL import Image
from ultralytics import YOLO


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SmartLogix - Drone Damage Classification",
    page_icon="🚁",
    layout="wide"
)


# ============================================================
# MODEL PATH
# ============================================================

MODEL_PATH = (
    r"C:\ML Project\SmartLogix AI_Intelligent_Multi_Modal_Logistics"
    r"\runs\classify\drone_classification"
    r"\drone_damage_classifier"
    r"\weights\best.pt"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main application background */
    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(59, 130, 246, 0.15),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(168, 85, 247, 0.15),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #f8fafc,
                #eef2ff
            );
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #475569;
        margin-bottom: 30px;
    }

    /* Prediction card */
    .prediction-card {
        padding: 25px;
        border-radius: 20px;
        background: rgba(255,255,255,0.90);
        box-shadow: 0px 8px 30px rgba(0,0,0,0.10);
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    /* Prediction title */
    .prediction-title {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    /* Confidence */
    .confidence {
        font-size: 22px;
        font-weight: 600;
    }

    /* Information card */
    .info-card {
        padding: 20px;
        border-radius: 15px;
        background: rgba(255,255,255,0.85);
        box-shadow: 0px 5px 20px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    /* Class card */
    .class-card {
        padding: 15px;
        border-radius: 15px;
        background: white;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD YOLO MODEL
# ============================================================

@st.cache_resource
def load_model():

    if not os.path.exists(MODEL_PATH):
        return None

    model = YOLO(MODEL_PATH)

    return model


model = load_model()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🚁 SmartLogix Drone Damage Classification</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered drone damage classification using YOLO'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# CHECK MODEL
# ============================================================

if model is None:

    st.error("❌ YOLO model was not found.")

    st.write("Expected model location:")

    st.code(MODEL_PATH)

    st.stop()


# ============================================================
# GET MODEL CLASSES
# ============================================================

model_names = model.names

if isinstance(model_names, dict):

    class_names = list(model_names.values())

else:

    class_names = list(model_names)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🚁 Model Information")

    st.success("YOLO model loaded successfully")

    st.write("### Model Classes")

    for index, class_name in enumerate(class_names):

        st.write(
            f"**{index}.** "
            f"{str(class_name).replace('_', ' ').title()}"
        )

    st.divider()

    st.write("### Model Path")

    st.caption(MODEL_PATH)

    st.divider()

    st.write("### Classification")

    st.info(
        "This model predicts the primary damage category "
        "present in the uploaded drone image."
    )


# ============================================================
# MODEL DEBUG INFORMATION
# ============================================================

with st.expander("🔍 Model Information"):

    st.write("Number of classes:", len(class_names))

    st.write("Model class mapping:")

    st.json(model_names)


# ============================================================
# IMAGE UPLOAD SECTION
# ============================================================

st.markdown("## 📤 Upload Drone Image")

uploaded_file = st.file_uploader(
    "Choose a drone image",
    type=["jpg", "jpeg", "png", "webp"],
    help="Upload a drone image for damage classification."
)


# ============================================================
# PREDICTION
# ============================================================

if uploaded_file is not None:

    # --------------------------------------------------------
    # Open uploaded image
    # --------------------------------------------------------

    image = Image.open(uploaded_file).convert("RGB")


    # --------------------------------------------------------
    # Display uploaded image
    # --------------------------------------------------------

    st.markdown("## 🖼️ Uploaded Drone Image")

    image_column, details_column = st.columns([1.3, 1])

    with image_column:

        st.image(
            image,
            caption="Uploaded Drone Image",
            use_container_width=True
        )


    with details_column:

        st.markdown(
            """
            <div class="info-card">

            <h3>📋 Image Information</h3>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write(
            "**File name:**",
            uploaded_file.name
        )

        st.write(
            "**Image width:**",
            image.width,
            "pixels"
        )

        st.write(
            "**Image height:**",
            image.height,
            "pixels"
        )

        st.write(
            "**Image format:**",
            image.format if image.format else "Unknown"
        )


    # ========================================================
    # PREDICT BUTTON
    # ========================================================

    st.markdown("---")

    predict_button = st.button(
        "🔍 Classify Drone Damage",
        type="primary",
        use_container_width=True
    )


    # ========================================================
    # RUN PREDICTION
    # ========================================================

    if predict_button:

        with st.spinner(
            "🤖 AI is analyzing the drone image..."
        ):

            try:

                # ------------------------------------------------
                # Save uploaded image temporarily
                # ------------------------------------------------

                suffix = os.path.splitext(
                    uploaded_file.name
                )[1]

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix
                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getbuffer()
                    )

                    temp_image_path = temp_file.name


                # ------------------------------------------------
                # YOLO Prediction
                # ------------------------------------------------

                results = model.predict(
                    source=temp_image_path,
                    imgsz=224,
                    verbose=False
                )


                # ------------------------------------------------
                # Get first result
                # ------------------------------------------------

                result = results[0]


                # ------------------------------------------------
                # Check classification probabilities
                # ------------------------------------------------

                if result.probs is None:

                    st.error(
                        "❌ The loaded model did not return "
                        "classification probabilities."
                    )

                    os.remove(temp_image_path)

                    st.stop()


                # ------------------------------------------------
                # Top prediction
                # ------------------------------------------------

                top_class_id = result.probs.top1

                top_confidence = (
                    result.probs.top1conf.item()
                )

                predicted_class = result.names[
                    top_class_id
                ]


                # ------------------------------------------------
                # Remove temporary image
                # ------------------------------------------------

                os.remove(temp_image_path)


                # =================================================
                # PREDICTION RESULT
                # =================================================

                st.markdown("---")

                st.markdown(
                    "## 🎯 Prediction Result"
                )


                st.markdown(
                    f"""
                    <div class="prediction-card">

                    <div class="prediction-title">
                    🔍 {str(predicted_class).replace("_", " ").title()}
                    </div>

                    <div class="confidence">
                    Confidence: {top_confidence * 100:.2f}%
                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # =================================================
                # CONFIDENCE STATUS
                # =================================================

                if top_confidence >= 0.80:

                    st.success(
                        f"✅ High confidence prediction: "
                        f"{str(predicted_class).replace('_', ' ').title()}"
                    )

                elif top_confidence >= 0.50:

                    st.warning(
                        f"⚠️ Moderate confidence prediction: "
                        f"{str(predicted_class).replace('_', ' ').title()}"
                    )

                else:

                    st.error(
                        "⚠️ Low confidence prediction. "
                        "Consider checking the image quality "
                        "or collecting more training images."
                    )


                # =================================================
                # PROBABILITIES
                # =================================================

                st.markdown("---")

                st.markdown(
                    "## 📊 Classification Probabilities"
                )


                probabilities = (
                    result.probs.data.tolist()
                )


                # ------------------------------------------------
                # IMPORTANT FIX
                # ------------------------------------------------
                # Do NOT use:
                #
                # st.columns(5)
                #
                # because the model may have a different
                # number of classes.
                #
                # We dynamically create columns based on
                # the actual number of probabilities.
                # ------------------------------------------------

                number_of_probabilities = len(
                    probabilities
                )


                st.write(
                    f"Model returned "
                    f"**{number_of_probabilities} "
                    f"class probabilities**."
                )


                # =================================================
                # DISPLAY PROBABILITIES
                # =================================================

                for index, probability in enumerate(
                    probabilities
                ):

                    # Get class name safely
                    if index in result.names:

                        class_name = result.names[index]

                    else:

                        class_name = f"Class {index}"


                    percentage = probability * 100


                    # ------------------------------------------------
                    # Class display
                    # ------------------------------------------------

                    st.markdown(
                        f"""
                        <div class="class-card">

                        <strong>
                        {str(class_name).replace("_", " ").title()}
                        </strong>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    st.progress(
                        float(probability)
                    )

                    st.caption(
                        f"{percentage:.2f}%"
                    )


                # =================================================
                # TOP 3 PREDICTIONS
                # =================================================

                st.markdown("---")

                st.markdown(
                    "## 🏆 Top Predictions"
                )


                # Create probability pairs
                probability_pairs = []

                for index, probability in enumerate(
                    probabilities
                ):

                    if index in result.names:

                        name = result.names[index]

                    else:

                        name = f"Class {index}"

                    probability_pairs.append(
                        (
                            name,
                            probability
                        )
                    )


                # Sort highest to lowest
                probability_pairs.sort(
                    key=lambda x: x[1],
                    reverse=True
                )


                # Display top 3
                top_n = min(
                    3,
                    len(probability_pairs)
                )


                for rank in range(top_n):

                    class_name, probability = (
                        probability_pairs[rank]
                    )

                    percentage = (
                        probability * 100
                    )


                    if rank == 0:

                        icon = "🥇"

                    elif rank == 1:

                        icon = "🥈"

                    else:

                        icon = "🥉"


                    col1, col2, col3 = st.columns(
                        [0.5, 3, 1]
                    )


                    with col1:

                        st.write(
                            icon
                        )


                    with col2:

                        st.write(
                            f"**{str(class_name).replace('_', ' ').title()}**"
                        )


                    with col3:

                        st.write(
                            f"**{percentage:.2f}%**"
                        )


                # =================================================
                # MODEL CLASS CHECK
                # =================================================

                st.markdown("---")

                with st.expander(
                    "🔧 Technical Prediction Details"
                ):

                    st.write(
                        "**Top Class ID:**",
                        top_class_id
                    )

                    st.write(
                        "**Top Class Name:**",
                        predicted_class
                    )

                    st.write(
                        "**Top Confidence:**",
                        f"{top_confidence:.6f}"
                    )

                    st.write(
                        "**Number of Model Classes:**",
                        len(class_names)
                    )

                    st.write(
                        "**Number of Probabilities:**",
                        len(probabilities)
                    )

                    st.write(
                        "**Model Classes:**"
                    )

                    st.json(model_names)


            except Exception as e:

                st.error(
                    "❌ Error while performing prediction."
                )

                st.exception(e)


# ============================================================
# NO IMAGE MESSAGE
# ============================================================

else:

    st.info(
        "👆 Please upload a drone image to start "
        "damage classification."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#64748b;">

    🚚 <strong>SmartLogix AI Intelligent Multi-Modal Logistics</strong>
    
    <br>
    
    Computer Vision Module | YOLO Drone Damage Classification

    </div>
    """,
    unsafe_allow_html=True
)