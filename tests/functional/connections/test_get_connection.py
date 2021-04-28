from http import HTTPStatus

from tests.factories import ConnectionFactory, PersonFactory

EXPECTED_CONNECTIONS_FIELDS = [
    'connection',
    'from_person',
    'to_person',
]

EXPECTED_CONNECTION_FIELDS = [
    'id',
    'from_person_id',
    'to_person_id',
    'connection_type'
]

EXPECTED_PERSON_FIELDS = [
    'id',
    'first_name',
    'last_name',
    'email',
    'date_of_birth',
]


def test_get_connection(db, testapp):
    from_person = PersonFactory()
    to_person = PersonFactory()
    ConnectionFactory.create_batch(10, from_person_id=from_person.id, to_person_id=to_person.id)
    db.session.commit()

    res = testapp.get('/connections')

    connections = res.json['connections']

    assert res.status_code == HTTPStatus.OK

    assert len(connections) == 10
    for connection in connections:
        for field in EXPECTED_CONNECTIONS_FIELDS:
            assert field in connection
        for field in EXPECTED_CONNECTION_FIELDS:
            assert field in connection['connection']
        for field in EXPECTED_PERSON_FIELDS:
            assert field in connection['from_person']
            assert field in connection['to_person']
