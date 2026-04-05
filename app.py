import streamlit as st
from src.pipeline.predict_pipeline import PredictPipeline

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="T20 Score Predictor", layout="centered")

st.title("🏏 T20 First Innings Score Predictor")

# -----------------------------
# Load Pipeline
# -----------------------------
pipeline = PredictPipeline()

# -----------------------------
# Teams & Cities
# -----------------------------
teams = ["India",
    "Pakistan", "New Zealand", "South Africa",
    "West Indies", "Sri Lanka", "Bangladesh",
    "Zimbabwe", "England", "Australia"
]

cities = [
    'Melbourne', 'Adelaide', 'Harare', 'Napier', 'Mount Maunganui',
       'Auckland', 'Southampton', 'Cardiff', 'Chester-le-Street',
       'Nagpur', 'Bangalore', 'Lauderhill', 'Dubai', 'Abu Dhabi',
       'Sydney', 'Hobart', 'Wellington', 'Hamilton', 'Barbados',
       'Trinidad', 'Colombo', 'Birmingham', 'Manchester', 'Bristol',
       'Delhi', 'Rajkot', 'Lahore', 'Johannesburg', 'Centurion',
       'Cape Town', 'Mumbai', 'Dhaka', 'Sylhet', 'Karachi', 'Brisbane',
       'Kolkata', 'Gros Islet', 'Basseterre', 'Canberra', 'Perth',
       'Durban', 'Chandigarh', 'Christchurch', 'Providence', 'Kandy',
       'Chattogram', 'Pune', 'Rawalpindi', 'Nottingham', 'Ahmedabad',
       'Bridgetown', "St George's", 'Sharjah', 'Tarouba', 'Kingston',
       'London', 'Dambulla', 'St Lucia', 'Pallekele', 'Mirpur',
       'Hambantota', 'Chittagong'
]  

# -----------------------------
# User Inputs
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox("Batting Team", teams)

with col2:
    bowling_team = st.selectbox("Bowling Team", teams)

city = st.selectbox("City", cities)

current_score = st.number_input("Current Score", min_value=0, max_value=300, value=50)

balls_left = st.number_input("Balls Left", min_value=0, max_value=120, value=60)

wickets_left = st.number_input("Wickets Left", min_value=0, max_value=10, value=8)

last_five_overs_runs = st.number_input(
    "Runs in Last 5 Overs", min_value=0, max_value=100, value=30
)

# -----------------------------
# Derived Feature (CRR)
# -----------------------------
if balls_left != 120:
    overs_completed = (120 - balls_left) / 6
    crr = current_score / overs_completed if overs_completed > 0 else 0
else:
    crr = 0

st.write(f"📊 Current Run Rate (CRR): **{round(crr,2)}**")

# -----------------------------
# Prediction Button
# -----------------------------
if st.button("Predict Final Score"):

    # Validation
    if batting_team == bowling_team:
        st.error("Batting and Bowling teams must be different!")
    else:
        input_data = {
            "batting_team": batting_team,
            "bowling_team": bowling_team,
            "city": city,
            "current_score": current_score,
            "balls_left": balls_left,
            "wickets_left": wickets_left,
            "crr": crr,
            "last_five_overs_runs": last_five_overs_runs
        }

        try:
            prediction = pipeline.predict(input_data)

            st.success(f"🏆 Predicted Final Score: {int(prediction)}")

        except Exception as e:
            st.error(f"Error: {str(e)}")