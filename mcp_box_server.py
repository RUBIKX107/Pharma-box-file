import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth

load_dotenv()

mcp = FastMCP("Pharma_Archivist")

def get_box_client():
    """Initializes the Box Client using the Developer Token from .env"""
    token = os.getenv("BOX_DEVELOPER_TOKEN")
    if not token:
        raise ValueError("BOX_DEVELOPER_TOKEN not found in .env")
    auth = BoxDeveloperTokenAuth(token=token)
    return BoxClient(auth=auth)

@mcp.tool()
def smart_process_medical_file(file_id: str):
    """
    Processes a medical file intelligently:
    - Small files: Downloaded for local Deep Learning analysis.
    - Large files: Uses Box AI (Cloud) to save local memory.
    """
    client = get_box_client()
    
    # 1. Get file metadata (size and name) without downloading the content
    file_info = client.files.get_file_by_id(file_id, fields=["size", "name"])
    file_size_mb = file_info.size / (1024 * 1024)
    
    print(f"Checking {file_info.name}... Size: {file_size_mb:.2f} MB")

    # We set a 5MB threshold to protect our RAM
    MEMORY_THRESHOLD_MB = 5.0

    if file_size_mb < MEMORY_THRESHOLD_MB:
        # Option A: Small file. Safe to download to RAM.
        content = client.files.download_file(file_id).content
        # Future: Insert your PyTorch/Transformers logic here
        return f"File '{file_info.name}' is small. Downloaded to local memory for DL analysis."
    
    else:
        # Option B: File is too big! Let the Box Cloud handle it.
        try:
            # We use Box AI to summarize findings without using our local memory
            ai_response = client.ai.extract_metadata_freeform(
                prompt="Summarize the medical findings and list mentioned medications.",
                items=[{"id": file_id, "type": "file"}]
            )
            return (f"File '{file_info.name}' is too large ({file_size_mb:.2f} MB). "
                    f"Processed via Box AI Cloud. Summary: {ai_response.answer}")
        except Exception as e:
            return f"File too large and Box AI processing failed: {str(e)}"