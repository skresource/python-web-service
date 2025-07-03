import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration Details"""
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    JIRA_SERVER = os.getenv("JIRA_SERVER")
    JIRA_USERNAME = os.getenv("JIRA_USERNAME")
    JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")