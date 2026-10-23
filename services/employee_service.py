import sqlite3

from database.connection import get_db_connection


class EmployeeService:

    @staticmethod           # allows us to call this function directly using the class name
    def create_employee(emp):
        conn = get_db_connection()    # Connect me to my SQLite database

        try:
            conn.execute(
                "INSERT INTO employees "
                "(employee_id, name, department, email, phone) "
                "VALUES (?, ?, ?, ?, ?)",    # These are placeholders 
                (
                    emp.employee_id,
                    emp.name,
                    emp.department,
                    emp.email,
                    emp.phone
                )
            )

            conn.commit()   # Save this change permanently in the database

            return {"message": "Employee created"}  # After successfully adding the employee, the function sends back

        except sqlite3.IntegrityError:   # If the database gives an IntegrityError, come here instead of crashing
            conn.rollback()      # Undo the database changes from this operation

            return {"error": "Employee ID or email already exists"}

        finally:
            conn.close()  # No matter whether the operation succeeded or failed, do this

    @staticmethod
    def get_employee(employee_id):
        conn = get_db_connection()

        try:
            row = conn.execute(            # Send a SQL command to the database and execute it
                "SELECT employee_id, name, department, email, phone "
                "FROM employees WHERE employee_id = ?",
                (employee_id,)
            ).fetchone()   # Get one matching row from the database.

            if row is None:
                return None

            return {
                "employee_id": row[0],
                "name": row[1],
                "department": row[2],
                "email": row[3],
                "phone": row[4]
            }

        finally:
            conn.close()
    
    @staticmethod
    def get_all_employees():
        conn = get_db_connection()

        try:
            rows = conn.execute(
                "SELECT employee_id, name, department, email, phone "
                "FROM employees "
                "ORDER BY employee_id"
            ).fetchall()

            employees = []

            for row in rows:
                employees.append({
                    "employee_id": row[0],
                    "name": row[1],
                    "department": row[2],
                    "email": row[3],
                    "phone": row[4]
                })

            return employees

        finally:
            conn.close()




    @staticmethod
    def update_employee(employee_id: str, employee):
        conn = get_db_connection()

        try:
            existing = conn.execute(
                "SELECT employee_id FROM employees WHERE employee_id = ?",
                (employee_id,)
            ).fetchone()

            if existing is None:
                return {"error": "Employee not found"}

            conn.execute(
                "UPDATE employees "
                "SET name = ?, department = ?, email = ?, phone = ? "
                "WHERE employee_id = ?",
                (
                    employee.name,
                    employee.department,
                    employee.email,
                    employee.phone,
                    employee_id
                )
            )

            conn.commit()

            return {
                "message": "Employee updated",
                "employee_id": employee_id
            }

        finally:
            conn.close()

    @staticmethod
    def delete_employee(employee_id: str):
        conn = get_db_connection()

        try:
            existing = conn.execute(
                "SELECT employee_id FROM employees WHERE employee_id = ?",
                (employee_id,)
            ).fetchone()

            if existing is None:
                return {"error": "Employee not found"}

            conn.execute(
                "DELETE FROM employees WHERE employee_id = ?",
                (employee_id,)
            )

            conn.commit()

            return {
                "message": "Employee deleted",
                "employee_id": employee_id
            }

        finally:
            conn.close()