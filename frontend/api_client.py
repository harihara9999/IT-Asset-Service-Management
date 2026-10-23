
import requests

API_BASE_URL = "http://127.0.0.1:8000"


# 1. Check FastAPI connection
def check_backend():
    try:
        response = requests.get(
            f"{API_BASE_URL}/",
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        return {"error": str(error)}


# 2. Create employee
def create_employee(employee_data):
    try:
        response = requests.post(
            f"{API_BASE_URL}/employees/",
            json=employee_data,
            timeout=5
        )
        try:
            result = response.json()
        except ValueError:
            result = {"error": response.text}
        return response.status_code, result
    except requests.RequestException as error:
        return None, {"error": str(error)}


# 3. Get all employees
def get_all_employees():
    try:
        response = requests.get(
            f"{API_BASE_URL}/employees/",
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        return {"error": str(error)}


# 4. Update employee
def update_employee(employee_id, employee_data):
    try:
        response = requests.put(
            f"{API_BASE_URL}/employees/{employee_id}",
            json=employee_data,
            timeout=5
        )
        try:
            result = response.json()
        except ValueError:
            result = {"error": response.text}
        return response.status_code, result
    except requests.RequestException as error:
        return None, {"error": str(error)}


# 5. Delete employee
def delete_employee(employee_id):
    try:
        response = requests.delete(
            f"{API_BASE_URL}/employees/{employee_id}",
            timeout=5
        )
        try:
            result = response.json()
        except ValueError:
            result = {"error": response.text}
        return response.status_code, result
    except requests.RequestException as error:
        return None, {"error": str(error)}


# 6. Get all assets
def get_all_assets():
    try:
        response = requests.get(
            f"{API_BASE_URL}/assets/",
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        return {"error": str(error)}


# 7. Create asset
def create_asset(asset_data):
    try:
        response = requests.post(
            f"{API_BASE_URL}/assets/",
            json=asset_data,
            timeout=5
        )
        try:
            result = response.json()
        except ValueError:
            result = {"error": response.text}
        return response.status_code, result
    except requests.RequestException as error:
        return None, {"error": str(error)}


# 8. Update asset
def update_asset(asset_id, asset_data):
    try:
        response = requests.put(
            f"{API_BASE_URL}/assets/{asset_id}",
            json=asset_data,
            timeout=5
        )
        try:
            result = response.json()
        except ValueError:
            result = {"error": response.text}
        return response.status_code, result
    except requests.RequestException as error:
        return None, {"error": str(error)}


# 9. Delete asset
def delete_asset(asset_id):
    try:
        response = requests.delete(
            f"{API_BASE_URL}/assets/{asset_id}",
            timeout=5
        )
        try:
            result = response.json()
        except ValueError:
            result = {"error": response.text}
        return response.status_code, result
    except requests.RequestException as error:
        return None, {"error": str(error)}


# 10. Assign an asset to an employee
def assign_asset(asset_id, employee_id):
    try:
        response = requests.post(
            f"{API_BASE_URL}/assignments/",
            json={
                "asset_id": asset_id,
                "employee_id": employee_id
            },
            timeout=5
        )
        try:
            result = response.json()
        except ValueError:
            result = {"error": response.text}
        return response.status_code, result
    except requests.RequestException as error:
        return None, {"error": str(error)}


# 11. Return an assigned asset
def return_asset(asset_id):
    try:
        response = requests.put(
            f"{API_BASE_URL}/assignments/{asset_id}/return",
            timeout=5
        )
        try:
            result = response.json()
        except ValueError:
            result = {"error": response.text}
        return response.status_code, result
    except requests.RequestException as error:
        return None, {"error": str(error)}


# 12. Get all service tickets
def get_all_tickets():
    try:
        response = requests.get(
            f"{API_BASE_URL}/tickets/",
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        return {"error": str(error)}


# 13. Create a service ticket
def create_ticket(ticket_data):
    try:
        response = requests.post(
            f"{API_BASE_URL}/tickets/",
            json=ticket_data,
            timeout=5
        )
        try:
            result = response.json()
        except ValueError:
            result = {"error": response.text}
        return response.status_code, result
    except requests.RequestException as error:
        return None, {"error": str(error)}


# 14. Assign a technician to a ticket
def assign_technician(ticket_id, technician_id):
    try:
        response = requests.put(
            f"{API_BASE_URL}/tickets/{ticket_id}/assign-technician",
            params={"technician_id": technician_id},
            timeout=5
        )
        try:
            result = response.json()
        except ValueError:
            result = {"error": response.text}
        return response.status_code, result
    except requests.RequestException as error:
        return None, {"error": str(error)}


# 15. Resolve a ticket with diagnosis
def resolve_ticket(ticket_id, diagnosis):
    try:
        response = requests.put(
            f"{API_BASE_URL}/tickets/{ticket_id}/resolve",
            params={"diagnosis": diagnosis},
            timeout=5
        )
        try:
            result = response.json()
        except ValueError:
            result = {"error": response.text}
        return response.status_code, result
    except requests.RequestException as error:
        return None, {"error": str(error)}


# 16. Change ticket status
def change_ticket_status(ticket_id, new_status):
    try:
        response = requests.put(
            f"{API_BASE_URL}/tickets/{ticket_id}/status",
            params={"new_status": new_status},
            timeout=5
        )
        try:
            result = response.json()
        except ValueError:
            result = {"error": response.text}
        return response.status_code, result
    except requests.RequestException as error:
        return None, {"error": str(error)}
