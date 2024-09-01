import csv

def atualiza_arquivo_veiculos(nome_arquivo, nao_lidos):
    with open(nome_arquivo, "w") as file:
        writer = csv.writer(file, delimiter=';', lineterminator='\n')

        for veiculo in nao_lidos:

            writer.writerow(veiculo)