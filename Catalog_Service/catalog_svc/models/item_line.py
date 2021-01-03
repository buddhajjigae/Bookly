from catalog_svc.extensions import db, ma


class ItemLine(db.Model):
    item_line_number = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.Integer)
    item_number = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    def __init__(self, item_line_number, order_number, item_number, quantity):
        self.item_line_number = item_line_number
        self.order_number = order_number
        self.item_number = item_number
        self.quantity = quantity


class ItemLineSchema(ma.Schema):
    class Meta:
        fields = (
            "item_line_number",
            "order_number",
            "item_number",
            "quantity",
        )
