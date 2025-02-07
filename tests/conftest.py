import sys
import os

# # Ensure the root directory is in the sys path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ.setdefault("AFRICASTALKING_API_KEY", "dummy_api_key")
