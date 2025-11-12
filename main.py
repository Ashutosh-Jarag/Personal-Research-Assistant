"""
This is the main file for the app. 
It contains the FastAPI application and all its routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.llm import test_llm_connection

# import warnings
# warnings.filterwarnings("ignore", category=UserWarning, module="langchain_google_genai")



# Create FastAPI instance

app = FastAPI(
    title=settings.APP_NAME,
    description="Autonomous research agent powered by LangGraph & Gemini",
    version=settings.APP_VERSION,
    docs_url="/docs", 
    redoc_url="/redoc" 
)


# CORS Middleware - allows frontend to connect from different domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message,
    and health check status.
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}!",
        "health_check": "OK",
        "version": f"{settings.APP_VERSION}",
        "status": "Runnig",
        "Docs": "/docs"
    }



# Healt check endpoint
@app.get("health")
async def health():
    """
    Health check endpoint that returns a success message.
    """
    return {"status": "success"}


# Check if LLM connection works
@app.get("/test-llm")
async def test_llm():
    """
    Test LLM Connection Endpoint.
    """
    result = await test_llm_connection()
    return result





# This runs when you execute: python main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes
    )