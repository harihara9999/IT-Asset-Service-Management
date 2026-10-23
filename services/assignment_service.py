from datetime import datetime

from database.connection import get_db_connection


class AssignmentService:

    @staticmethod
    def assign_asset(asset_id: str, employee_id: str):
        conn = get_db_connection()

        try:
            # 1. Check employee exists
            employee = conn.execute(
                "SELECT employee_id FROM employees WHERE employee_id = ?",
                (employee_id,)
            ).fetchone()

            if employee is None:
                return {"error": "Employee not found"}

            # 2. Check asset exists
            asset = conn.execute(
                "SELECT asset_id, status FROM assets WHERE asset_id = ?",
                (asset_id,)
            ).fetchone()

            if asset is None:
                return {"error": "Asset not found"}

            # 3. Check asset is AVAILABLE
            if asset[1] != "AVAILABLE":
                return {
                    "error": f"Asset '{asset_id}' is not available for assignment"
                }

            # 4. Insert assignment
            assigned_date = datetime.now().isoformat()

            conn.execute(
                "INSERT INTO asset_assignments "
                "(asset_id, employee_id, assigned_date) "
                "VALUES (?, ?, ?)",
                (asset_id, employee_id, assigned_date)
            )

            # 5. Change asset status to ASSIGNED
            conn.execute(
                "UPDATE assets SET status = 'ASSIGNED' "
                "WHERE asset_id = ?",
                (asset_id,)
            )

            # 6. Save both changes
            conn.commit()

            return {
                "message": f"Asset {asset_id} successfully assigned to {employee_id}",
                "assigned_date": assigned_date
            }

        except Exception:
            # Undo changes if anything fails
            conn.rollback()
            raise

        finally:
            conn.close()

    @staticmethod
    def return_asset(asset_id: str):
        conn = get_db_connection()

        try:
            asset = conn.execute(
                "SELECT asset_id, status FROM assets WHERE asset_id = ?",
                (asset_id,)
            ).fetchone()

            if asset is None:
                return {"error": "Asset not found"}

            if asset[1] != "ASSIGNED":
                return {"error": "Asset is not currently assigned"}

            return_date = datetime.now().isoformat()

            conn.execute(
                "UPDATE asset_assignments "
                "SET return_date = ? "
                "WHERE asset_id = ? AND return_date IS NULL",
                (return_date, asset_id)
            )

            conn.execute(
                "UPDATE assets SET status = 'AVAILABLE' "
                "WHERE asset_id = ?",
                (asset_id,)
            )

            conn.commit()

            return {
                "message": f"Asset {asset_id} returned successfully",
                "return_date": return_date
            }

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()