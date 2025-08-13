import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def get_drive_service():
    """Autentica o usuário e retorna o objeto de serviço da API do Drive."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("drive", "v3", credentials=creds)

def list_files_and_folders(service):
    """Lista os primeiros 10 arquivos e pastas na raiz do Drive."""
    try:
        results = service.files().list(
            pageSize=10,
            fields="nextPageToken, files(id, name, mimeType)"
        ).execute()
        items = results.get("files", [])

        if not items:
            print("Nenhum arquivo ou pasta encontrado.")
        else:
            print("Arquivos e Pastas na raiz do Drive:")
            for item in items:
                print(f"  {item['name']} (ID: {item['id']})")
                
    except HttpError as error:
        print(f"Ocorreu um erro: {error}")

# ... (Seu código anterior, incluindo a função get_drive_service) ...

def list_files_in_folder(service, folder_id):
    """
    Lista todos os arquivos em uma pasta específica do Drive.
    
    Args:
        service: O objeto de serviço do Drive API.
        folder_id: O ID da pasta no Google Drive.
        
    Returns:
        Uma lista de dicionários com os metadados dos arquivos.
    """
    try:
        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            pageSize=10, # Limita para 10 arquivos
            fields="nextPageToken, files(id, name, mimeType)"
        ).execute()
        
        items = results.get("files", [])
        if not items:
            print("Nenhum arquivo encontrado na pasta.")
        else:
            print("Arquivos encontrados:")
            for item in items:
                print(f"  - {item['name']} (ID: {item['id']})")
        
        return items
        
    except HttpError as error:
        print(f"Ocorreu um erro ao listar os arquivos: {error}")
        return None

def download_file(service, file_id, file_name, path="./"):
    """
    Baixa um arquivo do Google Drive.
    
    Args:
        service: O objeto de serviço do Drive API.
        file_id: O ID do arquivo a ser baixado.
        file_name: O nome que o arquivo terá no seu diretório local.
        path: O caminho para salvar o arquivo.
    """
    try:
        request = service.files().get_media(fileId=file_id)
        
        # Cria o caminho completo para o arquivo
        file_path = os.path.join(path, file_name)
        
        with open(file_path, "wb") as fh:
            fh.write(request.execute())
        
        print(f"Arquivo '{file_name}' baixado com sucesso em '{file_path}'")
        
    except HttpError as error:
        print(f"Ocorreu um erro ao baixar o arquivo: {error}")

if __name__ == "__main__":
    
    # Lista de IDs das pastas que você quer acessar
    # Substitua os IDs de exemplo pelos IDs reais das suas pastas
    PASTAS = [
        {"nome": "Extratos Argentina 2023", "id": "1D2Yy2tZAoV0nfU7h13awvMEwPI6FXU8y"},
        {"nome": "Extratos Argentina 2024", "id": "1dAaXwiey2trUYdYXZYJ_Au7bciJckOJC"},
        {"nome": "Extratos Argentina 2025", "id": "1WEQspstyL15vYe9aJHGJzKBI7h8kjXzf"},
        {"nome": "Extratos Bolívia 2024", "id": "1YgUaRc11JEPgUvtKLX2fyK-EuUjEO3Gt"},
        {"nome": "Extratos Bolívia 2025", "id": "1CCAC0QGFioEwsvQFR2rFzy7g4DZvblcI"},
        {"nome": "Extratos Colombia 2023", "id": "1AOq4743CAFPhrjUc5qh3N4h6ArxxR1ea"},
        {"nome": "Extratos Colombia 2024", "id": "1QSXm5CBkVXAzUlwOaNZvqFkZ11Kn8Cpj"},
        {"nome": "Extratos Colombia 2025", "id": "1OwYIfzX8z6TMYNJDfnvU8lS8jvC4YTa5"},
        {"nome": "Extratos Venezuela 2023", "id": "1OixEw4JeObJXB9xhECXugRhd-35zhPAM"},
        {"nome": "Extratos Venezuela 2024", "id": "18bLBa6V7uIckgf0_lJXa7i8nkEWvLfUy"},
        {"nome": "Extratos Venezuela 2025", "id": "1XJGsszxeAZL5Hzk99Pk-d-_NqpBsVsyE"},
    ]
    
    # Obter o serviço do Google Drive uma única vez
    drive_service = get_drive_service()
    
    if drive_service:
        # Loop para processar cada pasta na lista
        for pasta in PASTAS:
            folder_name = pasta['nome']
            folder_id = pasta['id']
            
            print(f"\n--- Processando pasta: '{folder_name}' ---")

            # Cria um diretório local para salvar os arquivos da pasta atual
            output_path = os.path.join("./extratosgerais")
            os.makedirs(output_path, exist_ok=True)

            try:
                # 1. Liste os arquivos na pasta
                files_to_download = list_files_in_folder(drive_service, folder_id)

                if files_to_download:
                    # 2. Itere sobre a lista de arquivos e baixe-os
                    for file_info in files_to_download:
                        file_id = file_info['id']
                        file_name = file_info['name']
                        
                        # Baixa o arquivo para o diretório local criado
                        download_file(drive_service, file_id, file_name, path=output_path)
            
            except HttpError as error:
                print(f"Não foi possível processar a pasta '{folder_name}'. Verifique o ID. Erro: {error}")