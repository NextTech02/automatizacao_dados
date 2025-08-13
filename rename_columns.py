import os
import pandas as pd
import numpy as np
import re

# Caminhos das pastas
input_folder = "extratosgerais/"
output_folder = "Extratos hist/"
file_mapping_path = 'colunas correspondentes.csv'

# Criar a pasta de saída se não existir
os.makedirs(output_folder, exist_ok=True)

# Carregar o arquivo de mapeamento
mapping_df = pd.read_csv(file_mapping_path)

# Função para alterar o tipo de dado das colunas de acordo com o mapeamento
def change_column_types(df, mapping_df):
    type_mapping = {
        "text": str,
        "int4": int,
        "bigint": int,
        "int2": int,
        "numeric": float
    }

    for _, row in mapping_df.iterrows():
        column_name = row['nome tabela nova']
        data_type = row['tipo de dado']

        if column_name in df.columns and data_type in type_mapping:
            df[column_name] = df[column_name].astype(type_mapping[data_type], errors='ignore')

    return df

# Função para limpar e preparar o dataframe removendo símbolos de moeda
def clean_and_prepare_csv_remove_all_currency_symbols(df):
    column_mapping = {
        "Grupo": "grupo",
        "Liga": "liga",
        "ID Slot": "id_slot",
        "Nome do Slot": "nome_slot",
        "Taxa Liga %": "taxa_liga_porc",
        "Taxa App%": "taxa_app_porc",
        "Taxa Rodeo GGR %": "taxa_rodeo_ggr_porc",
        "Taxa Rodeo APP %": "taxa_rodeo_app_porc",
        "Rake": "rake",
        "Ativos": "ativos",
        "Rodeo PL": "rodeo_pl",
        "Handcap": "handcap",
        "Resultado do Clube": "resultado_clube",
        "Resultado Final do Clube MTT/SNG": "resultado_final_mtt_sng",
        "Resultado Final do Clube RG": "resultado_final_rg",
        "Rebate": "rebate",
        "Taxa Liga": "taxa_liga_valor",
        "Taxa App": "taxa_app_valor",
        "Taxa Rodeo": "taxa_rodeo_valor",
        "Vendas": "vendas",
        "Acordos/Acertos": "acordos_acertos",
        "Diamantes Liga": "diamantes_liga",
        "Overlay": "overlay",
        "Security": "security",
        "Adiantamentos": "adiantamentos",
        "Inadimplencia": "inadimplencia",
        "Eventos": "eventos",
        "Estorno de Taxas": "estorno_taxas",
        "Rakeback": "rakeback",
        "Descontos": "descontos",
        "Acerto Final": "acerto_final"
    }

    df.rename(columns=column_mapping, inplace=True)

    # Remover "R$" e ajustar os pontos decimais
    df = df.map(lambda x: str(x).replace('R$', '').replace(',', '') if isinstance(x, str) else x)

    return df

# Iterar sobre os arquivos na pasta de entrada
for file_name in os.listdir(input_folder):
    if file_name.endswith(".xlsx"):
        file_path = os.path.join(input_folder, file_name)

        # Extrair as datas do nome do arquivo
        match = re.search(r'(\d{2})(\d{2})(\d{4}) à (\d{2})(\d{2})(\d{4})', file_name)
        if match:
            # Formatar as datas para yyyymmdd
            init_date = f"{match.group(3)}{match.group(2)}{match.group(1)}"
            final_date = f"{match.group(6)}{match.group(5)}{match.group(4)}"

            # Carregar o arquivo Excel ignorando a primeira linha
            df = pd.read_excel(file_path, skiprows=1)

            # Remover linhas onde a coluna 'grupo' não está preenchida
            df = df[df['Grupo'].notna()]

            # Aplicar as transformações
            df = change_column_types(df, mapping_df)
            df = clean_and_prepare_csv_remove_all_currency_symbols(df)
            
            # Adicionar as colunas init_date e final_date
            df['init_date'] = init_date
            df['final_date'] = final_date

            # Gerar o caminho de saída
            output_file_name = f"{os.path.splitext(file_name)[0]}_csv.csv"
            output_file_path = os.path.join(output_folder, output_file_name)

            # Salvar o arquivo transformado em CSV
            df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

# Realizar o merge de todos os arquivos CSV na pasta de saída
merged_df = pd.DataFrame()
for file_name in os.listdir(output_folder):
    if file_name.endswith(".csv"):
        file_path = os.path.join(output_folder, file_name)
        temp_df = pd.read_csv(file_path)
        merged_df = pd.concat([merged_df, temp_df], ignore_index=True)

# Salvar o dataframe mesclado
merged_file_path = os.path.join(output_folder, "merged_output.csv")
merged_df.to_csv(merged_file_path, index=False, encoding='utf-8-sig')

print("Processamento concluído. Arquivos CSV gerados e mesclados na pasta de saída.")
