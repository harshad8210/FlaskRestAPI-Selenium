from VahanApp import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


class Cookies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driverName = db.Column(db.String(20), nullable=False)
    domain = db.Column(db.String(60), nullable=False)
    httpOnly = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(60), nullable=False)
    path = db.Column(db.String(60), nullable=False)
    sameSite = db.Column(db.String(60), nullable=False)
    secure = db.Column(db.Boolean, default=False)
    value = db.Column(db.String(60), nullable=False)

    def __init__(self, data):
        self.domain = data.get("domain")
        self.httpOnly = data.get("httpOnly")
        self.name = data.get("name")
        self.path = data.get("path")
        self.sameSite = data.get("sameSite")
        self.secure = data.get("secure")
        self.value = data.get("value")

    def __repr__(self):
        return f"Cookies('{self.domain}','{self.httpOnly}','{self.name}','{self.path}','{self.sameSite}','{self.secure}','{self.value}')"

    @classmethod
    def get_cookies(cls, driverName):
        """
        find the existing user with user id
        :param id: integer
        :return: user or None
        """
        return cls.query.filter_by(driverName=driverName).all()

    def update(self, data):
        """
        Update cookies data
        :param data:
        :return:
        """
        try:
            for key, item in data.items():
                setattr(self, key, item)
            db.session.commit()
            return self
        except (IntegrityError, SQLAlchemyError) as error:
            db.session.rollback()
            raise error


class SearchCount(db.Model):
    driverName = db.Column(db.String, primary_key=True)
    searchCount = db.Column(db.Integer, default=0)

    def __init__(self, data):
        self.driverName = data.get("driverName")
        self.searchCount = data.get("searchCount")

    def __repr__(self):
        return f"Search Count('{self.driverName}','{self.searchCount}')"

    @classmethod
    def get_search_count(cls, driverName):
        """
        find the existing user with user id
        :param driverName: string
        :return: user or None
        """
        # return cls.query.first()
        return cls.query.filter_by(driverName=driverName).first()

    def update(self, data):
        """
        Update search vehicle count
        :param data:
        :return:
        """
        try:
            for key, item in data.items():
                setattr(self, key, item)
            db.session.commit()
            return self
        except (IntegrityError, SQLAlchemyError) as error:
            db.session.rollback()
            raise error

