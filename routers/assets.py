
from fastapi import APIRouter, HTTPException, status

from models.asset import AssetCreate
from services.asset_service import AssetService


router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)


# 1. Create a new asset
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_asset(asset: AssetCreate):
    result = AssetService.create_asset(asset)

    if "error" in result:
        raise HTTPException(
            status_code=409,
            detail=result["error"]
        )

    return result


# 2. Get all assets (NEW ENDPOINT)
@router.get("/")
def get_all_assets():
    return AssetService.get_all_assets()


# 3. Get one asset by ID
@router.get("/{asset_id}")
def get_asset(asset_id: str):
    result = AssetService.get_asset(asset_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return result


# 4. Update an asset
@router.put("/{asset_id}")
def update_asset(asset_id: str, asset: AssetCreate):
    result = AssetService.update_asset(
        asset_id,
        asset
    )

    if "error" in result:
        raise HTTPException(
            status_code=404,
            detail=result["error"]
        )

    return result


# 5. Delete an asset
@router.delete("/{asset_id}")
def delete_asset(asset_id: str):
    result = AssetService.delete_asset(asset_id)

    if "error" in result:
        raise HTTPException(
            status_code=404,
            detail=result["error"]
        )

    return result
