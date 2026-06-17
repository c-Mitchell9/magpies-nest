import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1516297935154053243/Vr0mCI2ivgG9QCasszBzXfECv-tU6ZkthszOswnyUxDh7Qw06h4j71fVTunMnVELtLIG"

message = """
🔥 **S TIER ALERT**

**ESP USA Horizon II**

Price: **$1,999**
Source: Guitar Center

Reason surfaced:
Matched ESP / Horizon target family

Link:
https://example.com
"""

response = requests.post(WEBHOOK_URL, json={"content": message})

print(response.status_code)