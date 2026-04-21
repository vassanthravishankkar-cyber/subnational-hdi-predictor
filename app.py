import streamlit as st
import pickle
import pandas as pd

# Load model
model = pickle.load(open('model.pkl', 'rb'))

st.title("HDI Prediction App")

# Example inputs (edit based on your dataset)
feature1 = st.number_input("Feature 1")
feature2 = st.number_input("Feature 2")

# Prediction
if st.button("Predict"):
    input_data = pd.DataFrame([[feature1, feature2]],
                              columns=['Feature1','Feature2'])
    
    prediction = model.predict(input_data)
    st.success(f"Predicted HDI: {prediction[0]}")