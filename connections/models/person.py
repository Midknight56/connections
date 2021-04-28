from connections.database import CreatedUpdatedMixin, CRUDMixin, db, Model


class Person(Model, CRUDMixin, CreatedUpdatedMixin):
    id = db.Column(db.String(64), primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(145), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    connections = db.relationship('Connection', foreign_keys='Connection.from_person_id')

    def mutual_friends(self, target_person):
        person_connection = self.connections
        target_connection = target_person.connections
        person_friend = []
        target_friend = []

        # Go through the list of connections and find those that are type friend
        for c in person_connection:
            if (c.connection_type.value is 'friend'):
                person_friend.append(c.to_person_id)

        for c in target_connection:
            if (c.connection_type.value is 'friend'):
                target_friend.append(c.to_person_id)

        # Convert to set for a faster comparison between the two list then convert
        # to an array and return
        return list(set(person_friend).intersection(target_friend))
