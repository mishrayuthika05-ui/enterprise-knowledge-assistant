import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Enterprise Knowledge Assistant")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")