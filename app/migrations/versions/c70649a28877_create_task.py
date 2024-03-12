"""create task

Revision ID: c70649a28877
Revises: 18af4e28e102
Create Date: 2024-03-12 18:10:42.475122

"""
from datetime import datetime
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from schemas.base_entity import Priority, TaskStatus


# revision identifiers, used by Alembic.
revision: str = 'c70649a28877'
down_revision: Union[str, None] = '18af4e28e102'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("tasks",
                    sa.Column('id', sa.UUID, nullable=False, primary_key=True, default=uuid4),
                    sa.Column('summary', sa.String, nullable=False),
                    sa.Column('description', sa.String, nullable=True),
                    sa.Column('status', sa.Enum(TaskStatus), nullable=False, default=TaskStatus.NEW),
                    sa.Column('priority', sa.Enum(Priority), nullable=False, default=Priority.MEDIUM),
                    sa.Column('user_id', sa.UUID, nullable=False),
                    sa.Column('created_at', sa.DateTime, nullable=False, default=datetime.utcnow),
                    sa.Column('updated_at', sa.DateTime, nullable=True)
                    )
    op.create_foreign_key('fk_task_user', 'tasks', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    op.drop_table('tasks')
    op.execute("DROP TYPE TaskStatus; DROP TYPE Priority;")
