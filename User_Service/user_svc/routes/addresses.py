from flask import jsonify, request
from flask import render_template
from smartystreets_python_sdk import StaticCredentials, ClientBuilder
from smartystreets_python_sdk.us_extract import Lookup as ExtractLookup
from smartystreets_python_sdk.us_autocomplete import (
    Lookup as AutocompleteLookup,
    geolocation_type,
)
from flask.blueprints import Blueprint

from user_svc.extensions import db
from user_svc.models.address import Address, AddressSchema

addresses = Blueprint("addresses", __name__)

address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)

# /addresses


@addresses.route("/autocompleteSmartyStreets/", methods=["GET"])
def autoCompleteSmartyAPI():
    addr = request.args.get("address")
    auth_id = "4db04845-3fbe-8b38-d005-5dc10f75a80b"
    auth_token = "pAKyFrPrrfishQdMPgzU"
    credentials = StaticCredentials(auth_id, auth_token)
    client = ClientBuilder(credentials).build_us_autocomplete_api_client()
    lookup = AutocompleteLookup(addr)
    client.send(lookup)
    local_res = []
    for suggestion in lookup.result:
        local_res.append(suggestion.text)
    return jsonify(local_res)


@addresses.route("/verifyAddress/")
def verifyAddr():
    return render_template("index.html")


@addresses.route("/verifyInputAddress/", methods=["GET"])
def verifyUserInput():
    addr = request.args.get("text")
    auth_id = "4db04845-3fbe-8b38-d005-5dc10f75a80b"
    auth_token = "pAKyFrPrrfishQdMPgzU"
    credentials = StaticCredentials(auth_id, auth_token)
    client = ClientBuilder(credentials).build_us_extract_api_client()
    lookup = ExtractLookup()
    lookup.text = addr
    lookup.aggressive = True
    lookup.addresses_have_line_breaks = False
    lookup.addresses_per_line = 1
    result = client.send(lookup)
    metadata = result.metadata
    print("Found {} addresses.".format(metadata.address_count))
    print("{} of them were valid.".format(metadata.verified_count))
    print()
    return jsonify(metadata.verified_count)


# endpoint to show all addresses
@addresses.route("/addresses/", methods=["GET"])
@addresses.route("/addresses/<int:page>", methods=["GET"])
def get_addresses(page=None):
    per_page = None
    if page:
        per_page = 2

    all_addresses = Address.query.paginate(page, per_page, error_out=False).items

    result = addresses_schema.dump(all_addresses)
    return jsonify(result)


# endpoint to create new address
@addresses.route("/addresses", methods=["POST"])
def add_address():
    street1 = request.json["street_no_1"]
    street2 = request.json["street_no_2"]
    state = request.json["state"]
    country = request.json["country"]
    postal_code = request.json["postal_code"]
    new_address = Address(street1, street2, state, country, postal_code)

    db.session.add(new_address)
    db.session.commit()

    return address_schema.jsonify(new_address)


# endpoint to get address detail by id
@addresses.route("/addresses/<id>", methods=["GET"])
def address_detail(id):
    address = Address.query.get(id)
    return address_schema.jsonify(address)


# endpoint to update address
@addresses.route("/addresses/<id>", methods=["PUT"])
def address_update(id):
    address = Address.query.get(id)

    street1 = request.json["street_no_1"]
    street2 = request.json["street_no_2"]
    state = request.json["state"]
    country = request.json["country"]
    postal_code = request.json["postal_code"]

    address.street_no_1 = street1
    address.street_no_2 = street2
    address.state = state
    address.country = country
    address.postal_code = postal_code

    db.session.commit()
    return address_schema.jsonfy(address)


@addresses.route("/users/<id>", methods=["DELETE"])
def address_delete(id):
    address = Address.query.get(id)
    db.session.delete(address)
    db.session.commit()

    return address_schema.jsonify(address)
