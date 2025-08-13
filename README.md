# Automatização de Extratos Google Drive + Supabase

Este projeto automatiza o download de extratos financeiros do Google Drive, realiza tratamento e padronização dos dados, gera arquivos consolidados e faz o upload dos resultados para uma tabela no Supabase.

## Funcionalidades

- Autenticação e acesso ao Google Drive via API.
- Download automático de arquivos `.xlsx` de múltiplas pastas do Drive.
- Padronização e limpeza dos dados dos extratos.
- Geração de arquivo CSV consolidado (`merged_output.csv`).
- Upload dos dados para uma tabela no Supabase, com atualização de registros existentes e inserção de novos.
- Controle de execução via agendamento (cron) em VPS Linux.

## Estrutura dos Principais Arquivos

- **drive_acess.py**  
  Script para autenticação, listagem e download dos arquivos do Google Drive.

- **rename_columns.py**  
  Script para padronização dos nomes de colunas e tipos dos dados dos extratos baixados.

- **upsert.py**  
  Script para upload dos dados tratados para o Supabase, utilizando upsert com chave única.

- **.env**  
  Arquivo de variáveis de ambiente para configuração do acesso ao Supabase.

- **requirements.txt**  
  Lista de dependências do projeto.

## Como Usar

### 1. Clone o repositório

```bash
git clone https://github.com/seuusuario/automatizacao_dados.git
cd automatizacao_dados
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o acesso ao Google Drive

- Coloque o arquivo `client_secret.json` na raiz do projeto.
- Na primeira execução, será gerado o `token.json` após autenticação.

### 4. Configure o Supabase

- Preencha o arquivo `.env` com suas credenciais do Supabase:
  ```
  url_supabase=https://<YOUR_PROJECT_ID>.supabase.co
  key_supabase=<YOUR_SUPABASE_API_KEY>
  table_supabase=<NOME_DA_TABELA>
  ```

### 5. Execute os scripts

1. **Baixar arquivos do Google Drive**
   ```bash
   python drive_acess.py
   ```

2. **Padronizar e consolidar os dados**
   ```bash
   python rename_columns.py
   ```

3. **Fazer upload para o Supabase**
   ```bash
   python upsert.py
   ```

### 6. (Opcional) Agendar execução automática

No Linux, edite o crontab:
```bash
crontab -e
```
Adicione, por exemplo:
```
0 2 * * * /usr/bin/python3 /caminho/para/drive_acess.py
```

## Observações

- Certifique-se de que as colunas do Supabase estejam corretamente configuradas, incluindo a chave única para o upsert.
- O projeto pode ser adaptado para outros tipos de extratos ou bancos de dados.
- Para dúvidas sobre permissões, autenticação ou agendamento, consulte a documentação oficial do Google Drive API e Supabase.

---

**Autor:**  
José Felipe Pinto Faria
https://www.linkedin.com/in/josefelipepintofaria/
