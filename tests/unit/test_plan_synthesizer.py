import pytest
from unittest.mock import patch, MagicMock
from backend.schemas.models import Allocation, DispatchPlan
from backend.agents.plan_synthesizer import PlanSynthesizer

@pytest.fixture
def agent():
    with patch('backend.agents.plan_synthesizer.get_llm') as mock_get_llm:
        mock_get_llm.return_value = MagicMock()
        yield PlanSynthesizer()

def test_plan_synthesizer_grounding_success(agent):
    allocations = [
        Allocation(need_id="need-1", resource_id="res-1", quantity_allocated=5, distance_km=1.2, allocation_method="greedy_fallback")
    ]
    unmet_needs = ["need-2"]
    
    agent.chain = MagicMock()
    agent.chain.invoke.return_value = "We allocated resources from res-1 to need-1. However, need-2 remains unmet."
    
    plan = agent.process(allocations, unmet_needs)
    
    assert plan.narrative == "We allocated resources from res-1 to need-1. However, need-2 remains unmet."

def test_plan_synthesizer_grounding_failure(agent):
    allocations = [
        Allocation(need_id="need-1", resource_id="res-1", quantity_allocated=5, distance_km=1.2, allocation_method="greedy_fallback")
    ]
    unmet_needs = []
    
    # LLM hallucinates need-999
    agent.chain = MagicMock()
    agent.chain.invoke.return_value = "We allocated resources to need-999."
    
    plan = agent.process(allocations, unmet_needs)
    
    # Grounding check should fail, and since it fails 3 times, fallback narrative is used.
    assert plan.narrative == "System processed 1 allocations. 0 needs remain unmet."
