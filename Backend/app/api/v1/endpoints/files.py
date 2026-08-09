from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_db, get_current_user
from app.models.uploaded_file import UploadedFile
from app.models.userModel import UserModel
from app.core.s3 import get_s3_client, build_s3_key
from app.core.config import settings

router = APIRouter()


def local_storage_path(storage_key: str) -> Path:
    root = Path(settings.LOCAL_UPLOAD_DIR).resolve()
    path = (root / storage_key).resolve()
    if path != root and root not in path.parents:
        raise HTTPException(status_code=400, detail="Invalid storage path")
    return path


@router.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    file_bytes = file.file.read()

    if not file_bytes:
        raise HTTPException(status_code=400, detail="Empty file")

    safe_filename = Path(file.filename or "upload.bin").name
    s3_key = build_s3_key(str(current_user.id), safe_filename)

    if settings.FILE_STORAGE_BACKEND == "s3":
        s3 = get_s3_client()
        s3.put_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=s3_key,
            Body=file_bytes,
            ContentType=file.content_type or "application/octet-stream",
        )
    else:
        path = local_storage_path(s3_key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(file_bytes)

    row = UploadedFile(
        user_id=current_user.id,
        original_filename=safe_filename,
        s3_key=s3_key,
        content_type=file.content_type,
        size_bytes=len(file_bytes),
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return {
        "id": row.id,
        "original_filename": row.original_filename,
        "s3_key": row.s3_key,
        "content_type": row.content_type,
        "size_bytes": row.size_bytes,
    }


@router.get("")
def list_files(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    rows = (
        db.query(UploadedFile)
        .filter(UploadedFile.user_id == current_user.id)
        .order_by(UploadedFile.created_at.desc())
        .all()
    )

    result = []
    for row in rows:
        if settings.FILE_STORAGE_BACKEND == "s3":
            s3 = get_s3_client()
            url = s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": settings.S3_BUCKET_NAME, "Key": row.s3_key},
                ExpiresIn=3600,
            )
        else:
            url = f"{settings.API_V1_PREFIX}/files/{row.id}/download"
        result.append(
            {
                "id": row.id,
                "original_filename": row.original_filename,
                "s3_key": row.s3_key,
                "content_type": row.content_type,
                "size_bytes": row.size_bytes,
                "download_url": url,
            }
        )

    return result


@router.get("/{file_id}/download")
def download_file(
    file_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    row = (
        db.query(UploadedFile)
        .filter(
            UploadedFile.id == file_id,
            UploadedFile.user_id == current_user.id,
        )
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="File not found")

    if settings.FILE_STORAGE_BACKEND == "s3":
        s3 = get_s3_client()
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.S3_BUCKET_NAME, "Key": row.s3_key},
            ExpiresIn=3600,
        )
        return RedirectResponse(url)

    path = local_storage_path(row.s3_key)
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Stored file is missing")
    return FileResponse(
        path,
        media_type=row.content_type or "application/octet-stream",
        filename=row.original_filename,
    )
