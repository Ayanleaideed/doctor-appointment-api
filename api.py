from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import uuid
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="ADRD Doctor Appointment Management System",
    description="A system for managing doctor profiles, availability, and appointment bookings."
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Models and Schemas
# -------------------------------

class TimeSlot(BaseModel):
    """Model to represent an individual time slot."""
    time: str  # Time in HH:MM AM/PM format


class DoctorProfile(BaseModel):
    """Model to represent a doctor's profile."""
    doctor_id: str
    name: str
    specialization: str
    schedule: Dict[str, List[TimeSlot]]  # Mapping of days to available time slots


class AppointmentRequest(BaseModel):
    """Model to capture a patient's appointment request."""
    patient_name: str
    doctor_id: str
    request_type: str = Field(..., examples=["consultation", "follow-up", "new_patient"])
    preferred_date: str  # Date in MM/DD/YYYY format
    preferred_time: str  # Time in HH:MM AM/PM format
    details: Optional[str] = None  # Optional additional details

    @field_validator('preferred_date')
    @classmethod
    def validate_date(cls, v):
        """Validate the preferred_date format."""
        try:
            datetime.strptime(v, "%m/%d/%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use MM/DD/YYYY.")
        return v

    @field_validator('preferred_time')
    @classmethod
    def validate_time(cls, v):
        """Validate the preferred_time format."""
        try:
            datetime.strptime(v, "%I:%M %p")
        except ValueError:
            raise ValueError("Invalid time format. Use HH:MM AM/PM.")
        return v


class Appointment(BaseModel):
    """Model to represent an appointment."""
    appointment_id: str = Field(default_factory=lambda: str(uuid.uuid4()))  # Auto-generate unique ID
    doctor_id: str
    patient_name: str
    request_type: str
    appointment_datetime: str  # Combined date and time in a readable format
    status: str  # Status of the appointment


# -------------------------------
# Initial Data
# -------------------------------

# Predefined doctor profiles with their availability schedules
doctors: Dict[str, DoctorProfile] = {
    "dr_001": DoctorProfile(
        doctor_id="dr_001",
        name="Dr. Sarah Johnson",
        specialization="General Medicine",
        schedule={
            "Monday": [TimeSlot(time=t) for t in ["09:00 AM", "10:00 AM", "11:00 AM", "01:00 PM", "02:00 PM", "03:00 PM"]],
            "Wednesday": [TimeSlot(time=t) for t in ["09:00 AM", "10:00 AM", "11:00 AM", "01:00 PM", "02:00 PM", "03:00 PM"]],
            "Friday": [TimeSlot(time=t) for t in ["09:00 AM", "10:00 AM", "11:00 AM", "01:00 PM", "02:00 PM", "03:00 PM"]],
        }
    ),
    "dr_002": DoctorProfile(
        doctor_id="dr_002",
        name="Dr. Emily Carter",
        specialization="Pediatrics",
        schedule={
            "Tuesday": [TimeSlot(time=t) for t in ["09:00 AM", "10:00 AM", "11:00 AM", "01:00 PM"]],
            "Thursday": [TimeSlot(time=t) for t in ["09:00 AM", "10:00 AM", "11:00 AM", "01:00 PM", "03:00 PM"]],
        }
    ),
    "dr_003": DoctorProfile(
        doctor_id="dr_003",
        name="Dr. Michael Brown",
        specialization="Dermatology",
        schedule={
            "Monday": [TimeSlot(time=t) for t in ["10:00 AM", "11:00 AM", "01:00 PM", "03:00 PM"]],
            "Wednesday": [TimeSlot(time=t) for t in ["09:00 AM", "10:00 AM", "02:00 PM"]],
            "Friday": [TimeSlot(time=t) for t in ["10:00 AM", "01:00 PM", "02:00 PM"]],
        }
    ),
}

# List to store booked appointments
appointments: List[Appointment] = []

# -------------------------------
# API Endpoints
# -------------------------------

