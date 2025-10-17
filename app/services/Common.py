from app.helpers.AzureStorage import AzureBlobUploader
import os


class CommonService:
    def __init__(self):
        self.azure_uploader = AzureBlobUploader()
        
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
            file_url = self.azure_uploader.upload_file_to_azure_blob(file_path, folder_name, file_type)       
            return {
                "success": True,
                "data": file_url
            }
        except Exception as e:
            return {
                "success": False,
                "data": str(e),
                "error": 'Unable to upload file'
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
            # Call helper to delete the file from Azure Blob
            self.azure_uploader.delete_file(file_url)

            return {
                "success": True,
                "data": f"File deleted successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Unable to delete file: {str(e)}"
            }