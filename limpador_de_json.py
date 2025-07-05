import json

def limpar_json(obj):
    """
    Percorre recursivamente um objeto Python (dicionário ou lista)
    e limpa caracteres estranhos de todas as strings encontradas.
    """
    if isinstance(obj, dict):
        # Se for um dicionário, itera sobre seus itens, aplicando a função
        # recursivamente tanto na chave quanto no valor.
        return {limpar_json(k): limpar_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        # Se for uma lista, itera sobre seus elementos.
        return [limpar_json(elem) for elem in obj]
    elif isinstance(obj, str):
        # Se for uma string, realiza as substituições necessárias.
        # 1. Substitui o espaço não quebrável (nbsp) por um espaço normal.
        # 2. Substitui "– " (en-dash seguido de nbsp) por um hífen "-".
        return obj.replace('\xa0', ' ') \
                  .replace('– ', '-')   \
                  .replace('−', '-')
    else:
        # Retorna o objeto como está se não for dicionário, lista ou string
        # (ex: números, booleanos, None).
        return obj

def processar_arquivo_json(caminho_arquivo):
    """
    Lê um arquivo JSON, limpa seu conteúdo e o reescreve no mesmo local.
    """
    try:
        # Abre o arquivo para leitura com codificação UTF-8
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        # Chama a função para limpar os dados carregados
        dados_limpos = limpar_json(dados)

        # Abre o mesmo arquivo para escrita (sobrescrevendo o conteúdo)
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            # Salva os dados limpos de volta no arquivo
            # indent=4 para formatação e ensure_ascii=False para manter acentos
            json.dump(dados_limpos, f, indent=4, ensure_ascii=False)
        
        print(f"Sucesso! O arquivo '{caminho_arquivo}' foi limpo e reescrito.")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não contém um JSON válido.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")