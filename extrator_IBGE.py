import requests
from bs4 import BeautifulSoup
import re
import unidecode
from padronizador import carregar_padronizacao, padronizar_dados

def _limpar_texto(texto: str) -> str:
    """
    Remove referências numéricas [2024] e espaços em branco extras.
    """
    texto = re.sub(r'\[\d+\]', '', texto)
    return texto.strip()

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
    chave = re.sub(r'<[^>]+>', '', chave)
    chave = chave.lower()
    chave = re.sub(r'[^\w\s]', '', chave)
    chave = chave.strip()
    chave = re.sub(r'\s+', '_', chave)
    return chave

def _coletar_dados_estado_ibge(url: str) -> dict:
    """
    Acessa a página de um estado no IBGE e extrai:
    - Título (h1) como 'Estado'
    - Código (via regex)
    - Itens de lista (<li>) que vêm após o h1 e
      que contenham <strong> (rótulos como 'Governador')
      ou <img alt="..."> (ícones dos indicadores)
    """
    resp = requests.get(url)
    resp.encoding = resp.apparent_encoding
    soup = BeautifulSoup(resp.text, 'html.parser')

    dados = {}
    # 1) Nome do estado
    if h1 := soup.find('h1'):
        # dados['Estado'] = _limpar_texto(h1.get_text())

        # 2) Código (só existe no header após o h1)
        texto_header = ''.join(h1.find_all_next(text=True, limit=5))
        if m := re.search(r'Código:\s*(\d+)', texto_header):
            dados['Código'] = m.group(1)

        # 3) Percorre somente os <li> que vêm após o h1
        for li in h1.find_all_next('li'):
            # (a) itens com <strong> → labels como 'Governador', 'Capital', 'Gentílico'
            if strong := li.find('strong'):
                label_original = strong.get_text(separator=' ').strip()
                chave = _normalizar_chave(label_original)
                txt = li.get_text(separator='\n')
                valor = _limpar_texto(txt.replace(label_original, '', 1))

            # (b) itens com <img alt="..."> → indicadores como 'Área Territorial', 'População estimada' etc.
            elif img := li.find('img'):
                label_original = img.get('alt', '').strip()
                chave = _normalizar_chave(label_original)
                txt = li.get_text(separator='\n')
                valor = _limpar_texto(txt.replace(label_original, '', 1))

            else:
                continue

            dados[chave] = valor

    for indicador in soup.select('div.indicador'):
        label_p = indicador.select_one('.ind-label > p')
        value_p = indicador.select_one('.ind-value')
        if label_p and value_p:
            chave = _normalizar_chave(label_p.get_text())
            valor = _limpar_texto(value_p.get_text())
            dados[chave] = valor
    
    # 4) Fonte
    dados['fonte_url'] = url
    return dados

def extrai_ibge(lista_siglas: list[str]) -> dict:
    """
    Recebe uma lista de siglas (por ex. ['sc','pr','rs']), monta as URLs
    https://www.ibge.gov.br/cidades-e-estados/{sigla}.html, coleta e retorna
    um dict com chaves em maiúsculo e valores sendo outro dict de campos.
    """
    url_base = 'https://www.ibge.gov.br/cidades-e-estados/'
    resultados: dict[str, dict] = {}
    padronizacao = carregar_padronizacao()
    padroes_campos = padronizacao["padronizacao_campos"]
    for sigla in lista_siglas:
        sig = sigla.lower()
        url = f'{url_base}{sig}.html'
        try:
            dados_extraidos = _coletar_dados_estado_ibge(url)
            dados_padronizados = padronizar_dados(dados_extraidos, padroes_campos)
            resultados[sig.upper()] = dados_padronizados
        except Exception as e:
            print(f'⚠️ Erro ao coletar {sig.upper()} ({url}): {e}')
    return resultados
