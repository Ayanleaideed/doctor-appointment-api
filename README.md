# ADRD Doctor Appointment Management System

Welcome to the **ADRD Doctor Appointment Management System**! This API is part of the ADRD project, designed to manage doctor profiles, check availability, and streamline appointment bookings. It serves as a foundation for integrating healthcare management into a multi-agent system.

This API allows developers and collaborators to test key features like availability tracking, appointment scheduling, and data clearing, making it an excellent starting point for advanced integrations in real-world healthcare applications.

---

## 🚀 Features

- **Doctor Availability**: Query available time slots for doctors by specific day or the entire week.
- **Appointment Booking**: Schedule an appointment with automatic conflict handling and alternative time suggestions.
- **Clear Appointments**: A developer-only endpoint for resetting all appointments (useful for testing).
- **Fetch Appointments**: Retrieve all booked appointments for verification or troubleshooting.
- **Dynamic Updates**: Availability automatically adjusts as appointments are booked or cleared.

---

## 📚 API Endpoints

### 1. **Get Doctor Availability**
**GET** `/api/v1/doctor/availability`

Fetch available time slots for a doctor by specific date or week.

| Parameter    | Type   | Required | Description                         |
|--------------|--------|----------|-------------------------------------|
| `doctor_id`  | String | Yes      | Unique ID of the doctor             |
| `date`       | String | No       | Date to check availability (MM/DD/YYYY) |

**Example Request:**
```bash
GET /api/v1/doctor/availability?doctor_id=dr_001&date=11/29/2024
```

**Example Response:**
```json
{
  "doctor_id": "dr_001",
  "name": "Dr. Sarah Johnson",
  "date": "11/29/2024",
  "available_times": ["09:00 AM", "10:00 AM", "11:00 AM"]
}
```

If no available times exist:
```json
{
  "message": "No available times on 11/29/2024."
}
```

---

### 2. **Book an Appointment**
**POST** `/api/v1/appointments/book`

Schedule an appointment with a specific doctor. Handles conflicts by providing alternative times if the requested slot is unavailable.

| Parameter         | Type   | Required | Description                           |
|-------------------|--------|----------|---------------------------------------|
| `patient_name`    | String | Yes      | Name of the patient                  |
| `doctor_id`       | String | Yes      | Unique ID of the doctor              |
| `request_type`    | String | Yes      | Type of appointment (consultation, follow-up, etc.) |
| `preferred_date`  | String | Yes      | Date for the appointment (MM/DD/YYYY)|
| `preferred_time`  | String | Yes      | Time for the appointment (HH:MM AM/PM)|
| `details`         | String | No       | Additional notes (optional)          |

**Example Request:**
```json
{
  "patient_name": "John Doe",
  "doctor_id": "dr_001",
  "request_type": "consultation",
  "preferred_date": "11/29/2024",
  "preferred_time": "09:00 AM"
}
```

**Example Response:**
```json
{
  "appointment_id": "123e4567-e89b-12d3-a456-426614174000",
  "doctor_id": "dr_001",
  "patient_name": "John Doe",
  "request_type": "consultation",
  "appointment_datetime": "11/29/2024 at 09:00 AM",
  "status": "success"
}
```

**If Conflict Exists:**
```json
{
  "detail": {
    "message": "Requested time is already booked.",
    "alternative_times": ["10:00 AM", "11:00 AM", "01:00 PM"]
  }
}
```

---

### 3. **Clear Appointments**
**DELETE** `/api/v1/appointments/clear`

Clears all booked appointments. This is primarily a developer endpoint used for testing purposes.

**Example Request:**
```bash
DELETE /api/v1/appointments/clear
```

**Example Response:**
```json
{
  "message": "All appointments have been cleared."
}
```

---

### 4. **Get All Appointments**
**GET** `/api/v1/appointments`

Retrieve a list of all booked appointments, including patient details and appointment times.

**Example Request:**
```bash
GET /api/v1/appointments
```

**Example Response:**
```json
[
  {
    "appointment_id": "123e4567-e89b-12d3-a456-426614174000",
    "doctor_id": "dr_001",
    "patient_name": "John Doe",
    "request_type": "consultation",
    "appointment_datetime": "11/29/2024 at 09:00 AM",
    "status": "success"
  },
  {
    "appointment_id": "987e6543-e21b-34c1-a890-65432174000",
    "doctor_id": "dr_002",
    "patient_name": "Jane Doe",
    "request_type": "follow-up",
    "appointment_datetime": "11/29/2024 at 10:00 AM",
    "status": "success"
  }
]
```

---

## 🛠️ How to Run Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Ayanleaideed/doctor-appointment-api.git
   cd doctor-appointment-api
   ```

2. **Install Dependencies**:
   Ensure Python is installed, then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Server**:
   Run the following command:
   ```bash
   uvicorn api:app --reload
   ```

4. **Access the API**:
   - Open **http://127.0.0.1:8000/docs** to view the interactive API documentation.
   - Test endpoints using Postman, curl, or the Swagger UI.

---

## 🧪 Example Scenarios for Testing

1. **Checking Availability**:
   - Ensure availability is accurate for a given doctor and date.
   - Validate that booked slots are excluded from available times.

2. **Booking an Appointment**:
   - Test normal booking behavior.
   - Validate conflict handling and alternative suggestions.

3. **Clearing Appointments**:
   - Test the ability to reset the system during development or testing.

4. **Fetching All Appointments**:
   - Verify that all bookings are correctly returned with accurate details.

---

## 🌐 Live Deployment

You can access the live version of the API here:
- **Base URL**: [https://adrd-doctor-appointment-api.vercel.app/](https://adrd-doctor-appointment-api.vercel.app/)
- **Interactive Documentation**: [Swagger UI](https://adrd-doctor-appointment-api.vercel.app/docs)

---

## 📝 Notes for Collaborators

This system is a sample implementation within the ADRD project, demonstrating how a multi-agent system can handle appointment scheduling. It focuses on simplicity and modularity to serve as a building block for more complex integrations.

If you're testing or extending this API:
- Use the `/appointments/clear` endpoint for resetting data during development.
- Follow the examples provided to ensure consistency in usage.

---

## ⚜️ 
![alt text](<Design-daigram.png>)
##### Direct link
https://whimsical.com/final-doctor-appointment-management-system-CeQ9xwjXJpMaAtcYvPgeEC@6HYTAunKLgTUqfLatmvaBuCjXtBABmdRHrQjxVdCHq3SAXi

## 📝 License

This project is licensed under the **MIT License**. Feel free to use, modify, and extend it with proper attribution.
---
