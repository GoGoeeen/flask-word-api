import os
from msal import ConfidentialClientApplication
import requests
from dotenv import load_dotenv

# .env-Datei laden
load_dotenv()

# Azure AD-Konfigurationswerte aus der .env-Datei laden
tenant_id = os.getenv('TENANT_ID')
client_id = os.getenv('CLIENT_ID')
sp_client_secret = os.getenv('SP_CLIENT_SECRET')
drive_id = os.getenv('DRIVE_ID')

# Authority und Scopes
authority = f"https://login.microsoftonline.com/{tenant_id}"
scopes = ["https://graph.microsoft.com/.default"]

# MSAL Authentifizierung
app = ConfidentialClientApplication(
    client_id=client_id,
    client_credential=sp_client_secret,
    authority=authority
)

result = app.acquire_token_for_client(scopes=scopes)
if "access_token" in result:
    print("Authentifizierung erfolgreich!")
else:
    print("Authentifizierung fehlgeschlagen!")
    print(result)
    exit()

# Funktion zum Hochladen der Datei zu SharePoint
def upload_to_sharepoint(file_path, file_name):
    upload_url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/Operations/9. Saved Docx/{file_name}:/content"

    headers = {
        "Authorization": f"Bearer {result['access_token']}",
        "Content-Type": "application/octet-stream"
    }

    with open(file_path, "rb") as file:
        response = requests.put(upload_url, headers=headers, data=file)

    if response.status_code == 201:
        print(f"Datei '{file_name}' wurde erfolgreich hochgeladen!")
    else:
        print(f"Fehler beim Hochladen der Datei: {response.status_code}")
        print(response.json())