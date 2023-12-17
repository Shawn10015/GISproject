from flask import Flask

def create_app():
    app = Flask(__name__)

    from .views import users, products
    app.register_blueprint(users.bp)
    app.register_blueprint(products.bp)

    return app
