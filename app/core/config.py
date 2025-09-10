import os
from typing import Optional


class Settings:
    def __init__(self):
        self.database_url: str = self._get_database_url()
        self.database_url_sync: str = self._get_database_url_sync()
        self.secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
        self.algorithm: str = os.getenv("ALGORITHM", "HS256")
        self.access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    def _get_database_url(self) -> str:
        """Get async database URL from environment variables"""
        db_user = os.getenv("DB_USER", "root")
        db_password = os.getenv("DB_PASSWORD", "1109")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "3306")
        db_name = os.getenv("DB_NAME", "rental_app")
        
        return f"mysql+aiomysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    def _get_database_url_sync(self) -> str:
        """Get sync database URL from environment variables"""
        db_user = os.getenv("DB_USER", "root")
        db_password = os.getenv("DB_PASSWORD", "1109")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "3306")
        db_name = os.getenv("DB_NAME", "rental_app")
        
        return f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def get_settings() -> Settings:
    """Get application settings"""
    return Settings()
