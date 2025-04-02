"""
Generates a Markdown-formatted document from OCR text using Gemini.

This script uses the Gemini 1.5 Pro to convert OCR-extracted text into a well-structured Markdown document. 
It follows specific guidelines for formatting headings, lists, tables, emphasis, paragraphs, code blocks, 
and links while preserving the original document's structure.
"""
import os
from google import genai
from utils.config import load_config
from utils.azure_analyzer import azure_ocr_info

config = load_config()
api_key = config["api_key"]

client = genai.Client(api_key=api_key)

root_path = config["root_path"] # Path to the root directory of the application
file_path = config["file_path"]  # Path to the document to be analyzed

# Fetch the base name and ocr path from the azure_ocr_info function in azure_analyzer.py
base_name, ocr_path = azure_ocr_info(file_path)

prompt = f"""You are an expert in converting OCR text into well-structured Markdown documents.
You will be provided with the OCR text extracted from an image or document.
Your task is to analyze this text and reformat it into a clean, readable Markdown document,
preserving the original document's structure as much as possible.

Here are the guidelines:

1. Headings: Identify headings and subheadings based on font size, positioning, and surrounding text.
Use appropriate Markdown heading levels (e.g., # for main title, ## for section headings, ### for sub-sections).

2. Lists: Detect bulleted or numbered lists and format them using Markdown list syntax (* for unordered, 1. 2. 3. for ordered).

3. Tables: Identify tabular data. Format tables using Markdown table syntax. Ensure proper column alignment.
If the table has a header row, clearly mark it.

4. Emphasis: Use Markdown's emphasis syntax (*italics* or **bold**) where appropriate to highlight key words or phrases,
mimicking the original document's emphasis.

5. Paragraphs: Separate paragraphs with blank lines.

6. Code Blocks: If the document contains code snippets, format them using Markdown code blocks (```).
Specify the programming language if possible.

7. Links: Identify and preserve any URLs or links using Markdown link syntax ([link text](URL)).

8. Spacing & Line Breaks: Preserve significant spacing and line breaks to maintain the document's visual structure.

Input:
{file_path}
{ocr_path}

Example Table Output:

| Header 1 | Header 2 | Header 3 |
| -------- | -------- | -------- |
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |

Example List Output:

* Item 1
* Item 2
    * Sub-item 1
    * Sub-item 2
* Item 3
 
Now, only return all of the formatted Markdown output given in the OCR, Do not include any introductory or concluding remarks."""

def gemini_markdown():
    response = client.models.generate_content(
        model = "gemini-1.5-pro", contents=prompt
    )

    return response.text

def gemini_markdown_save(file_path: str):
    response = gemini_markdown()
    
    # Create output/markdown directory if it doesn't exist
    markdown_dir = os.path.join(root_path, "output", "markdown")
    os.makedirs(markdown_dir, exist_ok=True)    

    # Create markdown filename 
    markdown_file = os.path.join(markdown_dir, f"{base_name}.md")
    
    # Write response to markdown file
    with open(markdown_file, 'w') as f:
        f.write(response)
        
    print(f"Markdown file saved to: {markdown_file}")
    return markdown_file
