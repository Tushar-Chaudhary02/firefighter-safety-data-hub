from fastapi import APIRouter, status
from pydantic import BaseModel, EmailStr, Field


support_router = APIRouter()


class ContactRequest(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    subject: str = Field(min_length=1)
    message: str = Field(min_length=1)


class AccountRequest(BaseModel):
    fullName: str = Field(min_length=1)
    workEmail: EmailStr
    company: str = Field(min_length=1)
    jobTitle: str = Field(min_length=1)
    reason: str = Field(min_length=20)


@support_router.post("/contact", status_code=status.HTTP_202_ACCEPTED)
def submit_contact(payload: ContactRequest):
    print(f"LOCAL CONTACT REQUEST from {payload.name} <{payload.email}>: {payload.subject}")
    return {"message": "Contact request accepted for local testing"}


@support_router.post("/account-requests", status_code=status.HTTP_202_ACCEPTED)
def submit_account_request(payload: AccountRequest):
    print(f"LOCAL ACCOUNT REQUEST from {payload.fullName} <{payload.workEmail}>")
    return {"message": "Account request accepted for local testing"}

