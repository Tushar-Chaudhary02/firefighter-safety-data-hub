import csv
import io

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.security import decode_access_token
from app.models.PpeModel import PpeModel
from app.models.userResearcherModel import UserResearcherModel
from app.api.v1.web_api.responseDTO.PpeDataResponse import PpeDataResponse

ppe_table_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/web_api/auth/login")


def _verify_researcher(token: str, db: Session) -> UserResearcherModel:
    data = decode_access_token(token)
    user = db.query(UserResearcherModel).filter(UserResearcherModel.id == data.get("sub")).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if user.refresh_token != token:
        raise HTTPException(status_code=401, detail="Invalid Token")

    return user


@ppe_table_router.get("/ppedata", response_model=PpeDataResponse)
def get_ppe_data(
    limit: int,
    page: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    _verify_researcher(token, db)

    if page < 1:
        page = 1
    if limit < 1:
        limit = 10

    offset_data = (page - 1) * limit

    stmt = (
        select(PpeModel).order_by(PpeModel.created_at.desc()).limit(limit).offset(offset_data)
    )
    count_stmt = select(func.count()).select_from(PpeModel)

    results = db.scalars(stmt).all()
    count = db.scalar(count_stmt)

    return {"count": count, "results": results}


@ppe_table_router.get("/export-ppe-data")
def export_ppe_data_csv(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    _verify_researcher(token, db)

    rows = db.scalars(select(PpeModel).order_by(PpeModel.created_at.desc())).all()

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        [
            "ppe_id",
            "user_id",
            "event_id",
            "helmet_id",
            "hood_id",
            "face_mask_id",
            "scba_id",
            "glove_id",
            "boot_id",
            "bunker_coat_id",
            "bunker_pants_id",
            "is_ppe_updated",
            "created_at",
        ]
    )

    for row in rows:
        writer.writerow(
            [
                str(row.ppe_id),
                row.user_id,
                str(row.event_id) if row.event_id is not None else "",
                row.helmet_id,
                row.hood_id,
                row.face_mask_id,
                row.scba_id,
                row.glove_id,
                row.boot_id,
                row.bunker_coat_id,
                row.bunker_pants_id,
                row.is_ppe_updated,
                row.created_at.isoformat() if row.created_at is not None else "",
            ]
        )

    csv_bytes = buffer.getvalue().encode("utf-8")
    return Response(
        content=csv_bytes,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="ppe_data.csv"'},
    )
