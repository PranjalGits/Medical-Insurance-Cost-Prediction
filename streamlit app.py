import streamlit as st
import requests
import pandas as pd
import numpy as np
import pickle

# Load the trained model
model = pickle.load(open("D:/Medical Insurance Cost Prediction/finalized_model_2.pkl", "rb"))

# Exchange rate (as of the latest data, you can update dynamically)
USD_TO_INR = 83.5  # Approximate conversion rate

def predict_charges(age, sex, bmi, children, smoker, region):
    sex_map = {'Male': 1, 'Female': 0}
    smoker_map = {'Yes': 1, 'No': 0}
    region_map = {'Northeast': 0, 'Northwest': 1, 'Southeast': 2, 'Southwest': 3}
    
    input_data = pd.DataFrame({
        'age': [age],
        'bmi': [bmi],
        'children': [children],
        'smoker': [smoker_map[smoker]]
    })
    
    prediction = model.predict(input_data)[0]
    return round(prediction, 2), round(prediction * USD_TO_INR, 2)

# Streamlit UI
def main():
    st.set_page_config(page_title="Medical Insurance Cost Predictor", layout="wide")
    st.title("💰 Advanced Medical Insurance Cost Prediction")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.slider("Select Age", 18, 100, 30)
        sex = st.radio("Select Gender", ["Male", "Female"], horizontal=True)
        bmi = st.slider("Enter BMI", 10.0, 50.0, 25.0)
        children = st.slider("Number of Children", 0, 10, 0)
    
    with col2:
        smoker = st.radio("Are you a Smoker?", ["Yes", "No"], horizontal=True)
        region = st.selectbox("Select Region", ["Northwest", "Northeast", "Southeast", "Southwest"])
        
        if st.button("📊 Predict Cost"):
            charges_usd, charges_inr = predict_charges(age, sex, bmi, children, smoker, region)
            
            st.success(f"Predicted Insurance Charges: **${charges_usd}** (~ ₹{charges_inr})")
            st.markdown("---")
            
            st.metric(label="💲 Cost in USD", value=f"${charges_usd}")
            st.metric(label="💰 Cost in INR", value=f"₹{charges_inr}")
            
            # Visualization
            st.subheader("📈 Cost Breakdown")
            data = pd.DataFrame({"Category": ["USD", "INR"], "Amount": [charges_usd, charges_inr]})
            st.bar_chart(data.set_index("Category"))
    
if __name__ == "__main__":
    main()
