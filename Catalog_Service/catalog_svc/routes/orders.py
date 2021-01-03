import json

from flask import jsonify, request, Response
from flask.blueprints import Blueprint

from catalog_svc.extensions import db
from catalog_svc.models.order import Order, OrderSchema

orders = Blueprint("orders", __name__)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# /orders

# endpoint to show all orders
@orders.route("/orders/", methods=["GET"])
@orders.route("/orders/<int:page>", methods=["GET"])
def get_orders(page=None):
    per_page = None
    if page:
        per_page = 2

    all_orders = Order.query.paginate(page, per_page, error_out=False).items
    result = orders_schema.dump(all_orders)

    return jsonify(result)


# endpoint to create new order
@orders.route("/orders/", methods=["POST"])
def add_order():
    order_number = request.json["order_number"]
    item_number = request.json["item_line_number"]
    user_id = request.json["user_id"]
    date = request.json["date"]
    comments = request.json["comments"]

    new_order = Order(order_number, item_number, user_id, date, comments)

    db.session.add(new_order)
    db.session.commit()

    location = "/api/orders/" + json.dumps(order_number)

    msg = {"Location:": location}

    rsp = Response(json.dumps(msg), status=201, content_type="application/json")
    return rsp


# /orders/<order_number>


# endpoint to update order
@orders.route("/orders/<order_number>", methods=["PUT"])
def order_update(order_number):
    order = Order.query.get(order_number)
    comments = request.json["comments"]

    order.comments = comments

    db.session.commit()
    return order_schema.jsonify(order)


# endpoint to delete order
@orders.route("/orders/<order_number>", methods=["DELETE"])
def order_delete(order_number):
    order = Order.query.get(order_number)
    db.session.delete(order)
    db.session.commit()

    return order_schema.jsonify(order)
