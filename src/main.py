from flask import Flask, request, jsonify, Response
from pymongo import MongoClient, errors
from flask_cors import CORS
from bson import json_util
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
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
            hashed_password = generate_password_hash(password)
            proveedor = {'tipo': tipo, 'nombre_empresa': nombre_empresa,
                         'direccion': direccion, 'nombres': nombres,
                         'apellidos': apellidos, 'email': email,
                         'password': hashed_password, 'celular': celular, 'foto': ''}
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
            hashed_password = generate_password_hash(password)
            cliente = {'tipo': tipo, 'nombre_empresa': '',
                       'direccion': direccion, 'nombres': nombres,
                       'apellidos': apellidos, 'email': email,
                       'password': hashed_password, 'celular': celular, 'foto': ''}
            id = db.usuarios.insert(proveedor)
            response = jsonify({
                '_id': str(id),
                'tipo': tipo, 'nombre_empresa': '',
                'direccion': direccion, 'nombres': nombres,
                'apellidos': apellidos, 'email': email,
                'password': hashed_password, 'celular': celular, 'foto': ''
            })
            response.status_code = 201
            return response
    else:
        return not_found()


@app.route('/users', methods=['GET'])
def getUsers():
    users = db.usuarios.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    print(id)
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
    user = db.usuarios.find_one({'email': content['email'], 'password': content['password']})
    if (user is None):
        return jsonify({'existe' : False})
    return jsonify({'existe' : True, 'data': str(user)})

@app.route('/update', methods=['POST'])
def update():
    content = request.json
    myquery = { "email": content['email'] }
    newValues = { "$set": {'nombre_empresa': content['nombre_empresa'], 'dirección': content['direccion'], 'nombres': content['nombres'], 'apellidos': content['apellidos'], 'email': content['email'], 'celular': content['celular']}}
    x = db.usuarios.update_one(myquery, newValues)
    print(x.modified_count)
    return jsonify('Actualizado'=x.modified_count)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    #app.run(host="0.0.0.0", port=5000, debug=True)
