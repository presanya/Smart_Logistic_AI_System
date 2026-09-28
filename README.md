# Smart_Logistic_AI_System

# 🚚 SmartLogix AI – Intelligent Multi-Modal Logistics

> **AI-powered logistics platform for intelligent transportation selection, route optimization, delivery ETA prediction, predictive maintenance, payload optimization, and customer delivery management.**

## 📌 Project Overview

**SmartLogix AI** is an intelligent logistics management platform designed to improve transportation and delivery operations using **Artificial Intelligence, Machine Learning, NLP, Computer Vision, PostgreSQL, and Streamlit**.

The system provides separate experiences for **Customers** and **Employees**.

### 👤 Customer

Customers can:

- Login using Customer ID and phone number
- View customer account information
- View customer name, email, and phone number
- Select delivery location
- Browse and search products
- Get intelligent product recommendations
- Add products to cart
- Track orders and delivery information
- Compare products
- Get product recommendations
- Ask questions through an AI chatbot
- View FAQs, return policy, delivery information, and cancellation information

### 👨‍💼 Employee

Employees can access:

- 📊 Logistics Dashboard
- 📦 Order Management
- 🚚 Intelligent Transport Selection
- 🗺️ Route Optimization
- ⏱️ Delivery ETA Prediction
- 🔧 Predictive Vehicle Maintenance
- 📦 Payload Optimization
- 📅 Delivery Scheduling
- 🚁 Drone Monitoring
- 🖼️ Drone Damage Detection
- 📈 Logistics Analytics

---

## 🎯 Project Objectives

1. Automate transportation mode selection.
2. Optimize delivery routes.
3. Predict delivery arrival time.
4. Predict potential vehicle failures.
5. Optimize vehicle selection based on payload.
6. Monitor drone telemetry.
7. Detect drone damage using computer vision.
8. Provide intelligent product recommendations.
9. Provide an AI-powered customer chatbot.
10. Store and manage logistics data using PostgreSQL.
11. Provide an interactive Streamlit application.

---

## 🏗️ System Architecture

```text
                         ┌─────────────────────────┐
                         │       SmartLogix AI     │
                         │   Intelligent Logistics │
                         └────────────┬────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
             ┌──────▼──────┐                    ┌──────▼──────┐
             │   Customer   │                    │  Employee   │
             │    Portal    │                    │   Portal    │
             └──────┬──────┘                    └──────┬──────┘
                    │                                   │
          ┌─────────┼─────────┐              ┌──────────┼───────────┐
          │         │         │              │          │           │
       Products   Orders    Chatbot       Transport   Route       ETA
          │         │         │              │          │           │
          └─────────┴─────────┘              ├──────────┼───────────┐
                                             │          │           │
                                        Maintenance  Payload     Scheduling
                                             │          │           │
                                             └──────────┴───────────┘
                                                        │
                                               ┌────────▼────────┐
                                               │ Machine Learning │
                                               │   Models / CV    │
                                               └────────┬─────────┘
                                                        │
                                               ┌────────▼────────┐
                                               │   PostgreSQL     │
                                               │    Database      │
                                               └─────────────────┘
```

---

# 🧩 Main Modules

## 1. 🔐 Login & Authentication

SmartLogix provides role-based authentication.

### Customer Login

Customers login using:

```text
Customer ID
+
Phone Number
```

After successful authentication, the system retrieves:

- Customer ID
- Customer Name
- Email
- Phone Number
- Delivery Location

### Employee Login

Employees can access employee-specific logistics features.

---

## 2. 📊 Logistics Dashboard

The dashboard provides an overview of logistics operations.

Example metrics:

- Total Orders
- Total Vehicles
- Total Customers
- Total Deliveries
- Delivery Performance
- Vehicle Status
- Transportation Distribution

The dashboard retrieves operational information from PostgreSQL.

---

## 3. 🚚 Intelligent Transport Selection

The Transport Selection module recommends a suitable transportation mode for an order.

### Transportation Modes

```text
Truck
Bike
Van
Drone
Air Cargo
Ship
```

### Example Input Features

```text
Quantity
Distance
Package Weight
Fragile
Hazmat
Cold Chain
Priority
Order Value
Weather
Promised ETA
Origin City
Destination City
```

### Machine Learning Model

```text
RandomForestClassifier
```

### Workflow

