import os, pdfplumber, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyPDF2 import PdfReader
from utils.manipula_csv import *
from utils.returnValueFromPDF import returnValueFromPDF, returnValueFromPDFPositions
from datetime import datetime, timedelta

def extrair_texto(pdf_path):
    texto = ''
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            texto += page.extract_text()
    save_to_txt(texto, "ipva")
    return texto


def validar_data_vencimento(data_vencimento, receber_ate):
    
    data_atual = datetime.now().date()
    
    data_vencimento = datetime.strptime(data_vencimento, '%d/%m/%Y').date()
    # print(f"receber_ate: {receber_ate}")
    if (data_vencimento < data_atual and receber_ate is not None and receber_ate != ''):
        # nova_data = data_atual + timedelta(days=1)
        receber_ate = datetime.strptime(receber_ate, '%d/%m/%Y').date()
        nova_data = receber_ate
    else:
        nova_data = data_vencimento
    print(f"nova_data: {nova_data}")
    return nova_data.strftime('%d/%m/%Y')

def extract_data(pdf_path, name_file):

    pdf = pdfplumber.open(pdf_path)

    final = ''
    for page in range(len(pdf.pages)):
        data = pdf.pages[page].extract_text()
        final = final + '\n' + data
        placa = returnValueFromPDF('PLACA:', final).strip()
        chassi = returnValueFromPDF('Placa/Chassi.', final).strip()
        cota = returnValueFromPDF('03.Cota ou Refer.', final).strip()
        exercicio = returnValueFromPDF('05.Exercício.', final).strip()
        vencimento = returnValueFromPDF('04.Vencimento.', final).strip()
        valor_veiculo = returnValueFromPDF('VALOR DO VEICULO:R$', final).strip()
        if not valor_veiculo:
            valor_veiculo = returnValueFromPDF(
                'VALOR VEICULO:R$', final).strip()
        if not valor_veiculo:
            valor_veiculo = returnValueFromPDF(
                'VLR DO VEICULO:R$', final).strip()
        if not valor_veiculo:
            valor_veiculo = returnValueFromPDF(
                'VLR VEICULO:R$', final).strip()
        valor_ipva = returnValueFromPDF('VALOR INTEGRAL DO IPVA: R$', final).strip()
        if not valor_ipva:
            valor_ipva = returnValueFromPDF(
                'VLR INTEGRAL DO IPVA: R$', final).strip()
        documento = returnValueFromPDF('12.Res. SEEC', final).strip()
        principal = returnValueFromPDF('13.Principal - R$ R$', final).strip()
        multa = returnValueFromPDF('14.Multa - R$ R$', final).strip()
        juros = returnValueFromPDF('15.Juros - R$ R$', final).strip()
        outros = returnValueFromPDF('16.Outros - R$ R$', final).strip()
        valor_total = returnValueFromPDF('17.Valor Total - R$ R$', final).strip()
        if outros: 
            text_target_index = final.find(
                "16.Outros - R$ R$") + len("16.Outros - R$ R$") + len(outros)
            text_target_index_end = final.find("17.Valor Total - R$ R$")
            codigo_barras = final[text_target_index+1:text_target_index_end].replace("\n", "").strip()
        receber_ate = returnValueFromPDF('AVISO AOS BANCOS: RECEBER ATE:', final).strip()
        if receber_ate:
            text_target_index = final.find(
                "AVISO AOS BANCOS: RECEBER ATE:") + len("AVISO AOS BANCOS: RECEBER ATE:")
            text_target_index_end = final.find("12.Res. SEEC")
            receber_ate = final[text_target_index:text_target_index_end].replace("\n", "").strip()
    
    save_to_txt(final, "ipva")

    data_info = []
    if placa:
        text_target_index_end = placa.find("TIPO:")
        placa_ok = placa[0:text_target_index_end].strip()
        data_info.append(placa_ok)
        if placa_ok == "REK3G34":
            print(f"REK3G34: {pdf_path}")
    if chassi:
        data_info.append(chassi)
    if cota:
        data_info.append(cota)
    if exercicio:
        data_info.append(exercicio)
    if documento:
        data_info.append(documento)
    data_atual = datetime.now().date()
    emissao = data_atual.strftime('%d/%m/%Y')
    data_info.append(emissao)
    # DATA DE VENCIMENTO DOS VENCIDOS PARA D+2 COLOCAR COMO DATA REAL 
    # REMOVIDO REGRA DA LINHA ANTERIOR A PEDIDO DO YURI DEVIDO ALGUNS ESTAREM VENCIADOS
    if vencimento:
        vencimento_ok = validar_data_vencimento(vencimento, receber_ate)
        data_info.append(vencimento_ok)
        data_info.append(vencimento_ok)
    if valor_veiculo:
        if valor_veiculo.find("BASE DE CALCULO:R$"):
            text_target_index_end = valor_veiculo.find("BASE DE CALCULO:R$")
            valor_veiculo_ok = valor_veiculo[0:text_target_index_end].strip().replace('.', '').replace(',', '.')
        else:
            valor_veiculo_ok = valor_veiculo.replace('.', '').replace(',', '.')
        data_info.append(valor_veiculo_ok)
    if valor_ipva:
        text_target_index_end = valor_ipva.find("ALIQUOTA:")
        valor_ipva_ok = valor_ipva[0:text_target_index_end].strip().replace('.', '').replace(',', '.')
        data_info.append(valor_ipva_ok)
    if principal:
        data_info.append(principal.replace('.', '').replace(',', '.'))
    if multa:
        data_info.append(multa.replace('.', '').replace(',', '.'))
    if juros:
        data_info.append(juros.replace('.', '').replace(',', '.'))
    if outros:
        data_info.append(outros.replace('.', '').replace(',', '.'))
    if valor_total:
        data_info.append(valor_total.replace('.', '').replace(',', '.'))
    if codigo_barras:
        data_info.append(codigo_barras.strip().replace('-', '').replace(' ', ''))
    historico = f"IPVA {exercicio} - {placa_ok}"
    data_info.append(historico)
    
    if f"{name_file}.csv" not in os.listdir('./files/'):
        header = [
            "PLACA", "CHASSI", "COTA", "EXERCICIO", "DOCUMENTO", "EMISSAO", "VENCIMENTO", "VENC_REAL", "VALOR_VEICULO", "VALOR_IPVA",
            "PRINCIPAL", "MULTA", "JUROS", "OUTROS", "VALOR_TOTAL", "LINHA_DIGITAVEL", "HISTORICO"
        ]
        save_to_csv_pad(data_info, f"{name_file}", header=header)
    else:
        save_to_csv_pad(data_info, f"{name_file}", mode="a")
    return data_info


