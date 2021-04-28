from http import HTTPStatus

from tests.factories import ConnectionFactory, PersonFactory


def test_valid_patch_connection(db, testapp):
    from_person = PersonFactory()
    to_person = PersonFactory()
    connection_before = ConnectionFactory.create(
        from_person_id=from_person.id, to_person_id=to_person.id
    )
    db.session.commit()

    assert connection_before.connection_type.value == 'friend'

    payload = {
        'connection_type': 'coworker',
    }

    res = testapp.patch(f'/connections/{connection_before.id}', json=payload)

    assert res.status_code == HTTPStatus.OK

    connection = res.json

    assert connection is not None
    assert connection['connection_type'] == 'coworker'


def test_invalid_patch_connection(db, testapp):
    from_person = PersonFactory()
    to_person = PersonFactory()
    connection = ConnectionFactory.create(from_person_id=from_person.id, to_person_id=to_person.id)

    db.session.commit()
    payload = {
        'connection_type': 'cousin',
    }

    res = testapp.patch(f'/connections/{connection.id}', json=payload)

    assert res.status_code == HTTPStatus.BAD_REQUEST

    assert connection is not None
    assert connection.connection_type.value is not 'cousin'
