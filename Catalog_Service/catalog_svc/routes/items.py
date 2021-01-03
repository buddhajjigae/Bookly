import json

from flask import jsonify, request, Response
from flask.blueprints import Blueprint

from catalog_svc.extensions import db
from catalog_svc.models.item import Item, ItemSchema

items = Blueprint("items", __name__)

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

# endpoint to show all items
@items.route("/items/", methods=["GET"])
@items.route("/items/<int:page>", methods=["GET"])
def get_items(page=None):
    per_page = None
    if page:
        per_page = 2

    all_items = Item.query.paginate(page, per_page, error_out=False).items
    result = items_schema.dump(all_items)

    return jsonify(result)


# USED FOR HATEOAS href link
# endpoint to get item details
@items.route("/item_details/<item_number>", methods=["GET"])
def get_item_details(item_number):
    item = Item.query.get(item_number)

    return item_schema.jsonify(item)


# endpoint to create new item
@items.route("/items/", methods=["POST"])
def add_item():
    item_number = request.json["item_number"]
    price = request.json["price"]
    title = request.json["title"]
    author = request.json["author"]
    isbn_10 = request.json["isbn_10"]
    isbn_13 = request.json["isbn_13"]
    publisher = request.json["publisher"]
    description = request.json["description"]

    new_item = Item(item_number, price, title, author, isbn_10, isbn_13 description)

    db.session.add(new_item)
    db.session.commit()

    location = "/api/items/" + json.dumps(item_number)

    msg = {
        "data": [
            {
                "links": [
                    {
                        "rel": "item_details", 
                        "href": "/item_details/" + item_number
                    },
                    {
                        "rel": "decrease_item_price", 
                        "href": "/decrease_price/" + item_number
                    },
                    {
                        "rel": "increase_price", 
                        "href": "/increase_price/" + item_number
                    }
                ],
                "data": {
                    "item_number": item_number,
                    "original_price": original_price,
                    "new_price": adjusted_price,
                    "title": title,
                    "author": author,
                    "publisher": publisher,
                    "description": description,
                },
            }
        ]
    }

    rsp = Response(json.dumps(msg), status=201, content_type="application/json")
    return rsp


# endpoint to update item
@items.route("/items/<item_number>", methods=["PUT"])
def item_update(item_number):
    item = Item.query.get(item_number)

    price = request.json["price"]
    description = request.json["description"]

    item.price = price
    item.description = description

    msg = {
        "data": [
            {
                "links": [
                    {
                        "rel": "item_details", 
                        "href": "/item_details/" + item_number
                    },
                    {
                        "rel": "delete_item", 
                        "href": "/items/" + item_number,
                        "method": "PUT"
                    }
                ],
                "data": {
                    "item_number": item_number,
                    "original_price": original_price,
                    "new_price": adjusted_price,
                    "title": title,
                    "author": author,
                    "publisher": publisher,
                    "description": description,
                },
            }
        ]
    }
    
    db.session.commit()
    return item_schema.jsonify(item)


# HATAEOAS attempt
# endpoint to increase item price
@items.route("/items/increase_price/<item_number>", methods=["PUT"])
def increase_price(item_number):
    item = Item.query.get(item_number)
    amount = request.json["amount"]
    title = item.title
    author = item.author
    publisher = item.publisher
    description = item.description

    original_price = item.price
    item.price = item.price + amount
    adjusted_price = item.price

    db.session.commit()

    msg = {
        "data": [
            {
                "links": [
                    {
                        "rel": "item_details", 
                        "href": "/item_details/" + item_number
                    },
                    {
                        "rel": "decrease_item_price", 
                        "href": "/decrease_price/" + item_number
                    }
                ],
                "data": {
                    "item_number": item_number,
                    "original_price": original_price,
                    "new_price": adjusted_price,
                    "title": title,
                    "author": author,
                    "publisher": publisher,
                    "description": description,
                },
            }
        ]
    }

    rsp = Response(json.dumps(msg), status=201, content_type="application/json")
    return rsp


# HATEOAS attempt
# endpoint to decrease item price
@items.route("/items/decrease_price/<item_number>", methods=["PUT"])
def decrease_price(item_number):
    item = Item.query.get(item_number)
    amount = request.json["amount"]
    title = item.title
    author = item.author
    publisher = item.publisher
    description = item.description
    
    original_price = item.price
    item.price = item.price - amount
    adjusted_price = item.price

    db.session.commit()

    msg = {
        "data": [
            {
                "links": [
                    {
                        "rel": "item_details", 
                        "href": "/item_details/" + item_number
                    },
                    {
                        "rel": "increase_item_price", 
                        "href": "/increase_price/" + item_number
                    }
                ],
                "data": {
                    "item_number": item_number,
                    "original_price": original_price,
                    "new_price": adjusted_price,
                    "title": title,
                    "author": author,
                    "publisher": publisher,
                    "description": description,
                },
            }
        ]
    }

    rsp = Response(json.dumps(msg), status=201, content_type="application/json")
    return rsp


# endpoint to delete item
@items.route("/items/<item_number>", methods=["DELETE"])
def item_delete(item_number):
    item = Item.query.get(item_number)   
    price = item.price
    title = item.title
    author = item.author
    publisher = item.publisher
    description = item.description

    db.session.delete(item)
    db.session.commit()

    msg = {
        "data": [
            {
                "links": [
                    {"rel": "item_details", "href": "/item_details/" + item_number}
                ],
                "data": {
                    "item_number": item_number,
                    "price": price,
                    "new_price": adjusted_price,
                    "title": title,
                    "author": author,
                    "publisher": publisher,
                    "description": description,
                },
            }
        ]
    }

    rsp = Response(json.dumps(msg), status=201, content_type="application/json")
    return rsp
