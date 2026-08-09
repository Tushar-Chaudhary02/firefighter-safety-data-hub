from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


class PpeData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ppe_id: UUID
    user_id: str
    event_id: Optional[UUID] = None
    helmet_id: str
    hood_id: str
    face_mask_id: str
    scba_id: str
    glove_id: str
    boot_id: str
    bunker_coat_id: str
    bunker_pants_id: str
    is_ppe_updated: bool
    created_at: datetime

    @field_validator("user_id", mode="before")
    @classmethod
    def user_id_uuid_to_str(cls, v: object) -> object:
        if isinstance(v, UUID):
            return str(v)
        return v


class PpeDataResponse(BaseModel):
    results: list[PpeData] = []
    count: int = 0
