from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@gisproject-postgres-1/gisDB'
    db.init_app(app)
    Swagger(app)

    from .views.City import city_bp
    app.register_blueprint(city_bp, url_prefix='/city')
    from .views.Province import province_bp
    app.register_blueprint(province_bp, url_prefix='/province')
    from .views.Scenic_spots import scenic_spots_bp
    app.register_blueprint(scenic_spots_bp, url_prefix='/scenic')
    from .views.Info import info_bp
    app.register_blueprint(info_bp, url_prefix='/info')

    return app
