import os

def limpa_diretorio(path: str):
    
    if os.path.exists(path): 

        filesToClear = os.listdir(path)

        for file in filesToClear:
            os.remove(path + file)
            