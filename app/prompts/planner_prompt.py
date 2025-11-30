"""
Planner Prompt - Guides AI to create research strategy
"""

from langchain.prompts import PromptTemplate, ChatPromptTemplate


PLANNER_SYSTEM_PROMPT = """You are an expert research planner. Your job is to create a comprehensive research strategy for a given topic.

You will:
1. Analyze the research topic
2. Break it down into key aspects that need investigation
3. Generate specific search queries to find the best information
4. Prioritize which aspects are most important

Be strategic and thorough. Think like a professional researcher."""


PLANNER_TEMPLATE = """
Topic: {topic}
Research Depth: {depth}
Maximum Sources: {max_sources}

Create a research plan with the following structure:

1. TOPIC ANALYSIS
   - What are the key aspects of this topic?
   - What makes this topic important or interesting?
   - What are the main questions to answer?

2. SEARCH STRATEGY
   - Generate {max_sources} specific search queries
   - Each query should target a different aspect of the topic
   - Prioritize recent, authoritative sources

3. EXPECTED OUTCOMES
   - What type of information should we find?
   - What would make this research comprehensive?

Format your response as a structured research plan.
"""


def get_planner_prompt() -> ChatPromptTemplate:
    """
    Create the planner prompt template
    
    Returns:
        ChatPromptTemplate with system and user messages
    """
    return ChatPromptTemplate.from_messages([
        ("system", PLANNER_SYSTEM_PROMPT),
        ("human", PLANNER_TEMPLATE)
    ])


# Alternative: Simple prompt for quick planning
QUICK_PLANNER_TEMPLATE = """
Create 3-5 specific search queries to research this topic: {topic}

Make them diverse to cover different aspects.
Return ONLY the search queries, one per line.
"""

def get_quick_planner_prompt() -> PromptTemplate:
    """Quick planner that just returns search queries"""
    return PromptTemplate(
        input_variables=["topic"],
        template=QUICK_PLANNER_TEMPLATE
    )