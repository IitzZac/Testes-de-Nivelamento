import pdfplumber
import csv
import os
import shutil

# Configuração
PASTA_DADOS = "dados_extraidos"
PDF_PATH = "pdfs/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf" 
CSV_ORIGINAL = os.path.join(PASTA_DADOS, "original.csv")
CSV_MODIFICADO = os.path.join(PASTA_DADOS, "modificado.csv")
ZIP_PATH = "Teste_{Guilherme Fortunato}.zip"

# Mapeamento de abreviações para descrições completas
ABREVIACOES = {
    "OD": "Procedimentos Odontológicos",
    "AMB": "Procedimentos Ambulatoriais"
}

def criar_pasta(pasta):
    
    os.makedirs(pasta, exist_ok=True)

def extrair_tabela_do_pdf(pdf_path):
    
    dados = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            tabelas = pagina.extract_tables()
            for tabela in tabelas:
                for linha in tabela:
                    if linha:  
                        dados.append(linha)
    
    return dados

def salvar_csv(dados, csv_path):
    
    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(dados)
    print(f"Dados salvos em {csv_path}")

def copiar_arquivo(origem, destino):
    
    shutil.copy(origem, destino)
    print(f"Cópia criada: {destino}")

def substituir_abreviacoes(csv_path):
    
    dados_corrigidos = []
    
    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for linha in reader:
            linha_corrigida = [ABREVIACOES.get(valor, valor) for valor in linha]
            dados_corrigidos.append(linha_corrigida)
    
    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(dados_corrigidos)
    
    print(f"Modificações aplicadas em {csv_path}")

def compactar_pasta(pasta, zip_path):
    
    shutil.make_archive(zip_path.replace(".zip", ""), "zip", pasta)
    print(f"Arquivos compactados em {zip_path}")

# Fluxo de execução
criar_pasta(PASTA_DADOS)

if os.path.exists(PDF_PATH):
    dados_extraidos = extrair_tabela_do_pdf(PDF_PATH)
    
    if dados_extraidos:
        # Passo 1: Salvar o CSV original
        salvar_csv(dados_extraidos, CSV_ORIGINAL)
        
        # Passo 2: Criar uma cópia para modificação
        copiar_arquivo(CSV_ORIGINAL, CSV_MODIFICADO)

        # Passo 3: Aplicar as modificações no arquivo copiado
        substituir_abreviacoes(CSV_MODIFICADO)

        # Passo 4: Compactar os arquivos
        compactar_pasta(PASTA_DADOS, ZIP_PATH)
    else:
        print("Nenhuma tabela foi extraída do PDF.")
else:
    print(f"Arquivo {PDF_PATH} não encontrado.")
