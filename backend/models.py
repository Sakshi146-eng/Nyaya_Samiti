from pydantic import BaseModel,EmailStr,Field,HttpUrl
from typing import List,Literal

class FamilyMember(BaseModel):
    name:str=Field(...,min_length=1)
    email:EmailStr=Field(...,description="Valid email address is required")
    mobno:str=Field(...,min_length=10)
    age:int=Field(...,gt=0)
    relation:str=Field(...,min_length=1)
    address:str=Field(...,min_length=10)
    video_urls:str=Field(...,description="URL of the video")


class Document(BaseModel):
    doc_urls:HttpUrl=Field(...,description="URL of the uploaded document")
    status:Literal["valid","invalid"]=Field(...,description="Status of the document")

class User(BaseModel):
    name: str=Field(...,min_length=1)
    email: EmailStr=Field(...,description="Valid email address is required")
    mobno: str=Field(...,min_length=10)
    age: int=Field(...,gt=0)
    address:str=Field(...,min_length=10)
    no_of_family_members:int=Field(...,gt=0)
    family_member:List[FamilyMember]=Field(...,description="List of family members")


    





