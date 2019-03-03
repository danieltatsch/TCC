#!/usr/bin/python

__author__ = "Daniel Tatsch"
__date__ = "09/06/2018"

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
	user='jit_user',
	password='1234',
	host='localhost',
	database='jit'
    )
    cr = cnx.cursor(buffered = True)
    return (cr,cnx)


def fecha_mysql(cr, cnx):
    cr.close()
    cnx.close()

@app.route('/cadastro',methods=['POST'])
def cadastro():
    if not request.json:
        abort(400);
    nome = request.json['nome']
    email = request.json['email']
    senha = request.json['senha']
    num_serie = request.json['num_serie']
    nome_ec = request.json['nome_ec']

    (cr,cnx) = abre_mysql()

    query = ("SELECT idUsuario FROM Usuario WHERE email = '%s'" % email)
    cr.execute(query)
    linhas = cr.rowcount

    #verifica se o email ainda nao esta em uso
    if (linhas == 0):
        query = ("SELECT * FROM Usuario")
        cr.execute(query)
        linhas_id = cr.rowcount

        if (linhas_id == 0):
            #Insere superusuario
            query = ("INSERT INTO Usuario (nome, email, senha, superusuario) VALUES ('%s','%s','%s', 1)" % (nome, email, senha))
            cr.execute(query)
            cnx.commit()

            #Insere usuario anonimo para atribuir a registros de consumo sem usuarios validos
            query = ("INSERT INTO Usuario (idUsuario, nome, email, senha, superusuario) VALUES (999, 'ANONIMO', 'usuario@anonimo.com', 'XXX', 0)")
            cr.execute(query)
            cnx.commit()
        else:
            #Insere usuario comum
            query = ("INSERT INTO Usuario (nome, email, senha, superusuario) VALUES ('%s','%s','%s', 0)" % (nome, email, senha))
            cr.execute(query)
            cnx.commit()

        query = ("SELECT * FROM Estacao_central WHERE num_serie= '%d'" % int(num_serie))
        cr.execute(query)
        linhas = cr.rowcount
        #verifica se a estacao central ainda nao esta cadastrada
        if (linhas == 0):
            #insere estacao_central
            query = ("INSERT INTO Estacao_central (num_serie, nome_ec) VALUES ('%d', '%s')" % (int(num_serie), nome_ec))
            cr.execute(query)
            cnx.commit()

        query = ("SELECT MAX(idUsuario) FROM Usuario WHERE idUsuario != 999")
        cr.execute(query)
        max_id = cr.fetchall()
        #Associa id do usuario com a estacao central correspondente
        query = ("INSERT INTO Ger_cadastros (Usuario_idUsuario, Estacao_central_num_serie) VALUES ('%d','%d')" % (max_id[0][0], int(num_serie)))
        cr.execute(query)
        cnx.commit()
        fecha_mysql(cr,cnx)
        return jsonify({'ok': '1'}), 201
    else:
        fecha_mysql(cr,cnx)
        return jsonify({'ok': '1'}), 304

@app.route('/login',methods=['POST'])
def login():
    if not request.json:
        abort(400);
    email = request.json['email']
    senha = request.json['senha']

    (cr,cnx) = abre_mysql()

    query = ("SELECT idUsuario FROM Usuario WHERE email = '%s' and senha = '%s'" % (email, senha))
    cr.execute(query)
    linhas = cr.rowcount
    res = cr.fetchall()

    fecha_mysql(cr,cnx)
    #Se nao possuir um cadastro com os dados passados
    if (linhas == 0):
        fecha_mysql(cr,cnx)
        return jsonify({'ok': '1'}), 401
    else:
        usuario_id = []
        usuario_id = {
            'estacao_central': res[0][0]}
        return jsonify(usuario_id)
        # return jsonify({'ok': '1'}), 201

