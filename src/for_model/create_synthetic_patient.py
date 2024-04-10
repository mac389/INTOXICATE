import random
import os
import yaml
import uuid
from slugify import slugify

'''
1. Don't use absolute paths. They don't transfer well between systems. Use relative paths.
2. Use os.path.join() to join paths. Unix, older Macs, and Windows use different path separators.
'''


project_path = os.path.join('..','..',) #  Relative to src/for_model 
DATA_PATH = os.path.join(project_path, 'data','for_model')

PATH_TO_KERNEL_VALUES = os.path.join(DATA_PATH, 'kernel.yml')
kernel =yaml.safe_load(open(PATH_TO_KERNEL_VALUES, 'r'))
flattened_kernel = {item['variable_name']: item['variable_value'] for item in kernel}

PATH_TO_PREDICTIVE_VARIABLES = os.path.join(DATA_PATH, 'predictive_variables.yml')
predictive_variables = yaml.safe_load(open(PATH_TO_PREDICTIVE_VARIABLES, 'r'))

score = {variable['value']:{value['name']:value['value'] 
         for value in yaml.safe_load(open(os.path.join(DATA_PATH, f"{variable['value']}_values.yml"), 'r'))}
         for variable in predictive_variables}

def create_patient():
    patient = {}
    for variable in predictive_variables:
        variable_name = variable['value']

        value_name, value_score = random.choice(list(score[variable_name].items()))

        patient[variable_name] = {}
        patient[variable_name]['value'] = value_name
        patient[variable_name]['score'] = value_score

    patient['risk'] = risk_score(patient)
    patient['patient_id'] = str(uuid.uuid4())

    return patient

def risk_score(patient):
    risk_score = 0
    for variable_name in patient:

        value = patient[variable_name]['value']
        score = patient[variable_name]['score']

        # hierarchy has two levels for intoxicants, one level for everything else.
        if variable_name == 'intoxicant':
            standard_name = slugify(value.lower(), separator='_')
        else:
            standard_name = slugify(variable_name.lower(), separator='_')
        weight = flattened_kernel[standard_name]
        risk_score += (score * weight)

    return risk_score
