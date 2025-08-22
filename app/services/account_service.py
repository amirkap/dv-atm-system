"""
Account Service - Unified business logic for account operations
"""

import threading
import uuid
from datetime import datetime
from typing import Dict
from collections import defaultdict
from fastapi import HTTPException, status

from ..schemas import Account, AccountCreateResponse, BalanceResponse, TransactionResponse
from ..config import settings
from ..utils.logger import logger

class AccountService:
    """Unified service for all account operations including transactions"""
    
    def __init__(self):
        """Initialize the account service with thread-safe storage"""
        self.accounts: Dict[str, Account] = {}
        # Global lock only for account creation/deletion and metadata operations
        self.global_lock = threading.RLock()
        # Per-account locks for transaction operations
        self.account_locks: Dict[str, threading.RLock] = defaultdict(threading.RLock)
    
    # Account Management Operations
    
    def create_account(self, initial_balance: float = 0.0) -> AccountCreateResponse:
        """Create a new account with initial balance"""
        with self.global_lock:
            if len(self.accounts) >= settings.MAX_ACCOUNTS:
                raise HTTPException(
                    status_code=status.HTTP_507_INSUFFICIENT_STORAGE,
                    detail=f"Maximum number of accounts ({settings.MAX_ACCOUNTS}) reached"
                )
            
            account_number = str(uuid.uuid4())
            now = datetime.now()
            
            account = Account(
                account_number=account_number,
                balance=initial_balance,
                created_at=now,
                last_updated=now
            )
            
            self.accounts[account_number] = account
            # Initialize the account lock (this is thread-safe due to defaultdict)
            _ = self.account_locks[account_number]
            
            logger.info(f"Created account {account_number} with balance {initial_balance}")
            
            return AccountCreateResponse(
                account_number=account_number,
                balance=initial_balance,
                message="Account created successfully"
            )
    
    def get_balance(self, account_number: str) -> BalanceResponse:
        """Get account balance"""
        with self.account_locks[account_number]:
            account = self._get_account_unsafe(account_number)
            return BalanceResponse(
                account_number=account.account_number,
                balance=account.balance
            )
    
    def delete_account(self, account_number: str) -> None:
        """Delete an account"""
        with self.global_lock:
            if account_number not in self.accounts:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Account not found"
                )
            # Get account lock first to ensure no ongoing transactions
            with self.account_locks[account_number]:
                del self.accounts[account_number]
                # Clean up the lock (optional, but good for memory)
                if account_number in self.account_locks:
                    del self.account_locks[account_number]
            logger.info(f"Deleted account {account_number}")
    
    def list_all_accounts(self) -> Dict:
        """List all accounts (for admin purposes)"""
        with self.global_lock:
            accounts_info = []
            for account_number, account in self.accounts.items():
                accounts_info.append({
                    "account_number": account_number,
                    "balance": account.balance,
                    "created_at": account.created_at.isoformat(),
                    "last_updated": account.last_updated.isoformat()
                })
            
            return {
                "total_accounts": len(accounts_info),
                "max_accounts": settings.MAX_ACCOUNTS,
                "accounts": accounts_info
            }
    
    def get_account_count(self) -> int:
        """Get total number of accounts"""
        with self.global_lock:
            return len(self.accounts)
    
    # Transaction Operations
    
    def withdraw_money(self, account_number: str, amount: float) -> TransactionResponse:
        """Process money withdrawal with atomic transaction"""
        try:
            return self._atomic_transaction(account_number, -amount, "withdrawal")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error withdrawing from account {account_number}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during withdrawal"
            )
    
    def deposit_money(self, account_number: str, amount: float) -> TransactionResponse:
        """Process money deposit with atomic transaction"""
        try:
            return self._atomic_transaction(account_number, amount, "deposit")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error depositing to account {account_number}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during deposit"
            )
    
    # Private Helper Methods
    
    def _get_account_unsafe(self, account_number: str) -> Account:
        """Get account by account number (must be called within appropriate lock)"""
        if account_number not in self.accounts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        return self.accounts[account_number]
    
    def _atomic_transaction(self, account_number: str, amount_change: float, transaction_type: str) -> TransactionResponse:
        """
        Perform an atomic transaction (deposit or withdrawal).
        
        Args:
            account_number: The account to modify
            amount_change: Positive for deposit, negative for withdrawal
            transaction_type: "deposit" or "withdrawal"
        
        Returns:
            TransactionResponse with updated account information
        """
        # Use per-account lock for maximum concurrency
        with self.account_locks[account_number]:
            # Get account (this will raise 404 if not found)
            account = self._get_account_unsafe(account_number)
            old_balance = account.balance
            new_balance = old_balance + amount_change
            
            # Check for insufficient funds on withdrawal
            if amount_change < 0 and new_balance < 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient funds"
                )
            
            # Update balance atomically
            account.balance = new_balance
            account.last_updated = datetime.now()
            self.accounts[account_number] = account
            
            # Get the absolute transaction amount for logging/response
            transaction_amount = abs(amount_change)
            
            logger.info(f"{transaction_type.title()}: Account {account_number}, Amount: {transaction_amount}, Old Balance: {old_balance}, New Balance: {new_balance}")
            
            return TransactionResponse(
                account_number=account_number,
                new_balance=new_balance,
                transaction_amount=transaction_amount,
                transaction_type=transaction_type,
                timestamp=account.last_updated
            )

# Global service instance
account_service = AccountService()
