"""create user

Revision ID: 18af4e28e102
Revises: abe5d766060f
Create Date: 2024-03-12 16:57:12.359645

"""
from datetime import datetime
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18af4e28e102'
down_revision: Union[str, None] = 'abe5d766060f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column('id', sa.UUID, nullable=False, primary_key=True, default=uuid4),
                    sa.Column('email', sa.String, nullable=False),
                    sa.Column('user_name', sa.String, nullable=False),
                    sa.Column('first_name', sa.String, nullable=True),
                    sa.Column('last_name', sa.String, nullable=True),
                    sa.Column('hashed_password', sa.String, nullable=True),
                    sa.Column('is_active', sa.Boolean, nullable=False, default=True),
                    sa.Column('is_admin', sa.Boolean, nullable=False, default=False),
                    sa.Column('company_id', sa.UUID, nullable=False),
                    sa.Column('created_at', sa.DateTime, nullable=False, default=datetime.utcnow),
                    sa.Column('updated_at', sa.DateTime, nullable=True)
                    )
    op.create_foreign_key('fk_user_company', 'users', 'companies', ['company_id'], ['id'])

def downgrade() -> None:
    op.drop_table("users")
