from flask import Flask
from flask_restful import Api, Resource
import sys


app = Flask(__name__)
api = Api(app)


class GetMessageResource(Resource):
    def get(self):
        return {"data":"There are no events for today!"}

      
api.add_resource(GetMessageResource, '/event/today')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
