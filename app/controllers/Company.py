from fastapi import APIRouter, HTTPException, Depends, Query, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from app.middleware.JWTVerification import jwt_validator
from app.schemas.ServerResponse import ServerResponse
from app.helpers.Utilities import Utils
from app.schemas.Company import CreateCompanySchema, UpdateCompanySchema
from app.services.Company import CompanyService

router = APIRouter(prefix="/api/v1/companies", tags=["Companies"])

def get_company_service() -> CompanyService:
    return CompanyService()

@router.post("/", response_model=ServerResponse)
async def create_company(
    body: CreateCompanySchema,
    service: CompanyService = Depends(get_company_service),
    jwt_payload: dict = Depends(jwt_validator)
):
    """
    Create a new company
    """
    try:
        result = await service.create_company(body)
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"data": None, "error": result.get("error"), "success": False}
            )
        
        return Utils.create_response(result["data"], result["success"], result.get("error", ""))
    except HTTPException as he:
        raise he
    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"data": None, "error": str(ve), "success": False}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"data": None, "error": "Internal server error", "success": False}
        )

@router.get("/{company_id}", response_model=ServerResponse)
async def get_company(
    company_id: str,
    service: CompanyService = Depends(get_company_service),
    jwt_payload: dict = Depends(jwt_validator)
):
    """
    Get a single company by ID
    """
    try:
        result = await service.get_company(company_id)
        if not result["success"]:
            status_code = status.HTTP_404_NOT_FOUND if "not found" in result.get("error", "").lower() else status.HTTP_400_BAD_REQUEST
            raise HTTPException(
                status_code=status_code,
                detail={"data": None, "error": result.get("error"), "success": False}
            )
        
        return Utils.create_response(result["data"], result["success"], result.get("error", ""))
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"data": None, "error": "Internal server error", "success": False}
        )

@router.get("/", response_model=ServerResponse)
async def get_companies(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    company_name: str = Query(None, description="Filter by company name"),
    country: str = Query(None, description="Filter by country"),
    jurisdiction: str = Query(None, description="Filter by jurisdiction"),
    service: CompanyService = Depends(get_company_service),
    jwt_payload: dict = Depends(jwt_validator)
):
    """
    Get list of companies with pagination and optional filters
    """
    try:
        # Build filters
        filters = {}
        if company_name:
            filters["companyName"] = {"$regex": company_name, "$options": "i"}
        if country:
            filters["country"] = {"$regex": country, "$options": "i"}
        if jurisdiction:
            filters["jurisdiction"] = {"$regex": jurisdiction, "$options": "i"}

        result = await service.get_companies(skip, limit, filters)
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"data": None, "error": result.get("error"), "success": False}
            )
        
        return Utils.create_response(result["data"], result["success"], result.get("error", ""))
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"data": None, "error": "Internal server error", "success": False}
        )

@router.put("/{company_id}", response_model=ServerResponse)
async def update_company(
    company_id: str,
    body: UpdateCompanySchema,
    service: CompanyService = Depends(get_company_service),
    jwt_payload: dict = Depends(jwt_validator)
):
    """
    Update an existing company
    """
    try:
        result = await service.update_company(company_id, body)
        if not result["success"]:
            status_code = status.HTTP_404_NOT_FOUND if "not found" in result.get("error", "").lower() else status.HTTP_400_BAD_REQUEST
            raise HTTPException(
                status_code=status_code,
                detail={"data": None, "error": result.get("error"), "success": False}
            )
        
        return Utils.create_response(result["data"], result["success"], result.get("error", ""))
    except HTTPException as he:
        raise he
    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"data": None, "error": str(ve), "success": False}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"data": None, "error": "Internal server error", "success": False}
        )

@router.delete("/{company_id}", response_model=ServerResponse)
async def delete_company(
    company_id: str,
    service: CompanyService = Depends(get_company_service),
    jwt_payload: dict = Depends(jwt_validator)
):
    """
    Delete a company permanently
    """
    try:
        result = await service.delete_company(company_id)
        if not result["success"]:
            status_code = status.HTTP_404_NOT_FOUND if "not found" in result.get("error", "").lower() else status.HTTP_400_BAD_REQUEST
            raise HTTPException(
                status_code=status_code,
                detail={"data": None, "error": result.get("error"), "success": False}
            )
        
        return Utils.create_response(result["data"], result["success"], result.get("error", ""))
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"data": None, "error": "Internal server error", "success": False}
        )
