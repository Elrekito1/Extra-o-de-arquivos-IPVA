import pyautogui as pag

def imprime_documento_licenc(sb, documento, placa, path):
    sb.driver.sleep(5)
    pag.hotkey('ctrl','p')
    
    sb.driver.sleep(5)
    
    pag.press("enter")
    sb.driver.sleep(3)        
                    
    if documento == 'IPVA':
        pag.typewrite(f'{path}\{placa} - IPVA.pdf')
    elif documento == 'LICEN':
        pag.typewrite(f'{path}\{placa} - LICENCIAMENTO.pdf')  
              
    sb.driver.sleep(3)
    pag.press("enter")
    sb.driver.sleep(3)