"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Posts
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/all_users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    print('\n')
    print('users sin serialize ----> ', users)
    print('\n')
    #users = [user.serialize() for user in users]
    #print( 'users CON serialize ----> ', users.serialize())
    # aux = []
    # for user in users:
    #     aux.append(user.serialize())
    aux = list(map(lambda x: x.serialize(), users))
    return jsonify({'msg': 'OK', 'data': aux}), 200


@api.route('/one_user/<int:id>', methods=['GET'])
def get_one_user(id):
    users = User.query.get(id)
    print('\n')
    print('users sin serialize ----> ', users)
    print('\n')
    print('users CON serialize ----> ', users.serialize())
    
    return jsonify({'msg': 'OK', 'user': users.serialize()}), 200

#CRUD --> Create Read Update Delete
#           POST GET    PUT  DELETE

@api.route('/delete_user/<int:id>', methods=['DELETE'])
def del_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'msg': 'Error, no se encontró el usuario a eliminar'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': 'Usuario eliminado'})
    
@api.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    if data['email'] and data['password']:
        user = User.query.filter_by(email=data['email']).first()
        if user:
            return jsonify({'msg': 'El usuario ya existe, intenta logearte'}), 200
        new_user = User(email=data['email'], password=data['password'], is_active=True)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'msg': 'OK', 'user': new_user.serialize()}), 201

    return jsonify({'msg': 'todos los datos son necesarios'}), 400
    
@api.route('/edit_user/<int:id>', methods=['PUT'])
def edit_user(id):
    data = request.json
    if data['email'] and data['is_active']:
        user = User.query.get(id)
        if not user:
            return jsonify({'msg': 'Error, no se encontró el usuario'}), 404
        user.email = data['email'] or user.email
        user.is_active=data['is_active'] or user.is_active
        db.session.commit()
        return jsonify({'msg': 'Usuario editado', 'user': user.serialize()})
    return jsonify({'error': 'Todos los datos son necesarios'})

   
@api.route('/deactivate/<int:id>', methods=['PUT'])
def deactivate(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'msg': 'Error, no se encontró el usuario'}), 404
    user.is_active = False
    db.session.commit()
    return jsonify({'msg': 'OK, usuario desactivado'})

     
@api.route('/activate/<int:id>', methods=['PUT'])
def activate(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'msg': 'Error, no se encontró el usuario'}), 404
    user.is_active = True
    db.session.commit()
    return jsonify({'msg': 'OK, usuario activado'})