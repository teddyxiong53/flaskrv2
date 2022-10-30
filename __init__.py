from distutils.command.config import config
import os

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flaskrv2.config import config
from flaskrv2 import dbcmd

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    print(app.config)

    @app.route('/hello')
    def hello():
        return 'hello flaskrv2'
    
    from flaskrv2 import auth, blog
    dbcmd.init_app(app)
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    app.add_url_rule('/', endpoint='index')
    return app
