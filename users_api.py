import sys

import flask
import requests
from flask import jsonify, request, render_template

from data import db_session
from data.users import User

blueprint = flask.Blueprint('users_api', __name__, template_folder='templates')


@blueprint.route('/api/users')
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'users': [item.to_dict(only=('id', 'name')) for item in users]
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['login', 'surname', 'name', 'age', 'position', 'position', 'speciality', 'address', 'password']):
        return jsonify({'error': 'Bad request'})
    # noinspection PyArgumentList
    user = User(
        login=request.json['login'],
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
    )
    user.set_password(request.json['password'])
    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict()
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['login', 'surname', 'name', 'age', 'position', 'position', 'speciality', 'address', 'password']):
        return jsonify({'error': 'Bad request'})
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    user.login = request.json['login']
    user.surname = request.json['surname']
    user.name = request.json['name']
    user.age = request.json['age']
    user.position = request.json['position']
    user.speciality = request.json['speciality']
    user.address = request.json['address']
    user.set_password(request.json['password'])
    session.merge(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/users_show/<int:user_id>')
def show_city(user_id):
    response = get_one_user(user_id).json
    if 'error' in response:
        return render_template('not_found.html', user_id=user_id)

    user = response['user']

    geo_request = "https://geocode-maps.yandex.ru/1.x/"
    map_request = "http://static-maps.yandex.ru/1.x/"
    d = {
        'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
        'format': 'json',
        'geocode': user['city_from'],
    }
    response = requests.get(geo_request, params=d).json()
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    d = {
        'l': 'sat',
        'll': ','.join(response['response']['GeoObjectCollection']
                       ['featureMember'][0]['GeoObject']['Point']['pos'].split()),
        'z': '12',
        'size': '650,450'
    }
    response = requests.get(map_request, params=d)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    return render_template('show_city.html', user=user, title='Hometown', url=response.url)
