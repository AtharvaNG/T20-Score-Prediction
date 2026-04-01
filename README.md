# 🏏 T20 Cricket Score Predictor

An end-to-end Machine Learning project that predicts the **final first-innings score in T20 cricket matches** based on the current match situation.

---

## 🚀 Overview

This project uses historical **ball-by-ball T20 match data (4,800+ matches)** to train a model that predicts the final score of the batting team during the first innings.

The system takes real-time match inputs such as:
- Current score
- Balls remaining
- Wickets left
- Recent performance (last 5 overs)

and predicts the expected final total.

---

## 📊 Dataset

- Source: Cricsheet (Kaggle)
- Format: YAML → Converted to structured DataFrame
- Matches: **4,800+**
- Rows after processing: **~78,000+ ball-by-ball entries**

---

## 🧠 Features Used

- Batting Team
- Bowling Team
- City (Venue)
- Current Score
- Balls Left
- Wickets Left
- Current Run Rate (CRR)
- Last 5 Overs Runs (Momentum)

---

## ⚙️ Machine Learning Pipeline

### 1. Data Ingestion
- Parsed YAML files into structured tabular format
- Assigned unique `match_id` to each match

### 2. Data Preprocessing
- Filtered only T20 matches
- Extracted ball-by-ball data
- Removed irrelevant matches and teams

### 3. Feature Engineering
- Calculated:
  - Cumulative score
  - Wickets remaining
  - Balls remaining
  - Current Run Rate (CRR)
  - Last 5 overs runs (momentum)
- Removed low-frequency cities (noise reduction)

### 4. Data Transformation
- OneHotEncoding for categorical features
- StandardScaler for numerical features
- Train-Test Split (80-20)

### 5. Model Training
- Model: **XGBoost Regressor**
- Performance:
  - **R² Score: ~0.86**
  - **MAE: ~8 runs**

### 6. Prediction Pipeline
- Loads trained model & preprocessor
- Applies transformations
- Returns predicted final score

---

## 🖥️ Tech Stack

- **Language**: Python
- **Libraries**: Pandas, NumPy, Scikit-learn, XGBoost
- **Visualization/UI**: Streamlit
- **Deployment**: Render
- **Version Control**: Git, GitHub

---

## 📁 Project Structure
```
project_root/
│
├── artifacts/
│   ├── ball_by_ball.pkl
│   ├── feature_df.pkl
│   ├── preprocessor.pkl
│   ├── model.pkl
├── src/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_preprocessing.py
│   │   ├── feature_engineering.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │
│   ├── pipeline/
│       ├── predict_pipeline.py
│
├── app.py
├── requirements.txt
```

## Example Prediction

**Input:**

Batting Team: India  
Bowling Team: Australia  
Score: 120  
Balls Left: 30  
Wickets Left: 6  
Last 5 Overs Runs: 45  

**Output:**

Predicted Score 175

---

## Author
Atharva Nitin Gholap

GitHub: https://github.com/AtharvaNG

LinkedIn: https://www.linkedin.com/in/atharva-gholap-67739828b/





