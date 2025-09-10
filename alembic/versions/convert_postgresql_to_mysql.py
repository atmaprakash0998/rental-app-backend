"""convert postgresql to mysql

Revision ID: convert_postgresql_to_mysql
Revises: f2ec033ee572
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'convert_postgresql_to_mysql'
down_revision = 'f2ec033ee572'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Convert PostgreSQL UUID columns to MySQL VARCHAR(36) columns"""
    
    # Convert users table
    op.alter_column('users', 'id',
                    existing_type=sa.dialects.postgresql.UUID(),
                    type_=sa.String(36),
                    existing_nullable=False)
    
    # Convert vehicles table
    op.alter_column('vehicles', 'id',
                    existing_type=sa.dialects.postgresql.UUID(),
                    type_=sa.String(36),
                    existing_nullable=False)
    
    # Convert documents table
    op.alter_column('documents', 'entity_id',
                    existing_type=sa.dialects.postgresql.UUID(),
                    type_=sa.String(36),
                    existing_nullable=False)
    
    # Convert user_vehicles table
    op.alter_column('user_vehicles', 'user_id',
                    existing_type=sa.dialects.postgresql.UUID(),
                    type_=sa.String(36),
                    existing_nullable=False)
    op.alter_column('user_vehicles', 'vehicle_id',
                    existing_type=sa.dialects.postgresql.UUID(),
                    type_=sa.String(36),
                    existing_nullable=False)
    
    # Convert payments table
    op.alter_column('payments', 'source_id',
                    existing_type=sa.dialects.postgresql.UUID(),
                    type_=sa.String(36),
                    existing_nullable=False)
    op.alter_column('payments', 'destination_id',
                    existing_type=sa.dialects.postgresql.UUID(),
                    type_=sa.String(36),
                    existing_nullable=False)
    
    # Convert user_payments table
    op.alter_column('user_payments', 'entity_id',
                    existing_type=sa.dialects.postgresql.UUID(),
                    type_=sa.String(36),
                    existing_nullable=False)
    
    # Convert challans table
    op.alter_column('challans', 'entity_id',
                    existing_type=sa.dialects.postgresql.UUID(),
                    type_=sa.String(36),
                    existing_nullable=False)


def downgrade() -> None:
    """Convert MySQL VARCHAR(36) columns back to PostgreSQL UUID columns"""
    
    # Convert users table
    op.alter_column('users', 'id',
                    existing_type=sa.String(36),
                    type_=sa.dialects.postgresql.UUID(),
                    existing_nullable=False)
    
    # Convert vehicles table
    op.alter_column('vehicles', 'id',
                    existing_type=sa.String(36),
                    type_=sa.dialects.postgresql.UUID(),
                    existing_nullable=False)
    
    # Convert documents table
    op.alter_column('documents', 'entity_id',
                    existing_type=sa.String(36),
                    type_=sa.dialects.postgresql.UUID(),
                    existing_nullable=False)
    
    # Convert user_vehicles table
    op.alter_column('user_vehicles', 'user_id',
                    existing_type=sa.String(36),
                    type_=sa.dialects.postgresql.UUID(),
                    existing_nullable=False)
    op.alter_column('user_vehicles', 'vehicle_id',
                    existing_type=sa.String(36),
                    type_=sa.dialects.postgresql.UUID(),
                    existing_nullable=False)
    
    # Convert payments table
    op.alter_column('payments', 'source_id',
                    existing_type=sa.String(36),
                    type_=sa.dialects.postgresql.UUID(),
                    existing_nullable=False)
    op.alter_column('payments', 'destination_id',
                    existing_type=sa.String(36),
                    type_=sa.dialects.postgresql.UUID(),
                    existing_nullable=False)
    
    # Convert user_payments table
    op.alter_column('user_payments', 'entity_id',
                    existing_type=sa.String(36),
                    type_=sa.dialects.postgresql.UUID(),
                    existing_nullable=False)
    
    # Convert challans table
    op.alter_column('challans', 'entity_id',
                    existing_type=sa.String(36),
                    type_=sa.dialects.postgresql.UUID(),
                    existing_nullable=False)