@app.get("/api/v1/doctor/availability")
async def get_doctor_availability(doctor_id: str, date: Optional[str] = None):
    """
    Check doctor's availability for a specific date or the entire week.
    - **doctor_id**: The unique ID of the doctor.
    - **date** (optional): A specific date in MM/DD/YYYY format to check availability.
    """
    if doctor_id not in doctors:
        raise HTTPException(status_code=404, detail="Doctor not found.")

    doctor = doctors[doctor_id]

    if date:
        # Validate and parse the date
        try:
            date_obj = datetime.strptime(date, "%m/%d/%Y")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use MM/DD/YYYY.")

        # Get day of the week and available times
        day_name = date_obj.strftime("%A")
        available_times = doctor.schedule.get(day_name, [])

        # Filter out already booked times
        booked_times = [
            appt.appointment_datetime.split(" at ")[1]  # Extract the time
            for appt in appointments
            if appt.doctor_id == doctor_id and appt.appointment_datetime.startswith(date)
        ]
        available_times = [slot for slot in available_times if slot.time not in booked_times]

        if not available_times:
            return {
                "doctor_id": doctor_id,
                "name": doctor.name,
                "date": date,
                "available_times": [],
                "message": f"No available times on {date}.",
            }

        return {
            "doctor_id": doctor_id,
            "name": doctor.name,
            "date": date,
            "available_times": [slot.time for slot in available_times],
        }
    else:
        # Get availability for the entire week
        availability = {}
        for day, times in doctor.schedule.items():
            # Calculate the date for this day
            date_obj = datetime.now()
            while date_obj.strftime("%A") != day:
                date_obj += timedelta(days=1)
            date_str = date_obj.strftime("%m/%d/%Y")

            # Filter out booked times for the specific date
            booked_times = [
                appt.appointment_datetime.split(" at ")[1]
                for appt in appointments
                if appt.doctor_id == doctor_id and appt.appointment_datetime.startswith(date_str)
            ]
            available_times = [slot.time for slot in times if slot.time not in booked_times]

            if available_times:
                availability[day] = available_times

        return {
            "doctor_id": doctor_id,
            "name": doctor.name,
            "weekly_availability": availability,
        }


@app.post("/api/v1/appointments/book", response_model=Appointment)
async def book_appointment(request: AppointmentRequest):
    """
    Book an appointment for a patient.
    - **patient_name**: Name of the patient.
    - **doctor_id**: The unique ID of the doctor.
    - **request_type**: Type of appointment (consultation, follow-up, new_patient).
    - **preferred_date**: Date of the appointment (MM/DD/YYYY).
    - **preferred_time**: Time of the appointment (HH:MM AM/PM).
    """
    doctor_id = request.doctor_id

    # Check if the doctor exists
    if doctor_id not in doctors:
        raise HTTPException(status_code=404, detail="Doctor not found.")

    doctor = doctors[doctor_id]

    # Parse and validate the date and time
    try:
        appointment_date = datetime.strptime(request.preferred_date, "%m/%d/%Y")
        appointment_time = datetime.strptime(request.preferred_time, "%I:%M %p")
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid date or time format.")

    # Combine date and time into a single datetime string
    appointment_datetime = datetime.combine(appointment_date.date(), appointment_time.time())
    appointment_datetime_str = appointment_datetime.strftime("%m/%d/%Y at %I:%M %p")
    day_name = appointment_datetime.strftime("%A")

    # Check if the doctor is available on the selected day
    if day_name not in doctor.schedule:
        raise HTTPException(
            status_code=400,
            detail=f"Doctor is not available on {day_name}s."
        )

    # Check if the selected time is available
    available_times = [slot.time for slot in doctor.schedule[day_name]]
    if request.preferred_time not in available_times:
        raise HTTPException(
            status_code=400,
            detail=f"Doctor is not available at {request.preferred_time} on {day_name}."
        )

    # Ensure no conflicting appointments
    for appt in appointments:
        if appt.doctor_id == doctor_id and appt.appointment_datetime == appointment_datetime_str:
            alternative_times = [
                time for time in available_times
                if f"{appointment_date.strftime('%m/%d/%Y')} at {time}" not in [
                    a.appointment_datetime for a in appointments
                    if a.doctor_id == doctor_id
                ]
            ]
            raise HTTPException(
                status_code=409,
                detail={
                    "message": "Requested time is already booked.",
                    "alternative_times": alternative_times,
                }
            )

    # Create and store the appointment
    new_appointment = Appointment(
        doctor_id=doctor_id,
        patient_name=request.patient_name,
        request_type=request.request_type,
        appointment_datetime=appointment_datetime_str,
        status="success"
    )
    appointments.append(new_appointment)

    return new_appointment

# endpoint to clear all the appointments
@app.delete("/api/v1/appointments/clear")
def clear_appointments():
    """
    Clear all the booked appointments.
    """
    appointments.clear()
    return {"message": "All appointments have been cleared."}

# endpoint to see all the appointments
@app.get("/api/v1/appointments")
def get_appointments():
    """
    Get all the booked appointments.
    """
    if not appointments:
        return {"message": "No appointments found."}
    return appointments


# # Run the app 
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
