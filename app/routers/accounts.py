"""
Unified Account Router - All account operations including transactions
"""

from fastapi import APIRouter, HTTPException, status

from ..schemas import (
    AccountCreate, 
    AccountCreateResponse, 
    BalanceResponse,
    TransactionRequest,
    TransactionResponse
)
from ..services.account_service import account_service
from ..utils.logger import logger

router = APIRouter(prefix="/accounts", tags=["accounts"])

# Account Management Endpoints

@router.post("", response_model=AccountCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_account(account_data: AccountCreate):
    """Create a new account with optional initial balance"""
    try:
        return account_service.create_account(account_data.initial_balance)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating account: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during account creation"
        )

@router.get("/{account_number}/balance", response_model=BalanceResponse)
async def get_balance(account_number: str):
    """Retrieve the current balance of the user's account"""
    try:
        return account_service.get_balance(account_number)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting balance for account {account_number}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during balance retrieval"
        )

@router.delete("/{account_number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(account_number: str):
    """Delete an account"""
    try:
        account_service.delete_account(account_number)
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting account {account_number}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during account deletion"
        )

@router.get("")
async def list_accounts():
    """List all accounts (for admin/debugging purposes)"""
    try:
        return account_service.list_all_accounts()
    except Exception as e:
        logger.error(f"Error listing accounts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during account listing"
        )

# Transaction Endpoints

@router.post("/{account_number}/withdraw", response_model=TransactionResponse)
async def withdraw_money(account_number: str, transaction: TransactionRequest):
    """Withdraw a specified amount of money from the user's account"""
    return account_service.withdraw_money(account_number, transaction.amount)

@router.post("/{account_number}/deposit", response_model=TransactionResponse)
async def deposit_money(account_number: str, transaction: TransactionRequest):
    """Deposit a specified amount of money into the user's account"""
    return account_service.deposit_money(account_number, transaction.amount)