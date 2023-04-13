from flask import jsonify, send_file
from flask_restful import reqparse, Resource, abort
from os import remove
from data import db_session
from data.goods import Goods

parser = reqparse.RequestParser()
parser.add_argument("title", required=True)
parser.add_argument("category", required=True)
parser.add_argument("price", required=True)
parser.add_argument("salesman_id", required=True, type=int)
parser.add_argument("short_description", required=True)
parser.add_argument("long_description", required=True)
parser.add_argument("social_salesman", required=True)
parser.add_argument("phonenumber_salesman", required=True)


class GoodsResource(Resource):
    def get(self, goods_id):
        session = db_session.create_session()
        goods = session.query(Goods).get(goods_id)
        if goods is None:
            return jsonify({"message": f"goods with id {goods_id} not found"})
        return jsonify(goods.to_dict(
            only=("id", "title", "category", "price", "salesman_id",
                  "short_description", "long_description", "social_salesman",
                  "phonenumber_salesman")))

    def delete(self, goods_id):
        session = db_session.create_session()
        goods = session.query(Goods).get(goods_id)
        if goods is None:
            return jsonify({"message": f"goods with id {goods_id} not found"})
        session.delete(goods)
        session.commit()
        remove(f"data/goods_photos/{goods_id}.jpg")
        return jsonify({"message": "OK"})


class GoodsListResourceWithCategories(Resource):
    def get(self, cat):
        session = db_session.create_session()
        goods = session.query(Goods).filter(Goods.category == cat)
        if goods is None:
            return jsonify({"message": f"goods with categories {cat} not found"})
        return jsonify({"goods": [item.to_dict(
            only=("id", "title", "category", "price", "salesman_id",
                  "short_description", "long_description", "social_salesman",
                  "phonenumber_salesman")) for item in goods]})


class GoodsListResourceSearch(Resource):
    def get(self, search):
        session = db_session.create_session()
        goods = session.query(Goods).all()
        for i in goods:
            if search.lower() not in i.title.lower():
                del goods[goods.index(i)]
        if goods is None:
            return jsonify({"message": f"goods with {search} not found"})
        return jsonify({"goods": [item.to_dict(
            only=("id", "title", "category", "price", "salesman_id",
                  "short_description", "long_description", "social_salesman",
                  "phonenumber_salesman")) for item in goods]})


class GoodsListResourceWithSalesmanId(Resource):
    def get(self, salesman_id):
        session = db_session.create_session()
        goods = session.query(Goods).filter(Goods.salesman_id == salesman_id)
        if goods is None:
            return jsonify({"message": f"goods with salesman_id {salesman_id} not found"})
        return jsonify({"goods": [item.to_dict(
            only=("id", "title", "category", "price", "salesman_id",
                  "short_description", "long_description", "social_salesman",
                  "phonenumber_salesman")) for item in goods]})


class GoodsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        goods = session.query(Goods).all()
        return jsonify({"goods": [item.to_dict(
            only=("id", "title", "category", "price", "salesman_id",
                  "short_description", "long_description", "social_salesman",
                  "phonenumber_salesman")) for item in goods]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        goods = Goods(
            title=args["title"],
            category=args["category"],
            price=args["price"],
            salesman_id=args["salesman_id"],
            short_description=args["short_description"],
            long_description=args["long_description"],
            social_salesman=args["social_salesman"],
            phonenumber_salesman=args["phonenumber_salesman"]
        )
        session.add(goods)
        session.commit()
        return jsonify({"success": "OK"})


class PhotoResource(Resource):
    def get(self, name):
        return send_file(f"data/goods_photos/{name}.jpg", mimetype="image/jpg")
