import os
import create_synthetic_patient as csp
import json
import numpy as np

n = 1000
output_file = "synthetic_patient_db.json"

class CustomJSONizer(json.JSONEncoder):
    def default(self, obj):
        return super().encode(bool(obj)) if isinstance(obj, np.bool_) else super().default(obj)

if __name__ == "__main__":
    simulation_variables = csp.load_simulation_variables()
    name_to_score = csp.create_name_to_score_dict(simulation_variables)

    patient_db = []
    for _ in range(n):
        patient = csp.create_patient(simulation_variables, name_to_score)
        patient_db.append(patient)

    with open(output_file, 'w') as f:
        json.dump(patient_db, f, indent=4, cls=CustomJSONizer)
