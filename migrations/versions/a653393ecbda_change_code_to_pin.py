"""change code to pin

Revision ID: a653393ecbda
Revises: 950e60672dcf
Create Date: 2024-07-05 16:45:04.362105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a653393ecbda'
down_revision = '950e60672dcf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pin', sa.String(length=4), nullable=False))
        batch_op.drop_column('code')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('code', sa.VARCHAR(length=4), nullable=False))
        batch_op.drop_column('pin')

    # ### end Alembic commands ###
