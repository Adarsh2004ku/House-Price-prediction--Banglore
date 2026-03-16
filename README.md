# 🏠 Bangalore House Price Predictor

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?logo=scikit-learn&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20App-000000?logo=flask&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Numerical-013243?logo=numpy&logoColor=white)
![Render](https://img.shields.io/badge/Deployed-Render.com-46E3B7?logo=render&logoColor=white)
![JavaScript](https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-F7DF1E?logo=javascript&logoColor=black)

A **full-stack machine learning web application** that predicts residential property prices in Bengaluru, India. Built on the Kaggle Bengaluru House Data (~13,320 records), the project demonstrates a complete ML pipeline — from raw data ingestion and feature engineering, through model training and serialisation, to a publicly deployed Flask web application on Render.com.

🔗 **Live App:** [https://house-price-prediction-banglore.onrender.com/](https://house-price-prediction-banglore.onrender.com/)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Dataset](#-dataset)
- [Data Preprocessing](#-data-preprocessing)
- [Machine Learning Model](#-machine-learning-model)
- [Application Architecture](#-application-architecture)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [Running Locally](#-running-locally)
- [Retraining the Model](#-retraining-the-model)
- [Deployment](#-deployment)

---

## 🧠 Overview

Predicting real estate prices in a city like Bengaluru is challenging due to high location variance, inconsistent data formats, and extreme outliers. This project tackles the problem end-to-end:

- ✅ Real-world dataset with 13,320 property listings from 99acres.com
- ✅ Comprehensive data cleaning handling range values, nulls, and outliers
- ✅ Location dimensionality reduced from **1,287 → ~241 categories**
- ✅ Linear Regression model selected via K-Fold CV + GridSearchCV
- ✅ Model serialised to `lr.pkl` — sub-second inference at runtime
- ✅ Deployed publicly on Render.com with HTTPS

---

## ✨ Features

| Feature | Details |
|---|---|
| 📍 Location-aware prediction | ~240 distinct Bengaluru localities via one-hot encoding |
| ⚡ Instant predictions | Pre-loaded `lr.pkl` model — no retraining on request |
| 📱 Responsive UI | CSS-styled interface adapting to mobile and desktop |
| ✅ Client-side validation | JavaScript prevents invalid/empty inputs before server call |
| 🔄 Retrainable | `retrain_model.py` refreshes the model without touching app code |
| 🌐 Public deployment | Live on Render.com — no local installation needed |

---

## 📊 Dataset

**Source:** [Kaggle — Bengaluru House Data](https://www.kaggle.com/datasets/amitabhajoy/bengaluru-house-price-data) (originally scraped from 99acres.com)

| Column | Type | Description |
|---|---|---|
| `area_type` | Categorical | Super built-up / Plot / Carpet area |
| `availability` | Text | Possession status or move-in date |
| `location` | Categorical | Locality within Bengaluru (1,000+ unique values) |
| `size` | Text | BHK/bedroom count in mixed format (e.g. `3 BHK`) |
| `society` | Text | Housing society name (high cardinality, often null) |
| `total_sqft` | Text/Numeric | Total area — sometimes ranges like `1000–1200` |
| `bath` | Numeric | Number of bathrooms |
| `balcony` | Numeric | Number of balconies |
| `price` | Numeric | **Target** — price in Indian Rupees (Lakhs) |

**Records:** ~13,320 raw → ~9,000 after cleaning

---

## 🔧 Data Preprocessing

All preprocessing steps are documented in the Jupyter Notebook:

1. **Drop irrelevant columns** — `area_type`, `society`, `balcony`, `availability` removed (low predictive signal / high nulls)

2. **Parse BHK from text** — Regex extracts integer bedroom count from strings like `3 BHK` or `4 Bedroom`

3. **Handle range values in `total_sqft`** — Entries like `1200–1400` are averaged; non-numeric entries dropped

4. **Remove null rows** — Records with missing `location`, `bath`, `price`, or BHK dropped

5. **Location normalisation** — Locations with fewer than 10 occurrences bucketed into `other`, reducing dimensionality from **1,287 → ~241 categories**

6. **Price-per-sqft feature** — Derived column `price_per_sqft` computed for outlier detection

7. **Outlier removal:**
   - Properties with `price_per_sqft` outside **mean ± 1 std dev** per location removed
   - Properties where `bathrooms > BHK + 2` excluded (data entry errors)

8. **One-hot encoding** — Location column encoded via `pandas.get_dummies()` producing ~241 binary columns

**Output:** `Cleaned_data.csv` — clean, model-ready dataset

---

## 🤖 Machine Learning Model

### Algorithm: Linear Regression

After cleaning and one-hot encoding, housing price data exhibits approximately linear relationships between area, location, BHK, and price. Linear Regression from `scikit-learn` is chosen as the primary model.

**Prediction function:**

```
ŷ = β₀ + β₁·sqft + β₂·bath + β₃·bhk + Σ βᵢ·locᵢ
```

Where `locᵢ` are the one-hot encoded location binary features.

### Training & Evaluation

| Split | Size |
|---|---|
| Training set | 80% |
| Test set | 20% (fixed `random_state=10`) |

**Model selection via GridSearchCV + K-Fold CV** comparing:
- Linear Regression ✅ (selected)
- Decision Tree Regressor
- Lasso Regression

**Evaluation metrics:** R² Score, RMSE, MAE

### Model Persistence

```python
import pickle
with open("lr.pkl", "wb") as f:
    pickle.dump(model, f)
```

The `lr.pkl` file is loaded once at Flask startup — no retraining per request.

---

## 🏗️ Application Architecture

```
User Browser
     │
     │  GET /           → Serves index.html (location dropdown, inputs)
     │  POST /predict   → Returns predicted price (JSON)
     ▼
Flask App (app.py)
     │
     ├── Loads lr.pkl at startup
     ├── Loads columns.json (location list for dropdown)
     ├── Constructs feature vector (sqft, bath, bhk + one-hot location)
     └── Returns predicted price in Lakhs INR
     │
     ▼
Linear Regression Model (lr.pkl)
```

### Request Flow

1. User fills form: **Location** + **BHK** + **Bathrooms** + **Square Footage**
2. JavaScript validates inputs client-side
3. Browser sends `POST /predict` with form data
4. Flask constructs feature vector with one-hot location encoding
5. `model.predict()` returns price in Lakhs INR
6. Result rendered back to user

### Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.x + Flask |
| ML Engine | Scikit-learn (Linear Regression) |
| Data Processing | Pandas, NumPy |
| Model Serialisation | Pickle (`lr.pkl`) |
| Frontend | HTML5 + CSS3 (Jinja2 templates) |
| Validation | JavaScript (client-side) |
| Deployment | Render.com (free tier, HTTPS) |
| Environment | `venv` + `requirements.txt` |

---

## 📁 Project Structure

```
House-Price-prediction--Banglore/
├── app.py                        # Flask entry point — routes & prediction logic
├── retrain_model.py              # Script to retrain model from cleaned data
├── lr.pkl                        # Serialised trained Linear Regression model
├── columns.json                  # Location list for dropdown & feature vector
├── Bengaluru_House_Data.csv      # Raw Kaggle dataset (13,320 records)
├── Cleaned_data.csv              # Pre-processed dataset after feature engineering
├── bangalore-house-price-predictor/
│   └── *.ipynb                   # Jupyter Notebooks — EDA + model development
├── templates/
│   ├── index.html                # Main prediction form
│   └── result.html               # Prediction result page
├── static/
│   └── css/
│       └── style.css             # Responsive UI styles
├── render.yaml                   # Render.com deployment config
├── requirements.txt              # Python dependency manifest
└── .gitignore
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- pip

### 1. Clone & Install

```bash
git clone https://github.com/Adarsh2004ku/House-Price-prediction--Banglore.git
cd House-Price-prediction--Banglore
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## ▶️ Running Locally

```bash
python app.py
```

Open your browser at: [http://localhost:5000](http://localhost:5000)

---

## 🔄 Retraining the Model

If you update the dataset or want to experiment with different preprocessing:

```bash
python retrain_model.py
```

This re-runs the full training pipeline and overwrites `lr.pkl` with the new model. No changes to `app.py` are needed.

---

## 🌐 Deployment

The app is deployed on **Render.com** using the `render.yaml` config:

```yaml
services:
  - type: web
    name: house-price-prediction-banglore
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    plan: free
```

- Render provides **automatic HTTPS** and a public URL
- Free tier spins down after inactivity — first load may take ~30 seconds to wake

**Live URL:** [https://house-price-prediction-banglore.onrender.com/](https://house-price-prediction-banglore.onrender.com/)

---

## 👤 Author

**Adarsh Kumar**
- GitHub: [@Adarsh2004ku](https://github.com/Adarsh2004ku)
- LinkedIn: [adarsh-kumar-714108314](https://www.linkedin.com/in/adarsh-kumar-714108314/)
- Portfolio: [View Portfolio](https://portfolio-five-roan-hettkeuqbc.vercel.app/)
