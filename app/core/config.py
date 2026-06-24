import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GITHUB_PAT = os.getenv("GITHUB_PAT")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATASET_DIR = BASE_DIR / "Dataset"

# File paths
INSTITUTE_MASTER_PATH = DATASET_DIR / "INSTITUTE_MASTER.csv"
FACTOR_MASTER_PATH = DATASET_DIR / "FACTOR_MASTER.csv"
PROFILE_SCORING_ENGINE_PATH = DATASET_DIR / "PROFILE_SCORING_ENGINE.csv"
KNOWLEDGE_BASE_PATH = DATASET_DIR / "CHATBOT_KNOWLEDGE_BASE.json"
BENCHMARK_PATH = DATASET_DIR / "mba_admissions_benchmark_reconstruction_v4.xlsx"
