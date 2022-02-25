from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager # this keeps track of logged in users


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.secret_key = 'super secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)



    # Import blueprints
    from .views import views
    from .auth import auth

    # register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note # see the video, the alternative is import .models

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # where should the user be redirected if not logged in
    login_manager.init_app(app)  # tells the login manager which app we is being used.

    # Tells flask how to load user and .get looks for primary id
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website1/' + DB_NAME):
        db.create_all(app=app)
        print('created database')

