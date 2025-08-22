"""
Account-related Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from ..config import settings

class AccountBase(BaseModel):
    """Base account model"""
    account_number: str
    balance: float = Field(ge=0, description="Account balance must be non-negative")

class Account(AccountBase):
    """Account model with timestamps"""
    created_at: datetime
    last_updated: datetime

class AccountCreate(BaseModel):
    """Account creation request"""
    initial_balance: float = Field(
        default=0.0, 
        ge=0, 
        le=settings.MAX_TRANSACTION_AMOUNT,
        description="Initial balance must be non-negative"
    )

class AccountCreateResponse(BaseModel):
    """Account creation response"""
    account_number: str
    balance: float
    message: str

class BalanceResponse(BaseModel):
    """Balance check response"""
    account_number: str
    balance: float
