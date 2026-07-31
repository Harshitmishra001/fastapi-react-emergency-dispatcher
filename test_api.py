import requests

url = "http://127.0.0.1:8000/reports"
payload = {
    "source_channel": "sms",
    "raw_text": "Urgent: We need medical supplies at 123 Oak St immediately! Send an ambulance.",
    "reporter_contact": "555-1234"
}
headers = {
    "Content-Type": "application/json"
}

print(f"Sending request to {url}...")
response = requests.post(url, json=payload)
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
