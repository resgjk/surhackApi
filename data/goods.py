import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Goods(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "goods"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    category = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.String)
    salesman_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    short_description = sqlalchemy.Column(sqlalchemy.String)
    long_description = sqlalchemy.Column(sqlalchemy.String)
    social_salesman = sqlalchemy.Column(sqlalchemy.String)
    phonenumber_salesman = sqlalchemy.Column(sqlalchemy.String)
