import requests, json

def token(request):
    if not requests.get("Authorization"):
        return "Auth header missing", 400

    resp = requests.post(f"http://{AUTH_SVC_ADDRESS}/validate", headers={
        "Authorization": requests["Authorization"]
    })
    if resp.status_code == 200:
        claims = json.loads(resp.txt)
        return claims, None

    return None, (resp.txt, resp.status_code)