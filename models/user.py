from pydantic import BaseModel
from typing import List, Dict, Any,Optional

class UserRegister(BaseModel):
    firstname: str
    lastname: str
    emailid: str
    mobileno: str
    password: str
    dateofbirth: str
    gender: str
    photo: Optional[str] = None
    status: str
    # created_on: str
    # updated_on: str

class UserLogin(BaseModel):
    mobileno: str
    password: str