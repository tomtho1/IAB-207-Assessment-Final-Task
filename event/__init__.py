# import flask - from the package import class
import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# this is the name of the module/package that is calling this app
app = Flask(__name__)


# create a function that creates a web application
# a web server will run this web application
def create_app():
    app.debug = True
    app.secret_key = 'utroutoru'
    # set the app configuration data

    database_uri = os.getenv("DATABASE_URL") or 'sqlite:///event_data.sqlite'
    if database_uri.startswith("postgres://"):  # fix for sqlalchemy & heroku
        database_uri = database_uri.replace("postgres://", "postgresql://", 1)

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # initialize db with flask app
    db.init_app(app)

    bootstrap = Bootstrap5(app)

    # initialize the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from . import users
    app.register_blueprint(users.bp)
    from . import artist
    app.register_blueprint(artist.bp)
    from . import events    
    app.register_blueprint(events.bp)
    from . import bookings
    app.register_blueprint(bookings.bp)
    from . import image
    app.register_blueprint(image.bp)
    from . import venue    
    app.register_blueprint(venue.bp)

    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    return app


@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    return render_template("error.html", error='404', message='Page Not Found', sub_message='The page you are looking for does not exist.')

@app.errorhandler(403)
# inbuilt function which takes error as parameter
def not_found(e):
    return render_template("error.html", error='403', message='Forbidden', sub_message="You don't have the permission to access the requested resource. It is either read-protected or not readable by the server.")

@app.errorhandler(500)
# inbuilt function which takes error as parameter
def not_found(e):
    return render_template("error.html", error='500', message='Internal Server Error',
                           sub_message='The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.')
