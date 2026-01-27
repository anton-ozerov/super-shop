from typing import Any

from pydantic import BaseModel, Field, field_validator

from shop_app.schemas._validating_id_as_uuid import validate_id_as_uuid


class ProductParameterOut(BaseModel):
    id: str = Field(..., description="Unique ID for the product parameter in UUIDv4 format")
    name: str = Field(..., description="Name of the parameter")
    value: str = Field(..., description="Value of the parameter")
    price: int = Field(..., description="Price of the product with this parameter")
    old_price: int = Field(..., description="Old price of the product with this parameter")
    is_main: bool = Field(..., description="Indicates if this parameter is the main one for the product")

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v: Any) -> str:
        """Validate that ID is a valid UUIDv4 string"""
        return validate_id_as_uuid(v_id=v)
