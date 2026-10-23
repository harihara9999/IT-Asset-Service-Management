from pydantic import BaseModel


class AssetCreate(BaseModel):
    asset_id: str
    type: str
    brand: str
    model: str
    serial_no: str
    purchase_date: str