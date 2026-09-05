from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, Base, engine
from models import Report
from schemas import ReportCreate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Civic Guardian API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "message": "AI Civic Guardian API is running",
        "status": "success"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/reports")
def create_report(
    report: ReportCreate,
    db: Session = Depends(get_db)
):
    db_report = Report(
        issue_type=report.issue_type,
        description=report.description,
        latitude=report.latitude,
        longitude=report.longitude
    )

    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    return {
        "message": "Report saved successfully",
        "report": {
            "id": db_report.id,
            "issue_type": db_report.issue_type,
            "description": db_report.description,
            "latitude": db_report.latitude,
            "longitude": db_report.longitude
        }
    }
