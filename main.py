from extrator_IBGE import extrai_ibge as ibge
import json
#Extrair dados

ESTADOS = ['sc', 'pr', 'rs']

estados_sul = ibge(ESTADOS)

with open('estados_sul_IBGE.json', 'w', encoding='utf-8') as f:
    json.dump(estados_sul, f, ensure_ascii=False, indent=4)
