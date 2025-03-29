"""
This module serves as the main entry point for the document analysis application.
It loads configuration settings and initiates the document analysis process.
"""

# Import configuration loading utility from utils.config module
from utils.azure_config import load_config_azure
from utils.google_config import load_config_google
# Import document analysis function from utils.analyzer module
from utils.azure_analyzer import analyze_document_read
from utils.google_analyzer import process_document_ocr

def main(service):
    """
    Main function that orchestrates the document analysis workflow.
    
    The function performs the following steps:
    1. Loads configuration from environment variables
    2. Extracts necessary configuration values
    3. Initiates document analysis
    """
    
    if service == "azure":
        config = load_config_azure()

        # Extract required configuration values from the loaded config
        endpoint = config["endpoint"]  # API endpoint for the analysis service
        key = config["key"]           # Authentication key for the service
        file_path = config["file_path"]  # Path to the document to be analyzed
        
        # Analyze the document using the provided configuration
        result = analyze_document_read(endpoint, key, file_path=file_path, save_output=True) 

    elif service == "google":
        config = load_config_google()
    else:
        print("Invalid service selection. Please choose 'azure' or 'google'.")
        return
    


if __name__ == "__main__":
    print(f"Choose service to use for OCR:")
    print("azure" + "/" + "google")
    service = input("Enter the number of the service you want to use: ")

    main(service)
