import os
import random
import uuid

from slugify import slugify
from yaml import safe_load

'''
1. Don't use absolute paths. They don't transfer well between systems. Use relative paths.
2. Use os.path.join() to join paths. Unix, older Macs, and Windows use different path separators.
'''


project_path = os.path.join('..','..',) #   Relative to src/for_model 
DATA_PATH = os.path.join(project_path, 'data', 'for_model')

PATH_TO_PREDICTIVE_VARIABLES = os.path.join(DATA_PATH, 'predictive_variables.yml')
predictive_variables = safe_load(open(PATH_TO_PREDICTIVE_VARIABLES, 'r'))

variable_numeric_range = os.path.join(DATA_PATH, 'variable_numeric_range.yml')

score = {variable['value']: {value['name']: value['value']
         for value in safe_load(open(os.path.join(DATA_PATH, f"{variable['value']}_values.yml"), 'r'))}
         for variable in predictive_variables}


def create_patient():
    patient = {}
    for variable in predictive_variables:
        variable_name = variable['value']

        value_numeric = random.int(variable_range[variable_name]['min'],
                                   variable_name[variable_name]['max'])
        value_name, value_score = random.choice(list(score[variable_name].items()))


        patient[variable_name] = {}
        patient[variable_name]['value'] = value_name
        patient[variable_name]['score'] = value_score

    patient['risk'] = sum([patient[variable_name]['score'] for variable_name in patient])
    patient['patient_id'] = str(uuid.uuid4())

    return patient
