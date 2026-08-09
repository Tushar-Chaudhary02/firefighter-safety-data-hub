import csv
import io

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.v1.web_api.responseDTO.SmokeSamplerDataResponse import (
    SmokeSamplerDataResponse,
    SmokeSamplerJoinedRow,
)
from app.core.deps import get_db
from app.core.security import decode_access_token
from app.models.SmokeSamplerModel import (
    SmokeSamplerSampleModel,
    SmokeSamplerSubmissionModel,
)
from app.models.userResearcherModel import UserResearcherModel

smoke_sampler_table_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/web_api/auth/login")


def _verify_researcher(token: str, db: Session) -> UserResearcherModel:
    data = decode_access_token(token)
    user = db.query(UserResearcherModel).filter(UserResearcherModel.id == data.get("sub")).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if user.refresh_token != token:
        raise HTTPException(status_code=401, detail="Invalid Token")

    return user


@smoke_sampler_table_router.get("/smoke-sampler-data", response_model=SmokeSamplerDataResponse)
def get_smoke_sampler_data(
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

    base = (
        select(SmokeSamplerSampleModel, SmokeSamplerSubmissionModel)
        .join(
            SmokeSamplerSubmissionModel,
            SmokeSamplerSampleModel.submission_id == SmokeSamplerSubmissionModel.submission_id,
        )
        .order_by(
            SmokeSamplerSubmissionModel.created_at.desc(),
            SmokeSamplerSampleModel.sample_id,
        )
    )

    stmt = base.limit(limit).offset(offset_data)
    count_stmt = select(func.count()).select_from(SmokeSamplerSampleModel)

    rows = db.execute(stmt).all()
    count = db.scalar(count_stmt) or 0

    results = [
        SmokeSamplerJoinedRow(
            sample_id=sample.sample_id,
            submission_id=sub.submission_id,
            user_id=sub.user_id,
            submission_created_at=sub.created_at,
            chemical_name=sample.chemical_name,
            percentage_proportion=sample.percentage_proportion,
        )
        for sample, sub in rows
    ]

    return SmokeSamplerDataResponse(results=results, count=count)


@smoke_sampler_table_router.get("/export-smoke-sampler-data")
def export_smoke_sampler_csv(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    _verify_researcher(token, db)

    stmt = (
        select(SmokeSamplerSampleModel, SmokeSamplerSubmissionModel)
        .join(
            SmokeSamplerSubmissionModel,
            SmokeSamplerSampleModel.submission_id == SmokeSamplerSubmissionModel.submission_id,
        )
        .order_by(
            SmokeSamplerSubmissionModel.created_at.desc(),
            SmokeSamplerSampleModel.sample_id,
        )
    )
    rows = db.execute(stmt).all()

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        [
            "sample_id",
            "submission_id",
            "user_id",
            "submission_created_at",
            "chemical_name",
            "percentage_proportion",
        ]
    )

    for sample, sub in rows:
        writer.writerow(
            [
                str(sample.sample_id),
                str(sub.submission_id),
                sub.user_id,
                sub.created_at.isoformat() if sub.created_at is not None else "",
                sample.chemical_name,
                sample.percentage_proportion,
            ]
        )

    csv_bytes = buffer.getvalue().encode("utf-8")
    return Response(
        content=csv_bytes,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="smoke_sampler_data.csv"'},
    )
