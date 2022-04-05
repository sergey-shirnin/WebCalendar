from flask_sqlalchemy import SQLAlchemy
from flask_restful import fields


db = SQLAlchemy()
user_id = 'default'
TABLE = 'my_events'

class EventDAO(db.Model):
    __tablename__ = f'{user_id}_{TABLE}'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)


resource_fields = {
    'id': fields.Integer,
    'event': fields.String,
    'date': fields.String
}
