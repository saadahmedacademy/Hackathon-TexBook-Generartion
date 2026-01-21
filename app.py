import sys
import os

# Ensure src is on PYTHONPATH
sys.path.append(os.path.abspath("src"))

from backend.main import app  # <-- imports your FastAPI app
