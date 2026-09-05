from pydantic import BaseModel


class ReportCreate(BaseModel):
    issue_type: str
    description: str
    latitude: float
    longitude: float