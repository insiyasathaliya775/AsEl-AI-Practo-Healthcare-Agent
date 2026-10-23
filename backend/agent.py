
import csv
from pathlib import Path

from rag import build_index, search_policies

ROOT = Path(__file__).resolve().parent
APPOINTMENTS_FILE = ROOT / "appointments.csv"


def load_appointments():
    with open(APPOINTMENTS_FILE, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def answer_question(question, collection, model):
    question_lower = question.lower()
    appointments = load_appointments()

    # Handle follow-up questions first.
    if "follow-up" in question_lower or "follow up" in question_lower:
        count = sum(
            row.get("follow_up_required", "").strip().lower()
            in {"true", "1", "yes"}
            for row in appointments
        )
        return (
            f"{count} of {len(appointments)} synthetic records "
            "are marked as requiring follow-up."
        )

    appointment_keywords = [
        "appointment", "booking", "scheduled", "cancelled",
        "canceled", "reschedule", "doctor", "specialist"
    ]

    if (
        any(word in question_lower for word in appointment_keywords)
        and ("how many" in question_lower or "total" in question_lower)
    ):
        return (
            f"The dataset contains {len(appointments)} "
            "synthetic appointment records."
        )

    results = search_policies(question, collection, model, top_k=3)

    if not results:
        return "I couldn't find a relevant policy. Please contact support."

    sources = "\n".join(
        f"- {item['source']}: {item['text']}" for item in results
    )

    return (
        "Relevant information from the fictional support policies:\n\n"
        f"{sources}\n\n"
        "Confirm booking details through the relevant booking system. "
        "For emergencies, seek appropriate medical care."
    )


if __name__ == "__main__":
    collection, model = build_index()
    print("Healthcare Support Agent ready. Type 'exit' to quit.")

    while True:
        question = input("\nYou: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        if not question:
            continue

        try:
            print("\nAgent:", answer_question(question, collection, model))
        except Exception as error:
            print("Could not answer the question:", error)
