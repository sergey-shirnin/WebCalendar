from flask_restful import reqparse, inputs


def initiate_post_parser():
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
        parser.add_argument(arg, type=post_args[arg]['type'], help=post_args[arg]['msg'], required=True)
    return parser
