import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder
from joblib import dump

# Load and clean your data
data = pd.read_csv("Cleaned_data.csv")

# Separate features and label
X = data[['location', 'total_sqft', 'bath', 'bhk']]
y = data['price']

# Preprocessing
column_trans = make_column_transformer(
    (OneHotEncoder(handle_unknown='ignore'), ['location']),
    remainder='passthrough'
)

# Model
model = LinearRegression()
pipe = make_pipeline(column_trans, model)

# Train
pipe.fit(X, y)

# Save
dump(pipe, 'lr.pkl')
print("✅ Model retrained and saved as 'lr.pkl'")
