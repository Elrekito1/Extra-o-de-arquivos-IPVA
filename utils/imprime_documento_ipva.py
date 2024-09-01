import pyautogui as pag
import ctypes
import time

def imprime_documento_ipva(sb, documento, placa, nova_placa):
    # Dê uma pausa para garantir que o aplicativo alvo esteja pronto
    time.sleep(2)

    # Simula a combinação de teclas Ctrl + S para abrir a janela de salvar
    pag.hotkey('ctrl', 's')
    time.sleep(1)

    # Define o nome do arquivo com base no tipo de documento
    if documento in ['IPVA', 'LICEN']:
        nome_arquivo = f'{placa}.pdf'
    else:
        raise ValueError("Tipo de documento inválido")

    # Digita o caminho completo para o arquivo
    pag.typewrite(f'C:\\Boletos\\{nome_arquivo}')
    time.sleep(1)

    # Usa a API do Windows para clicar no botão Salvar
    user32 = ctypes.windll.user32
    user32.keybd_event(0x0D, 0, 0, 0)  # Código virtual para "Enter" (pressionar)
    user32.keybd_event(0x0D, 0, 2, 0)  # Código virtual para "Enter" (soltar)
    time.sleep(1)



