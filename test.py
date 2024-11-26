# -------------------------------
# Tests
# -------------------------------

import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_get_doctor_availability():
    response = client.get("/api/v1/doctor/availability?doctor_id=dr_001")
    assert response.status_code == 200

def test_book_appointment():
    payload = {
        "patient_name": "John Doe",
        "doctor_id": "dr_001",
        "request_type": "consultation",
        "preferred_date": "12/01/2024",
        "preferred_time": "09:00 AM"
    }
    response = client.post("/api/v1/appointments/book", json=payload)
    assert response.status_code == 200
    assert "appointment_id" in response.json()









{
  "patient_name": "john doe",
  "doctor_id": "dr_002",
  "request_type": "consultation",
  "preferred_date": "12/03/2024",
  "preferred_time": "11:00 AM",
  "details": "I have a fever and cough."
}




