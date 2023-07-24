import os, json, requests
from cfx_address import Base32Address
from eth_account import Account
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
CROWDIN_CLIENT_ID = os.environ["CROWDIN_CLIENT_ID"]
CROWDIN_CLIENT_SECRET = os.environ["CROWDIN_CLIENT_SECRET"]
# GITHUB_URL = os.environ.get("GITHUB_URL", "https://github.com")
GITHUB_ACCESS_TOKEN_ENDPOINT = os.environ.get("GITHUB_ACCESS_TOKEN_ENDPOINT", "https://github.com/login/oauth/access_token")
GITHUB_API_URL = os.environ.get("GITHUB_API_URL", "https://api.github.com")
CROWDIN_ACCESS_TOKEN_ENDPOINT = os.environ.get("CROWDIN_ACCESS_TOKEN_ENDPOINT", "https://accounts.crowdin.com/oauth/token")
CROWDIN_API_URL = os.environ.get("CROWDIN_API_URL", "https://api.crowdin.com/api/v2")
CROWDIN_REDIRECT_URI = os.environ["CROWDIN_REDIRECT_URI"]

ORACLE_KEY = os.environ["ORACLE_KEY"]

def sign_username(username: str, batch_nbr: int, core_address: str, evm_address: str):
    username_hash = Web3.solidity_keccak(["string"], [username])
    message_hash = Web3.solidity_keccak(
        ["uint128", "bytes32", "address", "address"],
        [
            batch_nbr,
            username_hash,
            Base32Address(core_address).hex_address,
            evm_address,
        ],
    )
    signature = Account.signHash(
        message_hash,
        ORACLE_KEY,
    )
    return {
        "v": signature.v,
        "r": hex(signature.r),
        "s": hex(signature.s),
    }

def get_github_username(code: str, state: str) -> str:
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "state": state,
    }
    response = requests.post(
        GITHUB_ACCESS_TOKEN_ENDPOINT,
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

def get_crowdin_username(code: str, state: str) -> str:
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    payload = {
        "grant_type": "authorization_code",
        "redirect_uri": CROWDIN_REDIRECT_URI,
        "client_id": CROWDIN_CLIENT_ID,
        "client_secret": CROWDIN_CLIENT_SECRET,
        "code": code,
        # "state": state,
    }
    response = requests.post(
        CROWDIN_ACCESS_TOKEN_ENDPOINT,
        headers=headers,
        data=json.dumps(payload),
    )
    rtn = response.json()
    # print(rtn)
    access_token = rtn["access_token"]

    user_response = requests.get(
        f"{CROWDIN_API_URL}/user",
        headers={
            "Authorization": f"bearer {access_token}",
            "Accept": "application/json",
        },
    )
    return user_response.json()["data"]["username"]