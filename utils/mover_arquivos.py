import shutil as sh
import os

def mover_arquivos(fromFolder: str, toFolder: str, placa: str) -> None:
    files = os.listdir(fromFolder)
    for f in files:
        if f == placa+" - IPVA.pdf" or f == placa+" - LICENCIAMENTO.pdf":
            sh.move(fromFolder + f, toFolder)
