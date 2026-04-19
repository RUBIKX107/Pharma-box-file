import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth

# טעינת המשתנים מה-env. ה-Git מתעלם מזה, אז הכל בטוח.
load_dotenv()

# יצירת השרת - זה מה שה-AI יזהה
mcp = FastMCP("Pharma_Archivist")

def get_box_client():
    """יוצר חיבור ל-Box באמצעות ה-Token הזמני"""
    token = os.getenv("BOX_DEVELOPER_TOKEN")
    if not token:
        raise ValueError("Missing BOX_DEVELOPER_TOKEN in .env file")
    auth = BoxDeveloperTokenAuth(token=token)
    return BoxClient(auth=auth)

@mcp.tool()
def list_medical_documents(folder_id: str = "0"):
    """
    סורק תיקייה ב-Box ומחזיר רשימת קבצים (מרשמים, בדיקות מעבדה).
    ברירת מחדל היא תיקיית השורש (ID: 0).
    """
    try:
        client = get_box_client()
        items = client.folders.get_folder_items(folder_id)
        
        if not items.entries:
            return "התיקייה ריקה או שלא נמצאו קבצים."
            
        file_list = [f"- {item.name} (ID: {item.id})" for item in items.entries]
        return "נמצאו המסמכים הבאים:\n" + "\n".join(file_list)
    except Exception as e:
        return f"שגיאה בחיבור ל-Box: {str(e)}"

if __name__ == "__main__":
    mcp.run()