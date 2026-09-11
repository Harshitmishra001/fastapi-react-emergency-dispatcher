import base64
import urllib.request
import os

mermaid_code = """%%{init: {'theme': 'default', 'themeVariables': { 'background': '#ffffff'}}}%%
graph LR
    A([User Submits Raw Report]) --> B[Ingestion Agent]
    B --> C[Verification Agent]
    
    C -->|High Confidence & Unique| D[Resource Matcher]
    C -->|Low Confidence or Duplicate| E{Human-in-the-Loop Pause}
    
    E -.->|Dispatcher Approves| D
    E -.->|Dispatcher Rejects| F([Flow Ended / Archived])
    
    D --> G[Plan Synthesizer]
    G --> H[Evaluator Agent]
    
    H -->|Passes Fairness/Coverage| I([Dispatch Plan Finalized])
    H -->|Fails Thresholds| J{Revision Count < 2?}
    
    J -- Yes --> D
    J -- No --> I
"""

# Base64 encode the mermaid string
encoded = base64.b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
# mermaid.ink uses /img/<base64>
url = f"https://mermaid.ink/img/{encoded}?bgColor=ffffff"

print(f"Fetching from {url}...")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        img_data = response.read()

    output_path = os.path.join(os.getcwd(), "system_architecture.png")
    with open(output_path, "wb") as f:
        f.write(img_data)

    print(f"Diagram saved to {output_path}")
except Exception as e:
    print(f"Error: {e}")
