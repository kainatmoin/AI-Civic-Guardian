# 🚨 AI Civic Guardian

AI Civic Guardian is an AI-powered civic issue reporting platform designed to help citizens quickly report public infrastructure problems using **AI image detection, GPS location capture, and automated report generation**.

The platform aims to make civic issue reporting faster, simpler, and more structured by reducing the amount of manual information a citizen needs to provide.

---

## 🌍 Problem

Civic infrastructure problems are common in many communities and can create serious safety and accessibility issues.

Examples include:

- 🕳️ Potholes
- 🛣️ Road cracks
- 🚧 Open manholes
- 🌳 Fallen trees
- 🗑️ Garbage
- 💡 Broken streetlights
- 💧 Water leakage

Traditional complaint systems often require citizens to manually describe the issue, identify its category, and provide location information.

This can make reporting:

- Slow
- Manual
- Inconsistent
- Difficult to structure
- Difficult to analyze at scale

AI Civic Guardian addresses this problem by using AI to automatically analyze the uploaded image and assist with identifying the civic issue.

---

## 💡 Solution

AI Civic Guardian provides a simple citizen-first reporting workflow:

1. 📷 Citizen uploads a photo of the civic issue.
2. 🤖 AI analyzes the image.
3. 🔍 AI identifies the detected issue.
4. 📊 AI provides a confidence score.
5. 📍 Browser captures the citizen's GPS location.
6. 📝 Citizen adds a description.
7. 🚨 Citizen submits the report.
8. 🗄️ Backend stores the structured report in the database.

This creates a more structured and AI-assisted civic reporting process.

---

# ⭐ Key Features

## 🤖 AI-Powered Issue Detection

The system uses a fine-tuned YOLO object-detection model to analyze civic issue images.

Supported categories:

- Pothole
- Road Cracks
- Open Manhole
- Fallen Tree
- Garbage
- Broken Streetlight
- Water Leakage

The AI returns the detected issue and its confidence score.

> **Note:** The current model is an MVP. Detection performance can vary across different real-world images and categories.

---

## 📷 Photo-Based Reporting

Citizens can upload a photo of a civic issue directly from the browser.

The image is sent to the AI detection backend for analysis.

---

## 📍 GPS Location Capture

The application uses the browser's Geolocation API to capture:

- Latitude
- Longitude

The captured coordinates are attached to the civic report.

---

## 📝 Citizen Description

Citizens can provide additional details about the reported problem.

Example:

> Large pothole near the main road entrance causing a safety hazard.

---

## 🚨 Automated Report Submission

After AI analysis and GPS capture, the citizen can submit the report.

The backend stores the structured information in SQLite.

---

## 📊 AI Confidence

The application displays the AI confidence score with the detected issue.

Example:

```text
Detected Issue:
Pothole

Confidence:
65.3%
```

The confidence score helps indicate how strongly the model supports its prediction.

---

# 🧠 AI System

The project uses **transfer learning and fine-tuning** rather than training an object-detection model completely from scratch.

A pre-trained YOLO model was adapted for civic infrastructure issue detection.

The final model supports seven civic issue categories.

### AI Classes

| ID | Class |
|---|---|
| 0 | Pothole |
| 1 | Cracks |
| 2 | Open Manhole |
| 3 | Fallen Tree |
| 4 | Garbage |
| 5 | Streetlight |
| 6 | Water Leakage |

The model is integrated directly into the FastAPI backend.

---

# 🏗️ System Architecture

```text
                    CITIZEN
                       │
                       ▼
                Upload Photo
                       │
                       ▼
              AI Image Detection
                       │
                       ▼
             Detected Issue + Confidence
                       │
                       ▼
                Capture GPS
                       │
                       ▼
             Add Description
                       │
                       ▼
                Submit Report
                       │
                       ▼
               FastAPI Backend
                       │
                       ▼
                 SQLite Database
```

---

# 🔄 Application Workflow

```text
1. Open AI Civic Guardian
           ↓
2. Select civic issue photo
           ↓
3. Click "Analyze Photo with AI"
           ↓
4. AI identifies the issue
           ↓
5. Confidence score is displayed
           ↓
6. Capture GPS location
           ↓
7. Add issue description
           ↓
8. Submit report
           ↓
9. Backend stores report
```

---

# 🛠️ Technology Stack

## Frontend

- HTML5
- CSS3
- JavaScript
- Browser File API
- Browser Geolocation API

## Backend

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Python Multipart

## Artificial Intelligence

- Ultralytics YOLO
- PyTorch
- Transfer Learning
- Fine-Tuned Object Detection

## Development Tools

- Git
- GitHub
- Python Virtual Environment
- FastAPI Swagger Documentation

---

# 📁 Project Structure

```text
AI-Civic-Guardian/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
│
├── frontend/
│   └── index.html
│
├── .gitignore
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/kainatmoin/AI-Civic-Guardian.git
cd AI-Civic-Guardian
```

---

## 2. Create a Virtual Environment

Windows:

```cmd
python -m venv venv
```

Activate the environment:

```cmd
venv\Scripts\activate
```

---

## 3. Install Dependencies

```cmd
pip install fastapi uvicorn python-multipart sqlalchemy ultralytics
```

---

# ▶️ Run the Backend

Go to the backend directory:

```cmd
cd backend
```

Start FastAPI:

