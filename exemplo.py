import requests
from bs4 import BeautifulSoup
import json
import re

def limpar_texto(texto):
    texto = re.sub(r'\[\d+\]', '', texto)
    texto = texto.strip()
    return texto

def coletar_dados_estado(url):
    requisicaoDePagina = requests.get(url)
    conteudo = requisicaoDePagina.content
    site = BeautifulSoup(conteudo, 'html.parser')
    
    infobox = site.find("table", {"class": "infobox"})
    linhas = infobox.find_all('tr')

    dados = {}

    for linha in linhas:
        tds = linha.find_all('td')
        if len(tds) == 2:
            chave = limpar_texto(tds[0].get_text())
            valor = limpar_texto(tds[1].get_text())
            dados[chave] = valor

    dados["Fonte_URL"] = url
    return dados

url_base = 'https://pt.wikipedia.org/wiki/'

lista_de_estados = ['Santa_Catarina', 'Paraná', 'Rio_Grande_do_Sul']

estados_sul = {}

for estado_url in lista_de_estados:
    nome_estado = estado_url.replace('_', ' ')
    print(f"Coletando {nome_estado}...")
    dados_estado = coletar_dados_estado(url_base + estado_url)
    if dados_estado:
        estados_sul[nome_estado] = dados_estado
    else:
        print(f"⚠️ Atenção: Não conseguiu coletar {nome_estado}!")

with open('estados_sul.json', 'w', encoding='utf-8') as f:
    json.dump(estados_sul, f, ensure_ascii=False, indent=4)

print("✅ Dados salvos em 'estados_brasil.json'!")
