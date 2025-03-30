"""Configuration utilities for Azure Document Intelligence and Gemini.

This module provides functionality to load configuration settings from environment variables
using a .env file. It handles the Azure Document Intelligence credentials and document paths as well as
the Gemini API key.

Returns:
    dict: A configuration dictionary.
"""
import os
from dotenv import load_dotenv

def load_config():
    """Load configuration settings from environment variables.
    
    Loads the following settings from .env file:
    - AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT: Azure service endpoint URL
    - AZURE_DOCUMENT_INTELLIGENCE_KEY: Authentication key for Azure service
    - DOCUMENT_FILE_PATH: Path to the document file to be processed
    - GEMINI_API_KEY: API key for Gemini service
    
    Returns:
        dict: Configuration dictionary containing endpoint, key and file path
    """
    # Load variables from .env file into environment
    load_dotenv()
    
    # Create config dictionary with required settings
    config = {
        "file_path": os.getenv("DOCUMENT_FILE_PATH"),
        "endpoint": os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
        "key": os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY"),
        "api_key": os.getenv("GEMINI_API_KEY")
    }
    
    return config
