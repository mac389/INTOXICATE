import random
import os
import uuid

from yaml import safe_load

project_path = os.path.join('..', '..')
DATA_PATH = os.path.join(project_path, 'data', 'for_model')

PATH_TO_PREDICTIVE_VARIABLES = os.path.join(DATA_PATH, 'predictive_variables.yml')
predictive_variables = safe_load(open(PATH_TO_PREDICTIVE_VARIABLES, 'r'))

name_to_score = {variable['value']: safe_load(open(os.path.join(DATA_PATH,
                                f"{variable['value']}_score.yml"), 'r')) 
                                for variable in predictive_variables}

allowable_range = {variable['value']: variable['allowed_values'] for variable in predictive_variables}


def simulate_patient_value(variable_name):
    if isinstance(allowable_range[variable_name], list):
        return random.choice(allowable_range[variable_name])
    elif isinstance(allowable_range[variable_name], dict):
        min_value = allowable_range[variable_name]['min']
        max_value = allowable_range[variable_name]['max']
        return random.randint(min_value, max_value)
    else:
        raise ValueError(f"Variable {variable_name} not found")

def score_from_value(variable_name, variable_value):
    relevant_variable = name_to_score[variable_name]
    payload = []
    if relevant_variable['criteria'] == 'categorical':
        payload = [item for item in relevant_variable['values'] if variable_value == item['name']]
    elif relevant_variable['criteria'] == 'range':
        payload = [item for item in relevant_variable['values'] if variable_value >= item['min'] and variable_value <= item['max']]
    if len(payload) == 0:
            raise ValueError(f"Value {variable_value} not found in range for {variable_name}")
    else:
        return payload[0]['score']


def create_patient():
    patient = {}
    patient['presentation'] = []
    for variable in predictive_variables:
        name = variable['value']
        value = simulate_patient_value(name)
        score = score_from_value(name, value)
        patient['presentation'] += [{'name': name, 'score': score, 'value': value}]

    patient['risk'] = sum([feature['score'] for feature in patient['presentation']])
    patient['patient_id'] = str(uuid.uuid4())

    return patient

if __name__ == '__main__':
    patient = create_patient()
    print(patient)
