import csv


def save_to_csv(data, filename, mode = 'w'):
    dir_save = f"./file/{filename}.csv"

    filtered_data = [row for row in data if row and row != ['S']]

    # Verifica se há dados para gravar.
    if not filtered_data:
        print("Nenhum dado válido para gravar.")
        return

    with open(dir_save, mode=mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in filtered_data:
            writer.writerow(row)

def save_to_csv_pad(data, filename, header = '', mode='w'):
    dir_save = f"./file/{filename}.csv"

    with open(dir_save, mode=mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if header != '':
            writer.writerow(header)
        writer.writerow(data)

def save_to_txt(data, filename, mode='w'):
    dir_save = f"./file/{filename}.txt"

    # with open(dir_save, mode=mode, encoding='utf-8') as file:
    #     writer = csv.writer(file)
    #     for row in data:
    #         writer.writerow(row)
    with open(dir_save, mode=mode, encoding='utf-8') as file:
        file.write(data)
    

def salvar_id(id: str, arquivo: str) -> None:
    
    with open(arquivo, 'r') as file:
        linhas = file.readlines()

    if linhas:
        primeira_linha = linhas[1]
        valores = primeira_linha.strip().split(';')
        valores[0] = id
        linhas[1] = ';'.join(valores) + '\n'

    with open(arquivo, 'w') as file:
        file.writelines(linhas)


def ler_id(arquivo):
    with open(arquivo, 'r') as file:
        return file.readline().strip()


def ler_continue(arquivo):
    with open(arquivo, 'r') as file:
        # Lê todas as linhas do arquivo
        linhas = file.readlines()
        # Extrai os nomes das colunas do cabeçalho
        colunas = linhas[0].strip().split(';')
        # Extrai os valores da primeira linha de dados
        valores = linhas[1].strip().split(';')
        # Cria um dicionário para mapear os valores às colunas
        dados = {}
        for coluna, valor in zip(colunas, valores):
            dados[coluna] = valor
        # Retorna os dados em um único dicionário
        return dados


def read_file_csv(nome_arquivo, delimiter):
    dados = []
    with open(nome_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            dados.append(row)
    return dados


def read_file_verify(nome_arquivo, chave_primaria, separador):
    dados = {}
    with open(nome_arquivo, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=separador)
        for row in reader:
            chave = row[chave_primaria]
            dados[chave] = row
    return dados


def find_files_difer(arquivo_base, arquivo_novo):
    diferencas = {}
    for chave, dados in arquivo_base.items():
        if chave not in arquivo_novo:
            diferencas[chave] = dados
    return diferencas


def save_file_difer(data, filename, mode='w'):
    dir_save = f"./file/CPAGAR/{filename}.csv"

    with open(dir_save, mode=mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Primeiro, verifique se o dicionário não está vazio e prepare os cabeçalhos
        if data:
            headers = list(next(iter(data.values())).keys())
            writer.writerow(headers)  # Escreve os cabeçalhos

        # Agora, escreva os valores
        for record in data.values():
            writer.writerow(list(record.values()))
