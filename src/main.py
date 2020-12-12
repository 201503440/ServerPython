from flask import Flask, request, jsonify, Response
from pymongo import MongoClient, errors
from flask_cors import CORS
from flask_api import status
from bson import json_util
from bson.objectid import ObjectId
import os
import json
import base64


app = Flask(__name__)
CORS(app)

# Base de datos*********************************************
MONGO_HOST = base64.b64decode("My4xMzUuNjUuMTMz").decode("utf-8")
MONGO_PORT = base64.b64decode("MjcwMTc=").decode("utf-8")
MONGO_DB = base64.b64decode("ZGF0YWJhc2VwMQ==").decode("utf-8")
MONGO_USER = base64.b64decode("Z3J1cG8z").decode("utf-8")
MONGO_PASS = base64.b64decode("YWRtaW4=").decode("utf-8")

uri = "mongodb://{}:{}@{}:{}/{}?authMechanism=SCRAM-SHA-1".format(
    MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_PORT, MONGO_DB)
client = MongoClient(uri)
db = client[MONGO_DB]
# End Base de datos*****************************************


@app.route('/', methods=['GET', 'POST'])
def main():
    return {"Python_Server_Main": "Grupo 3"}


@app.route('/users', methods=['POST'])
def create_user():
    content = request.json
    tipo = content['tipo']

    if tipo == 1:
        nombre_empresa = content["nombre_empresa"]
        direccion = content["direccion"]
        nombres = content["nombres"]
        apellidos = content["apellidos"]
        email = content["email"]
        password = content["password"]
        celular = content["celular"]
        if nombre_empresa and nombres and email and password:
            proveedor = {'tipo': tipo, 'nombre_empresa': nombre_empresa,
                         'direccion': direccion, 'nombres': nombres,
                         'apellidos': apellidos, 'email': email,
                         'password': password, 'celular': celular, 'foto': ''}
            id = db.usuarios.insert(proveedor)
            response = jsonify({
                '_id': str(id),
                'tipo': tipo, 'nombre_empresa': nombre_empresa,
                'direccion': direccion, 'nombres': nombres,
                'apellidos': apellidos, 'email': email,
                'password': password, 'celular': celular, 'foto': ''
            })
            response.status_code = 201
            return response
    elif tipo == 2:
        direccion = content['direccion']
        nombres = content['nombres']
        apellidos = content['apellidos']
        email = content['email']
        password = content["password"]
        celular = content["celular"]
        if nombres and email and password:
            cliente = {'tipo': tipo, 'nombre_empresa': '',
                       'direccion': direccion, 'nombres': nombres,
                       'apellidos': apellidos, 'email': email,
                       'password': password, 'celular': celular, 'foto': ''}
            id = db.usuarios.insert(cliente)
            response = jsonify({
                '_id': str(id),
                'tipo': tipo, 'nombre_empresa': '',
                'direccion': direccion, 'nombres': nombres,
                'apellidos': apellidos, 'email': email,
                'password': password, 'celular': celular, 'foto': ''
            })
            response.status_code = 201
            return response
    else:
        return not_found()


@app.route('/users', methods=['GET'])
def get_users():
    users = db.usuarios.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = db.usuarios.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


@app.route('/login', methods=['POST'])
def login():
    content = request.json
    user = db.usuarios.find_one(
        {'email': content['email'], 'password': content['password']})
    if (user is None):
        return jsonify({'existe': False})
    response = json_util.dumps(user)
    return jsonify({'existe': True, 'data': response})


@app.route('/update', methods=['POST'])
def update():
    content = request.json
    myquery = { "email": content['email'] }
    if content['foto'] == '':
        newValues = { "$set": {'nombre_empresa': content['nombre_empresa'], 'direccion': content['direccion'], 
        'nombres': content['nombres'], 'apellidos': content['apellidos'], 'email': content['email'], 
        'celular': content['celular']}}
    else:
        newValues = { "$set": {'nombre_empresa': content['nombre_empresa'], 'direccion': content['direccion'], 
        'nombres': content['nombres'], 'apellidos': content['apellidos'], 'email': content['email'], 
        'celular': content['celular'], 'foto': content['foto'] }}
    x = db.usuarios.update_one(myquery, newValues)
    obj = {'Actualizado': x.modified_count}
    return jsonify(obj)


@app.route('/crear_producto', methods=['POST'])
def crear_producto():
    idP = db.catalogo_proveedor.count()
    content = request.json
    catalogo = {'imagen': content["imagen"], 'stock': content["stock"],
                'categoria': content["categoria"], 'nombre': content["nombre"],
                'precio': content["precio"], 'descripcion': content["descripcion"],
                'id': idP+1, 'email': content["email"]}
    db.catalogo_proveedor.insert_one(catalogo)
    return ""


@app.route('/actualizar_producto', methods=['POST'])
def actualizar_producto():
    content = request.json
    db.catalogo_proveedor.delete_one({'id': int(content['id'])})
    db.catalogo_proveedor.insert_one(content)
    return "ACTUALIZADO"


@app.route('/eliminar_producto/<id>', methods=['GET'])
def eliminar_producto(id):
    content = request.json
    eliminar = db.catalogo_proveedor.delete_one({'id': int(id)})
    response = json_util.dumps(eliminar)
    return Response(response, mimetype="application/json")


@app.route('/obtener_producto/<id>', methods=['GET'])
def obtener_producto(id):
    catalogo = db.catalogo_proveedor.find_one({'id': int(id)})
    response = json_util.dumps(catalogo)
    return Response(response, mimetype="application/json")


@app.route('/obtener_todos_mis_producto/<email>', methods=['GET'])
def obtener_todos_mis_producto(email):
    catalogo = db.catalogo_proveedor.find({'email': email})
    response = json_util.dumps(catalogo)
    return Response(response, mimetype="application/json")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
