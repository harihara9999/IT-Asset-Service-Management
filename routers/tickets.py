
from fastapi import APIRouter, HTTPException

from models.ticket import TicketCreate
from services.ticket_service import TicketService


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


# 1. Create a new ticket
@router.post("/")
def create_ticket(ticket: TicketCreate):
    result = TicketService.create_ticket(ticket)

    if result.get("error") == "Asset not found":
        raise HTTPException(
            status_code=404,
            detail=result["error"]
        )

    return result


# 2. Get all tickets (NEW ENDPOINT)
@router.get("/")
def get_all_tickets():
    return TicketService.get_all_tickets()


# 3. Assign a technician to a ticket
@router.put("/{ticket_id}/assign-technician")
def assign_technician(ticket_id: str, technician_id: str):
    return TicketService.assign_technician(
        ticket_id,
        technician_id
    )


# 4. Resolve a ticket
@router.put("/{ticket_id}/resolve")
def resolve_ticket(ticket_id: str, diagnosis: str):
    return TicketService.resolve_ticket(
        ticket_id,
        diagnosis
    )


# 5. Get one ticket by ID
@router.get("/{ticket_id}")
def get_ticket(ticket_id: str):
    result = TicketService.get_ticket(ticket_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return result


# 6. Change ticket status
@router.put("/{ticket_id}/status")
def change_status(ticket_id: str, new_status: str):
    result = TicketService.change_status(
        ticket_id,
        new_status
    )

    if "error" in result:
        raise HTTPException(
            status_code=409,
            detail=result["error"]
        )

    return result