```text
Raw Data
   ↓
Data Cleaning
   ↓
Feature Engineering
   ↓
Categorical Encoding
   ↓
Feature Scaling
   ↓
Train/Test Split
   ↓
Random Forest Classifier
   ↓
Transport Prediction
```

---

## 4. 🗺️ Route Optimization

The Route Optimization module helps identify and visualize delivery routes.

The system uses:

- Order information
- Hub information
- GPS route data
- Origin location
- Destination location
- Distance
- Vehicle information

### Features

- Select origin hub
- Display geographically relevant orders
- Display delivery routes
- Display GPS waypoints
- View vehicle route
- View route distance
- View fuel consumption
- Interactive map visualization

### Mapping Technology

```text
Folium
streamlit-folium
```

---

## 5. ⏱️ Delivery ETA Prediction

The ETA module predicts expected delivery duration.

### Target Variable

```text
actual_delivery_hours
```

### Features

```text
transport_mode
delivery_priority
weather_condition_at_dest
distance_km
origin_city
destination_city
order_value_inr
promised_eta_hours
```

### Preprocessing

Categorical features:

```text
OneHotEncoder
```

Ordinal features:

```text
OrdinalEncoder
```

Numerical features:

```text
StandardScaler
```

### Model

```text
Linear Regression
```

### Saved Model

```text
delivery_edt_linearRegression_model.pkl
```

---

## 6. 🔧 Predictive Vehicle Maintenance

The Predictive Maintenance module predicts whether a vehicle may report a failure.

### Features

```text
capacity_kg
max_range_km
avg_speed_kmph
odometer_km
vehicle_age_years
days_since_last_service
service_type
parts_replaced
model_name
vehicle_type
hub_code
fleet_status
```

### Target

```text
failure_reported
```

### Machine Learning Model

```text
RandomForestClassifier
```

### Preprocessing

Numerical features:

```text
MinMaxScaler
```

Categorical features:

```text
OneHotEncoder
handle_unknown = "ignore"
```

### Saved Model

```text
maintance_required_randomforest_classifier_model.pkl
```

---

## 7. 📦 Payload Optimization

Payload Optimization identifies a suitable vehicle for an order.

The system considers:

- Order weight
- Vehicle capacity
- Vehicle type
- Vehicle availability
- Vehicle range
- Vehicle characteristics

### Supported Vehicle Types

```text
Truck
Van
Bike
Drone
Air Cargo
Ship
```

### Data Sources

```text
Orders
Fleet Vehicles
Drone Telemetry
```

---

## 8. 📅 Delivery Scheduling

The Delivery Scheduling module helps employees manage delivery schedules.

Features:

- Create delivery schedules
- Select orders
- Select vehicles
- Assign delivery dates
- Assign delivery times
- Save schedules
- View saved schedules

Scheduling information is stored and retrieved using PostgreSQL.

---

## 9. 🚁 Drone Monitoring

SmartLogix includes drone telemetry monitoring.

### Drone Telemetry Features

```text
flight_id
battery
motor_temp_c
vibration_rms
payload_kg
wind
GPS
rotor_rpm
error_codes
maintenance_required
```

The system supports:

- Drone health monitoring
- Battery monitoring
- Motor monitoring
- Vibration analysis
- Payload analysis
- Maintenance prediction
- Error detection

---

## 10. 🖼️ Drone Damage Detection

SmartLogix includes a YOLO-based Computer Vision module for identifying drone damage.

### Detection Categories

```text
Healthy Drone
Damaged Drone
Frame Damage
Motor Damage
Broken Propeller
Battery Damage
```

### Workflow

```text
Drone Image
     ↓
Image Dataset
     ↓
Annotation
     ↓
Train / Validation / Test
     ↓
YOLO Model
     ↓
Object Detection
     ↓
Damage Classification
```

---

## 11. 🛍️ Customer Product Management

Customers can browse products through the SmartLogix customer portal.

### Product Information

```text
product_id
product_name
category
sub_category
is_fragile
is_hazmat
requires_cold_chain
stock_qty
rating
tags
launch_date
specs
price
```

Customers can:

- Search products
- View product details
- View product images
- View prices
- Compare products
- Add products to cart
- Receive recommendations

---

## 12. 🤖 AI Product Recommendation

The recommendation system uses:

```text
TF-IDF
+
Cosine Similarity
```

