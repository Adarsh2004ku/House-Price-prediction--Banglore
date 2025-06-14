from flask import Flask, render_template, request
import pandas as pd
from joblib import load
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load data
try:
    data = pd.read_csv(os.path.join(BASE_DIR, 'Cleaned_data.csv'))
    data.drop(columns=['Unnamed: 0'], errors='ignore', inplace=True)
    print("✅ Data loaded.")
except Exception as e:
    print(f"❌ Error loading data: {e}")
    data = pd.DataFrame(columns=['location'])

# Load model
try:
    pipe = load(os.path.join(BASE_DIR, 'lr.pkl'))
    print("✅ Model loaded.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    pipe = None

@app.route('/')
def index():
    locations = sorted(data['location'].unique()) if not data.empty else []
    return render_template('index.html', locations=locations)

@app.route('/predict', methods=['POST'])
def predict():
    if not pipe:
        return render_template('result.html', price="⚠️ Model not loaded.")

    try:
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])
        sqft = float(request.form['sqft'])

        if not (1 <= bhk <= 10):
            raise ValueError("BHK must be between 1 and 10.")
        if not (1 <= bath <= 5):
            raise ValueError("Bathrooms must be between 1 and 5.")
        if bath > bhk:
            raise ValueError("Bathrooms can't exceed BHK.")
        if not (200 <= sqft <= 10000):
            raise ValueError("Sqft must be between 200 and 10,000.")

        input_df = pd.DataFrame([{
            'location': location,
            'total_sqft': sqft,
            'bath': bath,
            'bhk': bhk
        }])

        prediction = pipe.predict(input_df)[0]
        price_lakhs = round(prediction / 1_00_000, 2)

        return render_template('result.html', price=f"₹ {price_lakhs:,} Lakhs")

    except ValueError as ve:
        return render_template('result.html', price=f"❗ {ve}")
    except Exception as e:
        return render_template('result.html', price=f"⚠️ Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)
