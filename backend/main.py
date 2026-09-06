from fastapi import FastAPI, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from ultralytics import YOLO
import os
import shutil
import uuid

from database import SessionLocal, engine, Base
from models import Report


# =========================================================
# BASE DIRECTORY
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# =========================================================
# DATABASE
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="AI Civic Guardian API",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# AI MODEL
# =========================================================

# Model can be overridden using an environment variable.
# Default location is backend/models/civic_guardian.pt
MODEL_PATH = os.getenv(
    "MODEL_PATH",
    os.path.join(
        BASE_DIR,
        "models",
        "civic_guardian.pt"
    )
)


# Check model file before loading
if not os.path.exists(MODEL_PATH):

    raise FileNotFoundError(
        f"AI model not found at: {MODEL_PATH}"
    )


model = YOLO(MODEL_PATH)


# =========================================================
# UPLOAD FOLDER
# =========================================================

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =========================================================
# DATABASE SESSION
# =========================================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# =========================================================
# BASIC ROUTES
# =========================================================

@app.get("/")
def root():

    return {
        "message": "AI Civic Guardian API is running",
        "status": "success"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model": "loaded"
    }


# =========================================================
# AI DETECTION
# =========================================================

@app.post("/detect")
def detect_issue(
    photo: UploadFile = File(...)
):

    # -----------------------------------------------------
    # CREATE TEMPORARY FILE
    # -----------------------------------------------------

    file_extension = os.path.splitext(
        photo.filename or ""
    )[1]

    if not file_extension:

        file_extension = ".jpg"


    temp_filename = (
        f"{uuid.uuid4()}{file_extension}"
    )


    temp_path = os.path.join(
        UPLOAD_FOLDER,
        temp_filename
    )


    # -----------------------------------------------------
    # SAVE UPLOADED IMAGE
    # -----------------------------------------------------

    with open(
        temp_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            photo.file,
            buffer
        )


    try:

        # =================================================
        # AI INFERENCE
        # =================================================

        results = model.predict(
            source=temp_path,
            imgsz=1024,
            conf=0.001,
            augment=True,
            verbose=False
        )


        detections = []


        # =================================================
        # PROCESS DETECTIONS
        # =================================================

        for result in results:

            boxes = result.boxes


            if boxes is None:

                continue


            for box in boxes:

                class_id = int(
                    box.cls[0]
                )


                confidence = float(
                    box.conf[0]
                )


                class_name = model.names[
                    class_id
                ]


                # -----------------------------------------
                # CLASS-SPECIFIC THRESHOLDS
                # -----------------------------------------

                if class_name == "fallen_tree":

                    minimum_confidence = 0.04

                elif class_name == "water_leak":

                    minimum_confidence = 0.05

                else:

                    minimum_confidence = 0.10


                # -----------------------------------------
                # KEEP ONLY ACCEPTED DETECTIONS
                # -----------------------------------------

                if confidence >= minimum_confidence:

                    detections.append(
                        {
                            "issue_type": class_name,
                            "confidence": round(
                                confidence,
                                4
                            )
                        }
                    )


        # =================================================
        # KEEP HIGHEST CONFIDENCE PER CLASS
        # =================================================

        best_by_class = {}


        for detection in detections:

            issue_type = detection[
                "issue_type"
            ]

            confidence = detection[
                "confidence"
            ]


            if (
                issue_type not in best_by_class
                or confidence >
                best_by_class[
                    issue_type
                ]["confidence"]
            ):

                best_by_class[
                    issue_type
                ] = detection


        detections = list(
            best_by_class.values()
        )


        # =================================================
        # SORT BY CONFIDENCE
        # =================================================

        detections.sort(
            key=lambda x: x["confidence"],
            reverse=True
        )


        # =================================================
        # BEST DETECTION
        # =================================================

        if detections:

            best_detection = detections[0]


            return {
                "success": True,

                "detected_issue":
                    best_detection[
                        "issue_type"
                    ],

                "confidence":
                    best_detection[
                        "confidence"
                    ],

                "detections":
                    detections
            }


        # =================================================
        # NO DETECTION
        # =================================================

        return {

            "success": True,

            "detected_issue": None,

            "confidence": 0,

            "detections": [],

            "message":
                "No civic issue detected"
        }


    finally:

        # =================================================
        # DELETE TEMPORARY IMAGE
        # =================================================

        if os.path.exists(temp_path):

            os.remove(temp_path)


# =========================================================
# CREATE REPORT
# =========================================================

@app.post("/reports")
def create_report(

    issue_type: str = Form(...),

    description: str = Form(...),

    latitude: float = Form(...),

    longitude: float = Form(...),

    photo: UploadFile = File(...),

    db: Session = Depends(get_db)

):

    # =====================================================
    # PHOTO FILE NAME
    # =====================================================

    file_extension = os.path.splitext(
        photo.filename or ""
    )[1]


    if not file_extension:

        file_extension = ".jpg"


    unique_filename = (
        f"{uuid.uuid4()}{file_extension}"
    )


    file_path = os.path.join(
        UPLOAD_FOLDER,
        unique_filename
    )


    # =====================================================
    # SAVE PHOTO
    # =====================================================

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            photo.file,
            buffer
        )


    # =====================================================
    # CREATE DATABASE REPORT
    # =====================================================

    new_report = Report(

        issue_type=issue_type,

        description=description,

        latitude=latitude,

        longitude=longitude

    )


    # =====================================================
    # SAVE REPORT
    # =====================================================

    db.add(new_report)

    db.commit()

    db.refresh(new_report)


    # =====================================================
    # RESPONSE
    # =====================================================

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