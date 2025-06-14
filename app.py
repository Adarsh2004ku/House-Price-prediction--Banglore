from flask import Flask, render_template, request
import pandas as pd
from joblib import load
import os

app = Flask(__name__)

# Define safe base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load cleaned data
try:
    data_path = os.path.join(BASE_DIR, 'Cleaned_data.csv')
    data = pd.read_csv(data_path)
    
    # Drop Unnamed column if present
    if 'Unnamed: 0' in data.columns:
        data.drop(columns=['Unnamed: 0'], inplace=True)

    print("✅ Cleaned_data.csv loaded.")
except Exception as e:
    print(f"❌ Failed to load Cleaned_data.csv: {e}")
    data = pd.DataFrame(columns=['location'])

# Load trained model
try:
    model_path = os.path.join(BASE_DIR, 'lr.pkl')
    pipe = load(model_path)
    print("✅ Model loaded.")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    pipe = None

@app.route('/')
def index():
    locations = sorted(data['location'].unique()) if not data.empty else []
    return render_template('index.html', locations=locations)

@app.route('/predict', methods=['POST'])
def predict():
    if pipe is None:
        return render_template('result.html', price="⚠️ Model not loaded.")

    try:
        location = request.form.get('location')
        bhk = int(request.form.get('bhk'))
        bath = int(request.form.get('bath'))
        sqft = float(request.form.get('sqft'))

        # Input validations
        if bhk < 1 or bhk > 10:
            raise ValueError("BHK must be between 1 and 10.")
        if bath < 1 or bath > 5:
            raise ValueError("Bathrooms must be between 1 and 5.")
        if bath > bhk:
            raise ValueError("Bathrooms cannot be more than BHK.")
        if sqft < 200 or sqft > 10000:
            raise ValueError("Sqft must be between 200 and 10,000.")

        # Ensure input is DataFrame with correct structure
        input_df = pd.DataFrame([{
            'location': location,
            'total_sqft': sqft,
            'bath': bath,
            'bhk': bhk
        }])

        # Predict using the pipeline (which handles encoding)
        prediction = pipe.predict(input_df)[0]
        price_lakhs = round(prediction / 1_00_000, 2)

        return render_template('result.html', price=f"₹ {price_lakhs:,} Lakhs")

    except ValueError as ve:
        return render_template('result.html', price=f"❗ {str(ve)}")

    except Exception as e:
        return render_template('result.html', price=f"⚠️ Something went wrong: {str(e)}")
