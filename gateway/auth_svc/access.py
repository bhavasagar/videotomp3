import requests, json, os

def login(request):
    auth = request.authorization
    if not auth:
        return None, ("Invalid Credentials", 400)

    resp = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login",
        auth=(auth.username, auth.password)
    )
    if resp.status_code == 200:
        return resp.txt, None
    return None, (resp.txt, resp.status_code)
