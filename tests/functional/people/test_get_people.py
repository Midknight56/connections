from http import HTTPStatus

from tests.factories import ConnectionFactory, PersonFactory


EXPECTED_FIELDS = [
    'id',
    'first_name',
    'last_name',
    'email',
]


def test_can_get_people(db, testapp):
    PersonFactory.create_batch(10)
    db.session.commit()

    res = testapp.get('/people')

    assert res.status_code == HTTPStatus.OK

    assert len(res.json) == 10
    for person in res.json:
        for field in EXPECTED_FIELDS:
            assert field in person


def test_get_mutual_friends(db, testapp):
    instance = PersonFactory()
    target = PersonFactory()
    sub = PersonFactory()

    # some decoy connections (not mutual)
    ConnectionFactory.create_batch(5, from_person_id=sub.id, to_person_id=instance.id)
    ConnectionFactory.create_batch(5, from_person_id=sub.id, to_person_id=target.id)

    mutual_friends = PersonFactory.create_batch(3)
    for f in mutual_friends:
        ConnectionFactory(from_person_id=instance.id, to_person_id=f.id, connection_type='friend')
        ConnectionFactory(from_person_id=target.id, to_person_id=f.id, connection_type='friend')

    # mutual connections, but not friends
    decoy = PersonFactory()
    ConnectionFactory(from_person_id=instance.id, to_person_id=decoy.id, connection_type='coworker')
    ConnectionFactory(from_person_id=target.id, to_person_id=decoy.id, connection_type='coworker')

    db.session.commit()

    expected_mutual_friend_ids = [f.id for f in mutual_friends]

    res = testapp.get(f'/people/{instance.id}/mutual_friends?target_id={target.id}')

    assert res.status_code == HTTPStatus.OK
    assert len(res.json) == 3
    for f in res.json:
        assert f['id'] in expected_mutual_friend_ids

    reverse_res = testapp.get(f'/people/{target.id}/mutual_friends?target_id={instance.id}')

    assert reverse_res.status_code == HTTPStatus.OK
    assert len(reverse_res.json) == 3
    for f in reverse_res.json:
        assert f['id'] in expected_mutual_friend_ids
