"""remove_vehicle_number_from_document_type_enum

Revision ID: 53f5cc23dbc2
Revises: 1d03ddb7236a
Create Date: 2025-09-09 12:30:50.133930

"""
from alembic import op
import sqlalchemy as sa

revision = '53f5cc23dbc2'
down_revision = '1d03ddb7236a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # First, delete related media_documents for vehicle_number documents
    op.execute("""
        DELETE FROM media_documents 
        WHERE documents_id IN (
            SELECT id FROM documents WHERE type = 'vehicle_number'
        )
    """)
    
    # Then delete the vehicle_number documents
    op.execute("DELETE FROM documents WHERE type = 'vehicle_number'")
    
    # Create a new enum without 'vehicle_number'
    op.execute("CREATE TYPE document_type_new AS ENUM ('DL', 'RC', 'PUC', 'Insurance', 'vehicle_image')")
    
    # Update the column to use the new enum
    op.execute("ALTER TABLE documents ALTER COLUMN type TYPE document_type_new USING type::text::document_type_new")
    
    # Drop the old enum and rename the new one
    op.execute("DROP TYPE document_type")
    op.execute("ALTER TYPE document_type_new RENAME TO document_type")


def downgrade() -> None:
    # Create the old enum with 'vehicle_number'
    op.execute("CREATE TYPE document_type_old AS ENUM ('DL', 'RC', 'PUC', 'Insurance', 'vehicle_number', 'vehicle_image')")
    
    # Update the column to use the old enum
    op.execute("ALTER TABLE documents ALTER COLUMN type TYPE document_type_old USING type::text::document_type_old")
    
    # Drop the new enum and rename the old one
    op.execute("DROP TYPE document_type")
    op.execute("ALTER TYPE document_type_old RENAME TO document_type")


