import http

from flask import Flask, request


def add_entry():
    json = request.get_json()
    print(json)

    return "", http.HTTPStatus.CREATED


def create_app():
    app = Flask(__name__)

    app.add_url_rule("/", add_entry.__name__, add_entry, methods=("POST",))

    return app
