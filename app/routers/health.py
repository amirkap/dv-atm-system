"""
Health check endpoints
"""

from fastapi import APIRouter
from datetime import datetime

from ..services.account_service import account_service
from ..config import settings

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():
    """Health check endpoint for load balancer"""
    return {
        "status": "healthy", 
        "accounts_count": account_service.get_account_count(),
        "max_accounts": settings.MAX_ACCOUNTS,
        "timestamp": datetime.now().isoformat(),
        "version": settings.APP_VERSION
    }
