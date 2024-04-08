
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

#Generate list of numpy vectors with weights for matrix containing each weight for diffent intoxicant
# order: intoxicant, 'age', 'sbp', 'hr', 'gcs', 'second_diagnose', 'cirrhosis', 'dysrhythmia', 'respiratory'
#extract fixed betas (age --> resp in order)
fixed_betas = []
for sample in kernel[8:-1]:
    fixed_betas.append(sample['variable_value'])

toxin_betas = []
for sample in kernel[1:8]:
    toxin_betas.append(sample['variable_value'])

#append the polysubstance beta to toxin betas
toxin_betas.append(kernel[-1]['variable_value']) 

#generate numpy array with each vector asssociated with each toxin
#convert vectors to numpy arrays 
fixed_betas = np.array(fixed_betas)
toxin_betas = np.array(toxin_betas)

#create matrix with repeat fixed betas for each different beta toxin
fixed_beta_rep = np.tile(fixed_betas, (len(toxin_betas),1))
#merge each individual toxin beta with each vector for fixed individual betas
beta_multiplier_vectors = np.hstack((np.atleast_2d(toxin_betas).T, fixed_beta_rep))

#calculate INTOXICATE score for each class of toxin 
# do this for each toxin matrix, concatenate scores (add each matrix as list, format, and merge into 1)
intoxicate_scores = []
for idx, toxin_matched_matrix in enumerate(all_values):
    intoxicate_scores.append(np.matmul(toxin_matched_matrix,beta_multiplier_vectors[idx,:]))
    print(idx)

#Dataframes with risk scores and associated numerical values for each parameter
all_input_scores = pd.DataFrame(np.vstack(all_values))
all_input_scores.columns = predictive_variables
#append column with calculated risk scores
all_input_scores.join(pd.DataFrame(np.hstack(intoxicate_scores),columns=['risk score']))

#generate 2nd dataframe with equivalent descriptive parameters

'''
def create_each_possible_input():
    for variable_name in predictive_variables:
        data = yaml.safe_load(open(os.path.join(DATA_PATH, f'{variable_name}_values.yml'), 'r'))
'''

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

