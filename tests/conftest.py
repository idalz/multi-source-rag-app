import os
import sys
from dotenv import load_dotenv

# Load .env file from the root directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
