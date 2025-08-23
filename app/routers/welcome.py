"""
Welcome router for the ATM system
"""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from ..utils.template_loader import load_template
from ..utils.logger import logger

# Create router
welcome_router = APIRouter(tags=["Welcome"])


@welcome_router.get("/", response_class=HTMLResponse)
async def welcome():
    """Welcome page with ATM system overview"""
    try:
        html_content = load_template("welcome.html")
        return HTMLResponse(content=html_content)
    except FileNotFoundError as e:
        logger.error(f"Template not found: {e}")
        return HTMLResponse(
            content="<h1>Welcome to DV ATM System</h1><p>Template loading error</p>",
            status_code=500
        )
