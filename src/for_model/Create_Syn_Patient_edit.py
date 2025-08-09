import os
import random
import uuid

import numpy as np
from scipy.stats import truncnorm
from yaml import safe_load

DATA_PATH = os.path.join('..','..', 'data', 'for_model')

PATH_TO_PREDICTIVE_VARIABLES = os.path.join(DATA_PATH, 'predictive_variables.yml')
predictive_variables = safe_load(open(PATH_TO_PREDICTIVE_VARIABLES, 'r'))

name_to_score = {variable['value']: safe_load(open(os.path.join(DATA_PATH,
                                f"{variable['value']}_score.yml"), 'r')) 
                                for variable in predictive_variables}

allowable_range = {variable['value']: variable['allowed_values'] for variable in predictive_variables}

PATH_TO_SIMULATION_VARIABLES = os.path.join(DATA_PATH, 'simulation_variables.yml')
simulation_variables = safe_load(open(PATH_TO_SIMULATION_VARIABLES, 'r'))

print("Loaded simulation variables:", simulation_variables)
def simulate_patient_value_i(variable_name):
    var = [item for item in simulation_variables if item['name'] == variable_name]
    if len(var) == 0:
        raise ValueError(f"Variable {variable_name} not found in simulation variables")
    else:
        var = var[0]

    if var['type'] == 'categorical':
        if 'values' in var:
            if isinstance(var['values'][0], int):
                return random.choice(var['values'])
            elif isinstance(var['values'][0], dict):
                options, probs = zip(*[(item['value'], item['probability']) for item in var['values']])
                return np.random.choice(options, p=probs)
        else:
            return random.choice(allowable_range[variable_name])
    elif var['type'] == 'continuous':
        if var['distribution']['type'] == 'normal':
            mean = var['distribution']['mean']
            std_dev = var['distribution']['stddev']
            lower_bound = allowable_range[var['name']]['min']
            upper_bound = allowable_range[var['name']]['max']
            return int(truncnorm.rvs(
                (lower_bound - mean) / std_dev,
                (upper_bound - mean) / std_dev,
                loc=mean,
                scale=std_dev
            ))
def is_value_in_range(value, score_data):
    for entry in score_data.get("values", []):
        min_val = entry.get("min")
        max_val = entry.get("max")
        if min_val is not None and max_val is not None:
            if min_val <= value <= max_val:
                return True
    return False

def score_from_value(variable_name, variable_value):
    relevant_variable = name_to_score[variable_name]

    # Add this block to determine if value is in range
    in_range = is_value_in_range(variable_value, relevant_variable)
    range_flag = "in range" if in_range else "out of range"

    if range_flag == 'in range':
        payload = []
        if relevant_variable['criteria'] == 'categorical':
            payload = [item for item in relevant_variable['values'] if variable_value == item['name']]
        elif relevant_variable['criteria'] == 'range':
            payload = [item for item in relevant_variable['values'] if variable_value >= item['min'] and variable_value <= item['max']]
        return payload[0]['score'], range_flag
    else:
        return 0, range_flag


def create_patient():
    patient = {}
    patient['presentation'] = []

    for variable in predictive_variables:
        name = variable['value']
        value = simulate_patient_value_i(name)
        score, range_flag = score_from_value(name, value)

        if name in name_to_score:
            score_data = name_to_score[name]
            in_range = is_value_in_range(value, score_data)
            range_flag = "in range" if in_range else "out of range"
        else:
            range_flag = "unknown"

        # Add range_flag into the presentation list
        patient['presentation'] += [{
            'name': name,
            'score': score,
            'value': value,
            'range_flag': range_flag
        }]

    patient['risk'] = sum([feature['score'] for feature in patient['presentation']])
    patient['patient_id'] = str(uuid.uuid4())

    return patient



