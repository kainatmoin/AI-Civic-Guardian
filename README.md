# AI Civic Guardian

AI Civic Guardian is an AI-powered civic issue reporting platform designed to help citizens report public infrastructure problems quickly and efficiently.

## 🚨 Problem

Civic issues such as potholes, damaged roads, garbage, open manholes, fallen trees, broken streetlights, and water leakage can create serious safety problems.

Traditional complaint systems often require manual descriptions and do not provide structured information about the reported issue.

## 💡 Solution

AI Civic Guardian allows a citizen to:

1. Upload a photo of a civic issue.
2. Let AI analyze the image.
3. Automatically identify the detected issue.
4. Capture the user's GPS location.
5. Add a description.
6. Submit the report.
7. Store the report in the backend database.

## 🤖 AI Detection

The system uses a fine-tuned YOLO object-detection model.

Supported civic issue categories:

- Pothole
- Road Cracks
- Open Manhole
- Fallen Tree
- Garbage
- Broken Streetlight
- Water Leakage

The AI returns the detected issue and confidence score.

## 🏗️ System Architecture

```text
Citizen
   ↓
Upload Photo
   ↓
AI Image Detection
   ↓
Detected Issue + Confidence
   ↓
GPS Location
   ↓
User Description
   ↓
Submit Report
   ↓
FastAPI Backend
   ↓
SQLite Database