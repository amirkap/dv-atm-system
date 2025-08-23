"""Routers module"""
from .accounts import router as accounts_router
from .health import router as health_router
from .welcome import welcome_router

__all__ = ["accounts_router", "health_router", "welcome_router"]
