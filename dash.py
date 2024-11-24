import pyrebase
import streamlit as st
import time
from datetime import datetime

# Firebase configuration
config = {
   "apiKey": "AIzaSyCPJkx4VP3JcATqa2RlEm2nMNp8v0Gw4Jc",
   "authDomain": "smart-bin-afa36.firebaseapp.com",
   "databaseURL": "https://smart-bin-afa36-default-rtdb.asia-southeast1.firebasedatabase.app",
   "projectId": "smart-bin-afa36",
   "storageBucket": "smart-bin-afa36.firebasestorage.app",
   "messagingSenderId": "110976262212",
   "appId": "1:110976262212:web:d5334ae8b3daae064adc11",
   "measurementId": "G-MXWE4GLHS3"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
database = firebase.database()

# Streamlit page settings
st.set_page_config(page_title="Dynamic Disturbance Structure", layout="wide")

# Styling
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #83a4d4, #b6fbff);
        color: #333333;
        font-family: Arial, sans-serif;
    }
    .centered-header {
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        color: #ff4500;
        text-shadow: 1px 1px 2px #000000;
    }
    .sensor-title {
        text-align: center;
        font-size: 1.5rem;
        color: #333;
        font-weight: bold;
    }
    .sensor-block {
        text-align: center;
        padding: 10px;
        background-color: #ffffff;
        border-radius: 15px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display time and date in the center of the page
def get_current_time():
    now = datetime.now()
    return now.strftime("%A, %B %d, %Y | %I:%M:%S %p")

placeholder_time = st.empty()

# Dynamic header with time and date
with placeholder_time.container():
    current_time = get_current_time()
    st.markdown(f"<div class='centered-header'>{current_time}</div>", unsafe_allow_html=True)

# Title and Description
st.markdown(
    """
    <div style="text-align: center; margin-top: 20px;">
        <h1 style="color: #333333; font-weight: bold;">Dynamic Disturbance Structure Dashboard</h1>
        <p style="font-size: 1.2rem; color: #555555; margin-bottom: 30px;">
            Real-time visualization of disturbance levels represented as colorful blocks. Each bar represents 2% of disturbance level.
        </p>
        <hr style="border: 1px solid #ccc; width: 60%; margin: 0 auto; margin-bottom: 40px;">
    </div>
    """,
    unsafe_allow_html=True,
)
# Create placeholders for real-time updates
placeholder = st.empty()
# Function to fetch sensor data from Firebase
def get_sensor_data():
    try:
        data = database.child("Ultrasonic_Sensor").get()
        if data.val():
            sensor_1 = data.val().get("Sensor1", 2)  # Default to 2
            sensor_2 = data.val().get("Sensor2", 2)  # Default to 2
            # Ensure values are within the range 2 to 300
            return max(2, min(300, int(sensor_1))), max(2, min(300, int(sensor_2)))
        else:
            return 2, 2  # Default values if no data found
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return 2,c
# Function to determine color based on disturbance
def get_color(disturbance):
    if disturbance <= 100:
        return "#32CD32"  # Green for low disturbance
    elif disturbance <= 200:
        return "#FFD700"  # Yellow for medium disturbance
    else:
        return "#FF4500"  # Red for high disturbance

# Function to render structure as blocks
def render_structure(disturbance, color):
    # Determine the number of bars (up to 5), each representing 60 units
    bars = min(5, (disturbance - 2) // 60 + 1)
    structure = ""
    for _ in range(bars):
        structure += f"""
        <div style="background-color:{color}; width:100px; height:20px; margin:4px auto; border-radius:5px; box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);"></div>
        """
    return structure

# Main loop for real-time updates
while True:
    # Fetch real-time data from Firebase
    disturbance_sensor_1, disturbance_sensor_2 = get_sensor_data()

    # Determine colors for each sensor
    color_1 = get_color(disturbance_sensor_1)
    color_2 = get_color(disturbance_sensor_2)

    # Update visualization dynamically
    with placeholder.container():
        col1, col2, col3, col4 = st.columns(4)

        # Sensor 1 visualization
        with col2:
            st.markdown("<div class='sensor-title'>Distbin 1</div>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class='sensor-block'>
                    {render_structure(disturbance_sensor_1, color_1)}
                    
                        {disturbance_sensor_1}
                
                """,
                unsafe_allow_html=True,
            )

        # Sensor 2 visualization
        with col3:
            st.markdown("<div class='sensor-title'>Distbin 2</div>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class='sensor-block'>
                    {render_structure(disturbance_sensor_2, color_2)}
                   
                        {disturbance_sensor_2}
                  
                """,
                unsafe_allow_html=True,
            )

    # Update time dynamically
    current_time = get_current_time()
    placeholder_time.empty()
    with placeholder_time.container():
        st.markdown(f"<div class='centered-header'>{current_time}</div>", unsafe_allow_html=True)

    # Add a delay for real-time updates
    time.sleep(2)
