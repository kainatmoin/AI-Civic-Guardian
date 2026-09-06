import os
import sqlite3
import uuid
from pathlib import Path

import streamlit as st
from PIL import Image
from ultralytics import YOLO
from streamlit_js_eval import get_geolocation


# =========================================================
# APP CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Civic Guardian",
    page_icon="🚨",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# =========================================================
# PATHS
# =========================================================

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
MODEL_PATH = BACKEND_DIR / "models" / "civic_guardian.pt"
UPLOAD_DIR = BACKEND_DIR / "uploads"
DB_PATH = BACKEND_DIR / "civic_guardian.db"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# CUSTOM STYLING
# =========================================================

st.markdown(
    """
    <style>
        .stApp {
            background: #0b0d08;
            color: #e8eadf;
        }

        .block-container {
            max-width: 700px;
            padding-top: 2.5rem;
            padding-bottom: 3rem;
        }

        h1 {
            color: #a8b86b !important;
            text-align: center;
            font-size: 38px !important;
            margin-bottom: 6px !important;
        }

        .subtitle {
            color: #9da18f;
            text-align: center;
            font-size: 16px;
            margin-bottom: 30px;
        }

        .card {
            background: #151810;
            border: 1px solid #303622;
            border-radius: 15px;
            padding: 22px;
            margin: 0 0 18px 0;
        }

        .card-title {
            color: #cbd39c;
            font-weight: 700;
            margin-bottom: 12px;
            font-size: 1rem;
        }

        .ai-result {
            background: #202618;
            border: 1px solid #65752f;
            border-radius: 10px;
            padding: 18px;
            margin-top: 15px;
        }

        .detected {
            color: #ffffff;
            font-size: 24px;
            font-weight: 700;
            margin: 6px 0;
        }

        .confidence {
            color: #b9bea9;
        }

        .note {
            color: #858a77;
            font-size: 13px;
            margin-top: 8px;
        }

        .success-box {
            background: #202618;
            border: 1px solid #65752f;
            color: #b9d66d;
            padding: 14px;
            border-radius: 8px;
            margin-top: 15px;
        }

        .error-box {
            background: #241616;
            border: 1px solid #814545;
            color: #e8a0a0;
            padding: 14px;
            border-radius: 8px;
            margin-top: 15px;
        }

        div[data-testid="stFileUploaderDropzone"] {
            background: #0d100b;
            border: 1px solid #3a4229;
        }

        div[data-testid="stTextArea"] textarea {
            background: #0d100b !important;
            color: #ffffff !important;
            border: 1px solid #3a4229 !important;
        }

        div[data-testid="stButton"] button {
            width: 100%;
            border-radius: 8px;
            min-height: 46px;
            font-weight: 700;
        }

        iframe[title^="streamlit_js_eval"] {
            display: none !important;
        }

        .stButton > button:first-child {
            background: #65752f;
            color: white;
            border: none;
        }

        .stButton > button:hover {
            border-color: #a8b86b;
            color: white;
        }

        .location-value {
            background: #0d100b;
            border: 1px solid #303622;
            border-radius: 8px;
            padding: 12px;
            color: #aeb39d;
            margin-top: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DATABASE
# =========================================================

def init_db():
    BACKEND_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                issue_type TEXT NOT NULL,
                description TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                photo_filename TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # Migrate the existing SQLite database created by the original
        # FastAPI app without deleting any existing reports.
        columns = {
            row[1]
            for row in conn.execute("PRAGMA table_info(reports)").fetchall()
        }

        if "photo_filename" not in columns:
            conn.execute(
                "ALTER TABLE reports ADD COLUMN photo_filename TEXT"
            )

        if "created_at" not in columns:
            conn.execute(
                "ALTER TABLE reports ADD COLUMN created_at TEXT"
            )

        conn.commit()


def save_report(issue_type, description, latitude, longitude, photo_bytes, extension):
    filename = f"{uuid.uuid4()}{extension}"
    photo_path = UPLOAD_DIR / filename

    with open(photo_path, "wb") as file:
        file.write(photo_bytes)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            INSERT INTO reports
                (issue_type, description, latitude, longitude, photo_filename)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                issue_type,
                description,
                float(latitude),
                float(longitude),
                filename,
            ),
        )
        conn.commit()
        return cursor.lastrowid, filename


init_db()


# =========================================================
# AI MODEL
# =========================================================

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )
    return YOLO(str(MODEL_PATH))


ISSUE_NAMES = {
    "pothole": "Pothole",
    "cracks": "Road Cracks",
    "open_manhole": "Open Manhole",
    "fallen_tree": "Fallen Tree",
    "garbage": "Garbage",
    "streetlight": "Broken Streetlight",
    "water_leak": "Water Leakage",
}


def analyze_image(image_path):
    model = load_model()

    results = model.predict(
        source=str(image_path),
        imgsz=640,
        conf=0.10,
        augment=False,
        verbose=False,
    )

    detections = []

    for result in results:
        boxes = result.boxes

        if boxes is None:
            continue

        for box in boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            class_name = str(model.names[class_id])

            if class_name == "fallen_tree":
                minimum_confidence = 0.04
            elif class_name == "water_leak":
                minimum_confidence = 0.05
            else:
                minimum_confidence = 0.10

            if confidence >= minimum_confidence:
                detections.append(
                    {
                        "issue_type": class_name,
                        "confidence": round(confidence, 4),
                    }
                )

    best_by_class = {}

    for detection in detections:
        issue_type = detection["issue_type"]
        confidence = detection["confidence"]

        if (
            issue_type not in best_by_class
            or confidence > best_by_class[issue_type]["confidence"]
        ):
            best_by_class[issue_type] = detection

    detections = sorted(
        best_by_class.values(),
        key=lambda item: item["confidence"],
        reverse=True,
    )

    return detections


# =========================================================
# SESSION STATE
# =========================================================

# Initialize every state key before first access.
_state_defaults = {
    "detected_issue": None,
    "confidence": 0.0,
    "latitude": None,
    "longitude": None,
    "location_error": None,
    "report_message": None,
}

for _key, _default in _state_defaults.items():
    if _key not in st.session_state:
        st.session_state[_key] = _default


# =========================================================
# HEADER
# =========================================================

st.markdown(
    "<h1>AI Civic Guardian</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">Report civic issues with AI-powered detection</div>',
    unsafe_allow_html=True,
)


# =========================================================
# PHOTO + AI
# =========================================================

st.markdown(
    '<div class="card-title">📷 Upload Civic Issue Photo <span class="required">*</span></div>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="collapsed",
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, use_container_width=True)

    if st.button(
        "🤖 Analyze Photo with AI",
        use_container_width=True,
        key="analyze_photo_button",
    ):
        suffix = Path(uploaded_file.name).suffix.lower() or ".jpg"
        temp_path = UPLOAD_DIR / f"temp_{uuid.uuid4()}{suffix}"

        try:
            with open(temp_path, "wb") as file:
                file.write(uploaded_file.getbuffer())

            with st.spinner("🤖 Analyzing..."):
                detections = analyze_image(temp_path)

            if detections:
                best = detections[0]
                st.session_state.detected_issue = best["issue_type"]
                st.session_state.confidence = best["confidence"]
            else:
                st.session_state.detected_issue = None
                st.session_state.confidence = 0.0
                st.warning(
                    "AI could not detect a supported civic issue. Try another clearer photo."
                )

        except Exception as error:
            st.session_state.detected_issue = None
            st.session_state.confidence = 0.0
            st.error(f"AI detection failed: {error}")

        finally:
            if temp_path.exists():
                temp_path.unlink()

if st.session_state.detected_issue:
    display_name = ISSUE_NAMES.get(
        st.session_state.detected_issue,
        st.session_state.detected_issue,
    )

    st.markdown(
        f"""
        <div class="ai-result">
            <div class="ai-title">🤖 AI Detection Result</div>
            <div class="detected">{display_name}</div>
            <div class="confidence">Confidence: {st.session_state.confidence * 100:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="note">AI can detect potholes, cracks, open manholes, fallen trees, garbage, streetlights and water leaks.</div>',
    unsafe_allow_html=True,
)


# =========================================================
# DESCRIPTION
# =========================================================

st.markdown(
    '<div class="card-title">📝 Description <span class="required">*</span></div>',
    unsafe_allow_html=True,
)

description = st.text_area(
    "Describe the issue",
    placeholder="Describe the issue or add any useful details...",
    height=120,
    label_visibility="collapsed",
)


# =========================================================
# GPS LOCATION
# =========================================================

st.markdown(
    '<div class="card-title">📍 Location <span class="required">*</span></div>',
    unsafe_allow_html=True,
)

# Location is requested only after the user clicks the button.
if "request_location" not in st.session_state:
    st.session_state.request_location = False

if st.button(
    "📍 Capture My Location",
    use_container_width=True,
    key="capture_location_button",
):
    st.session_state.request_location = True

location_data = None

if st.session_state.request_location and (
    st.session_state.latitude is None
    or st.session_state.longitude is None
):
    # The hidden component asks the browser for permission and returns coords.
    location_data = get_geolocation()

if location_data and "error" not in location_data:
    coords = location_data.get("coords", {})
    lat = coords.get("latitude")
    lon = coords.get("longitude")

    if lat is not None and lon is not None:
        st.session_state.latitude = float(lat)
        st.session_state.longitude = float(lon)
        st.session_state.location_error = None
        st.session_state.request_location = False

elif location_data and "error" in location_data:
    error = location_data["error"]
    st.session_state.location_error = (
        f"Location error: {error.get('message', 'Unable to get location.')}"
    )
    st.session_state.request_location = False

latitude = st.session_state.latitude
longitude = st.session_state.longitude

if latitude is not None and longitude is not None:
    st.markdown(
        f"""
        <div class="gps-status">
            ✅ Location captured:<br>
            {latitude:.6f}, {longitude:.6f}
        </div>
        """,
        unsafe_allow_html=True,
    )
elif st.session_state.location_error:
    st.markdown(
        f"""
        <div class="error-box">
            ❌ {st.session_state.location_error}
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<div class="gps-status">Location not captured yet.</div>',
        unsafe_allow_html=True,
    )


# =========================================================
# SUBMIT REPORT
# =========================================================

if st.button(
    "🚨 Submit Report",
    use_container_width=True,
    key="submit_report_button",
):
    if not st.session_state.detected_issue:
        st.error("Please upload a photo and analyze it with AI first.")

    elif not description.strip():
        st.error("Please enter a description.")

    elif uploaded_file is None:
        st.error("Please select a photo.")

    elif latitude is None or longitude is None:
        st.error("Please capture your location first.")

    else:
        try:
            extension = Path(uploaded_file.name).suffix.lower() or ".jpg"

            report_id, filename = save_report(
                issue_type=st.session_state.detected_issue,
                description=description.strip(),
                latitude=latitude,
                longitude=longitude,
                photo_bytes=uploaded_file.getbuffer(),
                extension=extension,
            )

            st.success(
                f"✅ Report submitted successfully! Report ID: {report_id}"
            )

            st.session_state.detected_issue = None
            st.session_state.confidence = 0.0
            st.session_state.latitude = None
            st.session_state.longitude = None
            st.session_state.location_error = None
            st.session_state.request_location = False

        except Exception as error:
            st.error(f"❌ Could not submit the report: {error}")


# FOOTER
# =========================================================

st.markdown(
    """
    <div style="text-align:center;color:#707563;font-size:12px;margin-top:20px;">
        AI Civic Guardian • AI-powered civic issue reporting
    </div>
    """,
    unsafe_allow_html=True,
)
