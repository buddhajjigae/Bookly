import json

from flask import jsonify, request, Response
from flask.blueprints import Blueprint

from catalog_svc.extensions import db
from catalog_svc.models.item_line import ItemLine, ItemLineSchema
from catalog_svc.models.order import Order

item_lines = Blueprint("itemline", __name__)

item_line_schema = ItemLineSchema()
item_lines_schema = ItemLineSchema(many=True)

# endpoint to show all item line numbers
@item_lines.route("/itemline/", methods=["GET"])
@item_lines.route("/itemline/<int:page>", methods=["GET"])
def get_item_lines(page=None):
    per_page = None
    if page:
        per_page = 2

    all_item_lines = ItemLine.query.paginate(page, per_page, error_out=False).items
    result = item_lines_schema.dump(all_item_lines)

    return jsonify(result)


# endpoint to create new item line number
@item_lines.route("/orders/<order_number>/itemline", methods=["POST"])
def add_item_line(order_number):
    order_number = Order.query.get(order_number)
    item_line_number = request.json["item_line_number"]
    item_number = request.json["item_number"]
    quantity = request.json["quantity"]

    new_item_line = ItemLine(item_line_number, order_number, item_number, quantity)

    db.session.add(new_item_line)
    db.session.commit()

    location = "/api/itemline/" + json.dumps(item_line_number)

    msg = {"Location:": location}

    rsp = Response(json.dumps(msg), status=201, content_type="application/json")
    return rsp


# endpoint to update item line number
@item_lines.route("/itemline/<item_line_number>", methods=["PUT"])
def item_line_update(item_line_number):
    item_line = ItemLine.query.get(item_line_number)

    quantity = request.json["quantity"]

    item_line.quantity = quantity

    db.session.commit()
    return item_line_schema.jsonify(item_line)


# endpoint to delete item line number
@item_lines.route("/itemline/<item_line_number>", methods=["DELETE"])
def item_line_delete(item_line_number):
    item_line = ItemLine.query.get(item_line_number)
    db.session.delete(item_line)
    db.session.commit()

    return item_line_schema.jsonify(item_line)
