import requests

# Defina a URL do endpoint
url = "http://127.0.0.1:8000/api/paciente/"

# Adicione seu token JWT aqui
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyODE3ODQyLCJpYXQiOjE3MzI4MTc1NDIsImp0aSI6ImE5NGFkMWVhY2VlNzQzNDM4NGU4YTNmZTY2YzZkMWQwIiwidXNlcl9pZCI6MX0.Go78zgjXnUJWS3XkwYubnLbarBedJ8omuU8d_76OYqs"
}

# Envia a requisição GET
response = requests.get(url, headers=headers)

# Verifica a resposta
if response.status_code == 200:
    print("Pacientes:", response.json())
else:
    print(f"Erro {response.status_code}: {response.text}")
