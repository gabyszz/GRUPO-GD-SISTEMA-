"""corrige financeiro planejamento

Revision ID: abfeafffa2c1
Revises: 3c38f202080d
Create Date: 2026-07-27 12:01:09.346167

"""

from alembic import op


# revision identifiers, used by Alembic.
revision = 'abfeafffa2c1'
down_revision = '3c38f202080d'
branch_labels = None
depends_on = None



def upgrade():

    """
    Essa migration originalmente alterava
    financeiro de projeto para planejamento.

    A alteração já existe no banco atual,
    portanto não há comandos de alteração.
    """

    pass



def downgrade():

    pass