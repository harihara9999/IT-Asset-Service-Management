from pydantic import BaseModel   # to check the data of the emp


class EmployeeCreate(BaseModel):  # basemodel is tool in pydantic and it gives access to check the data 
    employee_id: str
    name: str
    department: str
    email: str
    phone: str = ""