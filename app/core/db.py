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
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", "1109"),
        "database": os.getenv("MYSQL_DB", "rental_app"),
    }


def get_database_url():
    """Generate sync database URL"""
    config = get_database_config()
    return (
        f"mysql+pymysql://{config['user']}:{config['password']}"
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