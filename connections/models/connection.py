from enum import Enum

from connections.database import CreatedUpdatedMixin, CRUDMixin, db, Model


class ConnectionType(Enum):
    mother = 'mother'
    father = 'father'
    son = 'son'
    daughter = 'daughter'
    husband = 'husband'
    wife = 'wife'
    brother = 'brother'
    sister = 'sister'
    friend = 'friend'
    coworker = 'coworker'


class Connection(Model, CRUDMixin, CreatedUpdatedMixin):
    id = db.Column(db.String(64), primary_key=True)
    from_person_id = db.Column(db.String(64), db.ForeignKey('person.id'))
    to_person_id = db.Column(db.String(64), db.ForeignKey('person.id'))
    connection_type = db.Column(db.Enum(ConnectionType), nullable=False)
