import os, json, requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
GITHUB_URL = os.environ.get("GITHUB_URL", "https://github.com")
GITHUB_API_URL = os.environ.get("GITHUB_API_URL", "https://api.github.com")


def get_username(code: str, state: str) -> str:
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "state": state,
    }
    response = requests.post(
        f"{GITHUB_URL}/login/oauth/access_token",
        headers=headers,
        data=json.dumps(payload),
    )
    rtn = response.json()
    # print(rtn)
    access_token = rtn["access_token"]

    user_response = requests.get(
        f"{GITHUB_API_URL}/user",
        headers={
            "Authorization": f"bearer {access_token}",
            "Accept": "application/json",
        },
    )
    return user_response.json()["login"]
