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

def simulate_cirrhosis(context):
    # simple comment
    platelet = context.get('platelet', 200000)
    albumin = context.get('albumin', 4.0)
    ast = context.get('AST', 25)
    alt = context.get('ALT', 20)
    inr = context.get('INR', 1.0)

    diagnostic_criteria = (
        platelet < 150000 and
        albumin < 3.5 and
        ast > alt and
        inr > 1.2
    )

    if diagnostic_criteria:
        return random.choices([True, False], weights=[0.2, 0.8])[0]
    else:
        return random.choices([True, False], weights=[0.02, 0.98])[0]

def simulate_patient_value(variable_name, context=None):
    if context is None:
        context = {}

    if variable_name == 'hr':
        return random.randint(20, 240)
    elif variable_name == 'sbp':
        return random.randint(70, 240)
    elif variable_name == 'gcs':
        return random.randint(3, 15)
    elif variable_name == 'age':
        return random.randint(18, 100)
    elif variable_name == 'platelet':
        return random.randint(50_000, 400_000)
    elif variable_name == 'albumin':
        return round(random.uniform(2.0, 5.0), 2)
    elif variable_name == 'AST':
        return random.randint(10, 300)
    elif variable_name == 'ALT':
        return random.randint(10, 300)
    elif variable_name == 'INR':
        return round(random.uniform(0.9, 2.5), 2)
    elif variable_name == 'intoxicant':
        return random.choice(['Alcohol', 'Analgesic', 'Antidepressant', 'Street Drugs', 'Sedatives', 'CO, As, CN', 'Toxins NOS', 'Polysubstance'])
    elif variable_name == 'second_diagnose':
        return random.choice([True, False])
    elif variable_name == 'cirrhosis':
        return simulate_cirrhosis(context)
    elif variable_name == 'dysrhythmia':
        return random.choices([True, False], weights=[0.05, 0.95])[0]
    elif variable_name == 'respiratory':
        return random.choices([True, False], weights=[0.1, 0.9])[0]
    else:
        raise ValueError(f"Variable {variable_name} not found")





def score_from_value(variable_name, variable_value):
    relevant_variable = name_to_score[variable_name]
    if relevant_variable['criteria'] == 'categorical':
        payload = [item for item in relevant_variable['values'] if variable_value == item['name']]
        if len(payload) == 0:
            raise ValueError(f"Value {variable_value} not found in {variable_name}")
        else:
            return payload[0]['score']
    elif relevant_variable['criteria'] == 'range':
        payload = [item for item in relevant_variable['values'] if variable_value >= item['min'] and variable_value <= item['max']]
        if len(payload) == 0:
            raise ValueError(f"Value {variable_value} not found in range for {variable_name}")
        else:
            return payload[0]['score']


def create_patient():
    patient = {}
    patient['presentation'] = []
    context = {}

    for variable in predictive_variables:
        name = variable['value']
        value = simulate_patient_value(name, context)
        context[name] = value  # Save for dependency-aware logic
        score = score_from_value(name, value)
        patient['presentation'].append({'name': name, 'score': score, 'value': value})

    patient['risk'] = sum([feature['score'] for feature in patient['presentation']])
    patient['patient_id'] = str(uuid.uuid4())

    return patient
