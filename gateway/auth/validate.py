import requests, json, os

def token(request):
    if not request.headers or not request.headers.get("Authorization"):
        return "Auth header missing", 400

    resp = requests.post(f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate", headers={
        "Authorization": request.headers["Authorization"]
    })
    if resp.status_code == 200:
        claims = json.loads(resp.text)
        return claims, None

    return None, (resp.text, resp.status_code)