"""Comissão Financeiro

Revision ID: 4faf439113cd
Revises: abfeafffa2c1
Create Date: 2026-08-07 10:10:50.150540

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4faf439113cd"
down_revision = "abfeafffa2c1"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("financeiro", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("valor_comissao", sa.Float(), nullable=True)
        )

        batch_op.add_column(
            sa.Column("comissao_para", sa.String(length=120), nullable=True)
        )


def downgrade():
    with op.batch_alter_table("financeiro", schema=None) as batch_op:
        batch_op.drop_column("comissao_para")
        batch_op.drop_column("valor_comissao")