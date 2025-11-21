from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# ---------------------------
# DOCUMENT
# ---------------------------

class Document(BaseModel):
    id: int
    document: str
    user_id: int
    validity: bool

    model_config = {
        "from_attributes": True
    }


class DocumentIn(BaseModel):
    document: str
    user_id: int
    validity: Optional[bool] = False


# ---------------------------
# PROFILE
# ---------------------------

class Profile(BaseModel):
    user_id: int
    proceed: bool

    model_config = {
        "from_attributes": True
    }


class ProfileIn(BaseModel):
    proceed: Optional[bool] = False