@app.route('/insereconsumo',methods=['POST'])
def insere_consumo():
    if not request.json:
        abort(400);
    data = request.json['data']
    duracao = request.json['duracao']
    consumoAgua = request.json['consumoAgua']
    consumoEnergia = request.json['consumoEnergia']
    num_serie = request.json['num_serie']
    usuario_id = request.json['usuario_id']

    (cr,cnx) = abre_mysql()

    print('DATA: ' + data)
    query = ("SELECT MAX(data) FROM Custo WHERE DATE_FORMAT(data, '%%Y %%m %%d') <= DATE_FORMAT('%s', '%%Y %%m %%d')" % data)
    cr.execute(query)
    custo_data = cr.fetchall()
    print('Custo_data: ' + str(custo_data[0][0]))

    #Verifica se existe cadastro com o usuario e a estacao central recebidos
    query = ("SELECT * FROM Ger_cadastros WHERE Usuario_idUsuario = '%d' AND Estacao_central_num_serie = '%d'" % (int(usuario_id), int(num_serie)))
    cr.execute(query);

    linhas = cr.rowcount
    if (linhas != 0):
        query = ("INSERT INTO Banho (data, duracao, consumoAgua, consumoEnergia, Custo_data, ec_num_serie, usuario_id) VALUES ('%s','%f','%f','%f','%s','%d','%d')" % (data, float(duracao), float(consumoAgua), float(consumoEnergia), custo_data[0][0], int(num_serie), int(usuario_id)))
        cr.execute(query)
        cnx.commit()
        fecha_mysql(cr,cnx)
        return jsonify({'ok': '1'}), 201
    else:#Associa consumo ao usuario anonimo
        query = ("INSERT INTO Banho (data, duracao, consumoAgua, consumoEnergia, Custo_data, ec_num_serie, usuario_id) VALUES ('%s','%f','%f','%f','%s','%d',999)" % (data, float(duracao), float(consumoAgua), float(consumoEnergia), custo_data[0][0], int(num_serie)))
        cr.execute(query)
        cnx.commit()
        fecha_mysql(cr,cnx)
        return jsonify({'ok': 'Not Modified'}), 304

@app.route('/cadastraestacao/',methods=['POST'])
def cadastra_estacao():
    if not request.json:
        abort(400);
    num_serie = request.json['num_serie']
    nome_ec = request.json['nome_ec']
    usuario_id = request.json['usuario_id']

    (cr,cnx) = abre_mysql()

    query = ("SELECT superusuario FROM Usuario WHERE idUsuario = '%d'" % int(usuario_id))
    cr.execute(query)
    resultados = cr.fetchall()

    sUsuario = int(resultados[0][0])

    if (sUsuario == 1): #se for superusuario
        query = ("SELECT * FROM Estacao_central WHERE num_serie = '%d'" % int(num_serie))
        cr.execute(query)
        linhas = cr.rowcount
        if (linhas == 0): #se a estacao ainda nao estiver cadastrada
            query = ("INSERT INTO Estacao_central (num_serie, nome_ec) VALUES ('%d', '%s')" % (int(num_serie), nome_ec))
            cr.execute(query)
            cnx.commit()
            #cadastra usuario e estacao central na tabela Ger_cadastros
            query = ("INSERT INTO Ger_cadastros (Usuario_idUsuario, Estacao_central_num_serie) VALUES ('%d','%d')" % (int(usuario_id), int(num_serie)))
            cr.execute(query)
            cnx.commit()
            fecha_mysql(cr,cnx)
            return jsonify({'ok': '1'}), 201
        else:
            query = ("SELECT * FROM Ger_cadastros WHERE Usuario_idUsuario = '%d' AND Estacao_central_num_serie = '%d'" % (int(usuario_id), int(num_serie)))
            cr.execute(query)
            linhas = cr.rowcount
            if (linhas == 0):
                #Apenas insere usuario e estacao central no gerenciador de cadastros
                query = ("INSERT INTO Ger_cadastros (Usuario_idUsuario, Estacao_central_num_serie) VALUES ('%d','%d')" % (int(usuario_id), int(num_serie)))
                cr.execute(query)
                cnx.commit()
                fecha_mysql(cr,cnx)
                return jsonify({'ok': 'Not Modified'}), 304
            else:
                fecha_mysql(cr,cnx)
                print('Cadastro ja existe ')
                return jsonify({'ok': 'Not Modified'}), 304
    else:
        fecha_mysql(cr,cnx)
        return jsonify({'ok': 'Unauthorized'}), 401

