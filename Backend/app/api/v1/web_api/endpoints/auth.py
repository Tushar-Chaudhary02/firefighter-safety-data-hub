from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import get_db
from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.models.userResearcherModel import UserResearcherModel
from app.services.email_service import email_service

# Request DTOs
from app.api.v1.web_api.requestDTO.loginRequestDTO import LoginRequestDTO
from app.api.v1.web_api.requestDTO.registerRequestDTO import RegisterRequestDTO
from app.api.v1.web_api.requestDTO.updateMeRequestDTO import UpdateMeRequestDTO
from app.api.v1.web_api.requestDTO.passwordResetRequestDTO import PasswordResetRequestDTO


web_auth = APIRouter()
oauth2_web_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/web_api/auth/login")
_reset_serializer = URLSafeTimedSerializer(settings.EMAIL_TOKEN_SECRET)


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str = Field(min_length=1)
    newPassword: str = Field(min_length=8)


def _to_frontend_researcher_role(role: str) -> str:
    normalized = (role or "").lower().replace("-", "_").replace(" ", "_")
    if "admin" in normalized:
        return "RESEARCH_ADMIN"
    return "RESEARCHER"


def _researcher_payload(user: UserResearcherModel) -> dict:
    return {
        "id": str(user.id),
        "firstName": user.first_name,
        "lastName": user.last_name or "",
        "universityEmail": user.university_email,
        "personalEmail": user.personal_email,
        "role": _to_frontend_researcher_role(user.role),
        "phoneNumber": user.phonenumber,
    }


def get_current_researcher(
    token: str = Depends(oauth2_web_scheme),
    db: Session = Depends(get_db),
) -> UserResearcherModel:
    payload = decode_access_token(token)
    user = (
        db.query(UserResearcherModel)
        .filter(UserResearcherModel.id == payload.get("sub"))
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


@web_auth.get("/me")
def me(current: UserResearcherModel = Depends(get_current_researcher)):
    return _researcher_payload(current)


@web_auth.put("/me")
def update_me(
    payload: UpdateMeRequestDTO,
    current: UserResearcherModel = Depends(get_current_researcher),
    db: Session = Depends(get_db),
):
    if payload.personal_email is not None:
        existing = (
            db.query(UserResearcherModel)
            .filter(
                UserResearcherModel.personal_email == str(payload.personal_email),
                UserResearcherModel.id != current.id,
            )
            .first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="Personal email already in use")

    if payload.first_name is not None:
        current.first_name = payload.first_name
    if payload.last_name is not None:
        current.last_name = payload.last_name
    if payload.personal_email is not None:
        current.personal_email = str(payload.personal_email)
    if payload.phoneNumber is not None:
        current.phonenumber = payload.phoneNumber

    db.commit()
    db.refresh(current)
    return _researcher_payload(current)


@web_auth.post("/password-reset")
def password_reset(
    payload: PasswordResetRequestDTO,
    current: UserResearcherModel = Depends(get_current_researcher),
    db: Session = Depends(get_db),
):
    if not verify_password(payload.password, current.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
        )

    current.password_hash = hash_password(payload.newPassword)
    db.commit()
    return {"ok": True}


@web_auth.post("/login")
def login(payload: LoginRequestDTO, db: Session = Depends(get_db)):
    user = (
        db.query(UserResearcherModel)
        .filter(UserResearcherModel.university_email == payload.email)
        .first()
    )

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials",
        )

    token = create_access_token(subject=user.id, role=user.role)
    user.refresh_token = token
    db.commit()

    return {
        "user": _researcher_payload(user),
        "access_token": token,
        "token_type": "bearer",
    }


@web_auth.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequestDTO, db: Session = Depends(get_db)):
    existing = (
        db.query(UserResearcherModel)
        .filter(UserResearcherModel.university_email == payload.university_email)
        .first()
    )

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = UserResearcherModel(
        first_name=payload.first_name,
        last_name=payload.last_name,
        university_email=payload.university_email,
        personal_email=payload.personal_email,
        password_hash=hash_password(payload.password),
        role=payload.role.lower(),
        phonenumber=payload.phoneNumber,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Researcher account created", "user": _researcher_payload(user)}


@web_auth.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Create a short-lived reset link.

    In the default local setup the email backend prints the link in the backend
    terminal. The endpoint deliberately returns the same message for known and
    unknown email addresses.
    """
    user = (
        db.query(UserResearcherModel)
        .filter(UserResearcherModel.university_email == str(payload.email))
        .first()
    )

    if user:
        token = _reset_serializer.dumps(
            {
                "sub": str(user.id),
                "email": user.university_email,
                "purpose": "researcher_password_reset",
            },
            salt="researcher-password-reset",
        )
        reset_link = f"{settings.WEB_FRONTEND_BASE_URL.rstrip('/')}/reset-password?token={token}"
        email_service.send_email(
            to_email=user.university_email,
            subject="Firefighter Data Hub - Researcher Password Reset",
            html_body=(
                "<p>A password reset was requested for your researcher account.</p>"
                f"<p><a href=\"{reset_link}\">Reset your password</a></p>"
                "<p>If you did not request this, you can ignore this message.</p>"
            ),
            text_body=(
                "A password reset was requested for your researcher account.\n\n"
                f"Reset link: {reset_link}\n\n"
                "If you did not request this, you can ignore this message."
            ),
        )

    return {"message": "If this email is registered, a reset link has been created."}


@web_auth.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        data = _reset_serializer.loads(
            payload.token,
            salt="researcher-password-reset",
            max_age=3600,
        )
    except SignatureExpired as exc:
        raise HTTPException(status_code=400, detail="Reset token has expired") from exc
    except BadSignature as exc:
        raise HTTPException(status_code=400, detail="Invalid reset token") from exc

    if data.get("purpose") != "researcher_password_reset":
        raise HTTPException(status_code=400, detail="Invalid reset token")

    user = (
        db.query(UserResearcherModel)
        .filter(UserResearcherModel.id == data.get("sub"))
        .first()
    )
    if not user or user.university_email != data.get("email"):
        raise HTTPException(status_code=400, detail="Invalid reset token")

    user.password_hash = hash_password(payload.newPassword)
    user.refresh_token = None
    db.commit()

    return {"ok": True}


@web_auth.post("/resend-verification")
def resend_verification(payload: ForgotPasswordRequest):
    # Researcher accounts in the local demo do not require a separate email
    # verification workflow. Keep this compatibility endpoint so older UI links
    # fail gracefully instead of returning 404.
    return {
        "message": (
            "Researcher accounts are available immediately after registration "
            "in the local demo; no verification email is required."
        )
    }
