import pytest
from unittest.mock import patch, MagicMock
from backend.schemas.models import VerifiedNeed, DispatchPlan, Allocation, NeedType, UrgencyLevel
from backend.agents.evaluator_agent import EvaluatorAgent

@pytest.fixture
def agent():
    with patch('backend.agents.evaluator_agent.get_llm') as mock_get_llm:
        mock_get_llm.return_value = MagicMock()
        yield EvaluatorAgent()

def test_evaluator_agent_metrics(agent):
    # Needs: total qty = 20, 1 critical, 1 high
    needs = [
        VerifiedNeed(
            need_id="need-crit",
            source_report_ids=["r1"],
            location_text="A",
            need_type=NeedType.WATER,
            quantity_estimate=10,
            urgency=UrgencyLevel.CRITICAL,
            verification_confidence=1.0,
            requires_human_review=False
        ),
        VerifiedNeed(
            need_id="need-high",
            source_report_ids=["r2"],
            location_text="B",
            need_type=NeedType.WATER,
            quantity_estimate=10,
            urgency=UrgencyLevel.HIGH,
            verification_confidence=1.0,
            requires_human_review=False
        )
    ]
    
    # Plan: allocates 10 to high, leaves critical unmet
    plan = DispatchPlan(
        plan_id="plan-1",
        generated_at="2026-07-25T00:00:00Z",
        allocations=[
            Allocation(need_id="need-high", resource_id="res-1", quantity_allocated=10, distance_km=5.0, allocation_method="greedy")
        ],
        unmet_needs=["need-crit"],
        narrative="Allocated high urgency, left critical unmet."
    )
    
    class MockEval:
        fairness_score = 0.2
        passed = False
        rationale = "Left critical unmet"
        revision_notes = "Prioritize critical"
        
    agent.chain = MagicMock()
    agent.chain.invoke.return_value = MockEval()
    
    result = agent.process(plan, needs)
    
    assert result.coverage_pct == 50.0 # 10 / 20 allocated
    assert result.critical_unmet_count == 1
    assert result.passed is False
