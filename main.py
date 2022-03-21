import sys
from flask import Flask
from flask_restful import Api, Resource, reqparse, inputs


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
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
for arg in post_args:
    parser.add_argument(arg,
                        type=post_args[arg]['type'],
                        help=post_args[arg]['msg'],
                        required=True)


class GetEventResource(Resource):
    def get(self):
        return {"data": "There are no events for today!"}


class PostEventResource(Resource):
    def post(self):
        args = parser.parse_args()
        return {
            "message": "The event has been added!",
            "event": args['event'],
            "date": str(args['date'].date())
        }


api.add_resource(GetEventResource, '/event/today')
api.add_resource(PostEventResource, '/event')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
