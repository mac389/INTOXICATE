import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from tqdm import tqdm

DATA_PATH = os.path.join('..', 'data')
eq_idx_pairs = json.load(open(os.path.join(DATA_PATH, 'equivalence_dataset.json'), 'r'))

pt_db = json.load(open(os.path.join(DATA_PATH, 'patient_db._by_idx.json'), 'r')) 


#-- Preprocces for dataframe by flattening arbitrarilty nested dict ---

header = ['intoxicant','age','age_oor','gcs','hr','hr_oor','sbp','sbp_oor','respiratory','cirrhosis','dysrhythmia','second_diagnose']

dtypes = {
    'intoxicant': 'categorical',
    'age': 'numeric',
    'age_oor': 'bool',
    'gcs': 'categorical',
    'hr': 'numeric',
    'hr_oor': 'bool',
    'sbp': 'numeric',
    'sbp_oor': 'bool',
    'respiratory': 'categorical',
    'cirrhosis': 'categorical',
    'dysrhythmia': 'categorical',
    'second_diagnose': 'categorical',
    'risk': 'numeric',
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

rows = []
for i, pair in enumerate(eq_idx_pairs):
    left = flatten_patient(pt_db[pair['left_id']])
    right = flatten_patient(pt_db[pair['right_id']])

    left['pair_id'] = i
    left['side'] = 'left'
    left['model_same'] = bool(pair['model_same'])

    right['pair_id'] = i
    right['side'] = 'right'
    right['model_same'] = bool(pair['model_same'])

    rows.append(left)
    rows.append(right)

df = pd.DataFrame(rows)
print(df.head())
analysis_vars = [c for c in df.columns if c not in ['pair_id', 'side', 'model_same', 'patient_id']]

left_df = df[df['side'] == 'left'][['pair_id', 'model_same'] + analysis_vars].copy()
right_df = df[df['side'] == 'right'][['pair_id'] + analysis_vars].copy()

left_df = left_df.rename(columns={c: f"{c}_left" for c in analysis_vars})
right_df = right_df.rename(columns={c: f"{c}_right" for c in analysis_vars})

wide_df = left_df.merge(right_df, on='pair_id', how='inner')

numeric_vars = [k for k, v in dtypes.items() if v == 'numeric']
categorical_vars = [k for k, v in dtypes.items() if v == 'categorical']

for variable in numeric_vars:
    plt.figure(figsize=(6,4))
    sns.histplot(df[df['side']=='left'][variable].dropna(), label='Left', stat='density', alpha=0.4)
    sns.histplot(df[df['side']=='right'][variable].dropna(), label='Right', stat='density', alpha=0.4)
    plt.title(f"{variable}: left vs right")
    plt.legend()
    plt.tight_layout()
    plt.show()

for variable in numeric_vars:
    plt.figure(figsize=(6,4))
    sns.histplot(df[df['model_same']==True][variable].dropna(), label='model_same=True', stat='density', alpha=0.4)
    sns.histplot(df[df['model_same']==False][variable].dropna(), label='model_same=False', stat='density', alpha=0.4)
    plt.title(f"{variable}: model_same groups")
    plt.legend()
    plt.tight_layout()
    plt.show()

for variable in numeric_vars:
    plt.figure(figsize=(5,5))
    sns.scatterplot(
        data=wide_df,
        x=f"{variable}_left",
        y=f"{variable}_right",
        hue='model_same'
    )
    plt.title(f"{variable}: left vs right")
    plt.tight_layout()
    plt.show()

for variable in categorical_vars:
    plt.figure(figsize=(7,4))
    sns.countplot(data=df, x=variable, hue='side')
    plt.title(f"{variable}: left vs right")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

for variable in categorical_vars:
    plt.figure(figsize=(7,4))
    sns.countplot(data=df, x=variable, hue='model_same')
    plt.title(f"{variable}: by model_same")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

for variable in categorical_vars:
    ct = pd.crosstab(wide_df[f"{variable}_left"], wide_df[f"{variable}_right"])
    print(f"\nContingency table for {variable}")
    print(ct)

oor_vars = [c for c in df.columns if c.endswith('_oor')]

for oor_var in oor_vars:
    print(f"\nOOR summary for {oor_var}")
    print(df.groupby(['side', 'model_same'])[oor_var].mean())

for variable in ['age', 'hr', 'sbp']:
    oor_col = f"{variable}_oor"
    oor_frac = df[oor_col].mean() if oor_col in df.columns else None
    title = f"{variable}"
    if oor_frac is not None:
        title += f" (OOR fraction={oor_frac:.2%})"

for variable in numeric_vars:
    left = wide_df[f"{variable}_left"]
    right = wide_df[f"{variable}_right"]
    corr = pd.concat([left, right], axis=1).corr().iloc[0,1]
    print(f"{variable}: left-right Pearson correlation = {corr:.3f}")