```cmd
python -m uvicorn main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

---

# 📖 API Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Available API endpoints include:

```text
GET  /
GET  /health
POST /detect
POST /reports
```

---

# 📷 AI Detection API

The frontend sends the uploaded image to:

```text
POST /detect
```

The AI analyzes the image and returns information similar to:

```json
{
    "success": true,
    "detected_issue": "pothole",
    "confidence": 0.6532,
    "detections": [
        {
            "issue_type": "pothole",
            "confidence": 0.6532
        }
    ]
}
```

---

# 🚨 Report API

After AI detection, GPS capture, and description entry, the frontend submits the report to:

```text
POST /reports
```

The report contains:

- Issue type
- Description
- Latitude
- Longitude
- Photo

---

# 📍 GPS Implementation

The frontend uses the browser's built-in Geolocation API.

The user must allow location permission.

The application captures:

```text
Latitude
Longitude
```

These values are sent to the FastAPI backend with the report.

---

# 📷 Photo Upload

Citizens can select a civic issue photo from their device.

The image is sent to the AI detection endpoint for analysis, and the detected issue is shown in the interface before report submission.

---

# 📝 Report Creation

After AI analysis and GPS capture, the citizen can submit a report.

A successful submission returns a report ID and stores the report information in the database.

---

# 🗄️ Database

The current MVP uses:

- SQLite
- SQLAlchemy

Each report stores structured information such as:

```text
Report ID
Issue Type
Description
Latitude
Longitude
Photo Filename
```

This provides a simple persistence layer for the MVP.

---

# 🔐 Security and Repository Hygiene

The repository uses `.gitignore` to prevent local development files from being committed.

Ignored files include:

- Environment files
- Local databases
- Uploaded images
- AI model weights
- Training outputs
- Dataset files
- Backup files
- Virtual environment files

No API keys, private credentials, or secrets should be committed to the repository.

---

# 🎯 Current MVP

The current MVP focuses on the core reporting experience.

### Implemented

- ✅ AI image analysis
- ✅ Civic issue detection
- ✅ AI confidence score
- ✅ Photo upload
- ✅ GPS location capture
- ✅ Citizen description
- ✅ Report submission
- ✅ FastAPI backend
- ✅ SQLite database
- ✅ Frontend and backend integration
- ✅ Interactive API documentation

---

# 📈 Impact

AI Civic Guardian can help communities create more structured civic issue reports.

Potential benefits include:

- Faster civic issue reporting
- Less manual classification
- Structured complaint information
- Location-aware reports
- Easier organization of civic infrastructure data
- Better foundation for future civic analytics

---

# 🚀 Future Improvements

The current project is an MVP. Future versions can expand the platform with:

## 🗺️ Public Issue Map

Display reported civic issues on an interactive map.

## 📊 Admin Dashboard

Provide authorities with:

- Total complaints
- Pending complaints
- Resolved complaints
- High-priority complaints
- Issue categories
- Location-based analytics

## 🔁 Duplicate Complaint Detection

Identify multiple reports referring to the same nearby issue and reduce duplicate complaints.

## 📍 Nearby Issue Clustering

Group civic complaints based on geographic proximity.

## 🚦 Severity Prediction

Automatically estimate whether an issue is:

- Low
- Medium
- High

## 🏢 Department Routing

Automatically route different issue types to appropriate departments.

Example:

```text
Pothole
   ↓
Road Maintenance Department
```

```text
Broken Streetlight
   ↓
Electrical / Municipal Department
```

## 🔔 Complaint Notifications

Citizens could receive notifications when the status of their report changes.

## 📱 Mobile Application

The web MVP can later be extended into Android and iOS applications.

## 📈 Historical Civic Analytics

Historical reports could be analyzed to identify:

- Frequently affected locations
- Repeated infrastructure problems
- High-risk areas
- Maintenance trends

---

# 🧪 Project Status

```text
Status: MVP Completed ✅
```

Core workflow:

```text
Photo
   ↓
AI Detection
   ↓
Issue + Confidence
   ↓
GPS
   ↓
Description
   ↓
Report Submission
   ↓
Database
```

The current model is designed as an MVP and detection performance can vary between civic issue categories and real-world images.

---

# 🌟 Why AI Civic Guardian?

AI Civic Guardian combines three important pieces into a single reporting workflow:

```text
AI Vision
   +
GPS Location
   +
Structured Reporting
```

Instead of asking citizens to manually identify and categorize every civic problem, the platform uses AI to assist with identification while automatically attaching the geographic location.

---

# 🌍 Vision

The long-term vision of AI Civic Guardian is to create a scalable AI-assisted civic reporting platform that can help communities and municipal authorities understand infrastructure problems more efficiently.

The platform can evolve from a simple reporting tool into a complete civic intelligence system.

---

# 🔗 Project Repository

GitHub:

https://github.com/kainatmoin/AI-Civic-Guardian

---

# 🏆 Hackathon

Built for:

**Alibaba Cloud AI Hackathon Pakistan 2026**

Project:

**AI Civic Guardian**

---

# 👩‍💻 Project Team

**AI Civic Guardian**

AI-powered civic issue reporting for safer and smarter communities.

---

## 📌 Summary

AI Civic Guardian provides a simple workflow:

```text
📷 Take / Upload Photo
        ↓
🤖 AI Detects Issue
        ↓
📊 Confidence Score
        ↓
📍 Capture GPS
        ↓
📝 Add Description
        ↓
🚨 Submit Report
        ↓
🗄️ Store in Database
```

**AI Civic Guardian — Making civic reporting smarter, faster, and more structured.**
