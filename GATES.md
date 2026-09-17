# Gates: Phase C Finalization

OWNS: backend/utils/logger.py, backend/graph/build_graph.py, tests/test_adversarial.py, data/synthetic_reports.json

Scope: Implement structured audit logging, adversarial testing, and synthetic dataset.

- [x] G1: Structured JSON logger exists and can log events
  CHECK: .venv\Scripts\python -c "import json; from backend.utils.logger import get_audit_logger; logger = get_audit_logger('test'); logger.info('Test event', extra={'user_id': 123}); f = open('audit.log', 'r').readlines()[-1]; print('json' if json.loads(f)['user_id'] == 123 else 'fail')"
  EXPECT: json
  EVIDENCE: automatic-evidence=v1; definition-sha256=6b3031d624ad5c0cbd21b5d4839e573e10d562a8daa5901684cc29085904337c; exit=0; EXPECT=matched; output-sha256=120d081932fc68341122f9e292722e7b1ee77dbec3d78f440f27342a88f2605d; output-bytes=132; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries

- [x] G2: Graph uses audit logger for transitions
  CHECK: .venv\Scripts\python -c "f = open('backend/graph/build_graph.py').read(); print('logger' if 'get_audit_logger' in f else 'missing')"
  EXPECT: logger
  EVIDENCE: automatic-evidence=v1; definition-sha256=435328edb1acfcf9b9a230c8b9d5e3d753cd3f835d3b3c2b1b72deee00e4a1e4; exit=0; EXPECT=matched; output-sha256=8282c3762983f4b157647650dbe4d967e3725ce8a708be7a7aadd076d20a1526; output-bytes=8; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries

- [x] G3: Adversarial test suite exists
  CHECK: .venv\Scripts\python -c "import os; print('found' if os.path.exists('tests/test_adversarial.py') else 'missing')"
  EXPECT: found
  EVIDENCE: automatic-evidence=v1; definition-sha256=c190b775c9b0295e85548f83658413629d6d25b862a59d0d9e8e9e971bed7a84; exit=0; EXPECT=matched; output-sha256=8c6e7678c35c6653b6589a55bc699036cf54d7b4e064018bc7a8b784ee569229; output-bytes=7; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries

- [x] G4: Synthetic incident dataset exists
  CHECK: .venv\Scripts\python -c "import json; f = json.load(open('data/synthetic_reports.json')); print('found' if len(f) > 0 and 'raw_text' in f[0] else 'missing')"
  EXPECT: found
  EVIDENCE: automatic-evidence=v1; definition-sha256=da772e87042b45dd2388e052ae89af9b7f1ed53a5ad0dc1226f6b938cc4825ee; exit=0; EXPECT=matched; output-sha256=8c6e7678c35c6653b6589a55bc699036cf54d7b4e064018bc7a8b784ee569229; output-bytes=7; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries
