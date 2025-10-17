from app.schemas.User import UserSchema
from app.models.User import UserModel
from app.helpers.Utilities import Utils
from pydantic import ValidationError
from datetime import datetime, timedelta
from fastapi import HTTPException, UploadFile
from app.helpers.AzureStorage import AzureBlobUploader
import os 
from bson import ObjectId
class AuthService:
    
    def __init__(self):
        self.user_model = UserModel()
        self.uploader = AzureBlobUploader()
            
    async def get_user(self, email, password):
        """
        Authenticate user and return JWT token
        """
        try:
            # Get user by email
            user = await self.user_model.get_user({"email": email})
            if not user:
                return {
                    "success": False,
                    "data": None,
                    "error": "User does not exist"
                }

            # Verify password
            password_match = Utils.verify_password(password, user.password)
            if not password_match:
                return {
                    "success": False,
                    "data": None,
                    "error": "Invalid email or password"
                }

            # Create user response data
            user_dict = user.dict()
            user_dict.pop("password", None)  # Remove password from response
            
            # Create JWT token
            token = Utils.create_jwt_token(user_dict)
            
            return {
                "success": True,
                "data": {
                    "token": token
                }
            }
        except ValidationError as e:
            error_details = e.errors()
            return {
                "success": False,
                "data": None,
                "error": f"Validation error: {error_details}"
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }
    
    async def signup(self, user_data) -> dict:
        """
        Handle the signup process with enhanced validation and response.
        - Checks if user exists
        - Validates and sanitizes input data
        - Hashes password
        - Creates user record
        - Returns user data with JWT token
        """
        try:
            # Check if user exists
            existing_user = await self.user_model.get_user({"email": user_data.email})
            if existing_user:
                return {
                    "success": False,
                    "data": None,
                    "error": "User Already Exists."
                }

            # Prepare user data
            user_data_dict = user_data.dict()
            
            # Hash password
            hashed_password = Utils.hash_password(user_data.password)
            user_data_dict["password"] = hashed_password
            
            # Set timestamps
            current_time = datetime.utcnow()
            user_data_dict["createdOn"] = current_time
            user_data_dict["updatedOn"] = current_time
            
            # Create user
            user_id = await self.user_model.create_user(user_data_dict)
            
            # Prepare response data
            user_data_dict["_id"] = str(user_id)
            user_data_dict.pop("password", None)  # Remove password from response
            
            # Generate JWT token
            # token = Utils.create_jwt_token(user_data_dict)
            
            return {
                "success": True,
                "data": {
                    "user_id": user_data_dict["_id"]
                }
            }
        
        except ValidationError as e:
            return {
                "success": False,
                "data": None,
                "error": f"Validation error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }

    
    def upload_profile_picture(self, file: UploadFile):
        try:
            file_content = file.file.read()  
            file_name = file.filename
            return self.uploader.upload_profile_picture(file_content, file_name)
        except Exception as e:
            raise Exception(f"Error uploading profile picture: {str(e)}")
        
    async def get_all_users(self, page: int = 1, limit: int = 10):
        try:
            import asyncio
            filters = {}
            number_to_skip = (page - 1) * limit
            
            # Run queries in parallel for better performance
            total, users = await asyncio.gather(
                self.user_model.get_documents_count(filters),
                self.user_model.get_users(filters, number_to_skip, limit)
            )
            total_pages = (total + limit - 1) // limit
            
            # Remove password from user dicts
            users_data = []
            for user in users:
                user_dict = user.dict()
                user_dict.pop('password', None)
                users_data.append(user_dict)
            return {
                "success": True,
                "data": {
                    "users": users_data,
                    "pagination": {
                        "totalPages": total_pages,
                        "currentPage": page,
                        "limit": limit
                }
            }
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }
        
    async def delete_user(self, user_id: str):
        try:
            deleted = await self.user_model.delete_user(user_id)
            if deleted:
                return {"success": True, "data": "User deleted successfully."}
            else:
                return {"success": False, "data": None, "error": "User not found or already deleted."}
        except Exception as e:
            return {"success": False, "data": None, "error": str(e)}
        
    async def update_user(self, user_id: str, update_data: dict) -> dict:
        """
        Update user information by user_id.
        """
        try:
            if not update_data:
                return {"success": False, "data": None, "error": "No data provided for update."}
            updated = await self.user_model.update_user(user_id, update_data)
            if not updated:
                return {"success": True, "data": "No new changes in data."}
            return {"success": True, "data": "User info updated successfully."}
        except Exception as e:
            return {"success": False, "data": None, "error": str(e)}

    async def get_user_by_id(self, user_id: str, admin_id: str) -> dict:
        """
        Get a specific user by user_id.
        Verifies the user was created by the requesting admin.
        """
        try:
            # Get user by ID
            user = await self.user_model.get_user({"_id": ObjectId(user_id)})
            if not user:
                return {
                    "success": False,
                    "data": None,
                    "error": "User not found"
                }
            
            # Verify the user was created by this admin
            if user.adminId != admin_id:
                return {
                    "success": False,
                    "data": None,
                    "error": "You don't have permission to view this user"
                }
            
            # Remove password from response
            user_dict = user.dict()
            user_dict.pop('password', None)
            
            return {
                "success": True,
                "data": {"user": user_dict}
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }

    async def update_user_profile(self, user_id: str, update_data: dict) -> dict:
        """
        Update a user profile.
        Can be called by both admin and user.
        User can update their own profile, admin can update any user.
        """
        try:
            if not update_data:
                return {"success": False, "data": None, "error": "No data provided for update."}
            
            # Get user by ID
            user = await self.user_model.get_user({"_id": ObjectId(user_id)})
            if not user:
                return {
                    "success": False,
                    "data": None,
                    "error": "User not found"
                }
            
            # Don't allow updating certain protected fields
            protected_fields = ["password", "userType", "adminId", "createdOn", "_id"]
            for field in protected_fields:
                update_data.pop(field, None)
            
            if not update_data:
                return {"success": False, "data": None, "error": "No valid fields to update"}
            
            # Add updatedOn timestamp
            update_data["updatedOn"] = datetime.utcnow()
            
            # Update user
            updated = await self.user_model.update_user(user_id, update_data)
            if not updated:
                return {"success": True, "data": "No new changes in data."}
            
            # Get updated user
            updated_user = await self.user_model.get_user({"_id": ObjectId(user_id)})
            user_dict = updated_user.dict()
            user_dict.pop('password', None)
            
            return {
                "success": True,
                "data": {
                    "user": user_dict,
                    "message": "User updated successfully"
                }
            }
        except Exception as e:
            return {"success": False, "data": None, "error": str(e)}

    async def get_users_by_admin(self, admin_id: str, page: int = 1, limit: int = 10) -> dict:
        """
        Get all users created by a specific admin with pagination.
        """
        try:
            import asyncio
            filters = {"adminId": admin_id}
            number_to_skip = (page - 1) * limit
            
            # Run queries in parallel for better performance
            total, users = await asyncio.gather(
                self.user_model.get_documents_count(filters),
                self.user_model.get_users(filters, number_to_skip, limit)
            )
            total_pages = (total + limit - 1) // limit
            
            # Remove password from user dicts
            users_data = []
            for user in users:
                user_dict = user.dict()
                user_dict.pop('password', None)
                users_data.append(user_dict)
                
            return {
                "success": True,
                "data": {
                    "users": users_data,
                    "pagination": {
                        "total": total,
                        "totalPages": total_pages,
                        "currentPage": page,
                        "limit": limit
                    }
                }
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }

    async def create_user_by_admin(self, user_data, admin_id: str) -> dict:
        """
        Create a new user by admin with admin ID tracking.
        - Checks if user exists
        - Validates and sanitizes input data
        - Hashes password
        - Sets userType to USER
        - Saves admin ID who created the user
        - Creates user record
        """
        try:
            # Check if user exists
            existing_user = await self.user_model.get_user({"email": user_data.email})
            if existing_user:
                return {
                    "success": False,
                    "data": None,
                    "error": "User with this email already exists."
                }

            # Prepare user data
            user_data_dict = user_data.dict()
            
            # Hash password
            hashed_password = Utils.hash_password(user_data.password)
            user_data_dict["password"] = hashed_password
            
            # Set user type to USER (cannot create admin via this endpoint)
            user_data_dict["userType"] = "user"
            
            # Set the admin ID who created this user
            user_data_dict["adminId"] = admin_id
            
            # Set timestamps
            current_time = datetime.utcnow()
            user_data_dict["createdOn"] = current_time
            user_data_dict["updatedOn"] = current_time
            
            # Create user
            user_id = await self.user_model.create_user(user_data_dict)
            
            # Prepare response data
            response_data = {
                "_id": str(user_id),
                "email": user_data_dict["email"],
                "fullName": user_data_dict["fullName"],
                "phone": user_data_dict.get("phone"),
                "userType": user_data_dict["userType"],
                "adminId": admin_id,
                "createdOn": current_time
            }
            
            return {
                "success": True,
                "data": {
                    "user": response_data,
                    "message": "User created successfully"
                }
            }
        
        except ValidationError as e:
            return {
                "success": False,
                "data": None,
                "error": f"Validation error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }
        