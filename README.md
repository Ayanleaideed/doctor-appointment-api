Here's a more straightforward and professional README that emphasizes this system as part of a larger ADRD project, while sounding less "generated."

---

# Doctor Appointment Management System API

This API is a sample implementation for the ADRD project, showcasing how a multi-agent system can streamline doctor appointment management. It focuses on core functionalities like checking doctor availability, booking appointments, and handling conflicts with alternative suggestions.

This system is designed to be a foundational component for a more comprehensive multi-agent ecosystem capable of managing healthcare-related interactions.

---

## 🚀 Core Functionalities
- **Check Doctor Avasilability**: Retrieve available time slots for doctors by day or week.
- **Book Appointments**: Schedule appointments while avoiding conflicts.
- **Dynamic Updates**: Automatically adjusts availability based on booked slots.
- **Conflict Resolution**: Provides alternative time suggestions if a requested slot is unavailable.

---

## 📚 API Endpoints

### 1. **Check Doctor Availability**
**GET** `/api/v1/doctor/availability`

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

---

### 2. **Book an Appointment**
**POST** `/api/v1/appointments/book`

| Parameter         | Type   | Required | Description                           |
|-------------------|--------|----------|---------------------------------------|
| `patient_name`    | String | Yes      | Name of the patient                  |
| `doctor_id`       | String | Yes      | Unique ID of the doctor              |
| `request_type`    | String | Yes      | Type of appointment (e.g., consultation) |
| `preferred_date`  | String | Yes      | Date for the appointment (MM/DD/YYYY)|
| `preferred_time`  | String | Yes      | Time for the appointment (HH:MM AM/PM)|
| `details`         | String | No       | Additional details about the request |

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

## 🛠️ How to Use Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Ayanleaideed/doctor-appointment-api.git
   cd doctor-appointment-api
   ```

2. **Install Dependencies**:
   Ensure Python is installed, then:
   ```bash
   pip install fastapi uvicorn
   ```

3. **Start the Server**:
   Run:
   ```bash
   uvicorn main:app --reload
   ```

4. **Access the API**:
   - Visit **http://127.0.0.1:8000** for local development.
   - Test endpoints using Postman or curl.

---

## Purpose in the ADRD Project

This system represents a sample module for a larger multi-agent system aimed at managing interactions in healthcare settings, particularly for Alzheimer's Disease-Related Dementia (ADRD). The ultimate goal is to integrate this API with intelligent agents that handle complex workflows like:
- Coordinating between patients, doctors, and caregivers.
- Automating appointment scheduling and reminders.
- Providing personalized healthcare assistance based on patient needs.

This implementation demonstrates how an appointment system can be both practical on its own and a stepping stone to broader, more intelligent applications.

---

## 📝 License
This project is licensed under the MIT License. Feel free to use, modify, and extend it while acknowledging its role in the ADRD project.

--- 


![alt text](<Screenshot 2024-11-26 at 2.50.17 PM.png>)
https://whimsical.com/final-doctor-appointment-management-system-CeQ9xwjXJpMaAtcYvPgeEC@6HYTAunKLgTUqfLatmvaBuCjXtBABmdRHrQjxVdCHq3SAXi