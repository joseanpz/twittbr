from pony import orm
from datetime import datetime

db = orm.Database()


class Person(db.Entity):
    name = orm.Required(str)
    age = orm.Required(int)
    cars = orm.Set('Car')


class Car(db.Entity):
    make = orm.Required(str)
    model = orm.Required(str)
    owner = orm.Required(Person)


class Tweet(db.Entity):
    id = orm.PrimaryKey(str)
    created_at = orm.Required(datetime)
    text = orm.Required(str)
    truncated = orm.Required(bool)
    in_reply_to_status_id = orm.Optional(str, nullable=True)
    in_reply_to_user_id = orm.Optional(str, nullable=True)
    in_reply_to_screen_name = orm.Optional(str, nullable=True)
    entities = orm.Optional(orm.Json)
    user = orm.Required('User')


class User(db.Entity):
    id = orm.PrimaryKey(str)
    created_at = orm.Required(datetime)
    name = orm.Required(str)
    screen_name = orm.Required(str)
    tweets = orm.Set(Tweet)


db.bind(provider='sqlite', filename='C:/Users/BRM00000/dev/twitter/database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)


# populate samples
@orm.db_session
def populate():
    p1 = Person(name='John', age=20)
    p2 = Person(name='Mary', age=22)
    p3 = Person(name='Bob', age=30)
    c1 = Car(make='Toyota', model='Prius', owner=p2)
    c2 = Car(make='Ford', model='Explorer', owner=p3)

populate()