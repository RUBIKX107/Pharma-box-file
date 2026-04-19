from fastmcp import FastMCP
from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth
from classifier import classify_medical_doc

mcp = FastMCP("PharmaArchivist")

@mcp.tool()
async def organize_medical_file(file_id: str):
    """Downloads a file from Box, classifies it, and moves it to the right folder."""
    
    # 1. Logic to get text from Box (Simplified)
    # text_content = box_client.files.download_file(file_id)
    text_content = "Patient requires 500mg of Amoxicillin..." # Mock for example
    
    # 2. Run your Deep Learning logic
    category = classify_medical_doc(text_content)
    
    # 3. Logic to move file in Box based on category
    # box_client.files.update_file_by_id(file_id, parent={'id': folder_ids[category]})
    
    return f"File processed. Classified as: {category}. Moved to relevant folder."

if __name__ == "__main__":
    mcp.run()