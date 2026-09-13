# Gates: Real Authentication

OWNS: backend/security/auth.py, backend/db/models.py, backend/main.py

Scope: Replace the hardcoded fake_users_db dictionary with a DBUser SQLAlchemy model, implement bcrypt password hashing, seed a default user, and authenticate against the database.

- [x] G1: DBUser model exists in models.py
  CHECK: .venv\\Scripts\\python -c "from backend.db.models import DBUser; print('DBUser found')"
  EXPECT: DBUser found
  EVIDENCE: automatic-evidence=v1; definition-sha256=69e5a0e63dbdbd1ef81a213c3b9f37e36ed5c2e14f53f2906d132d7060fe4740; exit=0; EXPECT=matched; output-sha256=62e0a78c7a52ea4c1551a3295d2b366aa19f47ac93a2112a8548a1ca96e7dbac; output-bytes=14; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries

- [x] G2: fake_users_db is completely removed from auth.py
  CHECK: .venv\\Scripts\\python -c "f = open('backend/security/auth.py').read(); print('clean' if 'fake_users_db' not in f else 'found')"
  EXPECT: clean
  EVIDENCE: automatic-evidence=v1; definition-sha256=e3deddec1b5bdecc177963b3ae46316ca5b0b4735cba9752e424897e279d9c79; exit=0; EXPECT=matched; output-sha256=bf9b5d9576f23812d3a58c66a57a3fd7616cb25fd90538cbca5bd8b761f6c5fb; output-bytes=7; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries

- [x] G3: Database is seeded with default user 'alice'
  CHECK: .venv\\Scripts\\python -c "from backend.db.models import DBUser, SessionLocal; db = SessionLocal(); user = db.query(DBUser).filter(DBUser.username == 'alice').first(); print('Seeded' if user else 'Not found')"
  EXPECT: Seeded
  EVIDENCE: automatic-evidence=v1; definition-sha256=cbea0870c0f2a1474f8b303b2c9dffdc849d632370c54ae4d141a084b8f01563; exit=0; EXPECT=matched; output-sha256=f4a28d5e8dcfdbd155597c06ea5413ac80b75bd11cfa17ac4f7129bbdcaaf277; output-bytes=8; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries

- [x] G4: Authentication succeeds for valid credentials and returns a token
  CHECK: .venv\\Scripts\\python -c "import requests; r = requests.post('http://127.0.0.1:8000/api/v1/auth/token', data={'username': 'alice', 'password': 'reviewer_pass'}); print('TokenGenerated' if r.status_code == 200 and 'access_token' in r.json() else r.text)"
  EXPECT: TokenGenerated
  EVIDENCE: automatic-evidence=v1; definition-sha256=92f5c310ab5ff6c0231478da515d3172716e70ac4bd9c1906a71a3b813db7df1; exit=0; EXPECT=matched; output-sha256=93cc1e6d341cdfd1c8767a24c1d2ba4be6d1e55365be7259f91b959dca42de2d; output-bytes=16; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries
