import json
import os

def carregar_padronizacao(caminho_padronizacao="padronizacao.json"):
    with open(caminho_padronizacao, encoding='utf-8') as f:
        return json.load(f)

def padronizar_dados(dados, padroes_campos):
    dados_padronizados = {}
    for chave, valor in dados.items():
        chave_padronizada = None
        for nome_padrao, variantes in padroes_campos.items():
            if chave in variantes:
                chave_padronizada = nome_padrao
                break
        if not chave_padronizada:
            chave_padronizada = chave  # mantém a original se não houver mapeamento
        dados_padronizados[chave_padronizada] = valor
        print(dados_padronizados)
    return dados_padronizados

def adicionar_fonte_ao_json(caminho_arquivo_json, fonte_nome, caminho_padronizacao="padronizacao.json"):
    padronizacao = carregar_padronizacao(caminho_padronizacao)
    padroes_campos = padronizacao["padronizacao_campos"]
    conversao_siglas = padronizacao["conversao_siglas_estados"]

    with open(caminho_arquivo_json, encoding='utf-8') as f:
        dados_originais = json.load(f)

    dados_processados = {}

    for estado_chave, dados_estado in dados_originais.items():
        estado_nome = conversao_siglas.get(estado_chave, estado_chave)
        dados_padronizados = padronizar_dados(dados_estado, padroes_campos)
        if estado_nome not in dados_processados:
            dados_processados[estado_nome] = {}
        dados_processados[estado_nome][fonte_nome] = dados_padronizados

    caminho_unificado = "estados_sul_dados_integrados.json"
    if os.path.exists(caminho_unificado):
        with open(caminho_unificado, encoding='utf-8') as f:
            dados_unificados = json.load(f)
    else:
        dados_unificados = {}

    for estado, fontes in dados_processados.items():
        if estado not in dados_unificados:
            dados_unificados[estado] = {}
        dados_unificados[estado].update(fontes)

    with open(caminho_unificado, "w", encoding='utf-8') as f:
        json.dump(dados_unificados, f, ensure_ascii=False, indent=4)

# Exemplos de uso:
# adicionar_fonte_ao_json("estados_sul_wikipedia.json", "Wikipedia")
# adicionar_fonte_ao_json("estados_sul_IBGE.json", "IBGE")
