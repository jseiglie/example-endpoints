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


@api.route('/test', methods=['GET'])
def getTest():
    return jsonify({'test': 'OK'}),200

@api.route('/all_users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    print('\n')
    print('antes del serialize ---> ',users)
    print('\n')
    users = [user.serialize() for user in users]
    # aux = []
    # for user in users:
    #     aux.append(user.serialize())
    # users = list(map(lambda x: x.serialize(), users))
    print('******************* despues del serialize ---> ',users)

    return jsonify({'msg': 'ok',
                    'data': users})

@api.route('/all_users_active', methods=['GET'])
def get_all_active():
    #users = User.query.filter_by(is_active=True)
    users = User.query.filter_by(is_active=True)
    print('\n')
    print('antes del serialize ---> ',users)
    print('\n')
    users = [user.serialize() for user in users]
    # aux = []
    # for user in users:
    #     aux.append(user.serialize())
    # users = list(map(lambda x: x.serialize(), users))
    print('******************* despues del serialize ---> ',users)

    return jsonify({'msg': 'ok',
                    'data': users})



@api.route('/one_user/<int:id>', methods=['GET'])
def get_one_users(id):
    user = User.query.get(id)
    print('user antes del serialize ----> ', user)
    user = user.serialize()
    print('\n')
    print('user DESPUES del serialize ----> ', user)
    return jsonify({'msg': 'ok',
                    'data': user}),200


@api.route('/delete_user/<int:id>', methods=['DELETE'])
def del_user(id):
    user = User.query.get(id)
    print(user) 
    db.session.delete(user)
    db.session.commit()

    return jsonify({'msg': 'se elimino el usuario ' + user.email,
                    }),200

#CRUD create read update delete
#     POST   GET  PUT    DELETE

@api.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    print('\n')
    print('lo que recibimos ----> ', data)
    print('\n')
    new_user = User(email=data['email'], password=data['password'], is_active=True)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'msg': 'ok '}),200

@api.route('/edit_user/<int:id>', methods=['PUT'])
def edit_user(id):
    data = request.json
    user = User.query.get(id)
    user.email=data['email']
    user.is_active= data['is_active']
    db.session.commit()
    return jsonify({'msg': 'OK', 'data': user.serialize()}), 200



@api.route('/deactivate/<int:id>', methods=['PUT'])
def deactivate_user(id):
    user = User.query.get(id)
    user.is_active=False
    db.session.commit()
    return jsonify({'msg': 'OK', 'data': user.serialize()}), 200

@api.route('/activate/<int:id>', methods=['PUT'])
def activate_user(id):
    user = User.query.get(id)
    user.is_active=True
    db.session.commit()
    return jsonify({'msg': 'OK', 'data': user.serialize()}), 200