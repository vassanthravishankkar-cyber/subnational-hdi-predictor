import streamlit as st
import pandas as pd
import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))

st.title("HDI Prediction App")

features = list(model.feature_names_in_)

# 👉 Separate columns
year_cols = [f for f in features if f.isdigit()]
region_cols = [f for f in features if not f.isdigit()]

# -------------------------------
# 🎯 YEAR INPUT (RANGE BASED)
# -------------------------------
st.markdown("### Select Year Range")

start_year, end_year = st.slider(
    "Year Range",
    min_value=int(min(year_cols)),
    max_value=int(max(year_cols)),
    value=(1995, 2000)
)

range_value = st.slider("HDI for selected range", 0.0, 1.0, 0.5)
default_value = st.slider("Default for other years", 0.0, 1.0, 0.5)

# -------------------------------
# 🌍 REGION SELECTION
# -------------------------------
st.markdown("### Select Region")

selected_region = st.selectbox(
    "Region",
    [r.replace("Region_", "") for r in region_cols]
)

# -------------------------------
# 🔧 BUILD INPUT
# -------------------------------
input_data = {}

# Fill years
for year in year_cols:
    y = int(year)
    if start_year <= y <= end_year:
        input_data[year] = range_value
    else:
        input_data[year] = default_value

# Fill regions (one-hot encoding)
for r in region_cols:
    input_data[r] = 1 if r == f"Region_{selected_region}" else 0

# Convert
input_df = pd.DataFrame([input_data])

# Ensure correct order
input_df = input_df[features]

# -------------------------------
# 🚀 PREDICT
# -------------------------------
if st.button("Predict"):
    prediction = model.predict(input_df)
    st.success(f"Predicted Value: {prediction[0]:.3f}")
