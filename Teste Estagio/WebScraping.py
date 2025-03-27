import requests
import os
import shutil
from bs4 import BeautifulSoup


URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

def acessar_pagina(url):
    
    response = requests.get(url)
    if response.status_code == 200:
        print("Página acessada com sucesso!")
        return response.text
    else:
        print("Erro ao acessar a página:", response.status_code)
        return None

def extrair_links_pdfs(html):
    
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", href=True)

    # Filtra apenas os links que contêm "Anexo" no texto e terminam em ".pdf"
    pdf_links = [link["href"] for link in links if "Anexo" in link.text and link["href"].endswith(".pdf")]

    # Corrigir URLs relativas
    pdf_links = ["https://www.gov.br" + link if link.startswith("/") else link for link in pdf_links]

    return pdf_links

def baixar_pdfs(links, pasta_destino="pdfs"):
    
    os.makedirs(pasta_destino, exist_ok=True)

    for link in links:
        pdf_name = link.split("/")[-1]  # Extrai o nome do arquivo
        response = requests.get(link)

        if response.status_code == 200:
            with open(f"{pasta_destino}/{pdf_name}", "wb") as file:
                file.write(response.content)
            print(f"Baixado: {pdf_name}")
        else:
            print(f"Erro ao baixar {pdf_name}: {response.status_code}")

def compactar_pdfs(pasta_origem="pdfs", nome_arquivo="Anexos.zip"):
    
    shutil.make_archive(nome_arquivo.replace(".zip", ""), "zip", pasta_origem)
    print(f"Arquivos compactados em {nome_arquivo}")

# Fluxo do Web Scraping
html = acessar_pagina(URL)
if html:
    pdf_links = extrair_links_pdfs(html)
    if pdf_links:
        print("Links encontrados:", pdf_links)
        baixar_pdfs(pdf_links)
        compactar_pdfs()
    else:
        print("Nenhum link de PDF encontrado.")
