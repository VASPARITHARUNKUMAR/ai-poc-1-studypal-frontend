# api_client.py

import requests

BASE_URL = "http://localhost:8000"  # Change this if deployed elsewhere


def upload_documents(files, semester, subject):
    """Uploads multiple documents to the backend for processing."""
    files_payload = [("files", (f.name, f.getvalue(), f.type)) for f in files]
    data = {"semester": semester, "subject": subject}

    try:
        response = requests.post(f"{BASE_URL}/upload/", data=data, files=files_payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


def ask_question(question, semester, subject, model):
    """Sends a question to the backend RAG system."""
    payload = {
        "question": question,
        "semester": semester,
        "subject": subject,
        "model": model
    }

    try:
        response = requests.post(f"{BASE_URL}/chat/", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}
