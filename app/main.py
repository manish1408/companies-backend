import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from starlette.responses import RedirectResponse
from app.helpers.Database import MongoDB
from app.middleware.Cors import add_cors_middleware
from app.middleware.GlobalErrorHandling import GlobalErrorHandlingMiddleware
from app.controllers import Auth, Profile, Company
from app.middleware.JWTVerification import jwt_validator
import logging

load_dotenv()

app = FastAPI(
    title="User Management System",
    description="General User Management System API",
    version='1.0.0',
    docs_url="/api-docs",
    redoc_url="/api-redoc"
)

# Middleware
app.add_middleware(GlobalErrorHandlingMiddleware)
add_cors_middleware(app)

# Routes - User Management and Companies
app.include_router(Auth.router)
app.include_router(Profile.router, dependencies=[Depends(jwt_validator)])
app.include_router(Company.router, dependencies=[Depends(jwt_validator)])

@app.on_event("startup")
async def startup_event():
    connection_string = os.getenv("MONGODB_CONNECTION_STRING")
    # Connect async MongoDB (Motor)
    MongoDB.connect(connection_string)
    print("MongoDB connected (async with Motor)")

@app.on_event("shutdown") 
async def shutdown_event():
    """Cleanup resources on shutdown"""
    from app.dependencies import cleanup_resources
    cleanup_resources()
    if MongoDB.client:
        MongoDB.client.close()
    print("App shutdown complete - resources cleaned up")

@app.get("/")
def api_docs():
    return RedirectResponse(url="/api-docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3003, reload=True)