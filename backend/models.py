from sqlalchemy import Column, Integer, String, Float
from database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    issue_type = Column(String)
    description = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)