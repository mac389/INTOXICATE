import random
import os
import yaml

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

def create_patient():
    patient = {}
    for variable in predictive_variables:
        variable_name = variable['value']

        PATH_TO_VARIABLE_VALUES = os.path.join(DATA_PATH, f'{variable_name}_values.yml')
        variable_values = yaml.safe_load(open(PATH_TO_VARIABLE_VALUES, 'r'))

        value = random.choice(variable_values)
        value_name = value['name']

        patient[f'{variable_name}_value'] = value_name

    patient['risk'] = risk_score(patient)

    return patient

def risk_score(patient):
    risk_score = 0
    for variable_value in patient:
        variable,value = variable_value.split('_')
        score = score[variable][value]
        weight = kernel[variable]
        risk_score += (score * weight)

    return risk_score


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
