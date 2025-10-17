from typing import List, Optional
from app.helpers.Database import MongoDB
from bson import ObjectId
import os
from app.schemas.Company import CompanySchema
from datetime import datetime
from app.schemas.PyObjectId import PyObjectId
from dotenv import load_dotenv

load_dotenv()

class CompanyModel:
    def __init__(self, db_name=os.getenv('DB_NAME'), collection_name="companies"):
        self.collection = MongoDB.get_database(db_name)[collection_name]

    async def get_company(self, filters: dict) -> Optional[CompanySchema]:
        """
        Retrieve a single company matching the given filters.
        """
        document = await self.collection.find_one(filters)
        if document:
            return CompanySchema(**document)
        return None

    async def get_companies_count(self, filters: dict) -> int:
        """
        Retrieve a count of documents matching the given filters.
        """
        total_count = await self.collection.count_documents(filters)
        if total_count:
            return total_count
        return 0

    async def get_companies(self, filters: dict = {}, skip: int = 0, limit: int = 10) -> List[CompanySchema]:
        """
        Retrieve a list of companies matching the given filters with pagination.
        """
        cursor = self.collection.find(filters).skip(skip).limit(limit)
        companies = []
        async for doc in cursor:
            companies.append(CompanySchema(**doc))
        return companies

    async def get_companies_with_projection(self, filters: dict = {}, skip: int = 0, limit: int = 10, fields: List[str] = None) -> List[dict]:
        """
        Retrieve a list of companies matching the given filters with pagination and projection.
        """
        if fields is None:
            projection = {}
        else:
            projection = {field: 1 for field in fields}

        cursor = self.collection.find(filters, projection).skip(skip).limit(limit)
        result = []
        async for doc in cursor:
            result.append(doc)
        return result

    async def create_company(self, data: dict) -> PyObjectId:
        """
        Create a new company document in the database.
        """
        data["createdAt"] = datetime.utcnow()
        company = CompanySchema(**data)
        result = await self.collection.insert_one(company.dict(by_alias=True))
        return result.inserted_id

    async def update_company(self, company_id: str, updates: dict) -> bool:
        """
        Update an existing company by its ID.
        """
        filters = {"_id": ObjectId(company_id)}
        updates["updatedAt"] = datetime.utcnow()
        result = await self.collection.update_one(filters, {"$set": updates})
        return result.modified_count > 0


    async def delete_company(self, company_id: str) -> bool:
        """
        Permanently delete a company document from the database.
        """
        result = await self.collection.delete_one({"_id": ObjectId(company_id)})
        return result.deleted_count > 0

    async def update_many(self, filters: dict, update: dict) -> bool:
        """
        Update multiple documents matching the given filters.
        """
        await self.collection.update_many(filters, update)
        return True
