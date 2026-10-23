# IT Asset & Service Management System

A full-stack, modular IT Asset and Service Management System built with **Python**, **FastAPI**, **Streamlit**, and **SQLite**. 

This system helps organizations maintain a centralized inventory of IT assets, manage employee equipment assignments and returns, and resolve technical service requests through a strict lifecycle workflow.

---

## 🚀 Features

- **Employee Management**: Manage employee directories, departments, and contact information.
- **Asset Inventory Tracking**: Register, update, and categorize IT equipment (Laptops, Desktops, Monitors, etc.) across multiple statuses (`AVAILABLE`, `ASSIGNED`, `UNDER_REPAIR`, `RETIRED`).
- **Assignment & Return Tracking**:
  - Assign equipment only when in `AVAILABLE` status.
  - Automatically track assignment timestamps.
  - Mark equipment returned and restore availability status.
- **Service Ticket Center (Finite State Machine)**:
  - Create IT support tickets tagged to assets and employees.
  - Prioritize tickets (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).
  - Strict status progression: `OPEN` ➔ `IN_PROGRESS` (technician assigned) ➔ `RESOLVED` (diagnosis logged) ➔ `CLOSED`.
- **Interactive Web Interface**: Streamlit UI with live KPI metrics, search filters, and status badges.
- **RESTful API**: FastAPI backend with automated OpenAPI/Swagger documentation.

---

## 🛠️ Architecture & Tech Stack

```text
├── main.py                  # FastAPI application entry point
├── schema.sql               # SQLite schema with foreign key constraints
├── database/                # Database connection and startup initialization
├── models/                  # Pydantic schemas for request validation
├── routers/                 # FastAPI REST endpoint routes
├── services/                # Business logic, state transitions, & DB transactions
└── frontend/
    ├── api_client.py        # HTTP client library for backend communication
    └── app.py               # Streamlit web application
```

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/), [Pydantic](https://docs.pydantic.dev/), [Uvicorn](https://www.uvicorn.org/)
- **Frontend**: [Streamlit](https://streamlit.io/), [Pandas](https://pandas.pydata.org/)
- **Database**: [SQLite3](https://www.sqlite.org/) (Enforces foreign keys with `PRAGMA foreign_keys = ON`)

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/harihara9999/IT-Asset-Service-Management.git
cd IT-Asset-Service-Management
```

### 2. Create and Activate a Virtual Environment
```bash
# On Windows:
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 Running the Application

### 1. Start the FastAPI Backend
```bash
python -m uvicorn main:app --reload --port 8000
```
- API Base URL: `http://127.0.0.1:8000`
- Swagger UI Documentation: `http://127.0.0.1:8000/docs`
- ReDoc Documentation: `http://127.0.0.1:8000/redoc`

### 2. Start the Streamlit Frontend
In a separate terminal window:
```bash
python -m streamlit run frontend/app.py
```
- Web Application UI: `http://localhost:8501`

---

## 📋 API Endpoints Overview

| Category | Method | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| **System** | `GET` | `/` | Health check endpoint |
| **Employees** | `POST` | `/employees/` | Create a new employee |
| | `GET` | `/employees/` | Retrieve all employees |
| | `GET` | `/employees/{id}` | Retrieve employee by ID |
| | `PUT` | `/employees/{id}` | Update employee details |
| | `DELETE`| `/employees/{id}` | Delete employee |
| **Assets** | `POST` | `/assets/` | Register a new asset |
| | `GET` | `/assets/` | Retrieve all assets |
| | `GET` | `/assets/{id}` | Retrieve asset by ID |
| | `PUT` | `/assets/{id}` | Update asset details |
| | `DELETE`| `/assets/{id}` | Delete an asset |
| **Assignments**| `POST` | `/assignments/` | Assign an available asset to an employee |
| | `PUT` | `/assignments/{id}/return` | Record asset return and set to `AVAILABLE` |
| **Tickets** | `POST` | `/tickets/` | Create a service ticket |
| | `GET` | `/tickets/` | Retrieve all tickets |
| | `PUT` | `/tickets/{id}/assign-technician` | Assign technician (transitions to `IN_PROGRESS`) |
| | `PUT` | `/tickets/{id}/resolve` | Record diagnosis and resolve ticket |
| | `PUT` | `/tickets/{id}/status` | Update ticket status (`OPEN` ➔ `IN_PROGRESS` ➔ `RESOLVED` ➔ `CLOSED`) |
