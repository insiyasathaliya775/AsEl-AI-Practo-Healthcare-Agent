# AsEl-AI Practo Healthcare Agent

A healthcare support agent capstone prototype that combines Retrieval-Augmented Generation (RAG), semantic search, synthetic appointment data, and a FastAPI interface to answer healthcare support questions.

## Project Overview

The project demonstrates how a healthcare support assistant can retrieve relevant information from policy documents and respond to common appointment-related questions using a structured synthetic dataset.

## Features

- **Policy retrieval:** Searches healthcare support policy documents using semantic embeddings.
- **Knowledge base:** Includes 12 fictional healthcare support policy documents.
- **Appointment dataset:** Uses 50 synthetic appointment records.
- **Follow-up tracking:** Counts records marked as requiring follow-up.
- **REST API:** Provides endpoints through FastAPI.
- **Interactive API documentation:** Allows requests to be tested using Swagger UI.
- **Input validation:** Uses Pydantic to validate chat requests.
- **Emergency guidance:** Directs users to seek appropriate medical care for emergencies.

## Technology Stack

- Python
- Sentence Transformers
- ChromaDB
- FastAPI
- Uvicorn
- Pydantic
- CSV for synthetic appointment data

## Project Structure

```text
AsEl-AI-Practo-Healthcare-Agent/
├── backend/
│   ├── backend/
│   │   └── knowledge_base/
│   │       └── 12 policy documents
│   ├── appointments.csv
│   ├── dataset.py
│   ├── rag.py
│   ├── agent.py
│   └── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup Instructions

### 1. Install Python

Install Python 3.10 or later and verify the installation:

```bash
python --version
```

### 2. Install dependencies

From the project root directory, run:

```bash
python -m pip install -r requirements.txt
```

### 3. Start the API

Run the following command from the project root:

```bash
python -m uvicorn main:app --app-dir backend --reload
```

The API will be available at:

`http://127.0.0.1:8000`

### 4. Open the API documentation

Visit:

`http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Displays the API welcome message |
| GET | `/health` | Checks API health |
| POST | `/chat` | Processes a healthcare support question |

### Example request

Send a POST request to `/chat` with:

```json
{
  "question": "How many appointments require follow-up?"
}
```

### Example response

```json
{
  "answer": "8 of 50 synthetic records are marked as requiring follow-up."
}
```

The response above reflects the current synthetic dataset.

## Testing

The prototype was tested locally using the interactive API documentation. The chat endpoint returned HTTP 200 for the follow-up-count query, and the result matched the dataset count.

Other useful test questions include:

- How many appointments are in the dataset?
- What is the cancellation policy?
- What should I do in a medical emergency?

## Limitations and Responsible Use

- Appointment records are synthetic and do not represent real patients.
- Policy documents are fictional and created for this educational prototype; they are not official Practo policies.
- The prototype does not make real bookings, access a live appointment system, or provide medical diagnoses.
- Retrieved policy information should not replace advice from qualified healthcare professionals.
- Emergency symptoms require appropriate medical attention.

## Future Improvements

- Add a web-based chat interface.
- Improve intent classification and policy retrieval evaluation.
- Add automated unit and API tests.
- Integrate a verified appointment service if authorized.
- Add deployment and monitoring capabilities.

## Disclaimer

This project is an educational capstone prototype. It is not an official Practo product, does not represent official Practo policies, and is not intended for clinical decision-making.
