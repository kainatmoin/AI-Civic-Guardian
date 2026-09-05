from fastapi import FastAPI, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from ultralytics import YOLO
import os
import shutil
import uuid

from database import SessionLocal, engine, Base
from models import Report


# =========================
# DATABASE
# =========================

Base.metadata.create_all(bind=engine)


# =========================
# APP
# =========================

app = FastAPI(title="AI Civic Guardian API")


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# AI MODEL
# =========================

MODEL_PATH = r"E:\AI-Civic-Guardian\backend\models\civic_guardian.pt"

model = YOLO(MODEL_PATH)


# =========================
# UPLOADS
# =========================

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# =========================
# DATABASE SESSION
# =========================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# =========================
# BASIC ROUTES
# =========================

@app.get("/")
def root():
    return {
        "message": "AI Civic Guardian API is running",
        "status": "success"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =========================
# AI DETECTION
# =========================

@app.post("/detect")
def detect_issue(photo: UploadFile = File(...)):

    file_extension = os.path.splitext(photo.filename)[1]

    temp_filename = f"{uuid.uuid4()}{file_extension}"

    temp_path = os.path.join(
        UPLOAD_FOLDER,
        temp_filename
    )

    # Save temporary image
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(
            photo.file,
            buffer
        )

    try:

        # =========================
        # RUN AI WITH TTA
        # =========================

        results = model.predict(
            source=temp_path,
            imgsz=1024,
            conf=0.001,
            augment=True,
            verbose=False
        )

        detections = []

        # =========================
        # PROCESS DETECTIONS
        # =========================

        for result in results:

            boxes = result.boxes

            if boxes is None:
                continue

            for box in boxes:

                class_id = int(box.cls[0])

                confidence = float(
                    box.conf[0]
                )

                class_name = model.names[class_id]

                # =========================
                # CLASS-SPECIFIC THRESHOLDS
                # =========================

                if class_name == "fallen_tree":

                    minimum_confidence = 0.04

                elif class_name == "water_leak":

                    minimum_confidence = 0.05

                else:

                    minimum_confidence = 0.10


                # Only keep useful detections
                if confidence >= minimum_confidence:

                    detections.append({
                        "issue_type": class_name,
                        "confidence": round(
                            confidence,
                            4
                        )
                    })


        # =========================
        # REMOVE DUPLICATE CLASSES
        # KEEP HIGHEST CONFIDENCE
        # =========================

        best_by_class = {}

        for detection in detections:

            issue_type = detection["issue_type"]

            confidence = detection["confidence"]

            if (
                issue_type not in best_by_class
                or confidence >
                best_by_class[issue_type]["confidence"]
            ):

                best_by_class[issue_type] = detection


        detections = list(
            best_by_class.values()
        )


        # =========================
        # SORT
        # =========================

        detections.sort(
            key=lambda x: x["confidence"],
            reverse=True
        )


        # =========================
        # BEST DETECTION
        # =========================

        if detections:

            best_detection = detections[0]

            return {
                "success": True,
                "detected_issue":
                    best_detection["issue_type"],
                "confidence":
                    best_detection["confidence"],
                "detections":
                    detections
            }


        # =========================
        # NO DETECTION
        # =========================

        return {
            "success": True,
            "detected_issue": None,
            "confidence": 0,
            "detections": [],
            "message":
                "No civic issue detected"
        }


    finally:

        # Delete temporary file
        if os.path.exists(temp_path):

            os.remove(temp_path)


# =========================
# CREATE REPORT
# =========================

@app.post("/reports")
def create_report(
    issue_type: str = Form(...),
    description: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # =========================
    # SAVE PHOTO
    # =========================

    file_extension = os.path.splitext(
        photo.filename
    )[1]

    unique_filename = (
        f"{uuid.uuid4()}{file_extension}"
    )

    file_path = os.path.join(
        UPLOAD_FOLDER,
        unique_filename
    )

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            photo.file,
            buffer
        )


    # =========================
    # CREATE REPORT
    # =========================

    new_report = Report(
        issue_type=issue_type,
        description=description,
        latitude=latitude,
        longitude=longitude
    )


    # =========================
    # SAVE TO DATABASE
    # =========================

    db.add(new_report)

    db.commit()

    db.refresh(new_report)


    # =========================
    # RESPONSE
    # =========================

    return {

        "message":
            "Report and photo saved successfully",

        "report": {

            "id":
                new_report.id,

            "issue_type":
                new_report.issue_type,

            "description":
                new_report.description,

            "latitude":
                new_report.latitude,

            "longitude":
                new_report.longitude,

            "photo_filename":
                unique_filename
        }
    }