def extract_data_mt(pdf_path, name_file):

    pdf = pdfplumber.open(pdf_path)

    final = ''
    for page in range(len(pdf.pages)):

        data = pdf.pages[page].extract_text()
        # final = final + '\n' + data
        final = '\n' + data

        placa = returnValueFromPDF('Placa : ', final).strip()

        if placa is not None and placa != "":
            chassi = returnValueFromPDF('Chassi : ', final).strip()
            cota = returnValueFromPDF('Pagamento ', final).strip()
            exercicio = returnValueFromPDF('Ano de Referência: ', final).strip()
            documento = returnValueFromPDF('Controle: ', final).strip()
            vencimento = returnValueFromPDF('CUIABA 90000 ', final).strip()
            valor_veiculo = "0.00"
            valor_ipva = returnValueFromPDF(' 6114 ', final).strip()
            if not valor_ipva:
                valor_ipva = returnValueFromPDF(' 6122 ', final).strip()
            principal = returnValueFromPDF(' 6114 ', final).strip()
            if not principal:
                principal = returnValueFromPDF(' 6122 ', final).strip()
            correcao_monet = returnValueFromPDFPositions('27 - VALOR', 'Controle: ', final).strip()
            multa = returnValueFromPDF('Placa : ', final).strip()
            juros = returnValueFromPDFPositions('29 - VALOR', 'Mais agilidade e facilidade no seu pagamento', final).strip()
            outros = returnValueFromPDFPositions('30 - VALOR', 'TOTAL A RECOLHER 31', final).strip()
            valor_total = returnValueFromPDFPositions('31 - VALOR', '33 - VALOR', final).strip()
            codigo_barras_full = returnValueFromPDFPositions('Via Arrecadação', 'GOVERNO DO ESTADO', final).strip()
            # print(f"codigo_barras_full: {codigo_barras_full}")
            codigo_barras = returnValueFromPDFPositions('', '\n', codigo_barras_full).strip()
            # print(f"codigo_barras: {codigo_barras}")
            
            save_to_txt(final, f"ipva{page}")

            data_info = []
            if placa:
                text_target_index_end = placa.find(" ")
                placa_ok = placa[0:text_target_index_end].strip()
                data_info.append(placa_ok)
                # if placa_ok == "OAT9355":
                #     print(f"OAT9355: {placa}-{placa_ok}")
            if chassi:
                text_target_index_end = chassi.find(" Ano de Referência")
                chassi_ok = chassi[0:text_target_index_end].strip()
                data_info.append(chassi_ok)
            if cota:
                text_target_index_start = cota.find("X ")
                text_target_index_end = cota.find("/")
                cota_ok = cota[text_target_index_start+1:text_target_index_end].strip().replace('parcelado ', '')
                # if returnValueFromPDF('parcelado ', cota_ok).strip() is not None:
                #     cota_ok = returnValueFromPDF('parcelado ', cota_ok).strip()
                data_info.append(cota_ok)
            if exercicio:
                text_target_index_end = exercicio.find(" JUROS 29")
                exercicio_ok = exercicio[0:text_target_index_end].strip().replace('.', '')
                data_info.append(exercicio_ok)
            if documento:
                data_info.append(documento)
            data_atual = datetime.now().date()
            emissao = data_atual.strftime('%d/%m/%Y')
            data_info.append(emissao)
            # # DATA DE VENCIMENTO DOS VENCIDOS PARA D+2 COLOCAR COMO DATA REAL
            # # REMOVIDO REGRA DA LINHA ANTERIOR A PEDIDO DO YURI DEVIDO ALGUNS ESTAREM VENCIADOS
            if vencimento:
                # vencimento_ok = validar_data_vencimento(vencimento, receber_ate)
                text_target_index_start = vencimento.find("/")
                vencimento_ok = vencimento[text_target_index_start+5:18].strip()
                data_info.append(vencimento_ok)
                data_info.append(vencimento_ok)
            if valor_veiculo:
                data_info.append(valor_veiculo)
            if valor_ipva:
                data_info.append(valor_ipva.replace('.', '').replace(',', '.'))
            if principal:
                data_info.append(principal.replace('.', '').replace(',', '.'))
            if multa:
                text_target_index_start = multa.find(" ")
                multa_ok = multa[text_target_index_start:].strip()
                data_info.append(multa_ok.replace('.', '').replace(',', '.'))
            if juros:
                data_info.append(juros.replace('.', '').replace(',', '.'))
            # if outros:
            #     outros_ok = float(correcao_monet.replace('.', '').replace(',', '.')) + float(outros.replace('.', '').replace(',', '.'))
            #     data_info.append(outros_ok)
            if valor_total:
                text_inicial = valor_total[valor_total.find('\n')+1:].strip()
                text_final = text_inicial[0:text_inicial.find('\n')].strip()
                data_info.append(text_final.replace('.', '').replace(',', '.'))
            if codigo_barras:
                data_info.append(codigo_barras.strip().replace('-', '').replace(' ', ''))
            historico = f"IPVA {exercicio_ok} - {placa_ok}"
            data_info.append(historico)

            if f"{name_file}.csv" not in os.listdir('./file/'):
                header = [
                    "PLACA", "CHASSI", "COTA", "EXERCICIO", "DOCUMENTO", "EMISSAO", "VENCIMENTO", "VENC_REAL", "VALOR_VEICULO", "VALOR_IPVA",
                    "PRINCIPAL", "MULTA", "JUROS", "VALOR_TOTAL", "LINHA_DIGITAVEL", "HISTORICO"
                ]
                save_to_csv_pad(data_info, f"{name_file}", header=header)
            else:
                save_to_csv_pad(data_info, f"{name_file}", mode="a")
    
    return data_info