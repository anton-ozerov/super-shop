from typing import Any

from pydantic import BaseModel, Field, field_validator

from shop_app.schemas._validating_id_as_uuid import validate_id_as_uuid


class MarkOut(BaseModel):
    id: str = Field(..., description="Unique ID for the product mark in UUIDv4 format")
    name: str = Field(..., description="Name of the mark")
    banner_color_code: str = Field(..., description="Banner color code in HEX format")
    text_color_code: str = Field(..., description="Text color code in HEX format")
    is_visible: bool = Field(..., description="Indicates if the mark is visible")

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v: Any) -> str:
        """Validate that ID is a valid UUIDv4 string"""
        return validate_id_as_uuid(v_id=v)
