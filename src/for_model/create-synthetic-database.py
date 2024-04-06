
import pandas as pd
import random
import os
import yaml
import numpy as np


from slugify import slugify

'''
Ideally would populate a MongoDB database. I use a CSV here for the first iteration.
'''

#DATA_PATH = os.path.join(cwd, 'data','for_model')

project_path = 'c:\\Users\\rzeml\\intoxicate\\INTOXICATE'

DATA_PATH = os.path.join(project_path, 'data', 'for_model')
kernel =yaml.safe_load(open(os.path.join(DATA_PATH, 'kernel.yml'), 'r'))
#converts to a dict datatype
flattened_kernel = {item['variable_name']: item['variable_value'] for item in kernel}
predictive_variables = ['intoxicant', 'age', 'sbp', 'hr', 'gcs', 'second_diagnose', 'cirrhosis', 'dysrhythmia', 'respiratory'] 


def chose_variable(variable_name):
    data = yaml.safe_load(open(os.path.join(DATA_PATH, f'{variable_name}_values.yml'), 'r'))
    return random.choice(data)



def create_patient():
    ans = {}
    for variable_name in predictive_variables:
        tmp = chose_variable(variable_name)
        name = tmp['name']
        value = tmp['value']
        ans[f'{variable_name}_name'] = name
        ans[f'{variable_name}_value'] = value

    risk_score = calculate_risk_score(ans)
    ans['risk'] = risk_score
    return ans


input_ranges = []
#create list of lists for each possible values for each input class
for variable_name in predictive_variables:
#returns list of dicts
    data = yaml.safe_load(open(os.path.join(DATA_PATH, f'{variable_name}_values.yml'), 'r'))

    input_ranges.append(np.array([sample['value'] for sample in data]))

# Generate all possible combinations of values
#generate separate matrix for each possible toxin (they will be weighed differently to calculate INTOXICATE score)
all_values = []
for index,val in enumerate(input_ranges[0]):
    all_values.append(np.array(np.meshgrid(val,*input_ranges[1:])).T.reshape(-1,9))


#Generate list of numpy vectors with weights for matrix contained each weight for diffent intoxicant


#calculate INTOXICATE score for each class of toxin 

all_values_np = np.vstack(all_values)

#reconstuct the data into formatted dataFrame for export/analysis



'''
def create_each_possible_input():
    for variable_name in predictive_variables:
        data = yaml.safe_load(open(os.path.join(DATA_PATH, f'{variable_name}_values.yml'), 'r'))
'''

def calculate_risk_score(patient):
    risk_score = 0
    for variable_name in predictive_variables:
        score = patient[f'{variable_name}_value']
        kernel_variable_name = slugify(variable_name.lower(), separator='_')
        if kernel_variable_name == 'CO, As, CN':
            weight = flattened_kernel['toxins_nos']
        elif kernel_variable_name == 'intoxicant':
            weight = flattened_kernel[slugify(patient['intoxicant_name'].lower(), separator='_')]
        else:
            weight = flattened_kernel[kernel_variable_name]
        risk_score += (score * weight)
    return risk_score


def split_patient(patient):
    variable_names = {key: value['name'] for key, value in patient.items()}
    variable_values = {key: value['value'] for key, value in patient.items()}
    return (variable_names, variable_values)


n_patients = 1000
# names, codes = zip(*[split_patient(create_patient()) for _ in range(n_patients)])

patient = [create_patient() for _ in range(n_patients)]

# df_codes = pd.DataFrame(codes)
# df_names = pd.DataFrame(names)
#
# df_codes.to_csv(os.path.join(DATA_PATH, 'intoxicate_codes.csv'), index=False)
# df_names.to_csv(os.path.join(DATA_PATH, 'intoxicate_names.csv'), index=False)

df = pd.DataFrame(patient)
df.to_csv(os.path.join(DATA_PATH, 'intoxicate.patient_registry.csv'), index=False)

