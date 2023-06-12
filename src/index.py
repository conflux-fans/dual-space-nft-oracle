import os

from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware

from web3 import Web3
from eth_account import Account
from cfx_address import Base32Address

from src.dtos.RawMessageToSignDto import RawMessageToSign
from src.dtos.ISayHelloDto import ISayHelloDto
from src.utils import matches

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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/hello")
async def hello_message(dto: ISayHelloDto):
    return {"message": f"Hello {dto.message}"}


@app.post("/sign/{state}")
async def sign(dto: RawMessageToSign, state: str):
    print("get")
    try:
        if not matches(dto.code, state, dto.username):
            raise Exception("username does not match")
        username_hash = Web3.solidity_keccak(["string"], [dto.username])
        message_hash = Web3.solidity_keccak(
            ["uint128", "bytes32", "address", "address"],
            [
                dto.batch_nbr,
                username_hash,
                Base32Address(dto.core_address).hex_address,
                dto.evm_address
            ]
        )
        signature = Account.signHash(
            message_hash,
            ORACLE_KEY,
        )
        
        return {
            "v": signature.v,
            "r": hex(signature.r),
            "s": hex(signature.s)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))
