import os
import re
import yaml

import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from pathlib import Path
from scipy.special import expit

DATA_PATH = Path(__file__).parent.parent / 'data'
RESULTS_PATH = Path(__file__).parent.parent / 'results'
SNAPSHOTS_PATH = DATA_PATH / 'snapshots'
MODEL_PATH = DATA_PATH / 'model'
input_file = SNAPSHOTS_PATH / 'snapshot.05062024.xlsx'
OUTCOME_VAR = 'Actual Disposition'

def categorize(value, criteria):
    data_type = criteria['criteria']
    if data_type == "categorical":
        return categorize_categorical(value, criteria['values'])
    elif data_type == "range":
        return categorize_range(value, criteria['values'])
    else:
        raise ValueError(f"Unknown data type: {data_type}")

def categorize_range(value, rules):
    for r in rules:
        if r["min"] <= value <= r["max"]:
            return r["name"]
    return None

def categorize_categorical(value, rules):
    for r in rules:
        if r["name"] == value:
            return r["name"]
    return None

def load_category_bins(model_path):
    bins = {}
    for fname in os.listdir(model_path):
        if fname.endswith("_score.yml"):
            var = fname.replace("_score.yml", "")
            with open(os.path.join(model_path, fname), "r") as f:
                bins[var] = yaml.safe_load(f)
    return bins

df = pd.read_excel(input_file, sheet_name="INTOXICATE")
model_variables = [field for field in open(DATA_PATH / 'model_variables.txt').read().splitlines() if not field.startswith('%')]

df = df[model_variables]
df.rename({'Pulse': 'HR'}, axis=1, inplace=True)
df.columns = [var.lower() for var in df.columns]

category_bins = load_category_bins(MODEL_PATH)
for var, criteria in category_bins.items():
    if var.lower() in df.columns.str.lower().tolist():
        df[f"{var}_cat"] = df[var].apply(lambda x: categorize(x, criteria))

print(df.columns)
# --- Encode each category separately (one-hot encoding) ---
# This ensures each category has its own column and its own coefficient.

ordinal_cat_cols = [f"{var}_cat" for var in category_bins if f"{var}_cat" in df.columns]

onehot = OneHotEncoder(drop="first", sparse_output=False)
encoded = onehot.fit_transform(df[ordinal_cat_cols])
encoded_df = pd.DataFrame(encoded, columns=onehot.get_feature_names_out(ordinal_cat_cols))
df = pd.concat([df, encoded_df], axis=1)

# Combine predictors for regression
predictor_cols = list(encoded_df.columns)
X = df[predictor_cols]

# --- Map textual outcome to numeric ---
df[OUTCOME_VAR.lower()] = df[OUTCOME_VAR.lower()].map({
    "Discharge": 0,
    "GMF": 0,        # Treat GMF as low-risk; set to 1 if you prefer high-risk.
    "ICU": 1
})
y = df[OUTCOME_VAR.lower()]

# --- Fit logistic regression ---
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# --- Build coefficient + odds ratio table ---
coef_df = pd.DataFrame({
    "Variable": X.columns,
    "Coefficient": model.coef_[0],
    "Odds_Ratio": np.exp(model.coef_[0])
}).sort_values("Odds_Ratio", ascending=False)

# --- Derive point values ---
ref_coef = coef_df.loc[coef_df["Coefficient"].abs() > 0, "Coefficient"].abs().min()
coef_df["Points"] = (coef_df["Coefficient"] / ref_coef).round().astype(int)
coef_df.loc[coef_df["Points"] == 0, "Points"] = np.sign(coef_df["Coefficient"])

# --- Generate per-category composite scoring table ---
composite_rows = []
for var, rule_dict in category_bins.items():
    for r in rule_dict["values"]:
        cat_name = r["name"]
        col_name_matches = [col for col in coef_df["Variable"] if f"{var}_cat_{cat_name}" in col]
        coef_val = coef_df.loc[coef_df["Variable"].isin(col_name_matches), "Coefficient"].values
        points_val = coef_df.loc[coef_df["Variable"].isin(col_name_matches), "Points"].values

        subset = df[df[f"{var}_cat"] == cat_name]
        risk = subset[OUTCOME_VAR.lower()].mean() if not subset.empty else np.nan

        composite_rows.append({
            "Variable": var,
            "Category": cat_name,
            "N": len(subset),
            "Mean_Risk": round(risk, 3),
            "Coefficient": coef_val[0] if len(coef_val) else np.nan,
            "Points": points_val[0] if len(points_val) else np.nan
        })

composite_df = pd.DataFrame(composite_rows)
composite_df.to_csv(RESULTS_PATH / "composite_score_table.csv", index=False)