@app.route('/registraestacao/',methods=['POST'])
def registra_estacao():
    if not request.json:
        abort(400);
    num_serie = request.json['num_serie']
    usuario_id = request.json['usuario_id']

    (cr,cnx) = abre_mysql()

    query = ("SELECT * FROM Estacao_central WHERE num_serie = '%d'" % int(num_serie))
    cr.execute(query)
    linhas = cr.rowcount

    if (linhas == 0): #se a estacao ainda nao estiver cadastrada
        fecha_mysql(cr,cnx)
        return jsonify({'ok': 'Not Modified'}), 304
    else:
        query = ("SELECT * FROM Ger_cadastros WHERE Usuario_idUsuario = '%d' and Estacao_central_num_serie = '%d'" % (int(usuario_id), int(num_serie)))
        cr.execute(query)
        linhas = cr.rowcount
        if (linhas == 0):
            #cadastra usuario e estacao central na tabela Ger_cadastros
            query = ("INSERT INTO Ger_cadastros (Usuario_idUsuario, Estacao_central_num_serie) VALUES ('%d','%d')" % (int(usuario_id), int(num_serie)))
            cr.execute(query)
            cnx.commit()
            fecha_mysql(cr,cnx)
            return jsonify({'ok': '1'}), 201
        else:
            fecha_mysql(cr,cnx)
            return jsonify({'ok': 'Not Modified'}), 201

@app.route('/atualizacusto/',methods=['POST'])
def atualiza_custo():
    if not request.json:
        abort(400);
    custoAgua = request.json['custoAgua']
    custoEnergia = request.json['custoEnergia']
    usuario_id = request.json['usuario_id']

    (cr,cnx) = abre_mysql()

    query = ("SELECT superusuario FROM Usuario WHERE idUsuario = '%d'" % int(usuario_id))
    cr.execute(query)
    resultados = cr.fetchall()

    sUsuario = int(resultados[0][0])

    if (sUsuario == 1): #se for superusuario
        query = ("SELECT CURRENT_DATE")
        cr.execute(query)
        res = cr.fetchall()
        hoje = str(res[0][0])

        query = ("SELECT * FROM Custo WHERE DATE_FORMAT(data, '%%Y %%m %%d') = DATE_FORMAT('%s', '%%Y %%m %%d')" % hoje)
        cr.execute(query)
        linhas = cr.rowcount

        if (linhas == 0):
            query = ("INSERT INTO Custo (data, custoAgua, custoEnergia) VALUES (CURRENT_DATE, '%f', '%f')" % (float(custoAgua), float (custoEnergia)))
            cr.execute(query)
            cnx.commit()
            fecha_mysql(cr,cnx)
            return jsonify({'ok': '1'}), 201
        else:
            query = ("UPDATE Custo SET custoAgua = '%f', custoEnergia = '%f' WHERE DATE_FORMAT(data, '%%Y %%m %%d') = DATE_FORMAT('%s', '%%Y %%m %%d')" % (float(custoAgua), float(custoEnergia), hoje))
            cr.execute(query)
            cnx.commit()
            fecha_mysql(cr,cnx)
            return jsonify({'ok': 'ja existe'}), 304
    else:
        fecha_mysql(cr,cnx)
        return jsonify({'ok': 'Unauthorized'}), 401

@app.route('/meuconsumo/<string:usuario_id>', methods=['GET'])
def meu_consumo(usuario_id):
    (cr,cnx) = abre_mysql()

    query = ("SELECT b.Custo_data, e.nome_ec, b.data, b.duracao, b.consumoAgua, b.consumoEnergia FROM Usuario u INNER JOIN Banho b ON u.idUsuario = b.usuario_id  INNER JOIN Estacao_central e ON b.ec_num_serie = e.num_serie WHERE u.idUsuario = '%d'" % int(usuario_id))
    cr.execute(query)
    resultados = cr.fetchall()

    consumos = []

    for c in resultados:
        data = str(c[0])
        query = ("SELECT custoAgua, custoEnergia FROM Custo WHERE DATE_FORMAT(data, '%%Y %%m %%d') = DATE_FORMAT('%s', '%%Y %%m %%d')" %data)
        cr.execute(query)
        custos = cr.fetchall()
        custo_energia = (c[5]*int(c[3])/60)*custos[0][1]
        custo_agua = (c[4]/1000)*custos[0][0]
        consumo = {
            'estacao_central': c[1],
            'data': str(c[2]),
            'duracao': c[3],
            'consumo_agua': c[4],
            'custo_agua': custo_agua,
            'consumo_energia': c[5],
            'custo_energia': custo_energia}
        consumos.append(consumo)
    fecha_mysql(cr,cnx)
    return jsonify(consumos)

