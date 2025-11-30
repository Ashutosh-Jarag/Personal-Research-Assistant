"""
Summary Chain - Summarizes web content
"""

from langchain_core.output_parsers import StrOutputParser
from app.core.llm import get_llm
from app.prompts.summarizer_prompt import get_summarizer_prompt
from typing import Dict

class SummaryChain:
    """
    Summarizes web content relevant to a topic
    """
    
    def __init__(self):
        """Initialize the summary chain"""
        self.llm = get_llm()
        self.prompt = get_summarizer_prompt()
        
        # Create chain
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    async def summarize(
        self,
        topic: str,
        content: str,
        url: str = "",
        title: str = ""
    ) -> Dict:
        """
        Summarize content
        
        Args:
            topic: Research topic
            content: Text content to summarize
            url: Source URL
            title: Source title
            
        Returns:
            Dictionary with summary
        """
        try:
            # Invoke the chain
            summary = await self.chain.ainvoke({
                "topic": topic,
                "content": content,
                "url": url,
                "title": title
            })
            
            return {
                "success": True,
                "topic": topic,
                "url": url,
                "title": title,
                "summary": summary
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "url": url,
                "title": title
            }

# Test function
async def test_summary_chain():
    """Test the summary chain"""
    try:
        summarizer = SummaryChain()
        
        result = await summarizer.summarize(
            topic="Artificial Intelligence",
            content="Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by animals including humans.",
            url="https://example.com/ai",
            title="AI Wikipedia"
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