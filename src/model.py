import json
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import shap
import matplotlib.pyplot as plt
from tqdm import tqdm

# Ignore warnings for cleaner output
import warnings
warnings.filterwarnings("ignore")

# Load data
with open('../data/data_transform.json', 'r') as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data)

# Add total_btc
df['total_btc'] = df['total_in'] + df['total_out']

# Features to analyze
features = [
    'total_btc', 'mean_in_btc', 'mean_out_btc',
    'indegree', 'outdegree', 'total_in', 'total_out',
    'sender_entropy', 'receiver_entropy'
]

# Replace NaN values with 0
df[features] = df[features].fillna(0)

# Normalize features using z-score normalization (Standard Scaler)
scaler = StandardScaler()
df[features] = scaler.fit_transform(df[features])

# Anomalies detection using Isolation Forest
iso_forest = IsolationForest(contamination=0.01, random_state=42)
iso_forest.fit(df[features])

# Use tqdm for anomaly detection prediction
preds = []
for i in tqdm(range(len(df)), desc="Detecting anomalies"):
    pred = iso_forest.predict([df[features].iloc[i]])[0]
    preds.append(pred)

df['anomaly'] = [1 if p == -1 else 0 for p in preds]  # 1 = anomaly, 0 = normal

# Calculate SHAP values for interpretability
explainer = shap.TreeExplainer(iso_forest)
shap_values = explainer.shap_values(df[features])

# Convert SHAP summary into JSON format
shap_json = []
mean_abs_shap = np.abs(shap_values).mean(axis=0)

for feature, value in zip(features, mean_abs_shap):
    shap_json.append({
        "variable": feature,
        "value": float(value)  # ensure JSON serializable
    })

# Save SHAP values into variable.json
with open('../data/variable.json', 'w') as f:
    json.dump(shap_json, f, indent=4)

# Denormalize features for final output
df[features] = scaler.inverse_transform(df[features])

# Save the DataFrame with anomaly labels
df.to_csv('../data/result.csv', index=False)

# Just save hash_transaction and anomaly status
df = df[['hash_transaction', 'anomaly']]

# Save results
result = df.to_dict(orient='records')
with open('../data/result.json', 'w') as f:
    json.dump(result, f, indent=4)

print("✅ Anomaly detection completed and results saved to '../data/result.json'.")
print("✅ SHAP interpretability saved to '../data/variable.json'.")