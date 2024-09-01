import csv

def ler_arquivo_csv(nome_arquivo, delimiter):
    dados = []
    with open(nome_arquivo, encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, )
        for row in reader:
            dados.append(row)
    return dados