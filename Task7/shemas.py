from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional

class inptut_resource(BaseModel):
    name:str
    email:str

class input_project(BaseModel):
    name:str
    projectManager : uuid.UUID
    description : Optional[str] = None
    softDeadline : datetime 
    hardDeadline : Optional[datetime] = None
