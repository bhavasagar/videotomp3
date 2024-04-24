import requests
import json
import os


def login(request):
    auth = request.authorization
    print(auth, "AUTH")
    if not auth:
        return None, ("Invalid Credentials", 400)
    print(auth.username, auth.password)
    resp = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login",
        auth=(auth.username, auth.password)
    )
    if resp.status_code == 200:
        return resp.text, None
    return None, (resp.text, resp.status_code)
