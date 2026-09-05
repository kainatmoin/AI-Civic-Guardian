from pydantic import BaseModel


class Report(BaseModel):
    issue_type: str
    description: str
    latitude: float
    longitude: float