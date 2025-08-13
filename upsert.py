import pandas as pd 
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import numpy as np
from datetime import datetime

load_dotenv()

url_supabase = os.getenv("url_supabase")
key_supabase = os.getenv("key_supabase")
table_supabase = os.getenv("table_supabase")

supabase: Client = create_client(url_supabase, key_supabase)

# Carregar CSV
df = pd.read_csv('Extratos hist/merged_output.csv')

# Remove colunas "Unnamed" (geralmente criadas por excesso de vírgulas no CSV)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Adiciona uma coluna de 'data_upload'
df['data_upload'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Adicionando id (primary_key)
df['id'] = df['grupo'].astype(str) + df['final_date'].astype(str)

# Substitui NAN por None para compatibilidade com o Supabase
df = df.replace([np.nan, np.inf, -np.inf], None)

# Atualiza ou insere cada linha 
for _, row in df.iterrows():
    # Defina a chave única para update
    unique_key = {'id_slot': row['id_slot']}

    # Tenta atualziar, se não existir insere
    response = supabase.table(table_supabase).upsert(row.to_dict()).execute()

print("Upload concluído")