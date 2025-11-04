from pydantic import BaseModel
from typing import List, Dict, Any,Optional
class AddRole(BaseModel):
    role: str

class AddUserRole(BaseModel):
    user_id: int
    role_id: List[int]
