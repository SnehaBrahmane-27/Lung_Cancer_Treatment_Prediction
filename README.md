# 🩺 LUNG CANCER TREATMENT PREDICTION

A machine learning-based web application that predicts the most suitable lung cancer treatment for patients based on their medical records. This project uses the XGBoost model for accurate predictions and includes a user-friendly Flask web interface with SQLite database support.

---

## 🚀 FEATURES

- Predicts treatment options: Chemotherapy, Radiation, Surgery, and Targeted Therapy
- Flask web interface for input and result display
- Input validation for clean data entry
- SQLite integration to store patient records
- Lightweight, fast, and ready for enhancement

---

## 🧠 MACHINE LEARNING OVERVIEW

- Model: XGBoost Classifier
- Preprocessing: Feature selection, binning, encoding, scaling
- Feature Engineering: Derived features for better performance
- Evaluation Metrics:
  - Accuracy: **100%**
  - Confusion Matrix and Classification Report
- Label (target): Recommended treatment type

---

## 📥 MODEL INPUT FIELDS

The model expects the following inputs:

- Patient's id
- Patient's name
- Smoking History (Yes/No)
- Tumor Size (in cm)
- Cancer Stage (I, II, III, IV)
- WBC counts
- LDH level
- Comorbidities (e.g., Diabetes, Hypertension)

These inputs are collected through a web form and validated before prediction.

---

## 🛠️ TECHNOLOGIES USED

- Python
- Flask
- SQLite
- XGBoost
- Pandas, NumPy, Scikit-learn
- HTML5, CSS3

---

## 📂 PROJECT STRUCTURE

lung-cancer-treatment/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── app.py              
├── model.pkl          
├── database.db         
├── requirements.txt    
└── README.md           

---

## 💡 HOW TO RUN LOCALLY

1. Clone the repository:
   git clone https://github.com/SnehaBrahmane-27/Lung_Cancer_Treatment_Prediction.git
   cd lung-cancer-treatment

2. Install dependencies:
   pip install -r requirements.txt

3. Run the Flask app:
   python app.py

4. Open in your browser:
   http://127.0.0.1:5000/

---

## 📊 DATASET & LABELS

The dataset contains cleaned and structured patient records:
- Attributes: Age, Weight, Tumor Size, Cancer Stage, Genetic Markers, Comorbidities, etc.
- Output: Suggested treatment (Chemotherapy / Radiation / Surgery / Targeted Therapy)

---

## 📌 FUTURE ENHANCEMENTS

- Add user login and history tracking
- Graph-based insights and dashboards
- Cloud deployment (Heroku / AWS / Azure)
- REST API integration

---

## 👤 AUTHOR

Sneha Brahmane  
B.Tech in IT
Email: snehabrahmane281@gmail.com
GitHub: https://github.com/SnehaBrahmane-27

