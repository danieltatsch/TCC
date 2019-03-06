import requests

col = {}

col['cenario_nome'] = 'Sala'
# col['gateway_lugar'] = 'xablau'

url = 'http://localhost:5001/fim_cenario_medicao'
r = requests.post(url, json = col)

print(r)