@app.route('/consumogeral/<string:usuario_id>', methods=['GET'])
def consumo_geral(usuario_id):
    (cr,cnx) = abre_mysql()

    query = ("SELECT superusuario FROM Usuario WHERE idUsuario = '%s'" % usuario_id)
    cr.execute(query)
    resultados = cr.fetchall()

    sUsuario = int(resultados[0][0])

    if (sUsuario == 1):
        query = ("SELECT b.Custo_data, u.nome, e.nome_ec, b.data, b.duracao, b.consumoAgua, b.consumoEnergia FROM Usuario u INNER JOIN Banho b ON u.idUsuario = b.usuario_id  INNER JOIN Estacao_central e ON b.ec_num_serie = e.num_serie")
        cr.execute(query)
        resultados = cr.fetchall()

        consumos = []
        for c in resultados:
            data = str(c[0])
            query = ("SELECT custoAgua, custoEnergia FROM Custo WHERE DATE_FORMAT(data, '%%Y %%m %%d') = DATE_FORMAT('%s', '%%Y %%m %%d')" %data)
            cr.execute(query)
            custos = cr.fetchall()
            custo_energia = (c[6]*int(c[4])/60)*custos[0][1]
            custo_agua = (c[5]/1000)*custos[0][0]
            consumo = {
                'usuario': c[1],
                'estacao_central': c[2],
                'data': str(c[3]),
                'duracao': c[4],
                'consumo_agua': c[5],
                'custo_agua': custo_agua,
                'consumo_energia': c[6],
                'custo_energia': custo_energia}
            consumos.append(consumo)
        fecha_mysql(cr,cnx)
        return jsonify(consumos)
    else:
        return make_response(jsonify({'error': 'Unauthorized'}), 401)

@app.route('/removeusuario', methods=('GET','POST'))
def remove_usuario():
    (cr,cnx) = abre_mysql()
    #retorna lista de usuarios (menos ANONIMO)
    if (request.method == 'GET'):
        query = ("SELECT idUsuario, nome, email FROM Usuario WHERE idUsuario != 999")
        cr.execute(query)
        resultados = cr.fetchall()
        fecha_mysql(cr,cnx)

        usuarios = []

        for u in resultados:
            usuario = {
                'idUsuario': u[0],
                'nome': u[1],
                'email': u[2]}
            usuarios.append(usuario)
        return jsonify(usuarios)
    else:
        if not request.json:
            abort(400);
        usuario_id = request.json['usuario_id']
        id_remove = request.json['id_remove']

        query = ("SELECT superusuario FROM Usuario WHERE idUsuario = '%s'" % usuario_id)
        cr.execute(query)
        resultados = cr.fetchall()

        sUsuario = int(resultados[0][0])

        if (sUsuario == 1):
            query = ("SELECT * FROM Usuario WHERE idUsuario = '%d'" %int(id_remove))
            cr.execute(query)
            linhas = cr.rowcount

            #se existir o id do usuario que foi enviado
            if (linhas != 0):
                #Apaga todos os registros do usuario
                query = ("DELETE FROM Ger_cadastros WHERE Usuario_idUsuario = '%d'" %int(id_remove))
                cr.execute(query)
                cnx.commit()
                query = ("DELETE FROM Banho WHERE usuario_id = '%d'" %int(id_remove))
                cr.execute(query)
                cnx.commit()
                query = ("DELETE FROM Usuario WHERE idUsuario = '%d'" %int(id_remove))
                cr.execute(query)
                cnx.commit()
                fecha_mysql(cr,cnx)
                return jsonify({'ok': '1'}), 201
            else:
                fecha_mysql(cr,cnx)
                return jsonify({'ok': '1'}), 304
        else:
            fecha_mysql(cr,cnx)
            return jsonify({'ok': 'Unauthorized'}), 401

