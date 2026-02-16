"""
Agent State - Defines the data structure that flows through the workflow
"""

from typing import TypedDict, List, Dict, Optional, Annotated
from operator import add


class ResearchState(TypedDict):
    """
    The State that gets passed between nodes int the graph
    """

    topic : str
    depth : str
    max_sources : str


    research_plan: Optional[str]        
    search_queries: List[str]           
    
    search_results: Annotated[List[Dict], add] 
    
    scraped_content: Annotated[List[Dict], add] 

    summaries: Annotated[List[Dict], add]        
    

    final_report: Optional[str]         
    report_metadata: Optional[Dict]     
    
    current_step: str                   
    queries_executed: int               
    pages_scraped: int               
    should_continue: bool               
    error: Optional[str] 



def create_initial_state(
    topic: str,
    depth: str = "standard",
    max_sources: int = 5) -> ResearchState:
    """
    Create initial state for a new research task
    
    Args:
        topic: Research topic
        depth: Research depth level
        max_sources: Maximum sources to analyze
        
    Returns:
        Initial ResearchState
    """
    return ResearchState(
        # Input
        topic=topic,
        depth=depth,
        max_sources=max_sources,
        
        # Planning
        research_plan=None,
        search_queries=[],
        
        # Results
        search_results=[],
        scraped_content=[],
        summaries=[],
        
        # Output
        final_report=None,
        report_metadata=None,
        
        # Control
        current_step="initialized",
        queries_executed=0,
        pages_scraped=0,
        should_continue=True,
        error=None
    )