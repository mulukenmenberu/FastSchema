"""
Configuration management for the API generator
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Database connection settings
    db_type: Optional[str] = None  # mysql, postgresql, mongodb, sqlite
    db_host: Optional[str] = None
    db_port: Optional[int] = None
    db_name: Optional[str] = None
    db_user: Optional[str] = None
    db_password: Optional[str] = None
    db_uri: Optional[str] = None  # For MongoDB or full connection strings
    
    # SQLite specific
    sqlite_path: Optional[str] = None
    
    # API settings
    api_title: str = "Schemaless API Generator"
    api_version: str = "1.0.0"
    api_prefix: str = "/api"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

