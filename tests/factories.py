from uuid import uuid4

from factory import Faker, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from connections.database import db
from connections.models.connection import Connection
from connections.models.person import Person


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:

        abstract = True
        sqlalchemy_session = db.session


class PersonFactory(BaseFactory):
    """Person factory."""

    id = Sequence(lambda n: uuid4())
    email = Sequence(lambda n: f'person{n}@example.com')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    date_of_birth = Faker('date')

    class Meta:

        model = Person


class ConnectionFactory(BaseFactory):
    """Connection factory."""

    connection_type = 'friend'

    id = Sequence(lambda n: uuid4())
    from_person_id = Sequence(lambda n: uuid4())
    to_person_id = Sequence(lambda n: uuid4())

    class Meta:

        model = Connection
