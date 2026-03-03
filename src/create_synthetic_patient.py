import os
import uuid
import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from scipy.stats import truncnorm
from yaml import safe_load
from rich import print

DATA_PATH = os.path.join("..", "data", "model")


# ----------------------------
# Loading
# ----------------------------
def load_simulation_variables(filename: str = "predictive_variables.yml") -> List[Dict[str, Any]]:
    path = os.path.join(DATA_PATH, filename)
    with open(path, "r") as f:
        return safe_load(f)


def create_name_to_score_dict(predictive_variables: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    out = {}
    for variable in predictive_variables:
        name = variable["name"]
        score_path = os.path.join(DATA_PATH, f"{name}_score.yml")
        with open(score_path, "r") as f:
            out[name] = safe_load(f)
    return out


# ----------------------------
# Sampling helpers
# ----------------------------
def _truncnorm_sample(a: float, b: float, mean: float, sd: float) -> float:
    # guard against sd=0
    sd = max(sd, 1e-6)
    return truncnorm.rvs((a - mean) / sd, (b - mean) / sd, loc=mean, scale=sd)


def truncnorm_int(a: int, b: int, mean: float, sd: float) -> int:
    x = _truncnorm_sample(a, b, mean, sd)
    return int(round(x))


def clip(x: float, lo: float, hi: float) -> float:
    return float(min(max(x, lo), hi))


def weighted_choice(options: List[Any], probs: List[float]) -> Any:
    probs = np.array(probs, dtype=float)
    probs = probs / probs.sum()
    return np.random.choice(options, p=probs)


# ----------------------------
# Scoring 
# ----------------------------
def score_from_value(value: Any, score_table: Dict[str, Any]) -> int:
    criteria = score_table["criteria"]
    if criteria == "categorical":
        return score_categorical_value(value, score_table)
    if criteria == "range":
        return score_continuous_value(value, score_table)
    raise ValueError(f"Unknown score criteria: {criteria}")


def score_categorical_value(value: Any, score_table: Dict[str, Any]) -> int:
    if isinstance(value, np.bool_):
        value = "Yes" if value else "No"
    payload = [item for item in score_table["values"] if value == item["name"]]
    if not payload:
        raise ValueError(f"Value '{value}' not found in categorical score table.")
    return int(payload[0]["score"])


def score_continuous_value(value: float, score_table: Dict[str, Any]) -> int:
    payload = [item for item in score_table["values"] if item["min"] <= value <= item["max"]]
    if not payload:
        raise ValueError(f"Value '{value}' not found in range score table.")
    return int(payload[0]["score"])


# ----------------------------
# Legacy code with independent sampling
# ----------------------------
def simulate_categorical_independent(variable: Dict[str, Any]) -> Any:
    if "dist" in variable:
        options, probs = zip(*[(item["value"], item["probability"]) for item in variable["dist"]])
        v = np.random.choice(options, p=probs)
    else:
        v = random.choice(variable["allowed_values"])
    return normalize_bool(v) 

def simulate_continuous_independent(variable: Dict[str, Any]) -> float:
    lo = float(variable["allowed_values"]["min"])
    hi = float(variable["allowed_values"]["max"])
    mean = (lo + hi) / 2.0
    sd = (hi - lo) / 6.0
    return float(truncnorm_int(int(lo), int(hi), mean, sd))

# ----------------------------
#  Simulation with latent severity 
# ----------------------------
@dataclass
class Context:
    intoxicant: Optional[str] = None
    severity: Optional[int] = None
    gcs: Optional[int] = None
    respiratory: Optional[str] = None
    dysrhythmia: Optional[str] = None
    hr_true: Optional[int] = None
    sbp_true: Optional[int] = None


def sample_severity(intoxicant: str) -> int:
    """
    Latent severity 0..3. Bias by intoxicant category.
    Tune these base distributions to match your cohort.
    """
    base = {
        "Alcohol":        [0.60, 0.25, 0.12, 0.03],
        "Analgesic":      [0.45, 0.28, 0.18, 0.09],
        "Antidepressant": [0.45, 0.30, 0.18, 0.07],
        "Street Drugs":   [0.45, 0.30, 0.17, 0.08],
        "Sedatives":      [0.40, 0.28, 0.22, 0.10],
        "CO, As, CN":     [0.35, 0.30, 0.22, 0.13],
        "Toxins NOS":     [0.45, 0.30, 0.18, 0.07],
        "Polysubstance":  [0.30, 0.30, 0.25, 0.15],
    }.get(intoxicant, [0.45, 0.30, 0.18, 0.07])

    return int(weighted_choice([0, 1, 2, 3], base))


def sample_gcs_from_bins(score_table_gcs: Dict[str, Any], intoxicant: str, severity: int) -> int:
    """
    Uses your GCS score bins (range table) as the natural buckets,
    but sets bucket probabilities by severity/intoxicant.

    score_table_gcs['values'] has bins like:
      [14-15], [9-13], [7-8], [0-6]
    """
    bins = score_table_gcs["values"]
    # Normalize bins into a consistent order: best -> worst by max value
    bins_sorted = sorted(bins, key=lambda b: b["max"], reverse=True)  # 15, 13, 8, 6

    # Map: severity -> probabilities across bins_sorted
    # bins_sorted order: (14-15), (9-13), (7-8), (<=6)
    sev_probs = {
        0: [0.82, 0.14, 0.03, 0.01],
        1: [0.55, 0.28, 0.12, 0.05],
        2: [0.28, 0.35, 0.22, 0.15],
        3: [0.06, 0.22, 0.34, 0.38],
    }[severity]

    # intoxicant tweaks (optional, light touch)
    if intoxicant in ["Sedatives", "Analgesic", "Alcohol", "Polysubstance"]:
        sev_probs = np.array(sev_probs) * np.array([0.85, 1.10, 1.15, 1.25])
    elif intoxicant in ["Street Drugs"]:
        sev_probs = np.array(sev_probs) * np.array([1.10, 1.05, 0.90, 0.80])
    else:
        sev_probs = np.array(sev_probs)

    sev_probs = (sev_probs / sev_probs.sum()).tolist()
    chosen_bin = weighted_choice(bins_sorted, sev_probs)

    lo, hi = int(chosen_bin["min"]), int(chosen_bin["max"])
    # Uniform within bin is fine; you can make it skewed later.
    return int(np.random.randint(lo, hi + 1))


def sample_respiratory(gcs: int, intoxicant: str, severity: int) -> str:
    """
    Respiratory failure should cluster with low GCS and CNS depressants.
    """
    p = 0.05 + 0.07 * severity

    if gcs <= 8:
        p += 0.45
    if gcs <= 6:
        p += 0.20

    if intoxicant in ["Sedatives", "Analgesic", "Alcohol", "Polysubstance"]:
        p += 0.12

    if intoxicant in ["CO, As, CN"]:
        p += 0.05

    return "Yes" if np.random.rand() < min(p, 0.95) else "No"


def sample_dysrhythmia(intoxicant: str, severity: int) -> str:
    """
    Dysrhythmia should be more common in antidepressants, street drugs, and severe cases.
    """
    p = 0.06 + 0.06 * severity

    if intoxicant in ["Antidepressant", "Street Drugs", "CO, As, CN"]:
        p += 0.10
    if intoxicant == "Polysubstance":
        p += 0.07

    return "Yes" if np.random.rand() < min(p, 0.60) else "No"


def sample_hr_true(intoxicant: str, severity: int, dysrhythmia: str, respiratory: str) -> int:
    """
    Mixture model: normal cluster + abnormal cluster.
    """
    # Normal mode
    mu1, sd1 = 85, 12

    # Abnormal mode: toxidrome-ish shift
    if intoxicant == "Street Drugs":
        mu2 = 145
    elif intoxicant in ["Sedatives", "Analgesic", "Alcohol"]:
        mu2 = 62
    elif intoxicant == "Antidepressant":
        mu2 = 120
    else:
        mu2 = 110

    sd2 = 28

    p_abn = 0.10 + 0.15 * severity
    if dysrhythmia == "Yes":
        p_abn += 0.20
    if respiratory == "Yes":
        p_abn += 0.10

    if np.random.rand() < min(p_abn, 0.90):
        x = np.random.normal(mu2, sd2)
    else:
        x = np.random.normal(mu1, sd1)

    return int(round(clip(x, 40, 250)))


def sample_sbp_true(intoxicant: str, severity: int, hr_true: int) -> int:
    """
    SBP: shift up for stimulants, down for CNS depressants; more variance with severity.
    """
    mu = 125.0

    if intoxicant == "Street Drugs":
        mu += 18
    if intoxicant in ["Sedatives", "Analgesic", "Alcohol"]:
        mu -= 10
    if intoxicant == "Polysubstance":
        mu -= 6

    mu -= 9 * severity

    # Light coupling: very high HR nudges SBP down in severe illness (optional)
    if severity >= 2 and hr_true >= 140:
        mu -= 6

    sd = 14 + 6 * severity
    x = np.random.normal(mu, sd)

    return int(round(clip(x, 60, 220)))


def chart_rounding(name: str, value: Any) -> Any:
    """
    Optional: make numbers look charted in EHR (heaping).
    """
    if name == "sbp":
        # many devices are effectively even numbers
        return int(round(value / 2.0) * 2)
    if name == "hr":
        return int(value)  # already integer
    return value


def plausible(ctx: Context) -> bool:
    if ctx.gcs is None or ctx.respiratory is None or ctx.hr_true is None or ctx.sbp_true is None:
        return True

    # Very low GCS with no respiratory failure is uncommon in tox.
    if ctx.gcs <= 6 and ctx.respiratory == "No":
        return np.random.rand() < 0.25  # allow but rare

    # Respiratory failure with normal mentation is less common.
    if ctx.respiratory == "Yes" and ctx.gcs >= 14:
        return np.random.rand() < 0.20

    # Low BP + low HR is uncommon without beta-blocker/AV block context.
    if ctx.sbp_true <= 80 and ctx.hr_true <= 55:
        return np.random.rand() < 0.30

    return True


# ----------------------------
# Value generation with context
# ----------------------------
def simulate_value_with_context(
    variable: Dict[str, Any],
    ctx: Context,
    name_to_score: Dict[str, Dict[str, Any]],
) -> Tuple[Any, Optional[Any]]:
    name = variable["name"]

    # 1) intoxicant first
    if name == "intoxicant":
        v = simulate_categorical_independent(variable)
        ctx.intoxicant = str(v)
        return v, None

    # 2) age (keep simple but not uniform; you can make this empirical later)
    if name == "age":
        lo = int(variable["allowed_values"]["min"])
        hi = int(variable["allowed_values"]["max"])
        # mild right-skew in adult ED cohorts
        a = np.random.beta(2.2, 3.0)  # 0..1
        v = int(round(lo + a * (hi - lo)))
        return v, None

    # 3) severity is latent (not in YAML). We'll set it lazily once intoxicant exists.
    if ctx.severity is None and ctx.intoxicant is not None:
        ctx.severity = sample_severity(ctx.intoxicant)

    # 4) gcs depends on severity + intoxicant, using your score bins
    if name == "gcs":
        gcs_table = name_to_score["gcs"]
        v = sample_gcs_from_bins(gcs_table, ctx.intoxicant or "Polysubstance", ctx.severity or 1)
        ctx.gcs = int(v)
        return int(v), None

    # 5) respiratory depends on gcs + intoxicant + severity
    if name == "respiratory":
        g = ctx.gcs if ctx.gcs is not None else 15
        v = sample_respiratory(g, ctx.intoxicant or "Polysubstance", ctx.severity or 1)
        ctx.respiratory = v
        return v, None

    # 6) dysrhythmia depends on intoxicant + severity
    if name == "dysrhythmia":
        v = sample_dysrhythmia(ctx.intoxicant or "Polysubstance", ctx.severity or 1)
        ctx.dysrhythmia = v
        return v, None

    # 7) hr depends on intox + severity + dysrhythmia + respiratory
    if name == "hr":
        hr_true = sample_hr_true(
            ctx.intoxicant or "Polysubstance",
            ctx.severity or 1,
            ctx.dysrhythmia or "No",
            ctx.respiratory or "No",
        )

        hr_val = chart_rounding("hr", hr_true)
        ctx.hr_true = int(hr_val)

        return int(hr_val), int(hr_true)

    # 8) sbp depends on intox + severity + hr_true
    if name == "sbp":
        hr_true = ctx.hr_true if ctx.hr_true is not None else 90
        sbp_true = sample_sbp_true(ctx.intoxicant or "Polysubstance", ctx.severity or 1, hr_true)

        sbp_obs = chart_rounding("sbp", sbp_true)
        ctx.sbp_true = int(sbp_obs)
        return sbp_obs, sbp_true

    if variable["type"] == "categorical":
        return simulate_categorical_independent(variable), None
    if variable["type"] == "continuous":
        return simulate_continuous_independent(variable), None

    raise ValueError(f"Unknown variable type: {variable.get('type')}")

def normalize_bool(value):
    if isinstance(value, (bool, np.bool_)):
        return "Yes" if value else "No"
    return value

def is_value_in_range(value: Any, variable: Dict[str, Any]) -> bool:
    if variable["type"] == "categorical":
        return True
    if value is None:
        return True

    lo = float(variable["allowed_values"]["min"])
    hi = float(variable["allowed_values"]["max"])
    return lo <= float(value) <= hi


# ----------------------------
# Patient creation
# ----------------------------
def create_patient(predictive_variables: List[Dict[str, Any]], name_to_score: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Creates a patient with:
      - presentation list (like your current output)
      - risk score (sum of feature scores)
      - extras: latent severity, and true vitals when generated outside scoring bounds
    """
    patient: Dict[str, Any] = {
        "presentation": [],
        "patient_id": str(uuid.uuid4()),
        "extras": {},
    }

    ctx = Context()

    order = [
        "intoxicant",
        "age",
        "cirrhosis",
        "second_diagnose",
        "gcs",
        "respiratory",
        "dysrhythmia",
        "hr",
        "sbp",
    ]
    var_by_name = {v["name"]: v for v in predictive_variables}

    remaining = [v["name"] for v in predictive_variables if v["name"] not in order]
    full_order = order + remaining

    max_attempts = 10
    for attempt in range(max_attempts):
        patient["presentation"] = []
        ctx = Context()

        for name in full_order:
            variable = var_by_name[name]
            value, true_value = simulate_value_with_context(variable, ctx, name_to_score)

            if true_value is None:
                in_original_range = True 
            else:
                in_range = is_value_in_range(true_value, variable)
            
            entry = {"name": name,"value": value}

            entry["score"] = score_from_value(value, name_to_score[name])

            if variable["type"] == "categorical":
                entry["in_original_range"] = True

            else:
                entry["true_value"] = true_value
                entry["in_original_range"] = bool(is_value_in_range(true_value, variable))
                entry["model_range"] = {
                    "min": float(variable["allowed_values"]["min"]),
                    "max": float(variable["allowed_values"]["max"]),
                }

            patient["presentation"].append(entry)

        patient["extras"]["severity"] = ctx.severity
        patient["extras"]["hr_true"] = ctx.hr_true
        patient["extras"]["sbp_true"] = ctx.sbp_true

        if plausible(ctx):
            break

    patient["risk"] = int(sum(feature["score"] for feature in patient["presentation"]))
    return patient

def clip_to_model_range(true_value: float, variable: Dict[str, Any]) -> float:
    lo = float(variable["allowed_values"]["min"])
    hi = float(variable["allowed_values"]["max"])
    return float(min(max(true_value, lo), hi))

def simple_patient_display(patient: Dict[str, Any]) -> None:
    print(f"Risk Score: {patient['risk']}")
    for feature in patient["presentation"]:
        name = feature["name"]
        value = feature["value"]
        score = feature["score"]
        in_range = "in range" if feature["in_original_range"] else "out of range"
        print(f"  - {name}: {value} (score: {score}, {in_range})")

if __name__ == "__main__":
    simulation_variables = load_simulation_variables()
    name_to_score = create_name_to_score_dict(simulation_variables)

    pt = create_patient(simulation_variables, name_to_score)
    # print(pt)
    simple_patient_display(pt)
