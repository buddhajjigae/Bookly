from user_svc.extensions import db, ma


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street_no_1 = db.Column(db.String(80))
    street_no_2 = db.Column(db.String(80))
    city = db.Column(db.String(40))
    state = db.Column(db.String(40))
    country = db.Column(db.String(40))
    postal_code = db.Column(db.Integer)

    def __init__(self, street1, street2, city, state, country, pcode):
        self.street_no_1 = street1
        self.street_no_2 = street2
        self.city = city
        self.state = state
        self.country = country
        self.postal_code = pcode


class AddressSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "street_no_1",
            "street_no_2",
            "city",
            "state",
            "country",
            "postal_code",
        )
