import requests
import json

mid = "613b10513dca832446e16c3f"

API_URL = "http://123.214.186.231:4882"


# POST (JSON)
headers = {'Content-Type': 'application/json; chearset=utf-8'}
data = {"id": "613b10613dca832446e16c60"}
res = requests.post(f"{API_URL}/get_edgeInfo",
                    data=json.dumps(data), headers=headers)
print(str(res.status_code) + " | " + res.text)
