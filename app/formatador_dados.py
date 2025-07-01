import json
import re

def formatar_dados(dados):
    with open('padronizacao.json', 'r', encoding='utf-8') as f:
        padronizacao = json.load(f)
    
    campos_comparaveis = list(padronizacao['padronizacao_campos'].keys())
    
    dados_formatados = {}
    
    for estado, dados_estado in dados.items():
        dados_formatados[estado] = {
            'estado': dados_estado['estado'],
            'wikipedia': {
                'dados_correspondentes': {},
                'dados_unicos': {}
            },
            'ibge': {
                'dados_correspondentes': {},
                'dados_unicos': {}
            }
        }
        
        wiki_data = dados_estado['dados_wikipedia']
        ibge_data = dados_estado['dados_ibge']
        
        def encontrar_valor_campo(dados, campo):
            alternativas = padronizacao['padronizacao_campos'][campo]
            for alt in alternativas:
                if alt in dados:
                    return dados[alt]
            return ''
        
        def padronizar_valor(valor, campo):
            if not valor:
                return valor
            
            campos_numericos = [
                'area_territorial',
                'populacao_estimada',
                'populacao_no_ultimo_censo',
                'densidade_demografica',
                'idh_indice_de_desenvolvimento_humano'
            ]
            
            if campo in campos_numericos:
                if isinstance(valor, str):
                    valor = re.sub(r'[^\d.,]', '', valor)
                    valor = valor.replace('.', '').replace(',', '.')
                    return valor.strip()
            
            if isinstance(valor, str):
                return valor.strip().lower()
            
            return valor
        
        for campo in campos_comparaveis:
            wiki_valor = encontrar_valor_campo(wiki_data, campo)
            ibge_valor = encontrar_valor_campo(ibge_data, campo)

            if campo == 'fonte_url': continue
            
            if wiki_valor and ibge_valor:
                wiki_valor_pad = padronizar_valor(wiki_valor, campo)
                ibge_valor_pad = padronizar_valor(ibge_valor, campo)
                
                dados_formatados[estado]['wikipedia']['dados_correspondentes'][campo] = {
                    'valor': wiki_valor,
                    'corresponde': wiki_valor_pad == ibge_valor_pad,
                    'valor_comparado': ibge_valor
                }
                
                dados_formatados[estado]['ibge']['dados_correspondentes'][campo] = {
                    'valor': ibge_valor,
                    'corresponde': wiki_valor_pad == ibge_valor_pad,
                    'valor_comparado': wiki_valor
                }
        
        for campo, valor in wiki_data.items():
            if not any(campo in alt_list for alt_list in padronizacao['padronizacao_campos'].values()) and valor:
                dados_formatados[estado]['wikipedia']['dados_unicos'][campo] = valor
                
        for campo, valor in ibge_data.items():
            if not any(campo in alt_list for alt_list in padronizacao['padronizacao_campos'].values()) and valor:
                dados_formatados[estado]['ibge']['dados_unicos'][campo] = valor
    
    return dados_formatados