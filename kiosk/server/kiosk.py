import http
from datetime import datetime
from typing import List

from flask import Flask, abort, render_template, request

from kiosk.server.storage import Storage

storage = Storage()


def add_entry():
    json = request.get_json() or {}

    try:
        price: int = json["price"]
        product_ids: List[int] = json["product_ids"]
    except KeyError:
        abort(http.HTTPStatus.BAD_REQUEST)
        return

    storage.append(price, product_ids)

    return "", http.HTTPStatus.CREATED


def browse():
    return render_template("browse.html.j2", storage=storage, now=datetime.now().replace(microsecond=0))


def create_app():
    app = Flask(__name__)

    app.add_url_rule("/", browse.__name__, browse, methods=("GET",))

    app.add_url_rule("/", add_entry.__name__, add_entry, methods=("POST",))

    return app