### Workflow

```text
Product Information
       ↓
Text Processing
       ↓
TF-IDF Vectorization
       ↓
Cosine Similarity
       ↓
Similar Products
       ↓
Top Recommendations
```

---

## 13. 💬 AI Customer Chatbot

The customer portal includes an AI-powered chatbot.

### Supported Questions

#### Order Questions

```text
Where is my order?
Track my order
When will my order arrive?
```

#### Product Questions

```text
Compare products
Recommend a product
Summarize reviews
Tell me about this product
```

#### FAQ

```text
Return policy
Delivery time
Cancel order
Track order
```

### RAG Workflow

```text
Customer Question
       ↓
Text Processing
       ↓
Relevant Data Retrieval
       ↓
Product / Order / FAQ Data
       ↓
Context
       ↓
Gemini LLM
       ↓
Final Response
```

---

# 🗄️ PostgreSQL Database

SmartLogix uses **PostgreSQL** as the primary database.

### Database

```text
smartlogistic_db
```

Example SQLAlchemy connection:

```python
DATABASE = "smartlogistic_db"

DATABASE_URL = (
    f"postgresql://postgres:<password>@localhost:5432/{DATABASE}"
)
```

> Store database credentials in environment variables in production instead of committing them to source code.

### Main Tables

```text
customers
orders
product
fleet_vehicles
drone_telemetry
delivery_log
```

---

# 🔄 Database Workflow

```text
CSV / Dataset
      ↓
Data Cleaning
      ↓
Data Validation
      ↓
PostgreSQL
      ↓
SQLAlchemy
      ↓
Streamlit Application
      ↓
Dashboard / ML Modules
```

---

# 🧹 Data Cleaning

Data preprocessing includes:

- Missing-value handling
- Duplicate removal
- Data type correction
- Column standardization
- Categorical value cleaning
- Numerical value cleaning
- Outlier handling
- Feature engineering
- Invalid-value correction

Example:

```python
df.columns = df.columns.str.strip().str.lower()
```

---

# 🧠 Machine Learning Models

| Module | Model / Technique |
|---|---|
| Transport Selection | Random Forest Classifier |
| ETA Prediction | Linear Regression |
| Predictive Maintenance | Random Forest Classifier |
| Product Recommendation | TF-IDF + Cosine Similarity |
| Drone Damage Detection | YOLO |
| Route Optimization | GPS / Geospatial Processing |
| Payload Optimization | Vehicle selection / optimization |
| Customer Chatbot | RAG + Gemini |

---

# 🛠️ Technology Stack

### Programming

```text
Python
```

### Frontend

```text
Streamlit
HTML
CSS
```

### Database

```text
PostgreSQL
```

### Data Processing

```text
Pandas
NumPy
```

### Visualization
Matplotlib
Seaborn
Plotly

### Machine Learning

Scikit-learn


### NLP

```text
NLTK
TF-IDF
Cosine Similarity
```

### Computer Vision

```text
YOLO
OpenCV
```

### Mapping

```text
Folium
streamlit-folium
```

### Database Connectivity

```text
SQLAlchemy
psycopg2
```

### Generative AI

```text
Gemini

# 📁 Project Structure

```text
SmartLogix AI_Intelligent_Multi_Modal_Logistics/
│
├── app.py
│
├── pages/
│   ├── employee_features.py
│   ├── customer_page.py
│   ├── Delivery_scheduling_page.py
│   ├── route_optimization.py
│   ├── transport_selection.py
│   ├── predictive_maintenance.py
│   ├── payload_optimization.py
│   └── ...
│
├── models/
│   ├── pipeline.pkl
│   ├── delivery_edt_linearRegression_model.pkl
│   ├── maintance_required_randomforest_classifier_model.pkl
│   └── ...
│
├── data/
│   ├── orders_with_hub.csv
│   ├── fleet_vehicles.csv
│   ├── drone_telemetry.csv
│   ├── product.csv
│   ├── delivery_log_cleaned.csv
│   └── ...
│
├── images/
│   └── product images
│
├── drone_dataset/
│   ├── healthy/
│   ├── damaged/
│   ├── frame_damage/
│   ├── motor_damage/
│   └── battery_damage/
│
├── notebooks/
│   ├── EDA
│   ├── Data Cleaning
│   ├── Model Training
│   └── Model Evaluation
│
├── .env
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🔬 Machine Learning Workflow

