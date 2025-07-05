import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import os


def clean_numeric_value(value):
    if isinstance(value, str):
        # Remove pontos de milhar, "R$", "hab.", "km²", etc. e substitui vírgula por ponto decimal
        # Também remove textos explicativos como "-alto" do IDH
        value = re.sub(r'[.R$a-zA-Z²áéíóúçãõâêôü"\'\s‰/]', '', value)
        value = value.replace(',', '.')
    try:
        return float(value)
    except (ValueError, TypeError):
        return np.nan

# Carregar o arquivo JSON da pasta correta
with open('dados_json/estados_sul_dados_integrados.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

records = []
for sigla, estado_data in data.items():
    wiki_data = estado_data.get('dados_wikipedia', {})
    ibge_data = estado_data.get('dados_ibge', {})
    
    records.append({
        'Estado': estado_data.get('estado'),
        'Fonte': 'Wikipedia',
        'Área Territorial (km²)': clean_numeric_value(wiki_data.get('area_territorial')),
        'População (Censo)': clean_numeric_value(wiki_data.get('populacao_no_ultimo_censo')),
        'Densidade Demográfica (hab/km²)': clean_numeric_value(wiki_data.get('densidade_demografica')),
        'IDH': clean_numeric_value(wiki_data.get('idh_indice_de_desenvolvimento_humano')),
        'Governador': wiki_data.get('governador'),
        'Capital': wiki_data.get('capital', wiki_data.get('capital_e_municipiomais_populoso'))
    })
    records.append({
        'Estado': estado_data.get('estado'),
        'Fonte': 'IBGE',
        'Área Territorial (km²)': clean_numeric_value(ibge_data.get('area_territorial')),
        'População (Censo)': clean_numeric_value(ibge_data.get('populacao_no_ultimo_censo')),
        'Densidade Demográfica (hab/km²)': clean_numeric_value(ibge_data.get('densidade_demografica')),
        'IDH': clean_numeric_value(ibge_data.get('idh_indice_de_desenvolvimento_humano')),
        'Governador': ibge_data.get('governador'),
        'Capital': ibge_data.get('capital')
    })

df = pd.DataFrame(records)

# --- Geração do Gráfico de Barras Agrupadas ---
if not os.path.exists('graficos'):
    os.makedirs('graficos')

metrics_to_plot = {
    'Área Territorial (km²)': 'Área Territorial (km²)',
    'População (Censo)': 'População no Último Censo',
    'Densidade Demográfica (hab/km²)': 'Densidade Demográfica (hab/km²)',
    'IDH': 'Índice de Desenvolvimento Humano (IDH)'
}

for metric, title in metrics_to_plot.items():
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7))

    pivot_df = df.pivot(index='Estado', columns='Fonte', values=metric)
    pivot_df.plot(kind='bar', ax=ax, width=0.4)

    ax.set_title(f'Comparação de {title} por Estado (Wikipedia vs. IBGE)', fontsize=16)
    ax.set_ylabel(metric, fontsize=12)
    ax.set_xlabel('Estado', fontsize=12)
    ax.tick_params(axis='x', rotation=0)
    ax.legend(title='Fonte')
    plt.tight_layout()
    
    file_name = f'graficos/grafico_barras_{metric.split(" ")[0].lower()}.png'
    plt.savefig(file_name)
    print(f"Gráfico salvo como: {file_name}")

# --- Geração da Tabela Comparativa ---
# Extrair dados textuais e numéricos chave para a tabela
table_data = []
for sigla, estado_data in data.items():
    estado = estado_data.get('estado')
    wiki_data = estado_data.get('dados_wikipedia', {})
    ibge_data = estado_data.get('dados_ibge', {})
    
    table_data.append({'Métrica': 'Governador', 'Estado': estado, 'Fonte: Wikipedia': wiki_data.get('governador'), 'Fonte: IBGE': ibge_data.get('governador')})
    table_data.append({'Métrica': 'Capital', 'Estado': estado, 'Fonte: Wikipedia': wiki_data.get('capital', wiki_data.get('capital_e_municipiomais_populoso', '')).split(' ')[0], 'Fonte: IBGE': ibge_data.get('capital')})
    table_data.append({'Métrica': 'Área Territorial', 'Estado': estado, 'Fonte: Wikipedia': wiki_data.get('area_territorial'), 'Fonte: IBGE': ibge_data.get('area_territorial')})
    table_data.append({'Métrica': 'População (Censo)', 'Estado': estado, 'Fonte: Wikipedia': wiki_data.get('populacao_no_ultimo_censo'), 'Fonte: IBGE': ibge_data.get('populacao_no_ultimo_censo')})
    table_data.append({'Métrica': 'Densidade Demográfica', 'Estado': estado, 'Fonte: Wikipedia': wiki_data.get('densidade_demografica'), 'Fonte: IBGE': ibge_data.get('densidade_demografica')})
    table_data.append({'Métrica': 'IDH', 'Estado': estado, 'Fonte: Wikipedia': wiki_data.get('idh_indice_de_desenvolvimento_humano'), 'Fonte: IBGE': ibge_data.get('idh_indice_de_desenvolvimento_humano')})

df_table = pd.DataFrame(table_data)
df_table = df_table.set_index(['Estado', 'Métrica']).sort_index()

# Salvar a tabela em CSV
df_table.to_csv('tabela_comparativa.csv', encoding='utf-8-sig')
print("\nTabela Comparativa gerada e salva como tabela_comparativa.csv")
print(df_table)
