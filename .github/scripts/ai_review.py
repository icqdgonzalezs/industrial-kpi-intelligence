import os
import subprocess

import requests

# Obtener el diff del PR
try:
    diff = subprocess.check_output(['git', 'diff', 'origin/main...HEAD']).decode('utf-8')
except subprocess.CalledProcessError:
    print("No se pudo obtener el diff. ¿Es un PR?")
    exit(0)

if not diff:
    print("No hay cambios para revisar.")
    exit(0)

# Limitar el tamaño del diff para no exceder tokens (ej. 10,000 caracteres)
diff = diff[:10000]

# Llamar a DeepSeek
headers = {
    'Authorization': f'Bearer {os.environ["DEEPSEEK_API_KEY"]}',
    'Content-Type': 'application/json'
}
data = {
    'model': 'deepseek-chat',
    'messages': [
        {'role': 'system', 'content': 'Eres un ingeniero de software senior revisando código. Analiza el siguiente diff y proporciona comentarios constructivos en español. Señala posibles bugs, mejoras de legibilidad y seguridad. Sé directo y técnico.'},
        {'role': 'user', 'content': f"Revisa este diff:\n\n{diff}"}
    ],
    'temperature': 0.2
}

response = requests.post('https://api.deepseek.com/chat/completions', headers=headers, json=data)
response.raise_for_status()
review_text = response.json()['choices'][0]['message']['content']

# Publicar comentario en el PR
pr_number = os.environ.get('GITHUB_REF', '').split('/')[-2]
repo = os.environ.get('GITHUB_REPOSITORY')

comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
comment_headers = {
    'Authorization': f'token {os.environ["GITHUB_TOKEN"]}',
    'Accept': 'application/vnd.github.v3+json'
}
comment_data = {'body': f"## 🤖 Revisión de DeepSeek\n\n{review_text}"}

requests.post(comment_url, headers=comment_headers, json=comment_data)
print("Revisión publicada exitosamente.")
