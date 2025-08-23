"""
Template loader utility for HTML templates
"""
import os
from pathlib import Path


def load_template(template_name: str) -> str:
    """
    Load an HTML template from the templates directory
    
    Args:
        template_name: Name of the template file (e.g., 'welcome.html')
        
    Returns:
        The HTML content as a string
    """
    # Get the path to the templates directory
    current_dir = Path(__file__).parent.parent
    template_path = current_dir / "templates" / template_name
    
    # Check if template exists
    if not template_path.exists():
        raise FileNotFoundError(f"Template '{template_name}' not found at {template_path}")
    
    # Read and return the template content
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read()
