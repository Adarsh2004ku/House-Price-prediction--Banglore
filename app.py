from flask import Flask, render_template, request
import pandas as pd
from joblib import load

app = Flask(__name__)

data = pd.read_csv('Cleaned_data.csv')
pipe = load('lr.pkl')

@app.route('/')
def index():
    locations = sorted(data['location'].unique())
    return render_template('index.html', locations=locations)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        location = request.form.get('location')
        bhk = int(request.form.get('bhk'))
        bath = int(request.form.get('bath'))
        sqft = float(request.form.get('sqft'))

        # validations
        if bhk < 1 or bhk > 10:
            raise ValueError("Number of BHK should be between 1 and 10.")
        if bath < 1 or bath > 5:
            raise ValueError("Number of bathrooms should be between 1 and 5.")
        if bath > bhk:
            raise ValueError("Bathrooms cannot be more than bedrooms (BHK).")
        if sqft < 200 or sqft > 10000:
            raise ValueError("Total square feet should be between 200 and 10,000.")

        input_df = pd.DataFrame([[location, sqft, bath, bhk]],
                                columns=['location', 'total_sqft', 'bath', 'bhk'])

        prediction = pipe.predict(input_df)[0]
        return render_template('result.html', price=round(prediction, 2))

    except ValueError as ve:
        return render_template('result.html', price=f"❗ {str(ve)}")

    except Exception as e:
        return render_template('result.html', price=f"⚠️ Something went wrong: {str(e)}")
