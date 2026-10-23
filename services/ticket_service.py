import sqlite3
from datetime import datetime
from database.connection import get_db_connection


class TicketService:

    @staticmethod
    def create_ticket(ticket):
        conn = get_db_connection()

        try:
            # Check that the asset exists
            asset = conn.execute(
                "SELECT asset_id FROM assets WHERE asset_id = ?",
                (ticket.asset_id,)
            ).fetchone()

            if asset is None:
                return {"error": "Asset not found"}

            # Check that the employee exists
            employee = conn.execute(
                "SELECT employee_id FROM employees WHERE employee_id = ?",
                (ticket.employee_id,)
            ).fetchone()

            if employee is None:
                return {"error": "Employee not found"}

            # Create ticket
            conn.execute(
                "INSERT INTO service_tickets "
                "(ticket_id, asset_id, employee_id, title, description, priority) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    ticket.ticket_id,
                    ticket.asset_id,
                    ticket.employee_id,
                    ticket.title,
                    ticket.description,
                    ticket.priority
                )
            )

            conn.commit()

            return {
                "message": "Ticket created",
                "ticket_id": ticket.ticket_id,
                "status": "OPEN"
            }

        except sqlite3.IntegrityError:
            conn.rollback()

            return {
                "error": "Ticket ID already exists"
            }

        finally:
            conn.close()

    @staticmethod
    def assign_technician(ticket_id: str, technician_id: str):
        conn = get_db_connection()

        try:
            ticket = conn.execute(
                "SELECT ticket_id FROM service_tickets WHERE ticket_id = ?",
                (ticket_id,)
            ).fetchone()

            if ticket is None:
                return {"error": "Ticket not found"}

            conn.execute(
                "UPDATE service_tickets "
                "SET technician_id = ?, status = 'IN_PROGRESS' "
                "WHERE ticket_id = ?",
                (technician_id, ticket_id)
            )

            conn.commit()

            return {
                "message": f"Technician {technician_id} assigned to ticket {ticket_id}",
                "status": "IN_PROGRESS"
            }

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

    @staticmethod
    def resolve_ticket(ticket_id: str, diagnosis: str):
        conn = get_db_connection()

        try:
            ticket = conn.execute(
                "SELECT ticket_id, status "
                "FROM service_tickets WHERE ticket_id = ?",
                (ticket_id,)
            ).fetchone()

            if ticket is None:
                return {"error": "Ticket not found"}

            if ticket[1] != "IN_PROGRESS":
                return {
                    "error": "Ticket must be IN_PROGRESS before it can be resolved"
                }

            resolved_time = datetime.now().isoformat()

            conn.execute(
                "UPDATE service_tickets "
                "SET status = 'RESOLVED', "
                "diagnosis_notes = ?, "
                "resolved_at = ? "
                "WHERE ticket_id = ?",
                (diagnosis, resolved_time, ticket_id)
            )

            conn.commit()

            return {
                "message": "Ticket resolved",
                "ticket_id": ticket_id,
                "status": "RESOLVED",
                "resolved_at": resolved_time
            }

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

    @staticmethod
    def get_ticket(ticket_id: str):
        conn = get_db_connection()

        try:
            row = conn.execute(
                "SELECT ticket_id, asset_id, employee_id, technician_id, "
                "title, description, priority, status, diagnosis_notes, resolved_at "
                "FROM service_tickets WHERE ticket_id = ?",
                (ticket_id,)
            ).fetchone()

            if row is None:
                return None

            return {
                "ticket_id": row[0],
                "asset_id": row[1],
                "employee_id": row[2],
                "technician_id": row[3],
                "title": row[4],
                "description": row[5],
                "priority": row[6],
                "status": row[7],
                "diagnosis_notes": row[8],
                "resolved_at": row[9]
            }

        finally:
            conn.close()

    
    @staticmethod
    def get_all_tickets():
        conn = get_db_connection()

        try:
            rows = conn.execute(
                "SELECT ticket_id, asset_id, employee_id, technician_id, "
                "title, description, priority, status, "
                "diagnosis_notes, resolved_at "
                "FROM service_tickets "
                "ORDER BY ticket_id"
            ).fetchall()

            tickets = []

            for row in rows:
                tickets.append({
                    "ticket_id": row[0],
                    "asset_id": row[1],
                    "employee_id": row[2],
                    "technician_id": row[3],
                    "title": row[4],
                    "description": row[5],
                    "priority": row[6],
                    "status": row[7],
                    "diagnosis_notes": row[8],
                    "resolved_at": row[9]
                })

            return tickets

        finally:
            conn.close()


    @staticmethod
    def close_ticket(ticket_id: str):
        conn = get_db_connection()

        try:
            ticket = conn.execute(
                "SELECT ticket_id, status "
                "FROM service_tickets WHERE ticket_id = ?",
                (ticket_id,)
            ).fetchone()

            if ticket is None:
                return {"error": "Ticket not found"}

            if ticket[1] != "RESOLVED":
                return {
                    "error": "Ticket must be RESOLVED before it can be closed"
                }

            conn.execute(
                "UPDATE service_tickets "
                "SET status = 'CLOSED' "
                "WHERE ticket_id = ?",
                (ticket_id,)
            )

            conn.commit()

            return {
                "message": "Ticket closed",
                "ticket_id": ticket_id,
                "status": "CLOSED"
            }

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

    @staticmethod
    def change_status(ticket_id: str, new_status: str):
        conn = get_db_connection()

        try:
            ticket = conn.execute(
                "SELECT ticket_id, status "
                "FROM service_tickets WHERE ticket_id = ?",
                (ticket_id,)
            ).fetchone()

            if ticket is None:
                return {"error": "Ticket not found"}

            current_status = ticket[1]

            allowed_transitions = {
                "OPEN": "IN_PROGRESS",
                "IN_PROGRESS": "RESOLVED",
                "RESOLVED": "CLOSED"
            }

            if allowed_transitions.get(current_status) != new_status:
                return {
                    "error": f"Invalid status change from {current_status} to {new_status}"
                }

            conn.execute(
                "UPDATE service_tickets "
                "SET status = ? "
                "WHERE ticket_id = ?",
                (new_status, ticket_id)
            )

            conn.commit()

            return {
                "message": "Ticket status updated",
                "ticket_id": ticket_id,
                "status": new_status
            }

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()