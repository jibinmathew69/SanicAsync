from sanic import Sanic
from sanic_cors import CORS

completed = {}
pending = {}
failed = {}
created = {}
finished = {}


def make_app():
    app = Sanic(__name__)
    CORS(app,automatic_options=True)

    return app


if __name__ == '__main__':
    app = make_app()

    app.run(debug=True, host='0.0.0.0', port='8001')