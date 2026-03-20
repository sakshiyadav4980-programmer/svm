import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler

# Title of the Streamlit app
st.set_page_config(page_title="Position Salary Predictor (SVR)", layout="centered")
st.title("Position Salary Predictor using SVR")
st.markdown("Predict the expected salary for a given position level.")

# Load Data
@st.cache_data
def load_data():
    dataset = pd.read_csv('Position_Salaries.csv')
    return dataset

dataset = load_data()

st.subheader("Dataset Preview")
st.write(dataset)

# Splitting feature and target
X = dataset.iloc[:, 1:-1].values  # Level
y = dataset.iloc[:, -1].values    # Salary
y = y.reshape(len(y), 1)

# Feature Scaling
sc_X = StandardScaler()
sc_y = StandardScaler()
X_scaled = sc_X.fit_transform(X)
y_scaled = sc_y.fit_transform(y)

# Training the SVR model
regressor = SVR(kernel='rbf')
regressor.fit(X_scaled, y_scaled.ravel())

st.markdown("---")
st.subheader("Predict Salary")

# User Input for Prediction
position_level = st.number_input(
    "Enter Position Level (e.g., 1-10):", min_value=1.0, max_value=10.0, value=6.5, step=0.1
)

if st.button("Predict"):
    # Predict continuous value 
    scaled_prediction = regressor.predict(sc_X.transform([[position_level]]))
    predicted_salary = sc_y.inverse_transform(scaled_prediction.reshape(-1, 1))[0][0]
    
    st.success(f"The predicted salary for level {position_level} is **${predicted_salary:,.2f}**")

st.markdown("---")
st.subheader("SVR Regression Results Visualization")

# Visualizing the SVR results
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(sc_X.inverse_transform(X_scaled), sc_y.inverse_transform(y_scaled), color='red', label='Actual Data')
ax.plot(sc_X.inverse_transform(X_scaled), sc_y.inverse_transform(regressor.predict(X_scaled).reshape(-1, 1)), color='blue', label='SVR Prediction')
ax.set_title('Truth or Bluff (SVR)')
ax.set_xlabel('Position Level')
ax.set_ylabel('Salary')
ax.legend()
st.pyplot(fig)

# SVR Regression curve (high resolution and smoother)
st.subheader("SVR Regression Curve (High Resolution)")
fig2, ax2 = plt.subplots(figsize=(8, 5))
X_grid = np.arange(min(sc_X.inverse_transform(X_scaled)), max(sc_X.inverse_transform(X_scaled)), 0.1)
X_grid = X_grid.reshape((len(X_grid), 1))
ax2.scatter(sc_X.inverse_transform(X_scaled), sc_y.inverse_transform(y_scaled), color='red', label='Actual Data')
ax2.plot(X_grid, sc_y.inverse_transform(regressor.predict(sc_X.transform(X_grid)).reshape(-1, 1)), color='blue', label='SVR Smooth Curve')
ax2.set_title('Truth or Bluff (SVR Smoothed)')
ax2.set_xlabel('Position Level')
ax2.set_ylabel('Salary')
ax2.legend()
st.pyplot(fig2)
