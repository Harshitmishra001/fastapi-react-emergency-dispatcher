# Gates: ILP Resource Optimization

OWNS: backend/agents/resource_matcher.py

Scope: Replace greedy matching with an ILP (Integer Linear Programming) optimizer using PuLP.

- [x] G1: pulp is installed and in requirements.txt
  CHECK: .venv\Scripts\python -c "import pulp; print('pulp found')"
  EXPECT: pulp found
  EVIDENCE: automatic-evidence=v1; definition-sha256=6575ed3e24104bea8a1c3c1e368d2b39b9869c9afba8d099403cf5bf9507564c; exit=0; EXPECT=matched; output-sha256=c5698bad2be85bfc24c4b52ad8b422a91036122175e07a554da92dfe936269ed; output-bytes=12; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries

- [x] G2: resource_matcher uses PuLP for optimization
  CHECK: .venv\Scripts\python -c "f = open('backend/agents/resource_matcher.py').read(); print('pulp' if 'LpProblem' in f else 'missing')"
  EXPECT: pulp
  EVIDENCE: automatic-evidence=v1; definition-sha256=7f1d0872944dd9d418f15ed41a7c5aa695f16e768de3ea18fb75266f87850c24; exit=0; EXPECT=matched; output-sha256=cc13d31ec51c3b5c8c6a8f2fbe24f24dcc741353c49bac14b7400dd20bbda7f0; output-bytes=6; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries

- [x] G3: Allocations are tagged as 'ilp_optimal'
  CHECK: .venv\Scripts\python -c "from backend.agents.resource_matcher import ResourceMatcher; from backend.schemas.models import VerifiedNeed, ResourceRecord, NeedType, UrgencyLevel; n1 = VerifiedNeed(need_id='n1', source_report_ids=[], location_text='Loc', coordinates=(0.0,0.0), need_type=NeedType.WATER, quantity_estimate=10, urgency=UrgencyLevel.HIGH, verification_confidence=1.0, requires_human_review=False); r1 = ResourceRecord(resource_id='r1', resource_type=NeedType.WATER, quantity_available=20, location=(0.0, 0.1), status='available'); matcher = ResourceMatcher(); alloc = matcher.process([n1], [r1]); print(alloc[0].allocation_method if alloc else 'None')"
  EXPECT: ilp_optimal
  EVIDENCE: automatic-evidence=v1; definition-sha256=b9b7ccad0f3349368124a65a723c74ef5776467066f8d1b39b4f79c6e215516c; exit=0; EXPECT=matched; output-sha256=2ba301c6f1415282bd6428a57a7502eeb5bb905cf5a90b08b561fb12c4596366; output-bytes=13; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries
