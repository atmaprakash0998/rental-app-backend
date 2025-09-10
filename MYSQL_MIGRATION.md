# MySQL Migration Guide

This document outlines the changes made to migrate from PostgreSQL to MySQL.

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```bash
# MySQL Database Configuration
DB_USER=root
DB_PASSWORD=1109
DB_HOST=localhost
DB_PORT=3306
DB_NAME=rental_app

# Alternative MySQL environment variables (used in core/db.py)
MYSQL_USER=root
MYSQL_PASSWORD=1109
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=rental_app

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Alembic Database URL (optional - will use settings if not provided)
ALEMBIC_DATABASE_URL=mysql+pymysql://root:1109@localhost:3306/rental_app
```

## Changes Made

### 1. Dependencies Updated
- Removed: `asyncpg`, `psycopg`, `psycopg-binary`, `psycopg2-binary`
- Added: `aiomysql`, `PyMySQL`, `pymysql`

### 2. Database Configuration
- Updated connection strings from PostgreSQL to MySQL
- Changed default ports from 5432 to 3306
- Updated database drivers from `postgresql+asyncpg` to `mysql+aiomysql`
- Updated sync drivers from `postgresql+psycopg` to `mysql+pymysql`

### 3. Model Changes
- Replaced PostgreSQL `UUID` type with MySQL `String(36)`
- Updated all foreign key references to use string IDs
- Maintained UUID generation using Python's `uuid` module

### 4. Migration Script
- Created migration script to convert existing UUID columns to VARCHAR(36)
- Handles all tables: users, vehicles, documents, user_vehicles, payments, user_payments, challans

## Setup Instructions

1. **Install MySQL Server**
   ```bash
   # On macOS with Homebrew
   brew install mysql
   brew services start mysql
   
   # On Ubuntu/Debian
   sudo apt-get install mysql-server
   sudo systemctl start mysql
   ```

2. **Create Database**
   ```sql
   mysql -u root -p
   CREATE DATABASE rental_app;
   ```

3. **Install Dependencies**
   ```bash
   cd backend
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Run Migrations**
   ```bash
   alembic upgrade head
   ```

5. **Start the Application**
   ```bash
   uvicorn app.main:app --reload
   ```

## Important Notes

- UUIDs are now stored as strings (36 characters) instead of native UUID type
- All existing data will need to be migrated using the provided migration script
- Foreign key relationships are maintained but use string references
- JSON columns remain unchanged as MySQL supports JSON natively
- Enum types are supported in MySQL 8.0+

## Troubleshooting

### Connection Issues
- Ensure MySQL server is running
- Verify database credentials in `.env` file
- Check firewall settings for port 3306

### Migration Issues
- Ensure all dependencies are installed
- Check that the database exists
- Verify user has proper permissions

### Data Type Issues
- UUIDs are now strings - update any code that expects UUID objects
- Use `str(uuid.uuid4())` for generating new IDs
