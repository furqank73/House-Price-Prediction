import streamlit as st
import joblib
import pandas as pd
import numpy as np
from datetime import datetime

# Configure page settings
st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: none;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    div.block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .title-text {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(45deg, #2193b0, #6dd5ed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
    .custom-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Load the trained model
@st.cache_resource
def load_model():
    return joblib.load('house_price_model.pkl')

pipeline = load_model()

# Data
cities = ['Algona', 'Auburn', 'Beaux Arts Village', 'Bellevue', 'Black Diamond', 
         'Bothell', 'Burien', 'Carnation', 'Clyde Hill', 'Covington', 'Des Moines',
         'Duvall', 'Enumclaw', 'Fall City', 'Federal Way', 'Issaquah', 'Kenmore',
         'Kent', 'Kirkland', 'Lake Forest Park', 'Maple Valley', 'Medina',
         'Mercer Island', 'Milton', 'Newcastle', 'Normandy Park', 'North Bend',
         'Pacific', 'Preston', 'Ravensdale', 'Redmond', 'Renton', 'Sammamish',
         'SeaTac', 'Seattle', 'Shoreline', 'Snoqualmie', 'Snoqualmie Pass',
         'Tukwila', 'Vashon', 'Woodinville', 'Yarrow Point']

renovation_status = ['Never_Renovated', 'Renovated']
basement_status = ['Has_Basement', 'No_Basement']

# Title with custom styling
st.markdown('<h1 class="title-text">House Price Prediction</h1>', unsafe_allow_html=True)
st.markdown("""
    <div style='background-color: #f0f8ff; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem;'>
        Predict house prices accurately using our advanced machine learning model. 
        Enter your property details below to get an instant estimation.
    </div>
""", unsafe_allow_html=True)

# Main form
with st.form('prediction_form'):
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.subheader('📊 Basic Property Information')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        bedrooms = st.number_input('🛏️ Bedrooms', min_value=1, max_value=10, value=3)
        bathrooms = st.number_input('🚿 Bathrooms', min_value=1.0, max_value=6.0, value=2.0, step=0.5)
        sqft_living = st.number_input('🏠 Living Area (sqft)', min_value=500, max_value=10000, value=2000)
    
    with col2:
        sqft_lot = st.number_input('🌳 Lot Area (sqft)', min_value=500, max_value=50000, value=5000)
        floors = st.number_input('⬆️ Floors', min_value=1, max_value=3, value=1)
        waterfront = st.selectbox('🌊 Waterfront Property', [0, 1], format_func=lambda x: 'Yes' if x else 'No')
    
    with col3:
        view = st.number_input('👀 View Rating (0-4)', min_value=0, max_value=4, value=0)
        condition = st.number_input('🏗️ Condition Rating (1-5)', min_value=1, max_value=5, value=3)
        sqft_above = st.number_input('📏 Above Ground Sqft', min_value=500, max_value=10000, value=2000)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.subheader('🏗️ Property Details')
    
    col4, col5 = st.columns(2)
    
    with col4:
        yr_built = st.number_input('📅 Year Built', 
                                  min_value=1900, 
                                  max_value=datetime.now().year, 
                                  value=1990)
        renovation_age = st.slider('🔨 Renovation Age', 
                                 min_value=0, 
                                 max_value=100, 
                                 value=30)
    
    with col5:
        price_per_sqft = st.number_input('💰 Price per Sqft ($)', 
                                        min_value=100, 
                                        max_value=1000, 
                                        value=300)
        city = st.selectbox('🌆 City', cities)
    
    col6, col7 = st.columns(2)
    
    with col6:
        renovation_status_sel = st.selectbox('🔧 Renovation Status', renovation_status)
    
    with col7:
        basement_status_sel = st.selectbox('🏚️ Basement Status', basement_status)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    submitted = st.form_submit_button('Calculate Price Prediction')

if submitted:
    # Create input DataFrame
    input_data = pd.DataFrame([[bedrooms, bathrooms, sqft_living, sqft_lot, floors,
                              waterfront, view, condition, sqft_above, yr_built,
                              renovation_age, price_per_sqft, city, renovation_status_sel,
                              basement_status_sel]],
                             columns=['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot',
                                     'floors', 'waterfront', 'view', 'condition', 'sqft_above',
                                     'yr_built', 'renovation_age', 'price_per_sqft', 'city',
                                     'renovation_status', 'basement_status'])
    
    # Make prediction with error handling
    try:
        prediction = pipeline.predict(input_data)[0]
        
        # Display prediction in a styled card
        st.markdown("""
            <div style='background: linear-gradient(135deg, #00b09b, #96c93d);
                        padding: 2rem;
                        border-radius: 1rem;
                        text-align: center;
                        margin-top: 2rem;'>
                <h2 style='color: white; margin-bottom: 1rem;'>Predicted House Price</h2>
                <h1 style='color: white; font-size: 3rem;'>${:,.2f}</h1>
            </div>
        """.format(prediction), unsafe_allow_html=True)
        
        # Display key metrics
        st.markdown("<h3 style='margin-top: 2rem;'>Key Property Metrics</h3>", unsafe_allow_html=True)
        col8, col9, col10 = st.columns(3)
        
        with col8:
            st.markdown("""
                <div class="metric-card">
                    <h4>Price per Sqft</h4>
                    <h2>${:,.2f}</h2>
                </div>
            """.format(price_per_sqft), unsafe_allow_html=True)
            
        with col9:
            st.markdown("""
                <div class="metric-card">
                    <h4>Total Living Area</h4>
                    <h2>{:,} sqft</h2>
                </div>
            """.format(sqft_living), unsafe_allow_html=True)
            
        with col10:
            st.markdown("""
                <div class="metric-card">
                    <h4>Property Age</h4>
                    <h2>{} years</h2>
                </div>
            """.format(datetime.now().year - yr_built), unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f'An error occurred during prediction: {str(e)}')
        st.markdown("""
            <div style='background-color: #ffe5e5; 
                        padding: 1rem; 
                        border-radius: 0.5rem; 
                        border-left: 5px solid #ff0000;'>
                Please check your input values and try again.
            </div>
        """, unsafe_allow_html=True)

# Footer with personal information
st.markdown("""
    <div style='text-align: center; padding: 2rem; color: #666;'>
        <p><strong>M Furqan Khan</strong></p>
        <p>GitHub: <a href="https://github.com/furqank73" target="_blank">https://github.com/furqank73</a></p>
        <p>Kaggle: <a href="https://www.kaggle.com/fkgaming" target="_blank">https://www.kaggle.com/fkgaming</a></p>
        <p>LinkedIn: <a href="https://www.linkedin.com/in/furqan-khan-256798268/" target="_blank">https://www.linkedin.com/in/furqan-khan-256798268/</a></p>
    </div>
""", unsafe_allow_html=True)