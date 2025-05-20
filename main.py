from extrator_IBGE import extrai_ibge as ibge
from extrator_wikipedia import extrai_wikipedia as wiki
import json
from padronizador import *
#Extrair dados

ESTADOS = ['sc', 'pr', 'rs']

estados_sul = ibge(ESTADOS)

with open('estados_sul_IBGE.json', 'w', encoding='utf-8') as f:
    json.dump(estados_sul, f, ensure_ascii=False, indent=4)

ESTADOS_NOMES = ['Santa_Catarina', 'Paraná', 'Rio_Grande_do_Sul']

wiki_data = wiki(ESTADOS_NOMES)

with open('estados_sul_wikipedia.json', 'w', encoding='utf-8') as f:
    json.dump(wiki_data, f, ensure_ascii=False, indent=4)

