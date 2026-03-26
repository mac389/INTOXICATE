import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = os.path.join('..', 'data')
icu_idx = json.load(open(os.path.join(DATA_PATH, 'icu_dataset.json'), 'r'))

patient_db = [json.loads(line) for line in open(os.path.join(DATA_PATH, 'synthetic_patient_db.v2.jsonl'), 'r')]
icu_patients = [p for p in patient_db if str(p['patient_id']) in icu_idx]

header = [
    'intoxicant','age','age_oor','gcs','hr','hr_oor',
    'sbp','sbp_oor','respiratory','cirrhosis',
    'dysrhythmia','second_diagnose'
]

dtypes = {
    'intoxicant': 'categorical',
    'age': 'float',
    'age_oor': 'bool',
    'gcs': 'categorical',
    'hr': 'float',
    'hr_oor': 'bool',
    'sbp': 'float',
    'sbp_oor': 'bool',
    'respiratory': 'categorical',
    'cirrhosis': 'categorical',
    'dysrhythmia': 'categorical',
    'second_diagnose': 'categorical'
}

def flatten_patient(raw_patient):
    presentation = raw_patient.get('presentation', [])
    flat = {}

    for variable in presentation:
        name = variable['name']
        if name in header:
            flat[name] = variable.get('value')
            if f"{name}_oor" in header:
                flat[f"{name}_oor"] = not bool(variable.get('in_original_range', True))

    flat['risk'] = raw_patient.get('risk', None)
    flat['patient_id'] = raw_patient.get('patient_id', None)
    return flat

df = pd.DataFrame([flatten_patient(p) for p in icu_patients])

# --- dtype cleanup ---
for col, typ in dtypes.items():
    if col not in df:
        continue
    if typ == 'float':
        df[col] = pd.to_numeric(df[col], errors='coerce')
    elif typ == 'categorical':
        df[col] = df[col].astype('category')

df['risk'] = pd.to_numeric(df['risk'], errors='coerce')

numeric_vars = [k for k, v in dtypes.items() if v == 'float']
categorical_vars = [k for k, v in dtypes.items() if v == 'categorical']

# --- Descriptive ---
print("Descriptive statistics for ICU patients:")
print(df.describe())

# --- Risk distribution ---
plt.figure(figsize=(6,4))
sns.histplot(df['risk'].dropna(), bins=30)
plt.title("Risk distribution")
plt.show()

# --- Threshold analysis ---
THRESHOLD = 6
df['model_pred'] = df['risk'] > THRESHOLD

plt.figure(figsize=(6,4))
sns.histplot(data=df, x='risk', hue='model_pred', bins=30)
plt.title("Risk vs ICU decision threshold")
plt.show()

# --- OOR summary ---
oor_cols = [c for c in df.columns if c.endswith('_oor')]
df['any_oor'] = df[oor_cols].any(axis=1)

print("\nOOR summary:")
print(df[oor_cols].mean())

plt.figure(figsize=(6,4))
sns.boxplot(data=df, x='any_oor', y='risk')
plt.title("Risk vs any OOR")
plt.show()

# --- Numeric relationships ---
for var in numeric_vars:
    if var not in df:
        continue
    plt.figure(figsize=(5,4))
    sns.scatterplot(data=df, x=var, y='risk')
    plt.title(f"{var} vs risk")
    plt.show()

# --- Correlation ---
corr = df[numeric_vars + ['risk']].corr()
plt.figure(figsize=(6,5))
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Correlation matrix")
plt.show()
