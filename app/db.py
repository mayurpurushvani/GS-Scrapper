import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Db:
    def __init__(self):
        self.session = self.get_session()

    def __del__(self):
        pass

    def get_session(self):
        session = sessionmaker(bind=self.get_engine())
        return session()

    def get_engine(self):
        return create_engine(
            "mysql://{0}:{1}@{2}:{3}/{4}".format(
                os.getenv('MYSQL_USER'),
                os.getenv('MYSQL_PASSWORD'),
                os.getenv('MYSQL_HOST'),
                os.getenv('MYSQL_PORT'),
                os.getenv('MYSQL_DATABASE')
            ),
            echo=True
        )
db = Db()