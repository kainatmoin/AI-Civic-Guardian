import os
import sys

from fastapi import FastAPI

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from main import app as backend_app

app = FastAPI(title="AI Civic Guardian API")

app.mount("/api", backend_app)