from catalog_svc.extensions import db, ma


class Order(db.Model):
    order_number = db.Column(db.Integer, primary_key=True)
    item_line_number = db.Column(db.Integer)
    user_id = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    comments = db.Column(db.String(512))

    def __init__(self, order_number, item_line_number, user_id, date, comments):
        self.order_number = order_number
        self.item_line_number = item_line_number
        self.user_id = user_id
        self.date = date
        self.comments = comments


class OrderSchema(ma.Schema):
    class Meta:
        fields = (
            "order_number",
            "item_line_number",
            "user_id",
            "date",
            "comments",
        )
