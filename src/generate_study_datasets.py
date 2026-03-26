import json
import random
from collections import defaultdict

INPUT = "../data/synthetic_patient_db.v2.jsonl"
OUTPUT_ICU = "../data/icu_dataset.json"
OUTPUT_EQ = "../data/equivalence_dataset.json"

SEED = 42
random.seed(SEED)


def load_data():
    with open(INPUT) as f:
        return [json.loads(line) for line in f]


def get_score(p):
    return p.get("risk")


def is_icu(p):
    return get_score(p) > 6


def build_icu_dataset(patients):
    icu = [p for p in patients if is_icu(p)]
    non = [p for p in patients if not is_icu(p)]

    icu_sample = random.sample(icu, 60)
    non_sample = random.sample(non, 340)

    selected = icu_sample + non_sample
    random.shuffle(selected)

    return [str(p["patient_id"]) for p in selected]


def build_equivalence_dataset(patients, excluded_ids):
    patients = [p for p in patients if str(p["patient_id"]) not in excluded_ids]

    # group by score
    by_score = defaultdict(list)
    for p in patients:
        by_score[get_score(p)].append(p)

    used = set()
    pairs = []

    # ---------- SAME (equivalent) ----------
    same_pairs = []
    for score, lst in by_score.items():
        random.shuffle(lst)
        for i in range(0, len(lst) - 1, 2):
            a, b = lst[i], lst[i + 1]
            if a["patient_id"] in used or b["patient_id"] in used:
                continue

            # ensure no threshold crossing within 1 point
            if abs(get_score(a) - get_score(b)) <= 1:
                if (get_score(a) > 6) != (get_score(b) > 6):
                    continue

            same_pairs.append((a, b))
            used.add(a["patient_id"])
            used.add(b["patient_id"])

            if len(same_pairs) == 100:
                break
        if len(same_pairs) == 100:
            break

    # ---------- DIFFERENT ----------
    remaining = [p for p in patients if p["patient_id"] not in used]
    random.shuffle(remaining)

    diff_pairs = []
    attempts = 0

    while len(diff_pairs) < 100 and attempts < 100000:
        a, b = random.sample(remaining, 2)

        if a["patient_id"] in used or b["patient_id"] in used:
            attempts += 1
            continue

        if get_score(a) == get_score(b):
            attempts += 1
            continue

        diff_pairs.append((a, b))
        used.add(a["patient_id"])
        used.add(b["patient_id"])

    assert len(same_pairs) == 100, "Not enough equivalent pairs"
    assert len(diff_pairs) == 100, "Not enough different pairs"

    pairs = same_pairs + diff_pairs
    random.shuffle(pairs)

    return [
        {
            "left_id": str(a["patient_id"]),
            "right_id": str(b["patient_id"]),
            "model_same": abs(get_score(a) - get_score(b)) <= 1
            and ((get_score(a) > 6) == (get_score(b) > 6)),
        }
        for a, b in pairs
    ]


def main():
    patients = load_data()

    icu_ids = build_icu_dataset(patients)
    eq_pairs = build_equivalence_dataset(patients, set(icu_ids))

    with open(OUTPUT_ICU, "w") as f:
        json.dump(icu_ids, f, indent=2)

    with open(OUTPUT_EQ, "w") as f:
        json.dump(eq_pairs, f, indent=2)

    print("Done.")


if __name__ == "__main__":
    main()
