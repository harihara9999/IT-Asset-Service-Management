from pydantic import BaseModel


class AssignmentCreate(BaseModel):
    asset_id: str       # Which asset are we assigning?
    employee_id: str    #Which employee receives it?