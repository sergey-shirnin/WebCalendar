import sys
import datetime

import werkzeug
from flask import Flask, request, abort, jsonify
from flask_restful import Api, Resource, marshal_with
from POST_parser import initiate_post_parser
from DAO import EventDAO, db, resource_fields, TABLE


app = Flask(__name__)
api = Api(app)

db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s.db' % TABLE
with app.test_request_context():
    db.create_all()
app.config['JSON_SORT_KEYS'] = False


class NotFoundHTTPException(werkzeug.exceptions.HTTPException):
    code = 404; description = "The event doesn't exist!"


class GetEventsResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        start, end = request.args.get('start_time'), request.args.get('end_time')
        table_data = EventDAO.query.filter(EventDAO.date >= start, EventDAO.date <= end).all() if start and end \
            else EventDAO.query.all()  # or -> EventDAO.date.between(start, end)
        return table_data


class GetEventsTodayResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        table_data = EventDAO.query.filter(EventDAO.date == datetime.date.today()).all()
        if table_data:
            return table_data
        raise NotFoundHTTPException


class GetEventByIdResource(Resource):
    @marshal_with(resource_fields)
    def get(self, requested_id):
        table_data = EventDAO.query.filter(EventDAO.id == requested_id).first()
        if table_data:
            return table_data
        raise NotFoundHTTPException


class PostEventResource(Resource):
    def post(self):
        args = parser.parse_args()
        new_event = EventDAO(event=args['event'], date=args['date'].date())
        db.session.add(new_event); db.session.commit()
        return jsonify(message="The event has been added!", event=args['event'], date=str(args['date'].date()))


@app.route('/event/<int:requested_id>', methods=['DELETE'])
def delete_by_id(requested_id):
    event_to_delete = EventDAO.query.get(requested_id)
    if event_to_delete:
        db.session.delete(event_to_delete); db.session.commit()
        return jsonify(message="The event has been deleted!")
    return abort(404)


# this will work on any abort(404) call for
# @app.route functions scope with message pre-specified
@app.errorhandler(404)
def not_found(e):
    return jsonify(message="The event doesn't exist!"), 404


# this will work on routine raise Exception call (Resource classes scope)
# together with
# NotFoundHTTPExceptionClass
def handle_404(e):
    return jsonify(message=str(e)), 404


api.add_resource(GetEventsResource, '/event/')
api.add_resource(GetEventsTodayResource, '/event/today')
api.add_resource(GetEventByIdResource, '/event/<int:requested_id>/')

parser = initiate_post_parser()
api.add_resource(PostEventResource, '/event')

app.register_error_handler(NotFoundHTTPException, handle_404)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
