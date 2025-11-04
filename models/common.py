from pydantic import BaseModel
from typing import List, Dict, Any,Optional,Union

class MasterResponse(BaseModel):
    message:str
    status:str
    data: Union[Dict[str, Any], List[Any]]