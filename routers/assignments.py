from fastapi import APIRouter, HTTPException
from models.assignment import AssignmentCreate
from services.assignment_service import AssignmentService


router = APIRouter(
    prefix="/assignments",
    tags=["Assignments"]
)

@router.post("/")
def assign_asset(assignment: AssignmentCreate):
    result = AssignmentService.assign_asset(
        assignment.asset_id,
        assignment.employee_id
    )

    if "error" in result:
        raise HTTPException(
            status_code=409,
            detail=result["error"]
        )

    return result


@router.put("/{asset_id}/return")
def return_asset(asset_id: str):
    return AssignmentService.return_asset(asset_id)