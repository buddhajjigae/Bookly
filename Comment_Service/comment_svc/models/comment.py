import uuid

from datetime import datetime


class Comment(object):
    def __init__(self, user_email, text, tags):
        self.comment_id = str(uuid.uuid1())
        self.user_email = user_email
        self.comment_text = text

        self.created_date = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
        self.version_id = str(uuid.uuid4())

        self.responses = []
        self.tags = tags

    @property
    def as_dict(self):
        return self.__dict__
