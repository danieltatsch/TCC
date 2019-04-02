import os
import time
import requests

class counter:
	count = 0

def sendJson(json_data, url_path):
	url = 'http://192.168.0.14:5001/' + url_path
	
	if json_data is not None:
		r = requests.post(url, json = json_data)
	else: 
		r = requests.post(url)

	return r

def iniciaMedicao(cenario_nome, setor_nome):
	json_data = {}
	
	json_data['cenario_nome'] = cenario_nome
	json_data['setor_nome'] = setor_nome

	url_path = 'inicio_cenario_medicao'
	return sendJson(json_data, url_path)

def finalizaMedicao():
	url_path = 'fim_cenario_medicao'

	return sendJson(None, url_path)

def insereMedicao(gateway_mac, nodo_mac, rssi):
	json_data = {}

	json_data['gateway_mac'] = gateway_mac
	json_data['nodo_mac'] = nodo_mac
	json_data['rssi'] = rssi
	json_data['count'] = int(counter.count)

	counter.count += 1
	url_path = 'insere_medicao'
	return sendJson(json_data, url_path)

def geraCSV(cenario_nome, nodo_mac):
	json_data = {}

	json_data['cenario_nome'] = cenario_nome
	json_data['nodo_mac'] = nodo_mac

	url_path = 'gera_csv'
	return sendJson(json_data, url_path)

def formateAndClean(delay_secs):
	if (not str(delay_secs).isdigit()):
		return
	print("-------------------------------------------------------")
	time.sleep(delay_secs)
	os.system('clear')
	print("-------------------------------------------------------")

if __name__ == "__main__":
	os.system('clear')
	print("-------------------Rodando aplicacao-------------------")
	while(True):
		i = input("Selecione a operacao:\n 1 - Iniciar Coletas\n 2 - Inserir Dados (Teste)\n 3 - Finalizar Coletas\n 4 - Gerar CSV\n 5 - Sair\n\n")
		if not i.isdigit(): 
			print("Valor invalido")
			formateAndClean(2)
			continue
		elif int(i)== 1:
			cenario_nome = input("Insira o nome do cenario: ")
			setor_nome = input("Insira o nome do setor: ")
			print(iniciaMedicao(cenario_nome, setor_nome))
		elif int(i)== 2:
			gateway_mac = input("Insira o MAC do gateway: ")
			nodo_mac = input("Insira o MAC do nodo: ")
			rssi = input("Insira um valor de RSSI: ")
			if not rssi.lstrip('-').isdigit(): 
				print("\nValor invalido")
				formateAndClean(2)
				continue
			print(insereMedicao(gateway_mac, nodo_mac, rssi))
		elif int(i)== 3:
			print(finalizaMedicao())
			print("\nFinalizando medicoes...")
			print("As proximas medidas serao descartadas ate que se inicie um novo ciclo")
			formateAndClean(5)
			continue
		elif int(i)== 4:
			cenario_nome = input("Insira o nome do cenario: ")
			nodo_mac = input("Insira o MAC do nodo: ")
			print(geraCSV(cenario_nome, nodo_mac))

			print("\nArquivo CSV gerado!")
			print("Verificar no servidor")
		elif int(i)== 5:
			print("-------------------------------------------------------")
			break
		formateAndClean(3)