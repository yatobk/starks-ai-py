from pydantic.v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import Optional, Type
import random
import string

def create_password(lenght: int):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(lenght))
    return password

class PasswordGeneratorCheckInput(BaseModel):
    """The lenght of new password provided by the user"""

    lenght: int = Field(..., description="The lenght of new password provided by the user.")    

class PasswordGenerator(BaseTool):
    name="create_secure_password"
    description="Extract the lenght of password from user's request and generate a new secure one."

    def _run(self, lenght:int):
        result = create_password(lenght)
        return result
    def _arun(self, lenght:int):
        raise NotImplementedError("This tool does not support async")
    
    args_schema: Optional[Type[BaseModel]] = PasswordGeneratorCheckInput
