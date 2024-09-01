import os, csv
from utils.extractPdf import extract_data_mt
from utils.vincula_ccusto import ler_arquivo_csv, adicionar_ccusto
from utils.vincula_contrato import ler_arquivo_csv_contrato, ler_arquivo_csv_contrato_twokeys, adicionar_contrato_ccusto
from utils.manipula_csv import ler_continue
import datetime
from utils.manipula_csv import *
from utils.extractPdf import extract_data_mt
from utils.gera_leiaute import processar_arquivos
from utils.clear_file import clear_file

def converte_layout_protheus(path_boletos):

    if "config.csv" in os.listdir('./file/'):

        dados_csv = ler_continue("./file/config.csv")
        exercicio = str(dados_csv['EXERCICIO'])
        name_file_cars = str(dados_csv['NAME_FILE_CARS'])
        name_file_ipvas = str(dados_csv['NAME_FILE_IPVAS'])
        name_file_print_ipva = str(dados_csv['NAME_FILE_PRINT_IPVA'])
        name_file_ccusto = str(dados_csv['NAME_FILE_CCUSTO'])
        name_file_contrato = str(dados_csv['FILE_NAME_CONTRATO'])
        ccusto_padrao = str(dados_csv['CCUSTO_PADRAO'])

    else:
        exit()
    
    ########## extractPDF ##########
    dir_pad = path_boletos
    files = os.listdir(dir_pad)
    if files:
        clear_file("./file/", f"{name_file_contrato}.csv")
    for file in files:
        if file.endswith(".pdf"):
            texto_pdf = extract_data_mt(
                dir_pad + file, name_file_contrato)

    ########## vinculaCCusto ##########
    arquivo_novo = f'./file/{name_file_ccusto}.csv'
    arquivo_ccusto = './file/ccustos.csv'

    dados_ccusto = ler_arquivo_csv(arquivo_ccusto, ';')

    dados_arquivo_novo = ler_arquivo_csv(arquivo_novo, ',')

    adicionar_ccusto(dados_arquivo_novo, dados_ccusto, ccusto_padrao)

    cabecalho = list(dados_arquivo_novo[0].keys())
    with open(f'./file/CPAGAR/{name_file_ccusto}_atualizado.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=cabecalho)
        writer.writeheader()
        for dados in dados_arquivo_novo:
            writer.writerow(dados)
            
    ########## vinculaContrato ##########
    arquivo_novo = f'./file/{name_file_contrato}.csv'
    arquivo_contrato = f'./file/CPAGAR/{name_file_ccusto}_atualizado.csv'

    chave_primaria_contrato = 'PLACA'
    chave_primaria_novo = 'PLACA'
    chave_primaria_novo_two = 'COTA'

    dados_contrato = ler_arquivo_csv_contrato(
        arquivo_contrato, chave_primaria_contrato)

    dados_arquivo_novo = ler_arquivo_csv_contrato_twokeys(
        arquivo_novo, chave_primaria_novo, chave_primaria_novo_two)

    adicionar_contrato_ccusto(
        dados_arquivo_novo, dados_contrato, ccusto_padrao)

    cabecalho = list(dados_arquivo_novo.values())[0].keys()
    with open(f'./file/CPAGAR/{name_file_contrato}_atualizado.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=cabecalho)
        writer.writeheader()
        for dados in dados_arquivo_novo.values():
            writer.writerow(dados)
            
    ########## geraLeiauteProtheus ##########
    leiaute = './file/leiaute.csv'
    nome_origem = f'{name_file_contrato}_atualizado'
    file_origem = f'./file/CPAGAR/{nome_origem}.csv'
    file_destino = f'./file/CPAGAR/{nome_origem}_importar.csv'

    processar_arquivos(leiaute, file_origem, file_destino)

