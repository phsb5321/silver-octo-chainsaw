# app/config.py
"""This module holds application-wide configurations."""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration settings."""

    API_KEY = os.getenv("API_KEY")
    BASE_URL = "https://serpapi.com/search.json"
    DATABASE_URI = os.getenv("DATABASE_URI")
