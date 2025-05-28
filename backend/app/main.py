from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any
from app.api.v1 import search
from app.core.config import settings

app = FastAPI(
    title="Catan API",
    description="Corporate Intelligent Search & Analysis Engine API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    search.router,
    prefix="/api/v1/search",
    tags=["search"]
)

@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint returning API status."""
    return {
        "status": "operational",
        "service": "Catan API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}

# Import and include routers
# from app.api.v1 import search, documents, auth
# app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
# app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 