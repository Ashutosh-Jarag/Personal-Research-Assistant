"""
Summarizer Prompt - Guides AI to summarize web content
"""

from langchain.prompts import PromptTemplate, ChatPromptTemplate


SUMMARIZER_SYSTEM_PROMPT = """You are an expert at extracting and summarizing key information from web content.

Your goals:
- Identify the most important information relevant to the research topic
- Extract key facts, statistics, and insights
- Maintain accuracy - don't make up information
- Be concise but comprehensive
- Highlight novel or surprising findings"""


SUMMARIZER_TEMPLATE = """
Research Topic: {topic}

Source URL: {url}
Source Title: {title}

Content:
{content}

---

Summarize the above content focusing on information relevant to "{topic}".

Include:
1. Main points (bullet points)
2. Key facts and statistics
3. Important insights or conclusions
4. How this relates to the research topic

Keep the summary concise (200-300 words) but informative.
"""


def get_summarizer_prompt() -> ChatPromptTemplate:
    """
    Create the summarizer prompt template
    
    Returns:
        ChatPromptTemplate for summarizing content
    """
    return ChatPromptTemplate.from_messages([
        ("system", SUMMARIZER_SYSTEM_PROMPT),
        ("human", SUMMARIZER_TEMPLATE)
    ])


# Quick summarizer for shorter content
QUICK_SUMMARIZER_TEMPLATE = """
Topic: {topic}

Summarize this content in 2-3 sentences focusing on key points relevant to {topic}:

{content}
"""

def get_quick_summarizer_prompt() -> PromptTemplate:
    """Quick summarizer for brief summaries"""
    return PromptTemplate(
        input_variables=["topic", "content"],
        template=QUICK_SUMMARIZER_TEMPLATE
    )