#!/usr/bin/python

__author__ = "Daniel Tatsch"
__date__ = "26/02/2019"

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
# from flask_httpauth import HTTPBasicAuth
# auth = HTTPBasicAuth()

import mysql.connector
import subprocess
import os
import time
import math

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
        print "ERROR {}".format(error)
        fecha_mysql(cr,cnx)
        return jsonify({'ok': '1'}), 400


# Fase de treino -> json.lugar valido
# Fase de testes -> json.lugar: string que indica vazio
# Com a string especial a selecao dos dados de treino e teste fica mais clara
@app.route('/insere_medicao',methods=['POST'])
def insereMedicao():
    if not request.json:
        abort(400);
    gateway_mac = request.json['gateway_mac']
    Nodo_mac    = request.json['nodo_mac']
    rssi        = request.json['rssi']
    lugar       = request.json['lugar']

    (cr,cnx) = abre_mysql()

    #Verifica se o gateway ja estacadastrado, se nao estiver, retorna cod de erro
    query = ("SELECT * FROM Gateway WHERE mac = '%s'" % gateway_mac)
    cr.execute(query)
    if cr.rowcount == 0:
        fecha_mysql(cr,cnx)         
        return jsonify({'ok': '1'}), 400

    # Verifica se o Nodo ja esta cadastrado, se nao estiver, retorna cod de erro
    query = ("SELECT * FROM Nodo WHERE mac = '%s'" % nodo_mac)
    cr.execute(query)
    if cr.rowcount == 0:
        fecha_mysql(cr,cnx)         
        return jsonify({'ok': '1'}), 400

    query = ("INSERT INTO Medicao (Gateway_mac, Nodo_mac, rssi, Lugar_nome, data) VALUES ('%s','%s','%d', NOW())" % (gateway_mac, nodo_mac, rssi))
    cr.execute(query)
    cnx.commit()
    fecha_mysql(cr,cnx)
    return jsonify({'ok': '1'}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    print ("Servidor no ar!")
    app.run(host="localhost", port=5001, debug=True)
