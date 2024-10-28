import requests
from fastapi import HTTPException

API_URL = "https://apiexamen.compuflashgt.com/api"
USER_CREDENTIALS = {
    "usuario": "1000",
    "password": "!G4l3n0!",
    "api_key": "62245354621022924456"
}

def get_external_jwt_token():
    url = f"{API_URL}/login"
    response = requests.post(url, json=USER_CREDENTIALS)
    if response.status_code == 200:
        # Suponiendo que el token JWT se devuelve en el campo `access_token`
        return response.json().get("Token")
    else:
        raise HTTPException(status_code=401, detail="No se pudo autenticar con el servicio externo")
