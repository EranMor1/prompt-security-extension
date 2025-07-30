# Configuration file for server settings and API keys

import os

API_URL = os.getenv("PROMPT_API_URL", "https://eu.prompt.security/api/protect")
APP_ID = os.getenv("PROMPT_APP_ID", "cc6a6cfc-9570-4e5a-b6ea-92d2adac90e4")
DEBUG = os.getenv("FLASK_DEBUG", "True") == "True"
