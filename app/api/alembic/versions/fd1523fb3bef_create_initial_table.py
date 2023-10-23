"""create initial table

Revision ID: fd1523fb3bef
Revises: 
Create Date: 2023-10-18 21:12:16.365209

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'fd1523fb3bef'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('batting_centers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('place_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_charset='utf8mb4',
    mysql_collate='utf8mb4_bin',
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_batting_centers_id'), 'batting_centers', ['id'], unique=False)
    op.create_index(op.f('ix_batting_centers_place_id'), 'batting_centers', ['place_id'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255, collation='utf8mb4_bin'), nullable=False),
    sa.Column('email', sa.String(length=255, collation='utf8mb4_bin'), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_charset='utf8mb4',
    mysql_collate='utf8mb4_bin',
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('itta_users_centers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('batting_center_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['batting_center_id'], ['batting_centers.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'batting_center_id', name='unique_idx_userid_battingcenterid'),
    mysql_charset='utf8mb4',
    mysql_collate='utf8mb4_bin',
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_itta_users_centers_id'), 'itta_users_centers', ['id'], unique=False)
    op.create_table('machine_informations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ball_speed', mysql.MEDIUMTEXT(), nullable=True),
    sa.Column('pitch_type', mysql.MEDIUMTEXT(), nullable=True),
    sa.Column('batter_box', sa.Enum('BAT_AT_RIGHT', 'BAT_AT_LEFT', 'BAT_AT_BOTH', name='batterbox'), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('batting_centers_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['batting_centers_id'], ['batting_centers.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('batter_box'),
    mysql_charset='utf8mb4',
    mysql_collate='utf8mb4_bin',
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_machine_informations_id'), 'machine_informations', ['id'], unique=False)
    op.create_table('atta_users_machines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('machine_info_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['machine_info_id'], ['machine_informations.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'machine_info_id', name='unique_idx_atta_userid_machineinfoid'),
    mysql_charset='utf8mb4',
    mysql_collate='utf8mb4_bin',
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_atta_users_machines_id'), 'atta_users_machines', ['id'], unique=False)
    op.create_table('nakatta_users_machines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('machine_info_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['machine_info_id'], ['machine_informations.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'machine_info_id', name='unique_idx_nakatta_userid_machineinfoid'),
    mysql_charset='utf8mb4',
    mysql_collate='utf8mb4_bin',
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_nakatta_users_machines_id'), 'nakatta_users_machines', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_nakatta_users_machines_id'), table_name='nakatta_users_machines')
    op.drop_table('nakatta_users_machines')
    op.drop_index(op.f('ix_atta_users_machines_id'), table_name='atta_users_machines')
    op.drop_table('atta_users_machines')
    op.drop_index(op.f('ix_machine_informations_id'), table_name='machine_informations')
    op.drop_table('machine_informations')
    op.drop_index(op.f('ix_itta_users_centers_id'), table_name='itta_users_centers')
    op.drop_table('itta_users_centers')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_batting_centers_place_id'), table_name='batting_centers')
    op.drop_index(op.f('ix_batting_centers_id'), table_name='batting_centers')
    op.drop_table('batting_centers')
    # ### end Alembic commands ###
