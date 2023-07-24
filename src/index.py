import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.dtos.RawMessageToSignDto import RawMessageToSign
from src.utils import get_github_username, sign_username, get_crowdin_username

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ORACLE_KEY = os.environ["ORACLE_KEY"]
ORACLE_BATCH_NBR = int(os.environ["ORACLE_BATCH_NBR"])


@app.post("/sign/github/{state}")
async def sign(dto: RawMessageToSign, state: str):
    print(f"get request {dto}")
    try:
        if dto.batch_nbr != ORACLE_BATCH_NBR:
            raise Exception(
                f"this oracle has no permission to authorize batch number {dto.batch_nbr}"
            )
        username = f"github-{get_github_username(dto.code, state)}"
        signature = sign_username(
            username, dto.batch_nbr, dto.core_address, dto.evm_address
        )

        return {
            "signature": signature,
            "username": username,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))


@app.post("/sign/crowdin/{state}")
async def sign(dto: RawMessageToSign, state: str):
    print(f"get request {dto}")
    try:
        if dto.batch_nbr != ORACLE_BATCH_NBR:
            raise Exception(
                f"this oracle has no permission to authorize batch number {dto.batch_nbr}"
            )
        username = f"crowdin-{get_crowdin_username(dto.code, state)}"
        signature = sign_username(
            username, dto.batch_nbr, dto.core_address, dto.evm_address
        )

        return {
            "signature": signature,
            "username": username,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))
