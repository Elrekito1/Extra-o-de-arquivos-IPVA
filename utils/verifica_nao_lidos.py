def verifica_nao_lidos(veiculos: list, lidos: list):
    
    nao_lidos = []
    
    for veiculo in veiculos:
        if veiculo not in lidos:
            nao_lidos.append(veiculo)
    
    return nao_lidos
