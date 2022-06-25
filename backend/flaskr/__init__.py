import os

from flask import Flask
from flask_cors import CORS, cross_origin
from .variables import ORIGINS_URLS


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, origins=ORIGINS_URLS)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
    )


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'


    from . import db
    db.init_app(app)

    from . import score
    app.register_blueprint(score.bp)

    from . import game
    app.register_blueprint(game.bp)

    return app

app = create_app()
