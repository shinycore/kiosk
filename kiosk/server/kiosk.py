import http
from datetime import datetime
from typing import List

from flask import Flask, abort, render_template, request

from ..utils import get_product_names
from .storage import Storage

storage = Storage()
product_names = get_product_names()


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


def delete_entry(idx: int):
    try:
        del storage[idx]
    except IndexError:
        abort(http.HTTPStatus.NOT_FOUND)
    else:
        return "", http.HTTPStatus.OK


def browse():
    entries = [
        {
            "id": id_,
            "date": entry.date,
            "price": entry.price,
            "products": [(pid, product_names[pid]) for pid in entry.product_ids],
        }
        for id_, entry in storage.to_dict().items()
    ]

    return render_template("browse.html.j2", entries=entries, now=datetime.now().replace(microsecond=0))


def create_app():
    app = Flask(__name__)

    app.add_url_rule("/", browse.__name__, browse, methods=("GET",))

    app.add_url_rule("/", add_entry.__name__, add_entry, methods=("POST",))
    app.add_url_rule("/entry/<int:idx>", delete_entry.__name__, delete_entry, methods=("DELETE",))

    return app
