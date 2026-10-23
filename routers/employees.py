
from fastapi import APIRouter

from models.employee import EmployeeCreate
from services.employee_service import EmployeeService


router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


# Create a new employee
@router.post("/")
def create_employee(employee: EmployeeCreate):
    return EmployeeService.create_employee(employee)


# Get all employees (NEW)
@router.get("/")
def get_all_employees():
    return EmployeeService.get_all_employees()


# Get one employee by ID
@router.get("/{employee_id}")
def get_employee(employee_id: str):
    result = EmployeeService.get_employee(employee_id)

    if result is None:
        return {"error": "Employee not found"}

    return result


# Update an employee
@router.put("/{employee_id}")
def update_employee(employee_id: str, employee: EmployeeCreate):
    return EmployeeService.update_employee(
        employee_id,
        employee
    )


# Delete an employee
@router.delete("/{employee_id}")
def delete_employee(employee_id: str):
    return EmployeeService.delete_employee(employee_id)
