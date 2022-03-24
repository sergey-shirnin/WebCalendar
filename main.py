import sys
import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, inputs, marshal_with, fields


TABLE = 'events'
user_id = 'default'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s.db' % TABLE
db = SQLAlchemy(app)
api = Api(app)

post_args = {
    'event': {
        'type': str,
        'msg': 'The event name is required!'
    },
    'date': {
        'type': inputs.date,
        'msg': 'The event date with the correct format is required! The correct format is YYYY-MM-DD!'
    }
}

resource_fields = {
    'id': fields.Integer,
    'event': fields.String,
    'date': fields.String
}

parser = reqparse.RequestParser()
for arg in post_args:
    parser.add_argument(arg,
                        type=post_args[arg]['type'],
                        help=post_args[arg]['msg'],
                        required=True)


class EventDAO(db.Model):
    __tablename__ = f'{user_id}_{TABLE}'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)


db.create_all()


class GetEventResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        table_data = EventDAO.query.all()
        return table_data


class GetEventTodayResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        table_data = EventDAO.query.filter(EventDAO.date == datetime.date.today()).all()
        return [EventDAO(id=row.id, event=row.event, date=row.date) for row in table_data]


class PostEventResource(Resource):
    def post(self):
        args = parser.parse_args()
        new_event = EventDAO(event=args['event'], date=args['date'].date())
        db.session.add(new_event) ; db.session.commit()
        return {
            "message": "The event has been added!",
            "event": args['event'],
            "date": str(args['date'].date())
        }


api.add_resource(GetEventTodayResource, '/event/today')
api.add_resource(GetEventResource, '/event')
api.add_resource(PostEventResource, '/event')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
