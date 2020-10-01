"""empty message

Revision ID: 55acb7a92d48
Revises: c8a3f2eabd4e
Create Date: 2020-09-29 22:48:17.529688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55acb7a92d48'
down_revision = 'c8a3f2eabd4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('message', sa.String(length=150), nullable=False),
    sa.Column('time', sa.Time(), nullable=False),
    sa.ForeignKeyConstraint(['userid'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chat')
    # ### end Alembic commands ###
