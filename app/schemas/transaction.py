"""
Transaction-related Pydantic schemas
"""

from pydantic import BaseModel, Field, validator
from datetime import datetime
from ..config import settings

class TransactionRequest(BaseModel):
    """Transaction request (deposit/withdraw)"""
    amount: float = Field(
        gt=0, 
        le=settings.MAX_TRANSACTION_AMOUNT, 
        description=f"Amount must be positive and not exceed {settings.MAX_TRANSACTION_AMOUNT}"
    )

class TransactionResponse(BaseModel):
    """Transaction response"""
    account_number: str
    new_balance: float
    transaction_amount: float
    transaction_type: str
    timestamp: datetime
