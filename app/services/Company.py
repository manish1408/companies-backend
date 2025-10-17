from datetime import datetime
from bson import ObjectId
from app.models.Company import CompanyModel
from app.schemas.Company import CreateCompanySchema, UpdateCompanySchema

class CompanyService:
    def __init__(self):
        self.company_model = CompanyModel()
    
    async def create_company(self, data: CreateCompanySchema):
        """
        Create a new company with validation
        """
        try:
            # Convert Pydantic model to dict, excluding None values
            company_data = data.model_dump(exclude_unset=True)
            
            # Create company
            company_id = await self.company_model.create_company(company_data)
            
            # Get the created company
            created_company = await self.company_model.get_company({"_id": company_id})
            if not created_company:
                return {
                    "success": False,
                    "data": None,
                    "error": "Failed to retrieve created company"
                }

            return {
                "success": True,
                "data": {
                    "message": "Company created successfully",
                    "company": created_company.dict()
                }
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }

    async def get_company(self, company_id: str):
        """
        Get a single company by ID
        """
        try:
            if not ObjectId.is_valid(company_id):
                return {
                    "success": False,
                    "data": None,
                    "error": "Invalid company ID format"
                }

            company = await self.company_model.get_company({"_id": ObjectId(company_id)})
            if not company:
                return {
                    "success": False,
                    "data": None,
                    "error": "Company not found"
                }

            return {
                "success": True,
                "data": {
                    "company": company.dict()
                }
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }

    async def get_companies(self, skip: int = 0, limit: int = 10, filters: dict = None):
        """
        Get list of companies with pagination
        """
        try:
            if filters is None:
                filters = {}

            companies = await self.company_model.get_companies(filters, skip, limit)
            total_count = await self.company_model.get_companies_count(filters)

            companies_data = [company.dict() for company in companies]

            return {
                "success": True,
                "data": {
                    "companies": companies_data,
                    "pagination": {
                        "total": total_count,
                        "skip": skip,
                        "limit": limit,
                        "has_more": (skip + limit) < total_count
                    }
                }
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }

    async def update_company(self, company_id: str, data: UpdateCompanySchema):
        """
        Update an existing company
        """
        try:
            if not ObjectId.is_valid(company_id):
                return {
                    "success": False,
                    "data": None,
                    "error": "Invalid company ID format"
                }

            # Check if company exists
            existing_company = await self.company_model.get_company({"_id": ObjectId(company_id)})
            if not existing_company:
                return {
                    "success": False,
                    "data": None,
                    "error": "Company not found"
                }

            # Convert Pydantic model to dict, excluding None values
            update_data = data.model_dump(exclude_unset=True)
            
            if not update_data:
                return {
                    "success": False,
                    "data": None,
                    "error": "No data provided for update"
                }

            # Update company
            updated = await self.company_model.update_company(company_id, update_data)
            if not updated:
                return {
                    "success": True,
                    "data": "No changes detected in the provided data"
                }

            # Get updated company
            updated_company = await self.company_model.get_company({"_id": ObjectId(company_id)})
            if not updated_company:
                return {
                    "success": False,
                    "data": None,
                    "error": "Failed to retrieve updated company data"
                }

            return {
                "success": True,
                "data": {
                    "message": "Company updated successfully",
                    "company": updated_company.dict()
                }
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }

    async def delete_company(self, company_id: str):
        """
        Delete a company permanently
        """
        try:
            if not ObjectId.is_valid(company_id):
                return {
                    "success": False,
                    "data": None,
                    "error": "Invalid company ID format"
                }

            # Check if company exists
            existing_company = await self.company_model.get_company({"_id": ObjectId(company_id)})
            if not existing_company:
                return {
                    "success": False,
                    "data": None,
                    "error": "Company not found"
                }

            # Delete company permanently
            deleted = await self.company_model.delete_company(company_id)
            if not deleted:
                return {
                    "success": False,
                    "data": None,
                    "error": "Failed to delete company"
                }

            return {
                "success": True,
                "data": {
                    "message": "Company deleted successfully"
                }
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }
