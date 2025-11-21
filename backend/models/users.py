from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: int
    email: str
    mobno: Optional[str]
    confirmation: bool

    model_config = {
        "from_attributes": True
    }


class UserIn(BaseModel):
    email: str
    mobno: Optional[str]
    password: str

# ---------------------------
# CLIENT
# ---------------------------

class Client(BaseModel):
    user_id: int
    no_fm: int
    doc_type: str
    aadhar_no: str

    model_config = {
        "from_attributes": True
    }


class ClientIn(BaseModel):
    no_fm: int
    doc_type: str
    aadhar_no: str