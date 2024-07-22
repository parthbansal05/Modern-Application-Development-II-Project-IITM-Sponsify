from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_socketio import SocketIO

from flask_dropzone import Dropzone
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
socketio = SocketIO()
dropzone = Dropzone()
cors = CORS()
jwt = JWTManager()



def create_app():
    app = Flask(__name__)
    app.config.update(
    SECRET_KEY='&wZzC)ihhrt(.{!D6K.UL$twQ5/8;78Gia{!L*ui8u39jkU98U93BT6_k?z=u%C?=AJ?r7y/9(bn,Y4ahn?v_G?Ae_)pMQNj{$$=4$r{Fnk;EaMK',
    SQLALCHEMY_DATABASE_URI='sqlite:///UserDB.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    static_folder='static',
    # SERVER_NAME = '0.0.0.0'
)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    socketio.init_app(app)
    dropzone.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    
    return app, socketio, dropzone
