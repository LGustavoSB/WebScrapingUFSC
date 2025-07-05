from extrator_IBGE import extrai_ibge as ibge
from extrator_wikipedia import extrai_wikipedia as wiki
import json
from padronizador import *
from limpador_de_json import processar_arquivo_json
import os

# Função para garantir que o diretório de dados exista
def garantir_diretorio_dados():
    if not os.path.exists('dados_json'):
        os.makedirs('dados_json')

#Extrair dados
def integra_dados(wiki_data, ibge_data):
    estados_integrados = {}

    # Criar um mapeamento entre nomes e siglas
    nome_para_sigla = {
        "Santa Catarina": "SC",
        "Paraná": "PR",
        "Rio Grande do Sul": "RS"
    }

    for nome_estado, dados_wiki in wiki_data.items():
        nome_formatado = nome_estado.replace('_', ' ')
        sigla = nome_para_sigla.get(nome_formatado)

        dados_ibge = ibge_data[sigla]

        estado_integrado = {
            "estado": nome_formatado,
            "dados_wikipedia": {k: v for k, v in dados_wiki.items()},
            "dados_ibge": {k: v for k, v in dados_ibge.items()}
        }

        estados_integrados[sigla] = estado_integrado
    
    caminho_arquivo = 'dados_json/estados_sul_dados_integrados.json'
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(estados_integrados, f, ensure_ascii=False, indent=4)

# Garante que o diretório exista antes de qualquer operação
garantir_diretorio_dados()

ESTADOS = ['sc', 'pr', 'rs']
ibge_data = ibge(ESTADOS)

with open('dados_json/estados_sul_IBGE.json', 'w', encoding='utf-8') as f:
    json.dump(ibge_data, f, ensure_ascii=False, indent=4)

ESTADOS_NOMES = ['Santa_Catarina', 'Paraná', 'Rio_Grande_do_Sul']
wiki_data = wiki(ESTADOS_NOMES)

with open('dados_json/estados_sul_wikipedia.json', 'w', encoding='utf-8') as f:
    json.dump(wiki_data, f, ensure_ascii=False, indent=4)

integra_dados(wiki_data, ibge_data)
processar_arquivo_json('dados_json/estados_sul_dados_integrados.json')