@app.route('/removeestacao', methods=('GET','POST'))
def remove_estacao():
    (cr,cnx) = abre_mysql()
    #retorna lista de usuarios (menos ANONIMO)
    if (request.method == 'GET'):
        query = ("SELECT * FROM Estacao_central")
        cr.execute(query)
        resultados = cr.fetchall()
        fecha_mysql(cr,cnx)

        estacoes = []

        for e in resultados:
            estacao = {
                'num_serie': e[0],
                'nome_ec': e[1]}
            estacoes.append(estacao)
        return jsonify(estacoes)
    else:
        if not request.json:
            abort(400);
        usuario_id = request.json['usuario_id']
        num_serie = request.json['id_remove']

        query = ("SELECT superusuario FROM Usuario WHERE idUsuario = '%s'" % usuario_id)
        cr.execute(query)
        resultados = cr.fetchall()

        sUsuario = int(resultados[0][0])

        if (sUsuario == 1):
            query = ("SELECT * FROM Estacao_central WHERE num_serie = '%d'" %int(num_serie))
            cr.execute(query)
            linhas = cr.rowcount

            if (linhas != 0):
                #Apaga todos os registros do usuario
                query = ("DELETE FROM Ger_cadastros WHERE Estacao_central_num_serie = '%d'" %int(num_serie))
                cr.execute(query)
                cnx.commit()
                query = ("DELETE FROM Banho WHERE ec_num_serie = '%d'" %int(num_serie))
                cr.execute(query)
                cnx.commit()
                query = ("DELETE FROM Estacao_central WHERE num_serie = '%d'" %int(num_serie))
                cr.execute(query)
                cnx.commit()
                fecha_mysql(cr,cnx)
                return jsonify({'ok': '1'}), 201
            else:
                fecha_mysql(cr,cnx)
                return jsonify({'ok': '1'}), 304
        else:
            fecha_mysql(cr,cnx)
            return jsonify({'ok': 'Unauthorized'}), 401

@app.route('/superusuario', methods=('GET','POST'))
def superusuario():
    (cr,cnx) = abre_mysql()
    #retorna lista de usuarios (menos ANONIMO)
    if (request.method == 'GET'):
        query = ("SELECT idUsuario, nome, email FROM Usuario")
        cr.execute(query)
        resultados = cr.fetchall()
        fecha_mysql(cr,cnx)

        usuarios = []

        for u in resultados:
            usuario = {
                'idUsuario': u[0],
                'nome': u[1],
                'email': u[2]}
            usuarios.append(usuario)
        return jsonify(usuarios)
    else:
        if not request.json:
            abort(400);

        usuario_id = request.json['usuario_id'] #id do superusuario
        idUsuario = request.json['idUsuario'] #id do usuario solicitado

        query = ("SELECT superusuario FROM Usuario WHERE idUsuario = '%d'" % int(usuario_id))
        cr.execute(query)
        resultados = cr.fetchall()

        sUsuario = int(resultados[0][0])

        if (sUsuario == 1):
            query = ("SELECT superusuario FROM Usuario WHERE idUsuario = '%d'" % int(idUsuario))
            cr.execute(query)
            linhas = cr.rowcount

            #se existir o usuario que se quer alterar o valor
            if (linhas != 0):
                resultados = cr.fetchall()

                query = (" UPDATE Usuario SET superusuario = 1 WHERE idUsuario = '%d'" % int(idUsuario))
                cr.execute(query)
                cnx.commit()
                fecha_mysql(cr,cnx)
                return jsonify({'ok': '1'}), 201
            else:
                fecha_mysql(cr,cnx)
                return jsonify({'ok': '1'}), 304
        else:
            fecha_mysql(cr,cnx)
            return jsonify({'ok': 'Unauthorized'}), 401

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    print ("Servidor no ar!")
    app.run(host="localhost", port=5001, debug=True)
