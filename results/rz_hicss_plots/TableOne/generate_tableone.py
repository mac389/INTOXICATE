import pandas as pd
from tableone import TableOne
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

data = pd.read_csv('synthetic_patients_1.csv')
data.replace({True: "Yes", False: "No"}, inplace=True)
columns = [ ... ]

rename_dict = {
    'age': 'Age',
    'sbp': 'Systolic BP',
    'hr': 'Heart Rate',
    'gcs': 'GCS Score',
    'second_diagnose': 'Secondary Diagnosis',
    'cirrhosis': 'Cirrhosis',
    'dysrhythmia': 'Dysrhythmia',
    'respiratory': 'Respiratory Score',
    'risk': 'Risk Score'
}

columns = ['intoxicant', 'age', 'sbp', 'hr', 'gcs', 'second_diagnose', 'cirrhosis', 'dysrhythmia', 'respiratory', 'risk']
categorical = ['intoxicant', 'second_diagnose', 'gcs','cirrhosis', 'dysrhythmia', 'respiratory', 'risk']
continuous = ['age', 'sbp', 'hr']
nonnormal = ['age']
Table_One = TableOne(
    data,
    columns=columns,
    categorical=categorical,
    continuous=continuous,
    nonnormal=nonnormal,
    rename=rename_dict,
    #groupby='intoxicant',
    pval=False, # to get a pval, you need to group by some variable, intoxicant is best, but model is too simple right now for that 
    missing=False
)


Table_One.to_excel("results/Table_One.xlsx")


with open("results/Table_one_LA.html", "w") as f:
    f.write(Table_One.to_html())

# Export as CSV
table1_as_df = Table_One.tableone.reset_index()
table1_as_df.to_csv("results/Table_one_LA.csv", index=False)

