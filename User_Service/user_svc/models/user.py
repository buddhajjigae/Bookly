from datetime import datetime

from user_svc.extensions import db, ma


class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    last_name = db.Column(db.String(80))
    first_name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    hashed_password = db.Column(db.String(120), unique=True)
    address_id = db.Column(db.String(45))
    role = db.Column(db.String(120))
    created_date = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    status = db.Column(db.String(80))

    # added status and timestamp
    def __init__(
        self,
        uuid,
        last_name,
        first_name,
        email,
        hashed_password,
        address_id,
        role,
        created_date,
        status="PENDING",
    ):
        self.id = uuid
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        self.hashed_password = hashed_password
        self.address_id = address_id
        self.role = role
        self.created_date = created_date
        self.status = status


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose

        fields = (
            "id",
            "last_name",
            "first_name",
            "email",
            "hashed_password",
            "address_id",
            "role",
            "created_date",
            "status",
        )
