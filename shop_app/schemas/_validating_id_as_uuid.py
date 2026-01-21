from typing import Any
from uuid import UUID


def validate_id_as_uuid(v_id: Any) -> str:
    """Validate that ID is a valid UUIDv4 string"""
    if isinstance(v_id, str):
        try:
            uuid_obj = UUID(v_id)
        except ValueError as e:
            raise ValueError("ID must be a valid UUIDv4 string") from e
        if uuid_obj.version != 4:
            raise ValueError(f"ID must be a UUIDv4 string, got version {uuid_obj.version}")
        return str(uuid_obj)
    if isinstance(v_id, UUID):
        if v_id.version != 4:
            raise ValueError(f"ID must be a UUIDv4, got version {v_id.version}")
        return str(v_id)
    raise ValueError("ID must be a string or UUIDv4")
