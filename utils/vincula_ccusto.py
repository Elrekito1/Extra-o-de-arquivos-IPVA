import csv


def ler_arquivo_csv(nome_arquivo, delimiter):
    dados = []
    with open(nome_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            dados.append(row)
    return dados


def adicionar_ccusto(arquivo_contrato, dados_ccusto, ccusto_pad):
    for contrato in arquivo_contrato:
        encontrado = False
        for ccusto in dados_ccusto:
            if contrato['CONTRATO'] in ccusto['DESCRICAO']:
                contrato['CCUSTO'] = ccusto['CCUSTO'].replace('.', '')
                encontrado = True
                break
        if not encontrado:
            contrato['CCUSTO'] = ccusto_pad


# PARA TESTES INDIVIDUAIS
# arquivo_novo_nome = 'veiculos_contratos'
# arquivo_novo = f'./files/{arquivo_novo_nome}.csv'
# arquivo_ccusto = './files/ccustos.csv'

# dados_ccusto = ler_arquivo_csv(arquivo_ccusto, ';')

# dados_arquivo_novo = ler_arquivo_csv(arquivo_novo, ',')

# adicionar_ccusto(dados_arquivo_novo, dados_ccusto)

# cabecalho = list(dados_arquivo_novo[0].keys())  
# with open(f'./files/CPAGAR/{arquivo_novo_nome}_atualizado.csv', 'w', newline='', encoding='utf-8') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=cabecalho)
#     writer.writeheader()
#     for dados in dados_arquivo_novo:
#         writer.writerow(dados)
