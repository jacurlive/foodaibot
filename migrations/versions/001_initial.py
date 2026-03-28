"""Initial migration

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('telegram_id', sa.BigInteger(), nullable=False),
        sa.Column('username', sa.String(length=64), nullable=True),
        sa.Column('first_name', sa.String(length=128), nullable=True),
        sa.Column('language', sa.String(length=5), nullable=False, server_default='en'),
        sa.Column('is_onboarded', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('name', sa.String(length=128), nullable=True),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('gender', sa.String(length=10), nullable=True),
        sa.Column('height', sa.Float(), nullable=True),
        sa.Column('weight', sa.Float(), nullable=True),
        sa.Column('goal', sa.String(length=10), nullable=True),
        sa.Column('units', sa.String(length=10), nullable=False, server_default='metric'),
        sa.Column('daily_calories', sa.Float(), nullable=True),
        sa.Column('notify_morning', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('notify_afternoon', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('notify_evening', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_banned', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
        sa.UniqueConstraint('telegram_id', name=op.f('uq_users_telegram_id')),
    )
    op.create_index(op.f('ix_users_telegram_id'), 'users', ['telegram_id'], unique=True)

    op.create_table(
        'food_entries',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('dish_name', sa.String(length=256), nullable=False),
        sa.Column('calories', sa.Float(), nullable=False),
        sa.Column('protein', sa.Float(), nullable=False),
        sa.Column('fat', sa.Float(), nullable=False),
        sa.Column('carbs', sa.Float(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('photo_file_id', sa.String(length=256), nullable=True),
        sa.Column('eaten_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(
            ['user_id'], ['users.telegram_id'],
            name=op.f('fk_food_entries_user_id_users'),
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_food_entries')),
    )
    op.create_index(op.f('ix_food_entries_user_id'), 'food_entries', ['user_id'], unique=False)
    op.create_index(op.f('ix_food_entries_eaten_at'), 'food_entries', ['eaten_at'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_food_entries_eaten_at'), table_name='food_entries')
    op.drop_index(op.f('ix_food_entries_user_id'), table_name='food_entries')
    op.drop_table('food_entries')
    op.drop_index(op.f('ix_users_telegram_id'), table_name='users')
    op.drop_table('users')
