"""
Chains Manager - Central access to all chains
"""

from app.chains.planning_chain import PlanningChain
from app.chains.summary_chain import SummaryChain
from app.chains.report_chain import ReportChain


def get_planning_chain() -> PlanningChain:
    """Get planning chain instance"""
    return PlanningChain()


def get_summary_chain() -> SummaryChain:
    """Get summary chain instance"""
    return SummaryChain()


def get_report_chain() -> ReportChain:
    """Get report chain instance"""
    return ReportChain()


# Export for easy imports
__all__ = [
    'PlanningChain',
    'SummaryChain',
    'ReportChain',
    'get_planning_chain',
    'get_summary_chain',
    'get_report_chain'
]