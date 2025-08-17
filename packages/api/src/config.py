"""
Configuration management for Mindscribe API.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional, Any
import os


class Settings(BaseSettings):
    """Application settings with environment-specific configurations."""

    # Application
    environment: str = "development"
    app_name: str = "Mindscribe API"
    version: str = "1.0.0"

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"

    # Database
    database_url: str = ""
    database_test_url: Optional[str] = None

    # Security
    secret_key: str = ""
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:8080"

    # AWS
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-west-2"
    aws_secrets_manager_secret_name: Optional[str] = None

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # AI/ML
    openai_api_key: Optional[str] = None
    ai_model_version: str = "gpt-4"

    # File Storage
    upload_path: str = "/tmp/uploads"
    max_file_size_mb: int = 100

    # Email
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None

    # Notifications
    enable_email_notifications: bool = True
    enable_push_notifications: bool = False

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
    }

    @property
    def cors_origins(self) -> List[str]:
        """Get CORS origins as a list."""
        return [x.strip() for x in self.allowed_origins.split(",")]


class DevelopmentSettings(Settings):
    """Development environment settings."""

    environment: str = "development"
    log_level: str = "DEBUG"


class TestingSettings(Settings):
    """Testing environment settings."""

    environment: str = "testing"
    log_level: str = "DEBUG"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if self.database_test_url:
            self.database_url = self.database_test_url


class ProductionSettings(Settings):
    """Production environment settings."""

    environment: str = "production"
    log_level: str = "WARNING"
    log_format: str = "json"


def get_settings() -> Settings:
    """Get settings based on environment."""
    env = os.getenv("ENVIRONMENT", "development").lower()

    if env == "development":
        return DevelopmentSettings()
    elif env == "testing":
        return TestingSettings()
    elif env == "production":
        return ProductionSettings()
    else:
        return Settings()


# Global settings instance
settings = get_settings()
