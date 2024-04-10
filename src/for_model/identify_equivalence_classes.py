import os
from pymongo import MongoClient
import json
import matplotlib.pyplot as plt
import seaborn as sns

client = MongoClient()

db = client['intoxicate']
collection = db['synthetic_registry_sandbox']

project_path = os.path.join('..','..',)
OUTPUT_PATH = os.path.join(project_path, 'output','synthetic_registry')

# plot distribution of risk scores

risk_scores = [patient['risk'] for patient in collection.find()]

ax = sns.histplot(risk_scores, bins=20)
ax.set_xlabel('Risk Score')
ax.set_ylabel('Frequency')
sns.despine()
plt.savefig(os.path.join(OUTPUT_PATH, 'risk_score_distribution.png'))


for i in range(0, 100, 10):
    patients = collection.find({'risk': {'$gte': i, '$lt': i+10},'patient_id': {'$exists': True}}, {'_id': 0})
    json.dump(list(patients),
              open(os.path.join(OUTPUT_PATH, f'risk_{i}_to_{i+10}.json'), 'w'))
