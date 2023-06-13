from pydantic import BaseModel


class RawMessageToSign(BaseModel):
    batch_nbr: int
    # username: str
    core_address: str  # should be Base32Address
    evm_address: str
    code: str  # username from code
