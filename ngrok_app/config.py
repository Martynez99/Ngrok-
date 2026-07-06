"""Configuration management for Ngrok application."""

import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Config(BaseSettings):
    """Application configuration."""

    ngrok_authtoken: str = os.getenv("NGROK_AUTHTOKEN", "")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    api_port: int = int(os.getenv("API_PORT", 5000))
    local_service_port: int = int(os.getenv("LOCAL_SERVICE_PORT", 8000))
    debug: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = False


config = Config()