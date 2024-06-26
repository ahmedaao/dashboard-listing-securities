"""Load environmlent variables from .env"""

import os
from dotenv import load_dotenv


# Load environment variables from the .env file
load_dotenv()

# Access environment variables
ROOT_DIR = os.getenv("ROOT_DIR")
DB_FILE = os.getenv("DB_FILE")
