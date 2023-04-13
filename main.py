from flask import Flask
from flask_restful import Api

from data import db_session, goods_resources, users_resources

app = Flask(__name__)
api = Api(app)
app.config["SECRET_KEY"] = "che_za_tyagi_takie_barhatnie"


def main():
    db_session.global_init("db/market.db")

    api.add_resource(goods_resources.GoodsListResource, '/api/goods')
    api.add_resource(goods_resources.GoodsResource, '/api/goods/<int:goods_id>')
    api.add_resource(goods_resources.GoodsListResourceWithCategories, '/api/goods/catrgorieres/<cat>')
    api.add_resource(goods_resources.GoodsListResourceSearch, '/api/goods/search/<search>')
    api.add_resource(goods_resources.GoodsListResourceWithSalesmanId, '/api/goods/salesman_id/<int:salesman_id>')

    api.add_resource(users_resources.UsersListResource, '/api/users')
    api.add_resource(users_resources.UserResource, '/api/user/<int:user_id>')
    api.add_resource(users_resources.UserResourceWithEmail, "/api/user/email/<email>")
    api.add_resource(goods_resources.PhotoResource, "/api/photo/<name>")

    app.run()


if __name__ == "__main__":
    main()
