# 🚨 AI Civic Guardian

AI Civic Guardian is an AI-powered civic issue reporting platform designed to help citizens quickly report public infrastructure problems using **AI image detection, GPS location capture, and structured report submission**.

The platform makes civic issue reporting faster, simpler, and more structured by using computer vision to assist with identifying civic problems while capturing the user's location and description.

---

## 🌐 Live Demo

### 🚨 AI Civic Guardian — Live Application

**https://ai-civic-guardian-kryjzuyolzphxv7feqhxy4.streamlit.app/**

### 💻 GitHub Repository

**https://github.com/kainatmoin/AI-Civic-Guardian**

---

# 🌍 Problem

Civic infrastructure problems are common in many communities and can create serious safety, accessibility, and environmental concerns.

Examples include:

- 🕳️ Potholes
- 🛣️ Road cracks
- 🚧 Open manholes
- 🌳 Fallen trees
- 🗑️ Garbage
- 💡 Broken streetlights
- 💧 Water leakage

Traditional complaint systems often require citizens to manually identify the issue, describe the problem, choose a category, and provide location information.

This can make reporting:

- Slow
- Manual
- Inconsistent
- Difficult to structure
- Difficult to analyze at scale

AI Civic Guardian addresses this problem by using AI-powered image detection to assist citizens in identifying civic infrastructure issues.

---

# 💡 Solution

AI Civic Guardian provides a simple citizen-first reporting workflow:

1. 📷 Citizen uploads a photo of the civic issue.
2. 🤖 AI analyzes the image using a fine-tuned YOLO model.
3. 🔍 The AI identifies the detected civic issue.
4. 📊 The application displays the confidence score.
5. 📍 The user clicks **Capture My Location** to obtain GPS coordinates.
6. 📝 The citizen adds a description.
7. 🚨 The citizen submits the report.
8. 🆔 The system generates a report ID.
9. 🗄️ Report information is stored in the application's database layer.

This creates a structured and AI-assisted civic reporting experience.

---

# ⭐ Key Features

## 🤖 AI-Powered Issue Detection

The application uses a fine-tuned YOLO object-detection model for civic issue recognition.

Supported categories:

- Pothole
- Road Cracks
- Open Manhole
- Fallen Tree
- Garbage
- Broken Streetlight
- Water Leakage

The system displays:

- Detected issue
- AI confidence score

> **Note:** The current model is an MVP. Detection performance can vary depending on image quality, lighting, viewpoint, and civic issue category.

---

## 📷 Photo-Based Reporting

Citizens can upload a civic issue image directly from the web application.

Supported image formats include:

- JPG
- JPEG
- PNG
- WEBP

The uploaded image is analyzed by the AI model before report submission.

---

## 📍 GPS Location Capture

The application uses browser-based geolocation to capture:

- Latitude
- Longitude

Location capture is **user-triggered** through:

```text
📍 Capture My Location
```

The browser requests location permission before providing the coordinates.

---

## 📝 Citizen Description

Citizens can provide additional details about the reported problem.

Example:

> A large pothole near the main road entrance is creating a safety hazard for vehicles and pedestrians.

---

## 🚨 Report Submission

A report can be submitted after:

- AI analysis
- Description entry
- GPS location capture

The system generates a report ID after successful submission.

---

## 📊 AI Confidence

The application displays the AI confidence associated with the detected issue.

Example:

```text
Detected Issue:
Pothole

Confidence:
65.3%
```

The confidence score indicates how strongly the model supports its prediction.

---

# 🧠 AI System

The project uses **transfer learning and fine-tuning** rather than training an object-detection model completely from scratch.

A pre-trained YOLO model was adapted for civic infrastructure issue detection.

The final model supports seven civic issue categories.

## AI Classes

| ID | Class |
|---|---|
| 0 | Pothole |
| 1 | Cracks |
| 2 | Open Manhole |
| 3 | Fallen Tree |
| 4 | Garbage |
| 5 | Streetlight |
| 6 | Water Leakage |

The trained model is loaded by the Streamlit application during inference.

---

# 🏗️ System Architecture

```text
                         CITIZEN
                            │
                            ▼
                    Streamlit Web App
                            │
           ┌────────────────┼────────────────┐
           │                │                │
           ▼                ▼                ▼
      Upload Photo     Capture GPS     Add Description
           │                │                │
           ▼                │                │
        YOLO AI              │                │
           │                │                │
           ▼                │                │
 Issue + Confidence          │                │
           └────────────────┼────────────────┘
                            ▼
                     Submit Report
                            │
                            ▼
                  Generate Report ID
                            │
                            ▼
                    SQLite Storage
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
6. Click "Capture My Location"
           ↓
7. Allow browser location permission
           ↓
8. Add issue description
           ↓
9. Click "Submit Report"
           ↓
10. Receive Report ID
```

---

# 🛠️ Technology Stack

## Application

- Python
- Streamlit
- Streamlit JavaScript evaluation utilities

## Artificial Intelligence

- Ultralytics YOLO
- PyTorch
- Transfer Learning
- Fine-Tuned Object Detection

## Computer Vision

- OpenCV
- Pillow

## Data Storage

- SQLite
- Python `sqlite3`

## Development & Deployment

- Git
- GitHub
- Python Virtual Environment
- Streamlit Community Cloud

