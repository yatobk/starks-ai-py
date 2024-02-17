from pydantic.v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import Optional, Type
import requests

def getAssessment(id: str):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer daMAeCRcZyzFYCDdzEkHnKKgqcnwNpVjuP6Aq6FYo2hYGon2mPNsFiYkgYaqf75T"
    }
    response = requests.get(
        url=f"http://starksfit.vercel.app/api/customer/assessments?customerId={id}",
        headers=headers
    )
    return response.json()

class GetAssessmentsCheckInput(BaseModel):
    """Input for the user's id"""

    customerId: str = Field(..., description="The customer id from the user to search the assessments.")

class GetAssessmentsTool(BaseTool):
    name="get_assessments_tool"
    description="Useful for when you need get the assessments for the users"

    def _run(self, customerId:str):
        result = getAssessment(customerId)
        return result
    def _arun(self, customerId:str):
        raise NotImplementedError("This tool does not support async")
    
    args_schema: Optional[Type[BaseModel]] = GetAssessmentsCheckInput

