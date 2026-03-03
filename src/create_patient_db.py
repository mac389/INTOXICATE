import os
import create_synthetic_patient as csp
import json
import numpy as np
from tqdm import tqdm

n = 10000
output_file = "synthetic_patient_db.v2"
output_path = os.path.join('..', 'data', f'{output_file}.json')  
jsonl_path = os.path.join('..', 'data', f'{output_file}.jsonl')
class CustomJSONizer(json.JSONEncoder):
    def default(self, obj):
        return super().encode(bool(obj)) if isinstance(obj, np.bool_) else super().default(obj)

if __name__ == "__main__":
    simulation_variables = csp.load_simulation_variables()
    name_to_score = csp.create_name_to_score_dict(simulation_variables)

    patient_db = []
    for _ in tqdm(range(n)):
        patient = csp.create_patient(simulation_variables, name_to_score)
        patient_db.append(patient)

    with open(output_path, 'w') as f:
        json.dump(patient_db, f, indent=4, cls=CustomJSONizer)

    with open(jsonl_path, 'w') as f:
        for patient in patient_db:
            f.write(json.dumps(patient, cls=CustomJSONizer) + '\n')
