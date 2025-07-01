import requests
from bs4 import BeautifulSoup
import re
import unidecode
from padronizador import carregar_padronizacao, padronizar_dados

def _limpar_texto(texto):
    texto = re.sub(r'^•\s*', '', texto)
    texto = re.sub(r'\([^)]*\)', '', texto)
    texto = re.sub(r'\[\d+\]', '', texto)
    texto = re.sub(r'\s{2,}', ' ', texto)
    texto = re.sub(r'([a-záéíóúãõç])([A-Z])', r'\1, \2', texto)
    return texto.strip()


def _normalizar_chave(chave: str) -> str:
    chave = _limpar_texto(chave)
    chave = unidecode.unidecode(chave)
    chave = chave.lower()
    chave = re.sub(r'[^\w\s]', '', chave)
    chave = chave.strip()
    chave = re.sub(r'\s+', '_', chave)
    return chave


def _coletar_dados_estado_wikipedia(url):
    requisicaoDePagina = requests.get(url)
    conteudo = requisicaoDePagina.content
    site = BeautifulSoup(conteudo, 'html.parser')
    
    infobox = site.find("table", {"class": "infobox"})
    linhas = infobox.find_all('tr')

    dados = {}

    for linha in linhas:
        tds = linha.find_all('td')
        if len(tds) == 2:
            chave = _normalizar_chave(tds[0].get_text())
            valor = _limpar_texto(tds[1].get_text())
            dados[chave] = valor

    dados["fonte_url"] = url
    return dados

def extrai_wikipedia(lista_estados: list[str]) -> dict:
    """
    Recebe uma lista de nome de estados (por ex. ['Santa_Catarina', 'Paraná', 'Rio_Grande_do_Sul']), monta as URLs
    'https://pt.wikipedia.org/wiki/{nome_estado}', coleta e retorna
    um dict com chaves em maiúsculo e valores sendo outro dict de campos.
    """
    url_base = 'https://pt.wikipedia.org/wiki/'
    resultados: dict[str, dict] = {}
    padronizacao = carregar_padronizacao()
    padroes_campos = padronizacao["padronizacao_campos"]
    for estado_url in lista_estados:
        nome_estado = estado_url.replace('_', ' ')
        try:
            dados_extraidos = _coletar_dados_estado_wikipedia(url_base + estado_url)
            dados_padronizados = padronizar_dados(dados_extraidos, padroes_campos)
            resultados[nome_estado] = dados_padronizados
        except Exception as e:
            print(f"Erro ao coletar {nome_estado} ({url_base + estado_url}): {e}")
    return resultados

def padronizar_valor(valor):
    if not isinstance(valor, str):
        return valor

    valor = re.sub(r'\b(km²|hab\.?|pessoas?|veículos?|R\$|anos?|‰ nasc\.?|matrículas?|bilhões?|milhões?)\b', '', valor, flags=re.IGNORECASE)

    valor = re.sub(r'[^\w,.\- ]', '', valor)
    valor = re.sub(r'\s{2,}', ' ', valor)
    valor = valor.strip()

    valor = valor.replace('\xa0', '')
    valor = valor.replace('.', '').replace(',', '.')

    try:
        if '.' in valor:
            return float(valor)
        else:
            return int(valor)
    except ValueError:
        return valor.lower()
