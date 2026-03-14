from flask import Flask, render_template, request
import pandas as pd
from joblib import load
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load dataset
try:
    data = pd.read_csv(os.path.join(BASE_DIR, "Cleaned_data.csv"))
    data.drop(columns=["Unnamed: 0"], errors="ignore", inplace=True)
    print("✅ Data loaded")
except Exception as e:
    print("❌ Data loading error:", e)
    data = pd.DataFrame(columns=["location"])

# Load model
pipe = None
try:
    pipe = load(os.path.join(BASE_DIR, "lr.pkl"))
    print("✅ Model loaded")
except Exception as e:
    print("❌ Model loading error:", e)

@app.route("/")
def index():
    locations = sorted(data["location"].unique())
    return render_template("index.html", locations=locations)

@app.route("/predict", methods=["POST"])
def predict():

    if pipe is None:
        return render_template("result.html", price="⚠️ Model not loaded")

    try:
        location = request.form.get("location")
        bhk = int(request.form.get("bhk"))
        bath = int(request.form.get("bath"))
        sqft = float(request.form.get("sqft"))

        if bath > bhk:
            return render_template("result.html", price="❗ Bathrooms cannot exceed BHK")

        input_df = pd.DataFrame({
            "location": [location],
            "total_sqft": [sqft],
            "bath": [bath],
            "bhk": [bhk]
        })

        prediction = pipe.predict(input_df)[0]

        if prediction >= 1_00_00_000:
            price = f"₹ {round(prediction/1_00_00_000,2)} Crore"
        else:
            price = f"₹ {round(prediction/1_00_000,2)} Lakhs"

        return render_template("result.html", price=price)

    except Exception as e:
        return render_template("result.html", price=f"⚠️ Error: {e}")

if __name__ == "__main__":
    app.run(debug=True, port=8000)