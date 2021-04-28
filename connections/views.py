from http import HTTPStatus
from re import fullmatch

from flask import Blueprint, jsonify, request
from webargs.flaskparser import use_args

from connections.models.connection import Connection, ConnectionType
from connections.models.person import Person
from connections.schemas import ConnectionSchema, PersonSchema

blueprint = Blueprint('connections', __name__)


@blueprint.route('/people', methods=['GET'])
def get_people():
    people_schema = PersonSchema(many=True)
    people = Person.query.all()

    return people_schema.jsonify(people), HTTPStatus.OK


@blueprint.route('/people', methods=['POST'])
@use_args(PersonSchema())
def create_person(person: Person):
    valid_email_regex = r'^[A-Za-z\.\+_-]+@[A-Za-z\._-]+\.[a-zA-Z]*$'
    email = person.email

    if not fullmatch(valid_email_regex, email):
        json = {
            'description': 'Input failed validation.',
            'errors': {
                'email': 'Not a valid email address.'
            }
        }
        return jsonify(json), HTTPStatus.BAD_REQUEST

    person.save()
    return PersonSchema().jsonify(person), HTTPStatus.CREATED


@blueprint.route('/people/<person_id>/mutual_friends', methods=['GET'])
def get_mutual_friends(person_id):
    people_schema = PersonSchema(many=True)
    target_id = request.args['target_id']
    person = Person.query.get_or_404(person_id)
    target = Person.query.get_or_404(target_id)
    friends = []

    for friend in person.mutual_friends(target):
        friends.append(Person.query.get_or_404(friend))

    return people_schema.jsonify(friends), HTTPStatus.OK


@blueprint.route('/connections', methods=['POST'])
@use_args(ConnectionSchema(), locations=('json',))
def create_connection(connection):
    connection.save()

    return ConnectionSchema().jsonify(connection), HTTPStatus.CREATED


@blueprint.route('/connections', methods=['GET'])
def get_connection():
    connections = Connection.query.all()
    json_results = []

    for connection in connections:
        from_person = Person.query.get_or_404(connection.from_person_id)
        to_person = Person.query.get_or_404(connection.to_person_id)
        json_results.append({
            'connection': {
                'id': connection.id,
                'from_person_id': connection.from_person_id,
                'to_person_id': connection.to_person_id,
                'connection_type': connection.connection_type.value
            },
            'from_person': {
                'id': from_person.id,
                'first_name': from_person.first_name,
                'last_name': from_person.last_name,
                'email': from_person.email,
                'date_of_birth': from_person.date_of_birth
            },
            'to_person': {
                'id': to_person.id,
                'first_name': to_person.first_name,
                'last_name': to_person.last_name,
                'email': to_person.email,
                'date_of_birth': to_person.date_of_birth
            }
        })

    json = {
        'connections': json_results
    }

    return jsonify(json), HTTPStatus.OK


@blueprint.route('/connections/<connection_id>', methods=['PATCH'])
def update_connection(connection_id):
    connection = Connection.query.get_or_404(connection_id)
    connection_type = request.json['connection_type']
    json = {
        'description': 'Connection Type is not valid.',
        'errors': {
            'connection_type': 'Not a valid connection type.'
        }
    }

    if connection_type in (None, ''):

        return jsonify(json), HTTPStatus.BAD_REQUEST
    else:
        connection_types = set(item.value for item in ConnectionType)

        if connection_type in connection_types:
            connection.connection_type = ConnectionType[connection_type]

            return ConnectionSchema().jsonify(connection), HTTPStatus.OK
        else:

            return jsonify(json), HTTPStatus.BAD_REQUEST
