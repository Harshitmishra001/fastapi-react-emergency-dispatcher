# Gates: Vector Database Integration

OWNS: backend/db/vector_store.py, backend/agents/verification_agent.py

Scope: Replace NumPy-based O(N) duplicate search with a Vector Database (Qdrant) to support persistence and scale.

- [x] G1: qdrant-client is installed and in requirements.txt
  CHECK: .venv\\Scripts\\python -c "import qdrant_client; print('qdrant_client found')"
  EXPECT: qdrant_client found
  EVIDENCE: automatic-evidence=v1; definition-sha256=9b6cf034021f862ce8e09c989c1f111a60a56704bca66c6d5b13ed1378cea7d4; exit=0; EXPECT=matched; output-sha256=f5d90cfdb7085a8fb1e78d9f24c78bce727173463e7b15c081ed667f08818a50; output-bytes=21; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries

- [x] G2: VerificationAgent uses vector store instead of numpy
  CHECK: .venv\\Scripts\\python -c "f = open('backend/agents/verification_agent.py').read(); print('clean' if 'numpy' not in f else 'found')"
  EXPECT: clean
  EVIDENCE: automatic-evidence=v1; definition-sha256=47374fc1c123b81a76deeb98ebd26b3d0f16430ac97bc38f61339f902b80aa97; exit=0; EXPECT=matched; output-sha256=bf9b5d9576f23812d3a58c66a57a3fd7616cb25fd90538cbca5bd8b761f6c5fb; output-bytes=7; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries

- [x] G3: Vector deduplication successfully returns a match above threshold
  CHECK: .venv\Scripts\python -c "import shutil; shutil.rmtree('qdrant_data', ignore_errors=True); from backend.agents.verification_agent import VerificationAgent; from backend.schemas.models import ExtractedNeed, VerifiedNeed; agent = VerificationAgent(); n1 = VerifiedNeed(need_id='n1', need_type='water', location_text='123 Main St', source_report_ids=[], quantity_estimate=10, urgency='high', verification_confidence=0.9, requires_human_review=False); agent._get_vdb().upsert_need(n1, agent._get_model().encode('123 Main St water')); ext = ExtractedNeed(report_id='r2', need_type='water', location_text='123 Main St', quantity_estimate=5, stated_urgency='high', extraction_confidence=0.9); res = agent.process(ext, [n1]); print('Matched' if res.duplicate_of == 'n1' else 'No match')"
  EXPECT: Matched
  EVIDENCE: automatic-evidence=v1; definition-sha256=82f170e45204db6d69010ba3925dcdce8a4d96348a17e88fcd18268bccfede2c; exit=0; EXPECT=matched; output-sha256=2aaff913f0a7ee329ad4830abb2d47edd15e664f295d8321932e8aa7da6be52a; output-bytes=962; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries
