from fastapi import APIRouter, Form, HTTPException, UploadFile, File, Depends, Header, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from app.middleware.JWTVerification import jwt_validator
from app.schemas.ServerResponse import ServerResponse
from app.helpers.Utilities import Utils
from app.schemas.User import UpdateUserSchema

from app.dependencies import get_profile_service

router = APIRouter(prefix="/api/v1/profile", tags=["Profile"])
    
# @router.put("/update-user-info", response_model=ServerResponse)
# async def update_user_info(
#     body: UpdateUserSchema,
#     service: ProfileService = Depends(get_profile_service),
#     jwt_payload: dict = Depends(jwt_validator)
# ):
#     try:
#         user_id = jwt_payload.get("id")
#         if not user_id:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail={"data": None, "error": "Invalid authentication token", "success": False}
#             )
            
#         data = await service.update_user_info(user_id, body.model_dump(exclude_unset=True))
#         if not data["success"]:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail={"data": None, "error": data.get("error"), "success": False}
#             )
            
#         return Utils.create_response(data["data"], data["success"], data.get("error", ""))
#     except HTTPException as he:
#         raise he
#     except ValidationError as ve:
#         raise HTTPException(
#             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             detail={"data": None, "error": str(ve), "success": False}
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail={"data": None, "error": "Internal server error", "success": False}
#         )
    
@router.get("/me", response_model=ServerResponse)
async def get_me(
    authorization: str = Header(..., description="Bearer <token>"),
    profile_service = Depends(get_profile_service)
):
    try:
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"data": None, "error": "Invalid Authorization header format", "success": False}
            )
        
        token = authorization.split(" ")[1]
        result = await profile_service.get_current_user(token)
        
        if not result["success"]:
            status_code = status.HTTP_401_UNAUTHORIZED if "Invalid credentials" in result.get("error", "") else status.HTTP_400_BAD_REQUEST
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
    