"""
Planning Chain - Creates research strategy
"""

from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from app.core.llm import get_llm
from app.prompts.planner_prompt import get_planner_prompt, get_quick_planner_prompt
from typing import Dict, List
import re


class PlanningChain:
    """
    Creates a research plan for a given topic
    """
    
    def __init__(self):
        """Initialize the planning chain"""
        self.llm = get_llm()
        self.prompt = get_planner_prompt()
        self.quick_prompt = get_quick_planner_prompt()
        
        # Create chain: prompt -> LLM -> output parser
        self.chain = self.prompt | self.llm | StrOutputParser()
        self.quick_chain = self.quick_prompt | self.llm | StrOutputParser()
    
    async def create_plan(
        self,
        topic: str,
        depth: str = "standard",
        max_sources: int = 5
    ) -> Dict:
        """
        Create a comprehensive research plan
        
        Args:
            topic: Research topic
            depth: Research depth (quick/standard/detailed)
            max_sources: Maximum number of sources
            
        Returns:
            Dictionary with plan and search queries
        """
        try:
            # Invoke the chain
            plan = await self.chain.ainvoke({
                "topic": topic,
                "depth": depth,
                "max_sources": max_sources
            })
            
            # Extract search queries from the plan
            search_queries = self._extract_search_queries(plan, max_sources)
            
            return {
                "success": True,
                "topic": topic,
                "plan": plan,
                "search_queries": search_queries,
                "num_queries": len(search_queries)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def generate_search_queries(self, topic: str, num_queries: int = 5) -> List[str]:
        """
        Quick method to just generate search queries
        
        Args:
            topic: Research topic
            num_queries: Number of queries to generate
            
        Returns:
            List of search query strings
        """
        try:
            # Use quick chain
            response = await self.quick_chain.ainvoke({"topic": topic})
            
            # Parse queries
            queries = [q.strip() for q in response.split('\n') if q.strip()]
            
            # Ensure we have the right number
            if len(queries) < num_queries:
                # Add variations if needed
                queries.append(f"{topic} recent developments")
                queries.append(f"{topic} latest research")
            
            return queries[:num_queries]
            
        except Exception as e:
            # Fallback queries
            return [
                f"{topic}",
                f"{topic} latest developments",
                f"{topic} recent advances",
                f"{topic} research 2024",
                f"{topic} overview"
            ][:num_queries]
    
    def _extract_search_queries(self, plan: str, max_queries: int) -> List[str]:
        """
        Extract search queries from the plan text
        
        Args:
            plan: The full research plan text
            max_queries: Maximum number of queries to extract
            
        Returns:
            List of search queries
        """
        queries = []
        
        # Look for lines that look like search queries
        # Usually they're numbered or bulleted
        lines = plan.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and headers
            if not line or line.startswith('#'):
                continue
            
            # Remove common prefixes (numbers, bullets)
            cleaned = re.sub(r'^[\d\.\-\*\)]+\s*', '', line)
            cleaned = cleaned.strip('"\'')
            
            # If it looks like a query (not too long, no colons suggesting headers)
            if cleaned and len(cleaned) < 100 and ':' not in cleaned:
                queries.append(cleaned)
            
            if len(queries) >= max_queries:
                break
        
        return queries


# Test function
async def test_planning_chain():
    """Test the planning chain"""
    try:
        planner = PlanningChain()
        
        # Test full plan
        result = await planner.create_plan(
            topic="Quantum Computing Applications in Healthcare",
            depth="standard",
            max_sources=5
        )
        
        return {
            "status": "success",
            "result": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }