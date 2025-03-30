"""
Analyzes a document using Azure Document Intelligence 'Read' model for optical character recognition (OCR).

Args:
    endpoint (str): The Azure Document Intelligence service endpoint URL.
    key (str): The Azure service authentication key.
    file_path (str, optional): Local path to the document file to be analyzed. Defaults to None.
    doc_url (str, optional): URL of the document to be analyzed. Defaults to None.

Returns:
    AnalyzeResult: The result of the document analysis, containing extracted text and other metadata.
    None: If document analysis fails or no input is provided.

Raises:
    Prints error messages for invalid input or analysis failures.
"""
import os
from utils.config import load_config
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult, AnalyzeDocumentRequest

config = load_config()
root_path = config["root_path"]

def azure_ocr_info(file_path: str):
    # Create outputs/ocr directory if it doesn't exist
    ocr_dir = os.path.join(root_path, "outputs", "ocr")
    os.makedirs(ocr_dir, exist_ok=True)

    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    # Create output filename with the same base name but .txt extension
    ocr_path = os.path.join(ocr_dir, f"{base_name}.txt")

    return base_name, ocr_path

def analyze_document_read(endpoint: str, key: str, file_path: str = None, doc_url: str = None, save_output: bool = False):
    """Analyzes a document using the Document Intelligence 'Read' model."""

    if not file_path and not doc_url:
        print("Error: Please provide either a file_path or a doc_url.")
        return
    if file_path and not os.path.exists(file_path):
         print(f"Error: File not found at {file_path}")
         return

    print(f"Analyzing document using model 'prebuilt-layout'...")

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    # Prepare the request based on input type
    analyze_request = None
    if file_path:
        with open(file_path, "rb") as f:
            # Pass binary content directly
            analyze_request = f.read()

    elif doc_url:
        analyze_request = AnalyzeDocumentRequest(url_source=doc_url)

    # Use the 'prebuilt-layout' model for OCR
    poller = document_intelligence_client.begin_analyze_document(
        model_id="prebuilt-layout", body=analyze_request, content_type="application/octet-stream" if file_path else None
    )

    try:
        result: AnalyzeResult = poller.result()  # Wait for analysis to complete
        print("OCR process complete.")

        if result.content:
            # Print the first couple of words
            # print(f"Extracted Text (first 1000 chars):\n{result.content[:1000]}...")

            # Save the OCR result to a file if requested and we have a file_path
            if save_output and file_path:
                _, ocr_path = azure_ocr_info(file_path)

                with open(ocr_path, "w", encoding="utf-8") as output_file:
                    output_file.write(result.content)
                print(f"OCR result saved to: {ocr_path}")

        else:
            print("No text content found in the document.")

        return result

    except Exception as e:
        print(f"An error occurred during Document Intelligence analysis: {e}")
        return None
