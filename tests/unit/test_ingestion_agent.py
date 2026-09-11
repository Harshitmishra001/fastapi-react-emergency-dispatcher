import pytest
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

from backend.schemas.models import RawReport, NeedType, UrgencyLevel
from backend.agents.ingestion_agent import IngestionAgent

@pytest.fixture
def agent():
    # We patch get_llm so we don't actually hit LM Studio during tests
    with patch('backend.agents.ingestion_agent.get_llm') as mock_get_llm:
        mock_get_llm.return_value = MagicMock()
        yield IngestionAgent()

def test_ingestion_agent_regex_fallback(agent):
    # If the LLM throws an exception (simulating failure), it should fall back to regex
    agent.chain = MagicMock()
    agent.chain.invoke.side_effect = Exception("LLM offline")
    
    report = RawReport(
        report_id="rpt-123",
        source_channel="sms",
        raw_text="We have 5 injured people at the Main St shelter. Need a doctor immediately.",
        submitted_at=datetime.now(timezone.utc)
    )
    
    result = agent.process(report)
    
    assert result.report_id == "rpt-123"
    assert result.need_type == NeedType.MEDICAL # Caught by 'injured' or 'doctor'
    assert result.quantity_estimate == 5
    assert result.stated_urgency == UrgencyLevel.CRITICAL # Caught by 'immediately'
    # Regex fallback starts at 0.2 confidence and maxes at 0.9; never 0.0
    assert 0.0 < result.extraction_confidence < 1.0
    
def test_ingestion_agent_llm_success(agent):
    class MockLLMExtraction:
        location_text = "Main St shelter"
        need_type = NeedType.MEDICAL
        quantity_estimate = 5
        stated_urgency = UrgencyLevel.CRITICAL
        
    agent.chain = MagicMock()
    agent.chain.invoke.return_value = MockLLMExtraction()
    
    report = RawReport(
        report_id="rpt-124",
        source_channel="sms",
        raw_text="We have 5 injured people at the Main St shelter. Need a doctor immediately.",
        submitted_at=datetime.now(timezone.utc)
    )
    
    result = agent.process(report)
    
    assert result.report_id == "rpt-124"
    assert result.need_type == NeedType.MEDICAL
    assert result.extraction_confidence > 0.0 # Not a fallback
