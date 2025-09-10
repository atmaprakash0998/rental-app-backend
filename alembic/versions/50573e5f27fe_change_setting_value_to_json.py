"""change_setting_value_to_json

Revision ID: 50573e5f27fe
Revises: f2ec033ee572
Create Date: 2025-09-10 05:52:54.164488

"""
from alembic import op
import sqlalchemy as sa

revision = '50573e5f27fe'
down_revision = 'f2ec033ee572'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # First, wrap existing string values in quotes to make them valid JSON strings
    op.execute("""
        UPDATE settings 
        SET value = CASE 
            WHEN value IS NULL THEN NULL
            WHEN value = '' THEN '""'
            ELSE '"' || value || '"'
        END
        WHERE value IS NOT NULL
    """)
    
    # Then convert the column to JSON
    op.execute("ALTER TABLE settings ALTER COLUMN value TYPE JSON USING value::json")


def downgrade() -> None:
    # Convert the JSON column back to string
    op.execute("ALTER TABLE settings ALTER COLUMN value TYPE VARCHAR(255) USING value::text")


