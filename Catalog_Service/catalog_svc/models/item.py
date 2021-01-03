from catalog_svc.extensions import db, ma


class Item(db.Model):
    item_number = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    title = db.Column(db.String(45))
    author = db.Column(db.String(45))
    isbn_10 = db.Column(db.String(15))
    isbn_13 = db.Column(db.String(15))
    publisher = db.Column(db.String(128))
    description = db.Column(db.String(512))

    def __init__(self, item_number, price, title, author, isbn_10, isbn_13, publisher, description):
        self.item_number = item_number
        self.price = price
        self.title = title
        self.author = author
        self.isbn_10 = isbn_10
        self.isbn_13 = isbn_13
        self.publisher = publisher
        self.description = description


class ItemSchema(ma.Schema):
    class Meta:
        fields = (
            "item_number",
            "price",
            "title",
            "author",
            "isbn_10",
            "isbn_13",
            "publisher",
            "description",
        )
