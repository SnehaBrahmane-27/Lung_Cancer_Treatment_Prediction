from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import pickle
import os
import sqlite3


conn = sqlite3.connect('data/database.db')




with open('model.pkl', 'rb') as model_file:
    model_bundle = pickle.load(model_file)
    clf_selected = model_bundle['model']
    label_encoders = model_bundle['label_encoders']
    le_treatment = model_bundle['le_treatment']
    selected_features = model_bundle['selected_features']

app = Flask(__name__)
app.secret_key = 'sneha'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'patients.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class PatientRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(20))
    name = db.Column(db.String(100))
    tumor_size = db.Column(db.Float)
    smoking_history = db.Column(db.String(20))
    stage = db.Column(db.String(20))
    bp_systolic = db.Column(db.Float)
    wbc_count = db.Column(db.Float)
    ldh_level = db.Column(db.Float)
    diabetes = db.Column(db.Boolean)
    heart_disease = db.Column(db.Boolean)
    chronic_lung_disease = db.Column(db.Boolean)
    comorbidity_count = db.Column(db.Integer)
    tumor_burden_index = db.Column(db.Float)
    predicted_treatment = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'doctor' and password == 'secure123':
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid Credentials')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/index')
def render_index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    patient_id = request.form['patient_id']
    name = request.form['name']
    tumor_size = float(request.form['tumor_size'])
    smoking_history = request.form['smoking_history']
    stage = request.form['stage']
    bp_systolic = float(request.form['bp_systolic'])
    wbc_count = float(request.form['wbc_count'])
    ldh_level = float(request.form['ldh_level'])

    comorbidities = {
        'Comorbidity_Diabetes': 1 if request.form.get('diabetes') == 'Yes' else 0,
        'Comorbidity_Heart_Disease': 1 if request.form.get('heart_disease') == 'Yes' else 0,
        'Comorbidity_Chronic_Lung_Disease': 1 if request.form.get('chronic_lung_disease') == 'Yes' else 0
    }

    comorbidity_count = sum(comorbidities.values())
    tumor_burden_index = tumor_size * (1 + comorbidity_count / 10)

    input_data = {
        'Tumor_Size_mm': tumor_size,
        'Smoking_History': smoking_history,
        'Stage': stage,
        'Blood_Pressure_Systolic': bp_systolic,
        'White_Blood_Cell_Count': wbc_count,
        'LDH_Level': ldh_level,
        'Comorbidity_Score': comorbidity_count
    }

    for col in ['Smoking_History', 'Stage']:
        encoder = label_encoders[col]
        input_data[col] = encoder.transform([input_data[col]])[0]

    df_input = pd.DataFrame([input_data])
    df_input = df_input[selected_features]

    prediction = clf_selected.predict(df_input)
    predicted_treatment = le_treatment.inverse_transform(prediction)[0]

    new_record = PatientRecord(
        patient_id=patient_id,
        name=name,
        tumor_size=tumor_size,
        smoking_history=smoking_history,
        stage=stage,
        bp_systolic=bp_systolic,
        wbc_count=wbc_count,
        ldh_level=ldh_level,
        diabetes=comorbidities['Comorbidity_Diabetes'],
        heart_disease=comorbidities['Comorbidity_Heart_Disease'],
        chronic_lung_disease=comorbidities['Comorbidity_Chronic_Lung_Disease'],
        comorbidity_count=comorbidity_count,
        tumor_burden_index=tumor_burden_index,
        predicted_treatment=predicted_treatment
    )
    db.session.add(new_record)
    db.session.commit()

    return jsonify({'prediction': predicted_treatment})

@app.route('/records')
def records():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    patients = PatientRecord.query.all()
    return render_template('records.html', patients=patients)

if __name__ == '__main__':
    app.run(debug=True)
