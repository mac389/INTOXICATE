import os
import json
import Create_Syn_Patient_edit as csp
import pandas as pd

def flatten_patient(patient):
    flat = {}
    for entry in patient.get('presentation', []):
        flat[entry['name']] = entry['value']
        flat[f"{entry['name']}_range_flag"] = entry.get('range_flag', 'unknown')  
    flat['risk'] = patient.get('risk')
    flat['patient_id'] = patient.get('patient_id')
    return flat

n_patients = 10000
patients =[]
for i in range(n_patients):
    #patients += [csp.simulate_patient_value_i()]
    patients.append(csp.simulate_patient_value_i())


flat_patients = [flatten_patient(p) for p in patients]
df_flat_patients = pd.DataFrame(flat_patients)
sort_cols = [col for col in ['gcs', 'risk'] if col in df_flat_patients.columns]
if sort_cols:
    df_flat_patients = df_flat_patients.sort_values(sort_cols, ascending=True, inplace=False)
df_flat_patients.to_csv('synthetic_patients.csv')


project_path = os.path.join('..', '..')
DATABASE_PATH = os.path.join(project_path, 'output', 'synthetic_registry')
os.makedirs(DATABASE_PATH, exist_ok=True)  

output_file = os.path.join(DATABASE_PATH, 'synthetic_patients.json')

with open(output_file, 'w') as f:
    json.dump(patients, f, indent=2)

print(f" Saved {n_patients} synthetic patients to {output_file}")
