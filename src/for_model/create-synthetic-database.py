import os
import create_synthetic_patient as csp
from pymongo import MongoClient


client = MongoClient()
db = client['intoxicate']
collection = db['synthetic_registry_sandbox']

project_path = os.path.join('..','..',)

DATABASE_PATH = os.path.join(project_path, 'output','synthetic_registry')

n_patients = 2000

for i in range(n_patients):
    patient = csp.create_patient()
    collection.insert_one(patient)


