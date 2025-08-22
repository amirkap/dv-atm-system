"""
Configuration settings for the ATM System
"""

import os
from typing import Optional

class Settings:
    """Application settings"""
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = int(os.getenv("PORT", "8000"))  # Render sets PORT automatically
    
    # Application settings
    APP_NAME: str = "DV ATM System"
    APP_DESCRIPTION: str = "A thread-safe ATM system for DoubleVerify assignment"
    APP_VERSION: str = "1.0.0"
    
    # Account settings
    MAX_ACCOUNTS: int = int(os.getenv("MAX_ACCOUNTS", "1000"))
    MIN_BALANCE: float = 0.0
    MAX_TRANSACTION_AMOUNT: float = float(os.getenv("MAX_TRANSACTION_AMOUNT", "10000.0"))
    
    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"
    
    # Production settings
    RENDER_EXTERNAL_URL: Optional[str] = os.getenv("RENDER_EXTERNAL_URL")
    IS_RENDER: bool = os.getenv("RENDER") == "true"

# Global settings instance
settings = Settings()
