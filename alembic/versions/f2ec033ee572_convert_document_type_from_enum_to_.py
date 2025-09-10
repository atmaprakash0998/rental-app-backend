"""convert_document_type_from_enum_to_string

Revision ID: f2ec033ee572
Revises: 53f5cc23dbc2
Create Date: 2025-09-10 05:42:56.254238

"""
from alembic import op
import sqlalchemy as sa

revision = 'f2ec033ee572'
down_revision = '53f5cc23dbc2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Convert the enum column to string
    op.execute("ALTER TABLE documents ALTER COLUMN type TYPE VARCHAR(50) USING type::text")
    
    # Drop the enum type
    op.execute("DROP TYPE document_type")


def downgrade() -> None:
    # Recreate the enum type
    op.execute("CREATE TYPE document_type AS ENUM ('DL', 'RC', 'PUC', 'Insurance', 'vehicle_image')")
    
    # Convert the string column back to enum
    op.execute("ALTER TABLE documents ALTER COLUMN type TYPE document_type USING type::document_type")


