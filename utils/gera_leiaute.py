import csv


def processar_arquivos(arquivo_mapeamento, arquivo_origem, arquivo_destino):
    # Ler o mapeamento de campos
    mapeamento_campos = {}
    with open(arquivo_mapeamento, newline='', encoding='utf-8') as mapeamento_file:
        reader = csv.DictReader(mapeamento_file)
        for row in reader:
            # print(row)
            mapeamento_campos[row['De']] = row['Para'], row['ValorFixo']
        # print(mapeamento_campos)
        
    # Ler o arquivo de origem e gerar o arquivo de destino
    with open(arquivo_origem, newline='', encoding='utf-8') as origem_file, \
        open(arquivo_destino, 'w', newline='', encoding='utf-8') as destino_file:
        reader = csv.DictReader(origem_file)
        # Obter os nomes dos campos do arquivo de destino
        fieldnames = [campo_destino for campo_destino, _ in mapeamento_campos.values()]
        
        writer = csv.DictWriter(destino_file, fieldnames=fieldnames, delimiter='|')
        writer.writeheader()
        for row in reader:
            novo_registro = {}
            for campo_origem, (campo_destino, valor_fixo) in mapeamento_campos.items():
                if campo_origem in row:
                    novo_registro[campo_destino] = row[campo_origem]
                else:
                    novo_registro[campo_destino] = valor_fixo
            writer.writerow(novo_registro)


# TESTE MANUAL INDIVIDUAIS
# leiaute = './files/leiaute.csv'
# nome_origem = 'IPVA_REG_02_CPAGAR_atualizado'
# file_origem = f'./files/CPAGAR/{nome_origem}.csv'
# file_destino = f'./files/CPAGAR/{nome_origem}_importar.csv'

# processar_arquivos(leiaute, file_origem, file_destino)
