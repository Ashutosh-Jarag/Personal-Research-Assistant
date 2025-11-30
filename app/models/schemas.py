"""
Pydantic models for schemas - Data validation and serialization.
This define defins struture of our API Requests and Responses.
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import datetime
from enum import Enum



class ResearchDepth(str, Enum):
    """How deep should the research be?"""
    QUICK = "quick"          # 2-3 sources, brief summary
    STANDARD = "standard"    # 5 sources, balanced
    DETAILED = "detailed"    # 10+ sources, comprehensive

class ResearchRequest(BaseModel):
    """
    Request model for starting new research task.
    """
    topic : str = Field(
        ...,
        description="Topic to search on or research.",
        min_length=3,
        max_length=500,
        example = "Latest development on agentic ai"
    )
    depth : ResearchDepth = Field(
        default=ResearchDepth.STANDARD,
        description="How deep should the reaserch level be"
    )
    max_sources: int = Field(
        default=5,
        ge=1,  # greater than or equal to 1
        le=20,  # less than or equal to 20
        description="Maximum number of sources to analyze"
    )


    class config:
        json_schema_extra={
            "example": {
                "topic": "AI in Healthcare",
                "depth": "quick",
                "max_sources": 5
            }
        }

class ResearchResponse(BaseModel):
    """
    Response model for a successful research request.
    """
    research_id : str
    status : str
    message : str
    created_at : datetime = Field(default_factory=datetime.now)


class Source(BaseModel):
    """
    Individual source information.
    """
    url : HttpUrl
    title : str
    summary : str
    relevance_score: Optional[float] = None

class ResearchStatus(BaseModel):
    """
    Current status of a research task.
    """
    research_id : str 
    status : str
    progress : int = Field(ge=0, le=100)
    current_step: Optional[str] = None
    topic : str
    created_at : datetime
    completd_at : Optional[datetime] = None
    error : Optional[str] = None 

class ResearchReport(BaseModel):
    """
    Complete report of a research task.
    """
    research_id : str
    topic : str
    report_markdown : str
    sources : List[Source]
    created_at : datetime
    word_count : int 
    research_depth : ResearchDepth


