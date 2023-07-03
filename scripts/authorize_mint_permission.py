import os, json
from dotenv import load_dotenv
from conflux_web3.dev import get_testnet_web3


def main():
    load_dotenv()
    ORACLE_KEY = os.environ["ORACLE_KEY"]
    ORACLE_BATCH_NBR = int(os.environ["ORACLE_BATCH_NBR"])
    CORE_CONTRACT_ADDRESS = os.environ["CORE_CONTRACT_ADDRESS"]
    with open("./scripts/DualSpaceNFTCore.json") as f:
        metadata = json.load(f)

    w3 = get_testnet_web3()
    w3.cfx.default_account = w3.account.from_key(ORACLE_KEY)

    contract = w3.cfx.contract(address=CORE_CONTRACT_ADDRESS, abi=metadata["abi"])
    # this will not be applied in official env
    contract.functions.batchAuthorizeMintPermission(
        ORACLE_BATCH_NBR,
        ["darwintree"],
        [4],
    ).transact().executed()


if __name__ == "__main__":
    main()
