"""
Report Chain - Generates final research report
"""

from langchain_core.output_parsers import StrOutputParser
from app.core.llm import get_llm
from app.prompts.report_prompt import get_report_prompt
from typing import Dict, List
from datetime import datetime


class ReportChain:
    """
    Synthesizes summaries into a comprehensive report
    """
    
    def __init__(self):
        """Initialize the report chain"""
        self.llm = get_llm()
        self.prompt = get_report_prompt()
        
        # Create chain
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    async def generate_report(
        self,
        topic: str,
        summaries: List[Dict]
    ) -> Dict:
        """
        Generate final research report from summaries
        
        Args:
            topic: Research topic
            summaries: List of summary dictionaries
            
        Returns:
            Dictionary with report and metadata
        """
        try:
            # Format summaries for the prompt
            formatted_summaries = self._format_summaries(summaries)
            
            # Generate report
            report = await self.chain.ainvoke({
                "topic": topic,
                "num_sources": len(summaries),
                "summaries": formatted_summaries
            })
            
            # Add metadata
            word_count = len(report.split())
            
            return {
                "success": True,
                "topic": topic,
                "report": report,
                "num_sources": len(summaries),
                "word_count": word_count,
                "generated_at": datetime.now().isoformat(),
                "sources": self._extract_source_list(summaries)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _format_summaries(self, summaries: List[Dict]) -> str:
        """
        Format summaries into a single string for the prompt
        
        Args:
            summaries: List of summary dictionaries
            
        Returns:
            Formatted string
        """
        formatted = []
        
        for i, summary in enumerate(summaries, 1):
            if not summary.get('success', False):
                continue
            
            formatted.append(f"""
Source {i}:
Title: {summary.get('title', 'Untitled')}
URL: {summary.get('url', 'N/A')}
Summary:
{summary.get('summary', 'No summary available')}

---
""")
        
        return "\n".join(formatted)
    
    def _extract_source_list(self, summaries: List[Dict]) -> List[Dict]:
        """
        Extract clean list of sources for metadata
        
        Args:
            summaries: List of summary dictionaries
            
        Returns:
            List of source info
        """
        sources = []
        
        for summary in summaries:
            if summary.get('success', False):
                sources.append({
                    "title": summary.get('title', 'Untitled'),
                    "url": summary.get('url', '')
                })
        
        return sources


# Test function
async def test_report_chain():
    """Test the report chain"""
    try:
        reporter = ReportChain()
        
        # Sample summaries
        sample_summaries = [
            {
                "success": True,
                "title": "AI in Medical Diagnosis",
                "url": "https://example.com/1",
                "summary": "AI systems are achieving 95% accuracy in cancer detection..."
            },
            {
                "success": True,
                "title": "Drug Discovery with AI",
                "url": "https://example.com/2",
                "summary": "Machine learning accelerates drug discovery by 50x..."
            }
        ]
        
        result = await reporter.generate_report(
            topic="AI Applications in Healthcare",
            summaries=sample_summaries
        )
        
        return {
            "status": "success",
            "result": {
                "success": result.get("success"),
                "word_count": result.get("word_count"),
                "num_sources": result.get("num_sources"),
                "report_preview": result.get("report", "")[:500] + "..."
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }