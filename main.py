from extrator_IBGE import extrai_ibge as ibge
from extrator_wikipedia import extrai_wikipedia as wiki
import json
from padronizador import *
from limpador_de_json import processar_arquivo_json

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

    with open('estados_sul_dados_integrados.json', 'w', encoding='utf-8') as f:
        json.dump(estados_integrados, f, ensure_ascii=False, indent=4)



ESTADOS = ['sc', 'pr', 'rs']

ibge_data = ibge(ESTADOS)

with open('estados_sul_IBGE.json', 'w', encoding='utf-8') as f:
    json.dump(ibge_data, f, ensure_ascii=False, indent=4)

ESTADOS_NOMES = ['Santa_Catarina', 'Paraná', 'Rio_Grande_do_Sul']

wiki_data = wiki(ESTADOS_NOMES)

with open('estados_sul_wikipedia.json', 'w', encoding='utf-8') as f:
    json.dump(wiki_data, f, ensure_ascii=False, indent=4)

# adicionar_fonte_ao_json("estados_sul_wikipedia.json", "Wikipedia")
# adicionar_fonte_ao_json("estados_sul_IBGE.json", "IBGE")
integra_dados(wiki_data, ibge_data)
processar_arquivo_json('estados_sul_dados_integrados.json')