```text
Dataset
   ↓
Data Exploration
   ↓
Data Cleaning
   ↓
Feature Engineering
   ↓
Train/Test Split
   ↓
Preprocessing
   ↓
Model Training
   ↓
Model Evaluation
   ↓
Model Saving
   ↓
Streamlit Integration
   ↓
User Prediction
```

---

# 📊 Model Evaluation

## Classification Models

For Transport Selection and Predictive Maintenance


# 🔐 Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=your_database_connection_string
```

Python:

```python
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
```

Add `.env` to `.gitignore`:

```text
.env
.venv/
__pycache__/
*.pyc
```

---

# ⚙️ Installation

## Step 1 – Clone the Repository

```bash
git clone <your-github-repository-url>
cd SmartLogix-AI
```

## Step 2 – Create Virtual Environment

```bash
python -m venv .venv
```

Activate on Windows:

```bash
.venv\Scripts\activate
```

## Step 3 – Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄️ PostgreSQL Setup

Create the database:

```sql
CREATE DATABASE smartlogistic_db;
```

Create/load the required tables:

```text
customers
orders
product
fleet_vehicles
drone_telemetry
delivery_log
```

---

# ▶️ Run the Application

Start Streamlit:

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:
```

---

# 👤 Customer Workflow

```text
Customer
   ↓
Login
   ↓
Customer ID + Phone Number
   ↓
Validate Customer
   ↓
Customer Account
   ↓
View Name / Email / Phone
   ↓
Choose Delivery Location
   ↓
Browse Products
   ↓
Search / Recommendation
   ↓
Add to Cart
   ↓
Place Order
   ↓
Track Delivery
   ↓
AI Chatbot
```

---

# 👨‍💼 Employee Workflow

```text
Employee Login
      ↓
Employee Portal
      ↓
Logistics Dashboard
      ↓
Choose Module
      │
      ├── Transport Selection
      ├── Route Optimization
      ├── ETA Prediction
      ├── Predictive Maintenance
      ├── Payload Optimization
      ├── Delivery Scheduling
      └── Drone Monitoring
```

---

# 📈 Business Use Cases

### 🚚 Transportation

Select a suitable transportation mode based on order characteristics.

### ⏱️ Delivery Planning

Predict estimated delivery duration.

### 🔧 Fleet Management

Identify vehicles that may require maintenance.

### 📦 Vehicle Utilization

Select suitable vehicles according to payload requirements.

### 🗺️ Route Management

Visualize delivery routes and GPS information.

### 🤖 Customer Support

Provide automated customer assistance using an AI chatbot.

### 🛍️ Personalized Shopping

Recommend relevant products using similarity-based recommendations.

---

# 🚀 Future Enhancements

- Real-time GPS tracking
- Real-time traffic API integration
- Advanced graph-based route optimization
- Deep learning ETA prediction
- Real-time vehicle telemetry streaming
- Automated vehicle assignment
- Advanced drone fleet management
- Real-time drone damage alerts
- Demand forecasting
- Warehouse optimization
- Dynamic delivery pricing
- Advanced customer personalization
- Voice-enabled logistics assistant
- Cloud deployment
- Docker containerization
- CI/CD pipeline
- Model monitoring and automatic retraining

---

# 📌 Key Project Highlights

```text
✅ End-to-End AI Logistics Platform
✅ Multi-Modal Transportation
✅ Machine Learning
✅ Predictive Maintenance
✅ ETA Prediction
✅ Route Optimization
✅ Payload Optimization
✅ Drone Monitoring
✅ YOLO Computer Vision
✅ Product Recommendation
✅ NLP / RAG Chatbot
✅ PostgreSQL Database
✅ Streamlit Application
✅ Customer Portal
✅ Employee Portal
✅ Role-Based Workflow
```

---

# ⭐ Project Summary

**SmartLogix AI** combines data engineering, machine learning, NLP, computer vision, generative AI, PostgreSQL, and Streamlit into a single intelligent logistics platform.

```text
Customer
   ↓
Product
   ↓
Order
   ↓
Transport
   ↓
Vehicle
   ↓
Route
   ↓
ETA
   ↓
Delivery
   ↓
Tracking
```


The overall goal is to provide a unified, data-driven logistics management solution using modern AI and data-science technologies.
