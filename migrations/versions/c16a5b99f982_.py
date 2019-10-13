"""empty message

Revision ID: c16a5b99f982
Revises: 64cd0e854e7a
Create Date: 2019-10-13 19:08:34.384415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c16a5b99f982'
down_revision = '64cd0e854e7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('talks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.Column('visible', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_talks_add_time'), 'talks', ['add_time'], unique=False)
    op.create_table('tops',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('foreign_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('article', 'talk', 'leavemsg'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tops')
    op.drop_index(op.f('ix_talks_add_time'), table_name='talks')
    op.drop_table('talks')
    # ### end Alembic commands ###
