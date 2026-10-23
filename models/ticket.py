from pydantic import BaseModel


class TicketCreate(BaseModel):
    ticket_id: str
    asset_id: str
    employee_id: str
    title: str
    description: str
    priority: str = "MEDIUM"