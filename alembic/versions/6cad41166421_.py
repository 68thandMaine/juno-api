"""

Revision ID: 6cad41166421
Revises: 
Create Date: 2023-08-09 07:38:37.455901

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '6cad41166421'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bill',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('amount', sa.Numeric(), nullable=False),
    sa.Column('due_date', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('frequency', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('recurring', sa.Boolean(), nullable=True),
    sa.Column('category', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('notes', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('archived', sa.Boolean(), nullable=True),
    sa.Column('logo', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bill')
    # ### end Alembic commands ###
