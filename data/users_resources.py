from flask import jsonify
from flask_restful import reqparse, Resource, abort

from data import db_session
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument("firstname", required=True)
parser.add_argument("secondname", required=True)
parser.add_argument("email", required=True)
parser.add_argument("hashed_password", required=True)
parser.add_argument("status", required=True)


class UserResourceWithEmail(Resource):
    def get(self, email):
        session = db_session.create_session()
        user = session.query(User).filter(User.email == email).first()
        if user is None:
            return jsonify({"message": f"user with email {email} not found"})
        return jsonify(user.to_dict(
            only=("id", "firstname", "secondname", "email",
                  "hashed_password", "status")))

    def delete(self, email):

        session = db_session.create_session()
        user = session.query(User).filter(User.email == email).first()
        if user is None:
            return jsonify({"message": f"user with email {email} not found"})
        session.delete(user)
        session.commit()
        return jsonify({"success": "OK"})


class UserResource(Resource):
    def get(self, user_id):
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        if user is None:
            return jsonify({"message": f"user with id {user_id} not found"})
        return jsonify(user.to_dict(
            only=("id", "firstname", "secondname", "email",
                  "hashed_password", "status")))

    def delete(self, user_id):
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        if user is None:
            return jsonify({"message": f"user with id {user_id} not found"})
        session.delete(user)
        session.commit()
        return jsonify({"success": "OK"})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify([item.to_dict(
            only=("id", "firstname", "secondname", "email",
                  "hashed_password", "status")) for item in users])

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            firstname=args["firstname"],
            secondname=args["secondname"],
            email=args["email"],
            hashed_password=args["hashed_password"],
            status=args["status"]
        )
        session.add(user)
        session.commit()
        return jsonify({"success": "OK"})
