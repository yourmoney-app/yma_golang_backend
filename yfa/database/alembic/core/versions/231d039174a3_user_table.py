"""User Table

Revision ID: 231d039174a3
Revises: 
Create Date: 2022-01-21 15:01:34.189388

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '231d039174a3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
                    sa.Column(
                        'first_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column(
                        'last_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
                    sa.Column(
                        'country', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column(
                        'email_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
                    sa.Column('password_hash',
                              sqlmodel.sql.sqltypes.AutoString(), nullable=True),
                    sa.Column('password_salt',
                              sqlmodel.sql.sqltypes.AutoString(), nullable=True),
                    sa.Column(
                        'db_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
                    sa.Column(
                        'db_pwd', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
