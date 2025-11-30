from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.llm import test_llm_connection
from app.tools.search_tool import test_search_tool
from app.tools.scraper_tool import test_scraper_tool
from app.tools import WebSearchTool, WebScraperTool
from app.chains.planning_chain import test_planning_chain
from app.chains.summary_chain import test_summary_chain
from app.chains.report_chain import test_report_chain

app = FastAPI(
    title=settings.APP_NAME,
    description="Autonomous research agent powered by LangGraph & Gemini",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root
@app.get("/", tags=["System"])
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}!",
        "health_check": "OK",
        "version": f"{settings.APP_VERSION}",
        "status": "Running",
        "Docs": "/docs"
    }

# Health
@app.get("/health", tags=["System"])
async def health():
    return {"status": "success"}

# LLM
@app.get("/test-llm", tags=["LLM"])
async def test_llm():
    return await test_llm_connection()

# Tavily search
@app.get("/test-search", tags=["Tools → Web Search"])
async def test_search():
    return await test_search_tool()

# Web scraper
@app.get("/test-scraper", tags=["Tools → Web Scraper"])
async def test_scraper():
    return await test_scraper_tool()

# Planning chain
@app.get("/test-planner", tags=["Chains"])
async def test_planner():
    return await test_planning_chain()

# Summarization chain
@app.get("/test-summarizer", tags=["Chains"])
async def test_summarizer():
    return await test_summary_chain()

# Report chain
@app.get("/test-reporter", tags=["Chains"])
async def test_reporter():
    return await test_report_chain()

# Full research flow
@app.get("/test-research-flow", tags=["Workflow"])
async def test_research_flow():
    try:
        topic = "latest AI developments 2024"
        searcher = WebSearchTool()
        search_results = searcher.search(topic, max_results=3)

        if not search_results:
            return {"error": "No search results found"}

        top_result = search_results[0]
        scraper = WebScraperTool()
        scraped_content = scraper.scrape(top_result['url'])

        return {
            "status": "success",
            "topic": topic,
            "search_results_count": len(search_results),
            "top_result": {
                "title": top_result['title'],
                "url": top_result['url'],
                "search_summary": top_result['content']
            },
            "scraped_content": {
                "success": scraped_content.get('success'),
                "title": scraped_content.get('title'),
                "word_count": scraped_content.get('word_count'),
                "content_preview": scraped_content.get('content', '')[:300] + "..."
            }
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
