import requests

headers = {
    "xi-api-key": "sk_1ab17f99867d29114f3650a1e45e8a59ae5bb4264b809aa8"
}

r = requests.get(
    "https://api.elevenlabs.io/v1/voices",
    headers=headers
)

print(r.status_code)
print(r.json())