---

# 📁 Project Structure

```text
AI-Civic-Guardian/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── models/
│   │   └── civic_guardian.pt
│   └── uploads/
│
├── frontend/
│   └── index.html
│
├── api/
│   └── index.py
│
├── streamlit_app.py
├── requirements.txt
├── vercel.json
├── .gitignore
└── README.md
```

> The repository contains the original FastAPI/HTML implementation alongside the current Streamlit application used for the live demo.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/kainatmoin/AI-Civic-Guardian.git
cd AI-Civic-Guardian
```

---

## 2. Create a Virtual Environment

### Windows

```cmd
python -m venv venv
```

Activate:

```cmd
venv\Scripts\activate
```

---

## 3. Install Dependencies

```cmd
pip install -r requirements.txt
```

---

# ▶️ Run the Application

From the project root:

```cmd
streamlit run streamlit_app.py
```

The application will open at:

```text
http://localhost:8501
```

---

# 🧪 Local Testing

Recommended testing flow:

```text
Upload civic issue image
        ↓
Analyze Photo with AI
        ↓
Verify detected issue
        ↓
Verify confidence score
        ↓
Capture My Location
        ↓
Verify latitude + longitude
        ↓
Enter description
        ↓
Submit Report
        ↓
Verify Report ID
```

---

# 📷 AI Detection

The application accepts common image formats such as:

- JPG
- JPEG
- PNG
- WEBP

The YOLO model analyzes the uploaded image and identifies supported civic issues.

Example result:

```json
{
  "success": true,
  "detected_issue": "pothole",
  "confidence": 0.6532
}
```

The Streamlit interface converts the model output into a citizen-friendly result.

---

# 📍 GPS Implementation

The application uses browser-based geolocation.

The user explicitly clicks:

```text
📍 Capture My Location
```

The browser then requests location permission.

When successful, the application displays:

```text
Latitude
Longitude
```

These coordinates are attached to the report.

> Location availability depends on browser permission and device location capabilities.

---

# 🚨 Report Submission

A report combines the main information collected during the reporting workflow:

```text
Report ID
Issue Type
Description
Latitude
Longitude
Photo Filename
Created At
```

After successful submission, the application displays the generated report ID.

---

# 🗄️ Database

The MVP uses SQLite for lightweight report storage.

The database provides a simple persistence layer for the prototype.

For a larger production deployment, the database can later be migrated to a managed cloud database.

---

# 🔐 Security and Repository Hygiene

The repository uses `.gitignore` to reduce accidental commits of development-only files.

Typical ignored content includes:

- Environment files
- Local databases
- Uploaded images
- Training outputs
- Dataset files
- Virtual environments
- Temporary files

No API keys, private credentials, or secrets should be committed to the repository.

> Model weights required by the current demo are included so the deployed Streamlit application can load the AI model.

---

# 🎯 Current MVP

The current MVP implements the core civic reporting experience:

- ✅ AI image analysis
- ✅ Civic issue detection
- ✅ AI confidence score
- ✅ Photo upload
- ✅ User-triggered GPS location capture
- ✅ Citizen description
- ✅ Report submission
- ✅ Report ID generation
- ✅ Streamlit web application
- ✅ SQLite report storage
- ✅ GitHub repository
- ✅ Live Streamlit deployment

---

# 📈 Impact

AI Civic Guardian can help communities create more structured civic issue reports.

Potential benefits include:

- Faster civic issue reporting
- Reduced manual classification
- More structured complaint information
- Location-aware reporting
- Easier organization of civic infrastructure data
- A foundation for future civic analytics

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

Automatically route different issue types to the appropriate department.

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
Live Demo: Available ✅
```

Core workflow:

```text
Photo
   ↓
AI Detection
   ↓
Issue + Confidence
   ↓
GPS Capture
   ↓
Description
   ↓
Report Submission
   ↓
Report ID
```

The current model is designed as an MVP and detection performance can vary across civic issue categories and real-world images.

---

# 🌟 Why AI Civic Guardian?

AI Civic Guardian combines three important capabilities into a single reporting workflow:

```text
AI Vision
   +
GPS Location
   +
Structured Reporting
```

Instead of asking citizens to manually identify and categorize every civic problem, the platform uses AI to assist with issue identification while allowing the citizen to attach a precise location and description.

---

# 🌍 Vision

The long-term vision of AI Civic Guardian is to create a scalable AI-assisted civic reporting platform that helps communities and municipal authorities understand infrastructure problems more efficiently.

The platform can evolve from a simple reporting tool into a broader civic intelligence system.

---

# 🏆 Hackathon

Built for:

**Alibaba Cloud AI Hackathon Pakistan 2026**

Project:

**AI Civic Guardian**

---

# 👩‍💻 Project Team

**AI Civic Guardian**

## 👥 Team Members

- Kainat Moin
- Hafsa Naz
- Saira Jabeen

---

# 🔗 Links

### 🚨 Live Demo

https://ai-civic-guardian-kryjzuyolzphxv7feqhxy4.streamlit.app/

### 💻 GitHub Repository

https://github.com/kainatmoin/AI-Civic-Guardian

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
🆔 Receive Report ID
```

**AI Civic Guardian — Making civic reporting smarter, faster, and more structured.**
