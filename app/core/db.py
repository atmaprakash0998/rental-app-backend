import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Load environment variables
load_dotenv()

# Create declarative base
Base = declarative_base()

def get_database_config():
    """Get database configuration from environment variables"""
    return {
        "host": os.getenv("POSTGRES_HOST", ""),
        "port": int(os.getenv("POSTGRES_PORT", "")),
        "user": os.getenv("POSTGRES_USER", ""),
        "password": os.getenv("POSTGRES_PASSWORD", ""),
        "database": os.getenv("POSTGRES_DB", ""),
    }


def get_database_url():
    """Generate sync database URL"""
    config = get_database_config()
    return (
        f"postgresql+psycopg://{config['user']}:{config['password']}"
        f"@{config['host']}:{config['port']}/{config['database']}"
    )


def create_database_engine():
    """Create sync database engine"""
    return create_engine(
        get_database_url(),
        echo=False,
        pool_pre_ping=True,
    )

def create_session_local():
    """Create sync session local"""
    return sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )


# Create engine instances
engine = create_database_engine()

# Create session locals
SessionLocal = create_session_local()


def get_db_session():
    """Dependency to get sync database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()