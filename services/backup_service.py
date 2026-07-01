import os
import shutil

from datetime import datetime


# ==========================
# CONFIGURAÇÃO
# ==========================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

BANCO = os.path.join(
    BASE_DIR,
    "topografia.db"
)

PASTA_BACKUP = os.path.join(
    BASE_DIR,
    "backups"
)

MAX_BACKUPS = 30


# ==========================
# CRIA PASTA
# ==========================

if not os.path.exists(PASTA_BACKUP):

    os.makedirs(PASTA_BACKUP)


# ==========================
# BACKUP
# ==========================

def criar_backup():

    if not os.path.exists(BANCO):

        return

    data = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    destino = os.path.join(

        PASTA_BACKUP,

        f"{data}_topografia.db"

    )

    shutil.copy2(

        BANCO,

        destino

    )

    limpar_backups()


# ==========================
# LIMPAR ANTIGOS
# ==========================

def limpar_backups():

    arquivos = sorted(

        os.listdir(PASTA_BACKUP)

    )

    while len(arquivos) > MAX_BACKUPS:

        apagar = arquivos.pop(0)

        os.remove(

            os.path.join(

                PASTA_BACKUP,

                apagar

            )

        )