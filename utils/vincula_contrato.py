import csv


def ler_arquivo_csv_contrato(nome_arquivo, chave_primaria):
    dados = {}
    with open(nome_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            chave = row[chave_primaria]
            dados[chave] = row
    return dados


def ler_arquivo_csv_contrato_twokeys(nome_arquivo, chave_primaria, chave_primaria_two):
    dados = {}
    with open(nome_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            chave = f"{row[chave_primaria]}-{row[chave_primaria_two]}"
            dados[chave] = row
    return dados


def adicionar_contrato_ccusto(arquivo_novo, dados_contrato, ccusto_pad):
    for placa, dados in arquivo_novo.items():
        placa = placa[0:7]
        # print(placa)
        if placa in dados_contrato:
            dados['CONTRATO'] = dados_contrato[placa]['CONTRATO']
            dados['CCUSTO'] = dados_contrato[placa]['CCUSTO']
        else:
            dados['CONTRATO'] = ''
            dados['CCUSTO'] = ccusto_pad


def adicionar_ccusto(arquivo_novo, dados_contrato, ccusto_pad):
    for placa, dados in arquivo_novo.items():
        if placa in dados_contrato:
            dados['CCUSTO'] = dados_contrato[placa]['CCUSTO']
        else:
            dados['CCUSTO'] = ccusto_pad


# TESTE MANUAL INDIVIDUAIS
# Nomes dos arquivos CSV
# arquivo_novo_nome = 'IPVA_REG_01_CPAGAR'
# arquivo_novo = f'./files/{arquivo_novo_nome}.csv'
# arquivo_contrato = './files/CPAGAR/veiculos_contratos_atualizado.csv'

# chave_primaria_contrato = 'PLACA'
# chave_primaria_novo = 'PLACA'

# dados_contrato = ler_arquivo_csv_contrato(arquivo_contrato, chave_primaria_contrato)

# dados_arquivo_novo = ler_arquivo_csv_contrato(arquivo_novo, chave_primaria_novo)

# adicionar_contrato_ccusto(dados_arquivo_novo, dados_contrato)

# cabecalho = list(dados_arquivo_novo.values())[0].keys()
# with open(f'./files/CPAGAR/{arquivo_novo_nome}_atualizado.csv', 'w', newline='', encoding='utf-8') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=cabecalho)
#     writer.writeheader()
#     for dados in dados_arquivo_novo.values():
#         writer.writerow(dados)


