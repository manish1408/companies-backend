# from app.helpers.AzureStorage import AzureBlobUploader  # Disabled: Azure blob not in use
import os


class CommonService:
    def __init__(self):
        # self.azure_uploader = AzureBlobUploader()  # Disabled: Azure blob not in use
        
    async def upload_file(self, file_path, folder_name="general-storage", file_type=".png"):
        """
        Upload a file to Azure Blob Storage
        
        Args:
            file_path: Path to the file to upload
            folder_name: Azure blob container folder name
            file_type: File extension/type
            
        Returns:
            dict: Success status and file URL or error message
        """
        try:
            return {
                "success": False,
                "data": None,
                "error": "Azure Blob upload is disabled"
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }
    
    async def delete_file(self, file_url: str) -> dict:
        """
        Delete a file from Azure Blob Storage
        
        Args:
            file_url: URL of the file to delete
            
        Returns:
            dict: Success status and message or error
        """
        try:
            return {
                "success": False,
                "data": None,
                "error": "Azure Blob delete is disabled"
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }