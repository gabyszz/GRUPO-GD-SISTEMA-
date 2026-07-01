from services.backup_service import criar_backup


def backup_antes_de_alteracao():

    """
    Cria um backup do banco antes de qualquer operação crítica.
    """

    criar_backup()