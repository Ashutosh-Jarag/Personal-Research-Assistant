"""
LLM Configuration - Initialize Gemini
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings


def get_llm():
    """
    Initialize and return Gemini LLM instance
    
    Model: gemini-2.5-flash (good balance of speed and quality)
    Temperature: 0.7 (creative but not too random)
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.7,
        convert_system_message_to_human=True  # Gemini-specific setting
    )
    return llm


# Test function
async def test_llm_connection():
    """Test if Gemini API is working"""
    try:
        llm = get_llm()
        response = await llm.ainvoke("Say 'Hello! I am working!'")
        return {
            "status": "success",
            "response": response.content
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }