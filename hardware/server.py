#!/usr/bin/python

__author__ = "Daniel Tatsch"
__date__ = "26/02/2019"

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
# auth = HTTPBasicAuth()
#import std
import mysql.connector
import subprocess
import os
import time
import math
import csv
import io

app = Flask(__name__)
CORS(app)

def abre_mysql():
    cnx = mysql.connector.connect(
	user='daniel',
	password='daniel',
	host='localhost',
	database='TCC'
    )
    cr = cnx.cursor(buffered = True)
    return (cr,cnx)


def fecha_mysql(cr, cnx):
    cr.close()
    cnx.close()

@app.route('/retorna_gw',methods=['GET'])
def retorna_gw():

    (cr,cnx) = abre_mysql()

    query = ("SELECT * FROM Gateway")
    cr.execute(query)

    gws = cr.fetchall()
    gw = []
    for c in gws:
    	g = {
    		'idGateway': c[0],
    		'mac': c[1],
    		'lugar': c[2]
    	}
    	gw.append(g)
    return jsonify(gw)

@app.route('/cadastra_nodo',methods=['POST'])
def cadastraNodo():
    if not request.json:
        abort(400);
    nodo_mac = request.json['nodo_mac']

    (cr,cnx) = abre_mysql()

    query = ("SELECT * FROM Nodo WHERE mac = ('%s')" % nodo_mac)
    cr.execute(query)

    if cr.rowcount != 0:
        fecha_mysql(cr,cnx)
        return jsonify({'ok': '1'}), 400

    query = ("INSERT INTO Nodo (mac) VALUES ('%s')" % nodo_mac)
    cr.execute(query)
    cnx.commit()
    fecha_mysql(cr,cnx)
    return jsonify({'ok': '1'}), 201

# Garante que nao exista gws com mesmo mac e que nao tenha mais de um gw no mesmo lugar
@app.route('/cadastra_gateway',methods=['POST'])
def cadastraGateway():
    if not request.json:
        abort(400);
    gateway_mac = request.json['gateway_mac']
    gateway_lugar  = request.json['gateway_lugar']

    (cr,cnx) = abre_mysql()

    query = ("SELECT * FROM Gateway WHERE mac = ('%s') OR lugar = ('%s')" % (gateway_mac, gateway_lugar))
    cr.execute(query)

    if cr.rowcount != 0:
        fecha_mysql(cr,cnx)
        return jsonify({'ok': '1'}), 400

    query = ("INSERT INTO Gateway (mac, lugar) VALUES ('%s','%s')" % (gateway_mac, gateway_lugar))
    cr.execute(query)
    cnx.commit()
    fecha_mysql(cr,cnx)
    return jsonify({'ok': '1'}), 201

# Garante que so exista um cenario com nome = cenario_nome
@app.route('/cadastra_cenario',methods=['POST'])
def cadastraCenario():
    if not request.json:
        abort(400);
    cenario_nome = request.json['cenario_nome']

    (cr,cnx) = abre_mysql()

    query = ("SELECT * FROM Cenario WHERE nome = ('%s')" % cenario_nome)
    cr.execute(query)

    if cr.rowcount != 0:
        fecha_mysql(cr,cnx)
        return jsonify({'ok': '1'}), 400

    query = ("INSERT INTO Cenario (nome) VALUES ('%s')" % (cenario_nome))
    cr.execute(query)
    cnx.commit()
    fecha_mysql(cr,cnx)
    return jsonify({'ok': '1'}), 201

# Cadastra setor na Tab Setor e na tab CenarioSetor, caso ja exista na tab 
# Setor atualiza a tab CenarioSetor com o Cenario que se deseja cadastrar
@app.route('/cadastra_setor',methods=['POST'])
def cadastraSetor():
    if not request.json:
        abort(400);
    setor_nome   = request.json['setor_nome']
    cenario_nome = request.json['cenario_nome']

    ids = [] # ids[1] = idcenario, ids[0] = idSetor

    (cr,cnx) = abre_mysql()
 
    query = ("SELECT * FROM Cenario WHERE nome = ('%s')" % cenario_nome)
    cr.execute(query)

    if cr.rowcount == 0:
        fecha_mysql(cr,cnx) 
        return jsonify({'ok': '1'}), 404

    resultados = cr.fetchall()
    ids.append(int(resultados[0][0]))

    query = ("SELECT * FROM Setor WHERE nome = ('%s')" % setor_nome)
    cr.execute(query)

    if cr.rowcount == 0:
        query = ("INSERT INTO Setor (nome) VALUES ('%s')" % setor_nome)
        cr.execute(query)
        cnx.commit()

        query = ("SELECT * FROM Setor WHERE nome = ('%s')" % setor_nome)
        cr.execute(query)
    
    resultados = cr.fetchall()
    ids.append(int(resultados[0][0]))

    try:
        query = ("INSERT INTO CenarioSetor (idCenario, idSetor) VALUES ('%d', '%d')" % (ids[0], ids[1]))
        cr.execute(query)
        cnx.commit()
        fecha_mysql(cr,cnx)
        return jsonify({'ok': '1'}), 201
    except mysql.connector.Error as error:
        print ("ERROR {}".format(error))
        fecha_mysql(cr,cnx)
        return jsonify({'ok': '1'}), 400

# Garante que so exista um cenario com nome = cenario_nome
@app.route('/inicio_cenario_medicao',methods=['POST'])
def inicioCenarioMedicao():
	if not request.json:
		abort(400);
	cenario_nome = request.json['cenario_nome']
	setor_nome = request.json['setor_nome']
	(cr,cnx) = abre_mysql()

	query = ("SELECT * FROM Cenario WHERE nome = ('%s')" % cenario_nome)
	cr.execute(query)
	if cr.rowcount == 0:
		fecha_mysql(cr,cnx)
		return jsonify({'ok': '1'}), 400

	idCenario = int (cr.fetchall()[0][0])

	# se existir alguma medicao que nao encerrou ainda
	query = ("SELECT fim FROM GerMedicao WHERE idCenario = '%d' AND fim IS NULL" % idCenario)
	cr.execute(query)

	if cr.rowcount != 0:
		fecha_mysql(cr,cnx)
		return jsonify({'ok': '1'}), 401

	query = ("SELECT * FROM Setor WHERE nome = '%s'" % setor_nome)
	cr.execute(query)

	if cr.rowcount == 0:
		fecha_mysql(cr,cnx)
		return jsonify({'ok': '1'}), 402

	idSetor = int (cr.fetchall()[0][0])

	#Verificar se o Setor esta  presente no cenario em questao
	query = ("SELECT * FROM CenarioSetor WHERE idCenario = '%d' AND idSetor = '%d'" % (idCenario, idSetor))
	cr.execute(query)
	if cr.rowcount == 0:
		fecha_mysql(cr,cnx)
		return jsonify({'ok': '1'}), 403

	query = ("INSERT INTO GerMedicao (idCenario, idSetor, inicio, fim) VALUES ('%d', '%d', NOW(), NULL)" % (idCenario, idSetor))
	cr.execute(query)
	cnx.commit()
	fecha_mysql(cr,cnx)
	return jsonify({'ok': '1'}), 201

#COMO NO inicio_cenario_medicao JA PROIBE INICIAR MEDICAO MAIS DE UMA MEDICAO AO MESMO TEMPO, AQUI SO ENCERRA A MEDICAO ATUAL
@app.route('/fim_cenario_medicao',methods=['POST'])
def fimCenarioMedicao():
	# if not request.json:
	# 	abort(400);
	(cr,cnx) = abre_mysql()

	query = ("SELECT * FROM GerMedicao WHERE fim IS NULL")
	cr.execute(query)
	# Caso nao exista uma medicao iniciada com idCenario ou caso ela ja tenha siod encerrada
	if cr.rowcount == 0:
		fecha_mysql(cr,cnx)
		return jsonify({'ok': '1'}), 401

	idGerMedicao = int (cr.fetchall()[0][0])

	query = ("UPDATE GerMedicao SET fim = NOW() WHERE idGerMedicao = '%d'" % idGerMedicao)
	cr.execute(query)
	cnx.commit()
	fecha_mysql(cr,cnx)
	return jsonify({'ok': '1'}), 201

# Fase de treino -> json.lugar valido
# Fase de testes -> json.lugar: string que indica vazio
# Com a string especial a selecao dos dados de treino e teste fica mais clara
@app.route('/insere_medicao',methods=['POST'])
def insereMedicao():
	if not request.json:
		abort(400);
	gateway_mac = request.json['gateway_mac']
	nodo_mac    = request.json['nodo_mac']
	rssi        = request.json['rssi']
	count        = request.json['count']
        
        #print(request.json, file=std.err)

	(cr,cnx) = abre_mysql()

	query = ("SELECT NOW()")
	cr.execute(query)
	time_med = str(cr.fetchall()[0][0])

	#Verifica se existe algum GerMedicao em andamento
	query = ("SELECT * FROM GerMedicao WHERE DATE_FORMAT(inicio, '%%Y %%m %%d %%H %%i %%S') < DATE_FORMAT('%s', '%%Y %%m %%d %%H %%i %%S') AND fim IS NULL" % time_med)
	cr.execute(query)
	if cr.rowcount == 0:
		fecha_mysql(cr,cnx)
		return jsonify({'ok': '1'}), 400

	idGerMed = cr.fetchall()[0][0]

	#Verifica se o gateway ja esta cadastrado, se nao estiver, retorna cod de erro
	query = ("SELECT * FROM Gateway WHERE mac = '%s'" % gateway_mac)
	cr.execute(query)
	if cr.rowcount == 0:
		fecha_mysql(cr,cnx)         
		return jsonify({'ok': '1'}), 401
	idGateway = int (cr.fetchall()[0][0])    

	# Verifica se o Nodo ja esta cadastrado, se nao estiver, retorna cod de erro
	query = ("SELECT * FROM Nodo WHERE mac = '%s'" % nodo_mac)
	cr.execute(query)
	if cr.rowcount == 0:
		fecha_mysql(cr,cnx)         
		return jsonify({'ok': '1'}), 402
	idNodo = int (cr.fetchall()[0][0])

	query = ("INSERT INTO Medicao (idGateway, idNodo, rssi, data, idGerMedicao, count) VALUES ('%d','%d','%d','%s','%d','%d')" % (idGateway, idNodo, rssi, time_med, idGerMed, count))
	cr.execute(query)
	cnx.commit()
	fecha_mysql(cr,cnx)
	return jsonify({'ok': '1'})

@app.route('/gera_csv',methods=['POST'])
def geraCsv():
	if not request.json:
	    abort(400);
	cenario_nome = request.json['cenario_nome']
	nodo_mac = request.json['nodo_mac']

	#SELECIONAR DE ACORDO COM O CENARIO PASSADO COMO PARAMETRO
	(cr,cnx) = abre_mysql()

	query = ("SELECT * FROM Cenario WHERE nome = '%s'" % str(cenario_nome))
	cr.execute(query)
	if cr.rowcount == 0:
	    fecha_mysql(cr,cnx)
	    return jsonify({'ok': '1'}), 402

	query = ("SELECT * FROM Nodo WHERE mac = '%s'" % str(nodo_mac))
	cr.execute(query)
	if cr.rowcount == 0:
	    fecha_mysql(cr,cnx)
	    return jsonify({'ok': '1'}), 401

	query = ("SELECT fim FROM GerMedicao g INNER JOIN Cenario c ON g.idCenario = c.idCenario WHERE c.nome = '%s' AND fim IS NULL" % str(cenario_nome))
	cr.execute(query)

	if cr.rowcount != 0:
	    fecha_mysql(cr,cnx)
	    return jsonify({'ok': '1'}), 405

	query = ("SELECT m.idGateway, m.rssi, s.nome, m.count FROM Medicao m INNER JOIN GerMedicao g ON m.idGerMedicao = g.idGerMedicao INNER JOIN Setor s ON g.idSetor = s.idSetor WHERE g.idGerMedicao = (SELECT MAX(idGerMedicao) From GerMedicao)")
	cr.execute(query)
	if cr.rowcount == 0:
	    fecha_mysql(cr,cnx)
	    return jsonify({'ok': '1'}), 403

	result = cr.fetchall()
	# print("O QUE VEIO DO SELECT: " + str(result))
	# result = [(1, -43, 'mesa', 1), (3, -70, 'mesa', 0), (2, -63, 'mesa', 1), (3, -91, 'mesa', 1), (1, -63, 'mesa', 0), (1, -49, 'mesa', 2), (2, -59, 'mesa', 2), (3, -85, 'mesa', 2), (2, -47, 'mesa', 3), (3, -88, 'mesa', 3), (1, -33, 'mesa', 4), (2, -55, 'mesa', 4), (3, -94, 'mesa', 4) , (3, -94, 'mesa', 5), (3, -94, 'mesa', 5), (2, -88, 'telefone', 6), (1, -99, 'telefone', 6), (3, -77, 'telefone', 6), (3, -22, 'telefone', 7), (1, -33, 'telefone', 7), (2, -44, 'telefone', 7)]
	# print("INVENTADO: " + str(result))

	out = parseToCSV(result)

	with open('csv_TESTE2.csv', 'w', newline='') as csvfile:
	    fieldnames = ['GW1', 'GW2', 'GW3', 'Setor']
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	    writer.writeheader()
	    writer.writerows(out)    

	fecha_mysql(cr,cnx)
	return jsonify({'ok': '1'}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def parseToCSV(result):
	a = []

	# pega os valores dos contadores das coletas
	for i in result:
		a.append(i[3])	

	# ordena e tira valores repetidos
	b = sorted(set(a))
	c = b.copy()

	# verifica se todos os gws tem valor do contador e os exclui senao tiverem
	i = 0
	while i <= max(b):
		count = a.count(i)
		if count != 3:
			c.remove(i)
		i += 1
	# pega somente as tuplas com valores de count correspondentes a c
	prev = [elem for elem in result if elem[3] in c]

	# ordena lista de tuplas de acordo com idGateway	
	prev = sorted(prev, key=lambda x: x[0])

	d = {}
	
	d['GW1'] = []
	d['GW2'] = []
	d['GW3'] = []
	d['Setor'] = []
	
	# preenche os valores de rssi dos gws em suas respectivas listas
	for i in prev:
		if i[0] == 1:
			d['GW1'].append(i[1])
		if i[0] == 2:
			d['GW2'].append(i[1])
		if i[0] == 3:
			d['GW3'].append(i[1])		
		d['Setor'].append(i[2])
	print("RSSI POR GWs: " + str(d))
	
	out = []
	o = {}
	i = 0
	while i < len(d['GW1']):
		o['GW1'] = d['GW1'][i]
		o['GW2'] = d['GW2'][i]
		o['GW3'] = d['GW3'][i]
		o['Setor'] = d['Setor'][i]
		i += 1
		print(o)
		out.insert(0, o.copy())
	return out

if __name__ == "__main__":
    print ("Servidor no ar!")
    app.run(host="0.0.0.0", port=5001, debug=True)
