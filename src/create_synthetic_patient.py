import random
import os
import uuid
import numpy as np
from scipy.stats import truncnorm

from yaml import safe_load

DATA_PATH = os.path.join('..', 'data', 'model')

def load_simulation_variables(filename="predictive_variables.yml"):
    path = os.path.join(DATA_PATH, filename)
    return safe_load(open(path, 'r'))

def create_name_to_score_dict(predictive_variables):
    return {variable['name']: safe_load(open(os.path.join(DATA_PATH,
                                f"{variable['name']}_score.yml"), 'r')) 
                                for variable in predictive_variables}

def simulate_patient_value(variable):
    if variable['type'] == 'categorical':
        return simulate_categorical_variable(variable)
    elif variable['type'] == 'continuous':
        return simulate_continuous_variable(variable)
    else:
        raise ValueError(f"Unknown variable type: {variable['type']}")

def simulate_categorical_variable(variable):
    if 'dist' in variable:
        options, probs = zip(*[(item['value'], item['probability']) for item in variable['dist']])
        return np.random.choice(options, p=probs)
    else: 
        return random.choice(variable['allowed_values'])

def simulate_continuous_variable(var):
    if 'dist' in var:
        pass # Future implementation for custom distributions
    else: #Default is normal distribution
        lower_bound = var['allowed_values']['min']
        upper_bound = var['allowed_values']['max']
        
        # no mean and std_dev provided
        # use midpoint and 1/6th of range as std_dev
        mean = (lower_bound + upper_bound) / 2
        std_dev = (upper_bound - lower_bound) / 6
        return int(truncnorm.rvs( #
            (lower_bound - mean) / std_dev,
            (upper_bound - mean) / std_dev,
            loc=mean,
            scale=std_dev
        ))

def score_from_value(value, score_table):
    if score_table['criteria'] == 'categorical':
        return score_categorical_value(value, score_table)
    elif score_table['criteria'] == 'range':
        return score_continuous_value(value, score_table)
    else:
        raise ValueError(f"Unknown variable type: {variable['type']}")

def score_categorical_value(value, score_table):
    if isinstance(value, np.bool_):
        value = "Yes" if value else "No"
    payload = [item for item in score_table['values'] if value == item['name']]
    return payload[0]['score']

def score_continuous_value(value, score_table):
    payload = [item for item in score_table['values'] if item['min'] <= value <= item['max']] 
    return payload[0]['score']

def is_value_in_range(value, variable):
    if variable['type'] == 'categorical':
        return value in variable['allowed_values']
    elif variable['type'] == 'continuous':
        min_allowed = variable['allowed_values']['min'] 
        max_allowed = variable['allowed_values']['max']
        return min_allowed <= value <= max_allowed
    else:
        raise ValueError(f"Unknown variable type: {variable['type']}")

def create_patient(predictive_variables, name_to_score):
    patient = {}
    patient['presentation'] = []
    patient['patient_id'] = str(uuid.uuid4())

    for variable in predictive_variables:
        name = variable['name']
        value = simulate_patient_value(variable)
        score = score_from_value(value, name_to_score[variable['name']])

        patient['presentation'] += [{
            'name': name,
            'score': score,
            'value': value,
            'in_original_range': bool(is_value_in_range(value, variable))
        }]

    patient['risk'] = sum([feature['score'] for feature in patient['presentation']])

    return patient

#sample size calculation 
#how do we want to describe the final results and work backwards
    #how would physicians perceive the database - what stats should we use/ plots 
    # ? is this patient realistic/ plausible or not - can they distinguish between synthetic and real patient 
    
if __name__ == "__main__":
    simulation_variables = load_simulation_variables()
    name_to_score = create_name_to_score_dict(simulation_variables)

    pt = create_patient(simulation_variables, name_to_score)
    print(pt)

