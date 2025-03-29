"""
This module serves as the main entry point for the document analysis application.
It provides functionality to analyze documents using either Azure's Computer Vision
or Google Cloud Vision API services.

The module handles:
- Configuration loading for both services
- File type validation
- Document processing and analysis
- User interaction for service selection
"""
from utils.azure_config import load_config_azure
from utils.azure_analyzer import analyze_document_read

def main():
    """
    Main function that orchestrates the document analysis workflow.
    
    Args:
        service (str): The service to use for document analysis.
                      Valid values are 'azure' or 'google'.
    
    Returns:
        None
    
    The function performs the following steps:
    1. Loads configuration from environment variables
    2. Extracts necessary configuration values
    3. Initiates document analysis based on selected service
    4. Handles document processing with appropriate parameters
    """
    
    # Load Azure-specific configuration
    config = load_config_azure()

    # Extract required configuration values from the loaded config
    endpoint = config["endpoint"]  # API endpoint for the analysis service
    key = config["key"]           # Authentication key for the service
    file_path = config["file_path"]  # Path to the document to be analyzed
    
    # Analyze the document using the provided configuration
    result = analyze_document_read(endpoint, key, file_path=file_path, save_output=False) 
    

if __name__ == "__main__":
    main()
