"""create company

Revision ID: abe5d766060f
Revises: 
Create Date: 2024-03-12 14:50:22.680669

"""
import random
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from datetime import datetime

from schemas.base_entity import CompanyMode


# revision identifiers, used by Alembic.
revision: str = 'abe5d766060f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    company_table = op.create_table("companies",
                    sa.Column('id', sa.UUID, nullable=False, primary_key=True),
                    sa.Column('name', sa.String, nullable=False),
                    sa.Column('description', sa.String, nullable=True),
                    sa.Column('mode', sa.Enum(CompanyMode), nullable=True, default=CompanyMode.PUBLIC),
                    sa.Column('rating', sa.Float, nullable=True),
                    sa.Column('created_at', sa.DateTime, nullable=False, default=datetime.utcnow),
                    sa.Column('updated_at', sa.DateTime, nullable=True)
                    )
    
    # Bulk insert sample data
    data = []
    for i in range(1, 20):
        data.append(
                        {
                            "id": uuid4(),
                            "name": f"Company {i}", 
                            "description": f"Description for company {i}",
                            "mode": CompanyMode.PUBLIC if i%3 == 0 else CompanyMode.PRIVATE,
                            "rating": random.randint(1, 5)
                       }
                    )
    op.bulk_insert(company_table, data)

def downgrade() -> None:
    op.drop_table('companies')
    op.execute("DROP TYPE CompanyMode;")
