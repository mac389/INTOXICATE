import os

DATA_DIR = os.path.join('..','data')
MODEL_DIR   = os.path.join(DATA_DIR, 'model')
SCHEMA_YML  = os.path.join(MODEL_DIR, 'predictive_variables.yml')

with open(SCHEMA_YML) as mf:
    predictive_variables = yaml.safe_load(mf)

name_to_score = {}
for var in predictive_variables:
    name   = var['value']
    score_file = os.path.join(MODEL_DIR, f"{name}_score.yml")
    with open(score_file) as sf:
        name_to_score[name] = yaml.safe_load(sf)

def score_from_value(name, value):
    tbl = name_to_score.get(name)
    if not tbl:
        raise ValueError(f"No scoring table for `{name}`")

    if isinstance(value, bool):
        v = 'yes' if value else 'no'
    else:
        v = str(value).strip().lower()

    if tbl['criteria'] == 'categorical':
        for it in tbl['values']:
            nm = it['name']
            if isinstance(nm, bool):
                nm = 'yes' if nm else 'no'
            nm_s = str(nm).strip().lower()

            rep = it.get('representation', nm)
            if isinstance(rep, bool):
                rep = 'yes' if rep else 'no'
            rep_s = str(rep).strip().lower()

            if v == nm_s or v == rep_s:
                return it['score']

    else:
        try:
            x = float(value)
        except Exception:
            raise ValueError(f"Field `{name}` must be numeric")
        for it in tbl['values']:
            if it['min'] <= x <= it['max']:
                return it['score']

    # 4) Nothing matched
    raise ValueError(f"Value `{value}` not found for `{name}`")

def underage(raw_patient):
    """Check if the patient is under 12 years old."""
    age = next((feat['value'] for feat in raw_patient.get('presentation', [])
                if feat['name'] == 'age'), None)
    if age is None:
        raise ValueError("Missing age in patient data")
    try:
        return float(age) < 12.0
    except ValueError:
        raise ValueError(f"Invalid age value: {age}")

# ── 4) compute_score over the full raw_patient ────────────────────────────────
def compute_score(raw_patient):
    print(f"Computing score for patient {raw_patient}", flush=True)
    return sum(score_from_value(feat['name'], feat['value'])
        for feat in raw_patient.get('presentation', [])) if not underage(raw_patient) else 0

# ── 5) ICU threshold ───────────────────────────────────────────────────────────
THRESHOLD = 6.0
RECALIBRATED_THRESHOLD = 16.0 

# ── 6) Utility to flatten for template rendering ───────────────────────────────
def flatten_patient(raw):
    pres = {e['name']: e['value'] for e in raw.get('presentation', [])}
    return {
        'id':         raw.get('patient_id'),
        'age':        pres.get('age'),
        'gcs':        pres.get('gcs'),
        'hr':         pres.get('hr'),
        'sbp':        pres.get('sbp'),
        'intoxicant': pres.get('intoxicant'),
        'second_diagnose': pres.get('second_diagnose'),
        'cirrhosis':  pres.get('cirrhosis'),
        'respiratory':pres.get('respiratory'),
        'dysrhythmia':pres.get('dysrhythmia'),
        'score':      raw.get('risk') if 'risk' in raw else compute_score(raw)
}

