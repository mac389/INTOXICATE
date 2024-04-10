import os 

import create_synthetic_patient as csp


def test_create_patient():
    patient = csp.create_patient()
    print(patient)

test_create_patient()
