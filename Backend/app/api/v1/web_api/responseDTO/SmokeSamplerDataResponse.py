from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SmokeSamplerJoinedRow(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sample_id: UUID
    submission_id: UUID
    user_id: str
    submission_created_at: datetime
    chemical_name: str
    percentage_proportion: float


class SmokeSamplerDataResponse(BaseModel):
    results: list[SmokeSamplerJoinedRow] = []
    count: int = 0
