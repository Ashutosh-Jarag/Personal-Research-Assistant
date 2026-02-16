"""
Workflow Nodes - Individual steps in the research process
Each node performs a specific task and updates the state
"""

from app.agent.state import ResearchState
from app.chains import get_planning_chain, get_summary_chain, get_report_chain
from app.tools import WebSearchTool, WebScraperTool
from typing import Dict
import asyncio


class ResearchNodes:
    """
    Contains all node functions for the research workflow
    Each node takes state, performs action, returns updated state
    """
    
    def __init__(self):
        """Initialize tools and chains"""
        self.planner = get_planning_chain()
        self.summarizer = get_summary_chain()
        self.reporter = get_report_chain()
        self.searcher = WebSearchTool()
        self.scraper = WebScraperTool()
    
    async def planning_node(self, state: ResearchState) -> Dict:
        """
        Node 1: Create research plan and generate search queries
        
        Args:
            state: Current research state
            
        Returns:
            Updated state with plan and queries
        """
        print(f"🧠 PLANNING: Analyzing topic '{state['topic']}'...")
        
        try:
            # Determine number of queries based on depth
            depth_to_queries = {
                "quick": 2,
                "standard": 5,
                "detailed": 8
            }
            num_queries = depth_to_queries.get(state['depth'], 5)
            
            # Generate search queries
            queries = await self.planner.generate_search_queries(
                topic=state['topic'],
                num_queries=num_queries
            )
            
            print(f"✅ Generated {len(queries)} search queries")
            
            return {
                "search_queries": queries,
                "current_step": "planning_complete"
            }
            
        except Exception as e:
            print(f"❌ Planning error: {str(e)}")
            return {
                "error": f"Planning failed: {str(e)}",
                "should_continue": False
            }
    
    async def search_node(self, state: ResearchState) -> Dict:
        """
        Node 2: Execute search queries
        
        Args:
            state: Current research state
            
        Returns:
            Updated state with search results
        """
        print(f"🔍 SEARCHING: Executing {len(state['search_queries'])} queries...")
        
        try:
            all_results = []
            
            # Execute each query
            for i, query in enumerate(state['search_queries'], 1):
                print(f"   Query {i}/{len(state['search_queries'])}: {query}")
                
                results = self.searcher.search(query, max_results=2)
                all_results.extend(results)
                
                # Small delay to be respectful to API
                await asyncio.sleep(0.5)
            
            # Remove duplicates based on URL
            unique_results = []
            seen_urls = set()
            for result in all_results:
                url = result.get('url', '')
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    unique_results.append(result)
            
            # Limit to max_sources
            unique_results = unique_results[:state['max_sources']]
            
            print(f"✅ Found {len(unique_results)} unique sources")
            
            return {
                "search_results": unique_results,
                "queries_executed": len(state['search_queries']),
                "current_step": "search_complete"
            }
            
        except Exception as e:
            print(f"❌ Search error: {str(e)}")
            return {
                "error": f"Search failed: {str(e)}",
                "should_continue": False
            }
    
    async def scraping_node(self, state: ResearchState) -> Dict:
        """
        Node 3: Scrape content from search results
        
        Args:
            state: Current research state
            
        Returns:
            Updated state with scraped content
        """
        print(f"🕷️  SCRAPING: Extracting content from {len(state['search_results'])} pages...")
        
        try:
            scraped_pages = []
            
            for i, result in enumerate(state['search_results'], 1):
                url = result.get('url', '')
                if not url:
                    continue
                
                print(f"   Scraping {i}/{len(state['search_results'])}: {url[:50]}...")
                
                # Scrape page
                content = self.scraper.scrape(url)
                
                if content.get('success'):
                    scraped_pages.append(content)
                    print(f"   ✓ Success ({content.get('word_count', 0)} words)")
                else:
                    print(f"   ✗ Failed: {content.get('error', 'Unknown error')}")
                
                # Small delay
                await asyncio.sleep(0.5)
            
            print(f"✅ Successfully scraped {len(scraped_pages)}/{len(state['search_results'])} pages")
            
            return {
                "scraped_content": scraped_pages,
                "pages_scraped": len(scraped_pages),
                "current_step": "scraping_complete"
            }
            
        except Exception as e:
            print(f"❌ Scraping error: {str(e)}")
            return {
                "error": f"Scraping failed: {str(e)}",
                "should_continue": False
            }
    
    async def summarization_node(self, state: ResearchState) -> Dict:
        """
        Node 4: Summarize scraped content
        
        Args:
            state: Current research state
            
        Returns:
            Updated state with summaries
        """
        print(f"📝 SUMMARIZING: Processing {len(state['scraped_content'])} pages...")
        
        try:
            # Summarize all content
            summaries = await self.summarizer.summarize_multiple(
                topic=state['topic'],
                sources=state['scraped_content']
            )
            
            successful_summaries = [s for s in summaries if s.get('success')]
            
            print(f"✅ Created {len(successful_summaries)} summaries")
            
            return {
                "summaries": summaries,
                "current_step": "summarization_complete"
            }
            
        except Exception as e:
            print(f"❌ Summarization error: {str(e)}")
            return {
                "error": f"Summarization failed: {str(e)}",
                "should_continue": False
            }
    
    async def report_generation_node(self, state: ResearchState) -> Dict:
        """
        Node 5: Generate final research report
        
        Args:
            state: Current research state
            
        Returns:
            Updated state with final report
        """
        print(f"📄 GENERATING REPORT: Synthesizing findings...")
        
        try:
            # Generate report
            report_result = await self.reporter.generate_report(
                topic=state['topic'],
                summaries=state['summaries']
            )
            
            if report_result.get('success'):
                print(f"✅ Report generated ({report_result.get('word_count', 0)} words)")
                
                return {
                    "final_report": report_result.get('report'),
                    "report_metadata": {
                        "word_count": report_result.get('word_count'),
                        "num_sources": report_result.get('num_sources'),
                        "generated_at": report_result.get('generated_at'),
                        "sources": report_result.get('sources', [])
                    },
                    "current_step": "completed",
                    "should_continue": False
                }
            else:
                raise Exception(report_result.get('error', 'Unknown error'))
                
        except Exception as e:
            print(f"❌ Report generation error: {str(e)}")
            return {
                "error": f"Report generation failed: {str(e)}",
                "should_continue": False,
                "current_step": "failed"
            }


# Helper function to check if we should continue
def should_continue_research(state: ResearchState) -> str:
    """
    Decide if we should continue or end
    This is used for conditional edges in the graph
    
    Args:
        state: Current research state
        
    Returns:
        "continue" or "end"
    """
    # Check for errors
    if state.get('error'):
        return "end"
    
    # Check if we should continue
    if state.get('should_continue', True):
        return "continue"
    
    return "end"