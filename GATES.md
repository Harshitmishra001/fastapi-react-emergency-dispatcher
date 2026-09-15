# Gates: Real Geocoding Integration

OWNS: backend/agents/ingestion_agent.py

Scope: Implement geocoding for extracted locations to populate coordinates using geopy and Nominatim.

- [x] G1: geopy is installed and in requirements.txt
  CHECK: .venv\Scripts\python -c "import geopy; print('geopy found')"
  EXPECT: geopy found
  EVIDENCE: automatic-evidence=v1; definition-sha256=851c57065a1f599ec8fc292e432f7f4a2582cc66f8decebae2106f498c6ab07d; exit=0; EXPECT=matched; output-sha256=6f3d9c03dcc84d184697a3813f93e212affb564967f4072c982594615f2d86e9; output-bytes=13; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries

- [x] G2: ingestion_agent uses Nominatim to resolve coordinates
  CHECK: .venv\Scripts\python -c "f = open('backend/agents/ingestion_agent.py').read(); print('nominatim' if 'Nominatim' in f else 'missing')"
  EXPECT: nominatim
  EVIDENCE: automatic-evidence=v1; definition-sha256=d7930e401b3c2f76f38d438e1e126092451270ab5d098ca44a58f2c9154eb29a; exit=0; EXPECT=matched; output-sha256=e43a85f357025ca7b0f92de706a02899cd838fe9ccbffc6f5d7a71e75dab26cd; output-bytes=11; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries

- [x] G3: Ingestion agent successfully fetches real coordinates for 'New York, NY'
  CHECK: .venv\Scripts\python -c "from backend.agents.ingestion_agent import IngestionAgent; print('HasCoords' if IngestionAgent()._geocode_location('New York, NY') is not None else 'NoCoords')"
  EXPECT: HasCoords
  EVIDENCE: automatic-evidence=v1; definition-sha256=9d87c1fa0d1988430b223e7673fd44da4d105bf526da28f969dcfe5493db75ae; exit=0; EXPECT=matched; output-sha256=bca124005e9712d6228750b7d615a4f8ad510ae327125168338abf10bd4d32f0; output-bytes=11; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\hmhar\Projects\Disaster_Coordinator; path=4c78bc975020/45 entries
