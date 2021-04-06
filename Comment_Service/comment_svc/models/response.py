import uuid

from datetime import datetime


class Response(object):
    def __init__(self, user_email, text):
        self.response_id = str(uuid.uuid1())
        self.user_email = user_email
        self.response_text = text

        self.created_date = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
        self.version_id = str(uuid.uuid4())

    @property
    def as_dict(self):
        return self.__dict__
