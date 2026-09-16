# Gates: Evaluator Retry Loop

OWNS: backend/agents/evaluator_agent.py, backend/agents/resource_matcher.py, backend/graph/build_graph.py

Scope: Make evaluator retry loop actually pass revision_notes to matcher, boosting priority of flagged needs.

- [x] G1: EvaluatorAgent instructs LLM to use exact need_ids in revision_notes
  CHECK: .venv\Scripts\python -c "f = open('backend/agents/evaluator_agent.py').read(); print('found' if 'exact need_id' in f.lower() else 'missing')"
  EXPECT: found
  EVIDENCE: automatic-evidence=v1; definition-sha256=68c61efacfa0e1ea88ec29bca8fc2babddbc52e658cfb9656dca28d35a967faa; exit=0; EXPECT=matched; output-sha256=8c6e7678c35c6653b6589a55bc699036cf54d7b4e064018bc7a8b784ee569229; output-bytes=7; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries

- [x] G2: ResourceMatcher boosts urgency weight when need_id is in revision_notes
  CHECK: .venv\Scripts\python -c "f = open('backend/agents/resource_matcher.py').read(); print('found' if 'revision_notes' in f else 'missing')"
  EXPECT: found
  EVIDENCE: automatic-evidence=v1; definition-sha256=885333400f404ed5d8a0706a39a7c78b9984747707b1bc12d748233c2bbff2f2; exit=0; EXPECT=matched; output-sha256=8c6e7678c35c6653b6589a55bc699036cf54d7b4e064018bc7a8b784ee569229; output-bytes=7; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries

- [x] G3: build_graph.py passes revision_notes to match_agent.process
  CHECK: .venv\Scripts\python -c "f = open('backend/graph/build_graph.py').read(); print('found' if 'revision_notes=' in f else 'missing')"
  EXPECT: found
  EVIDENCE: automatic-evidence=v1; definition-sha256=8d60c0d552f85aa3805dd01bc78bb2a580a793c25efb99991ee0aa96c185aab7; exit=0; EXPECT=matched; output-sha256=8c6e7678c35c6653b6589a55bc699036cf54d7b4e064018bc7a8b784ee569229; output-bytes=7; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries

- [x] G4: ResourceMatcher properly elevates a revised need
  CHECK: .venv\Scripts\python -c "from backend.agents.resource_matcher import ResourceMatcher; from backend.schemas.models import VerifiedNeed, ResourceRecord, NeedType, UrgencyLevel; n1 = VerifiedNeed(need_id='need-1', source_report_ids=[], location_text='A', coordinates=(0.0,0.0), need_type=NeedType.WATER, quantity_estimate=10, urgency=UrgencyLevel.LOW, verification_confidence=1.0, requires_human_review=False); n2 = VerifiedNeed(need_id='need-2', source_report_ids=[], location_text='B', coordinates=(0.0,0.0), need_type=NeedType.WATER, quantity_estimate=10, urgency=UrgencyLevel.LOW, verification_confidence=1.0, requires_human_review=False); r1 = ResourceRecord(resource_id='r1', resource_type=NeedType.WATER, quantity_available=10, location=(0.0, 0.0), status='available'); matcher = ResourceMatcher(); allocs = matcher.process([n1, n2], [r1], revision_notes='Prioritize need-2 immediately'); print('Boosted' if allocs[0].need_id == 'need-2' else allocs[0].need_id)"
  EXPECT: Boosted
  EVIDENCE: automatic-evidence=v1; definition-sha256=fac9746de2a66f2ae754bbea8f85ec6b8a8ad01eb104fba2e9e7c9c6fcc9b8d8; exit=0; EXPECT=matched; output-sha256=9e2ddd454f40a063af8cd88fb24724746be39d382b9445938eb4adbb321efe03; output-bytes=9; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries
