
"""
AsEl-AI Practo Healthcare Capstone
Part 1, Task 1: Synthetic appointment dataset
All records are fictional and generated locally.
"""

import random
from collections import Counter

CATEGORIES = [
    "General Medicine",
    "Cardiology",
    "Dermatology",
    "Pediatrics",
    "Orthopedics",
]

STATUSES = [
    "Scheduled",
    "Completed",
    "Cancelled",
    "No-Show",
    "Rescheduled",
]

# Relative generation weights for each category and status.
CATEGORY_WEIGHTS = [20, 20, 20, 20, 20]
STATUS_WEIGHTS = [35, 30, 10, 10, 15]

# Synthetic consultation fees in INR, by specialty.
FEE_RANGES = {
    "General Medicine": (300, 700),
    "Cardiology": (600, 1500),
    "Dermatology": (400, 1000),
    "Pediatrics": (350, 800),
    "Orthopedics": (500, 1200),
}

BASE_SEED = 42
RECORD_COUNT = 50


def generate_for_seed(seed):
    """Generate a reproducible dataset for the given seed."""
    rng = random.Random(seed)
    records = []

    for i in range(RECORD_COUNT):
        category = rng.choices(
            CATEGORIES, weights=CATEGORY_WEIGHTS, k=1
        )[0]

        status = rng.choices(
            STATUSES, weights=STATUS_WEIGHTS, k=1
        )[0]

        low, high = FEE_RANGES[category]

        records.append({
            "record_id": f"APPT-{1001 + i}",
            "category": category,
            "status": status,
            "consultation_fee_inr": rng.randrange(
                low, high + 1, 50
            ),
            "days_since_created": rng.randint(0, 30),
            "follow_up_required": rng.random() < 0.20,
        })

    return records


def validate_dataset(records):
    """Check all required dataset constraints."""
    category_counts = Counter(r["category"] for r in records)
    status_counts = Counter(r["status"] for r in records)

    follow_up_count = sum(
        r["follow_up_required"] for r in records
    )
    follow_up_pct = 100 * follow_up_count / len(records)

    valid = (
        len(records) >= 40
        and all(category_counts[c] >= 3 for c in CATEGORIES)
        and all(status_counts[s] >= 1 for s in STATUSES)
        and 10 <= follow_up_pct <= 30
    )

    return valid, category_counts, status_counts, follow_up_pct


# Regenerate with successive deterministic seeds if a constraint fails.
for seed in range(BASE_SEED, BASE_SEED + 1000):
    APPOINTMENTS = generate_for_seed(seed)
    valid, category_counts, status_counts, follow_up_pct = (
        validate_dataset(APPOINTMENTS)
    )

    if valid:
        SELECTED_SEED = seed
        break
else:
    raise RuntimeError("Could not generate a valid dataset.")

if __name__ == "__main__":
    print("Dataset generated successfully!")
    print(f"Selected seed: {SELECTED_SEED}")
    print(f"Total appointments: {len(APPOINTMENTS)}")

    print("\nCounts by category:")
    for category in CATEGORIES:
        print(f"{category}: {category_counts[category]}")

    print("\nCounts by status:")
    for status in STATUSES:
        print(f"{status}: {status_counts[status]}")

    print(f"\nFollow-up required: {follow_up_pct:.1f}%")
    print("\nFirst 3 sample records:")
    for record in APPOINTMENTS[:3]:
        print(record)
