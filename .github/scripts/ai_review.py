import os
import requests
import subprocess
import sys

# Obtener el diff del PR
try:
    diff = subprocess.check_output(['git', 'diff', 'origin/main...HEAD']).decode('utf-8')
except subprocess.CalledProcessError:
    print("No se pudo obtener el diff. ¿Es un PR?")
    exit(0)

if not diff:
    print("No hay cambios para revisar.")
    exit(0)

diff = diff[:10000]

# Obtener y limpiar la API Key
api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()

if not api_key or api_key == "***":
    print("Error: La API Key de DeepSeek no está configurada correctamente.")
    sys.exit(1)

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
data = {
    'model': 'deepseek/deepseek-r1:free',
    'messages': [
        {'role': 'system', 'content': 'Eres un ingeniero de software senior revisando código. Analiza el siguiente diff y proporciona comentarios constructivos en español. Señala posibles bugs, mejoras de legibilidad y seguridad. Sé directo y técnico.'},
        {'role': 'user', 'content': f"Revisa este diff:\n\n{diff}"}
    ],
    'temperature': 0.2
}

print("Llamando a la API de DeepSeek (timeout 60s)...")
try:
    response = requests.post(
        'https://openrouter.ai/api/v1/chat/completions',
        headers=headers,
        json=data,
        timeout=60
    )
    response.raise_for_status()
except requests.exceptions.Timeout:
    print("Error: La API de DeepSeek tardó más de 60 segundos en responder.")
    sys.exit(1)
except requests.exceptions.RequestException as e:
    print(f"Error en la petición a DeepSeek: {e}")
    sys.exit(1)

review_text = response.json()['choices'][0]['message']['content']
print("Respuesta recibida de DeepSeek. Publicando comentario...")

# Publicar comentario en el PR
pr_number = os.environ.get('GITHUB_REF', '').split('/')[-2]
repo = os.environ.get('GITHUB_REPOSITORY')

comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
comment_headers = {
    'Authorization': f'token {os.environ["GITHUB_TOKEN"]}',
    'Accept': 'application/vnd.github.v3+json'
}
comment_data = {'body': f"## 🤖 Revisión de DeepSeek\n\n{review_text}"}

try:
    comment_response = requests.post(comment_url, headers=comment_headers, json=comment_data, timeout=30)
    comment_response.raise_for_status()
    print("Revisión publicada exitosamente.")
except requests.exceptions.RequestException as e:
    print(f"Error al publicar el comentario: {e}")
    sys.exit(1)
