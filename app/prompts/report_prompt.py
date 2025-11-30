"""
Report Generator Prompt - Creates final research report
"""

from langchain.prompts import ChatPromptTemplate


REPORT_SYSTEM_PROMPT = """You are an expert research analyst and technical writer.

Your task is to synthesize multiple source summaries into a comprehensive, well-structured research report.

Guidelines:
- Create a clear, logical structure with sections
- Synthesize information across sources (don't just list them)
- Highlight key findings and insights
- Include relevant statistics and facts
- Maintain academic rigor while being readable
- Use markdown formatting for better readability
- Cite sources appropriately"""


REPORT_TEMPLATE = """
Research Topic: {topic}
Number of Sources Analyzed: {num_sources}

Source Summaries:
{summaries}

---

Create a comprehensive research report on "{topic}" based on the above summaries.

Structure your report as follows:

# {topic}

## Executive Summary
[2-3 paragraphs summarizing key findings]

## Key Findings
[Main discoveries and insights from your research]

## Detailed Analysis
[Deeper dive into important aspects, organized by themes]

## Statistics and Data
[Important numbers, trends, comparisons]

## Conclusions
[Synthesize everything into main takeaways]

## Sources
[List all sources with titles and URLs]

---

Make the report informative, well-organized, and professionally written.
Use markdown formatting (headers, lists, bold, etc.) for readability.
"""


def get_report_prompt() -> ChatPromptTemplate:
    """
    Create the report generation prompt template
    
    Returns:
        ChatPromptTemplate for generating final report
    """
    return ChatPromptTemplate.from_messages([
        ("system", REPORT_SYSTEM_PROMPT),
        ("human", REPORT_TEMPLATE)
    ])