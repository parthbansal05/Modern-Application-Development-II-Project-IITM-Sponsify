from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_socketio import SocketIO

from flask_dropzone import Dropzone
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS

from celery import Celery, Task
from celery.schedules import crontab
from . import task_routes

from flask_mail import Mail, Message

from .. import global_vars as gv

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
socketio = SocketIO()
dropzone = Dropzone()
cors = CORS()
jwt = JWTManager()


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

def create_app():
    app = Flask(__name__)
    
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost",
            result_backend="redis://localhost",
            task_ignore_result=True,
            beat_schedule={
                'daily-task': {
                    'task': 'server_pkg.server.tasks.daily_task',
                    # 'schedule': crontab(hour=18, minute=0),
                    'schedule': crontab(minute="*"),
                    'args': (),
                },
                'monthly-task': {
                    'task': 'server_pkg.server.tasks.monthly_task',
                    # 'schedule': crontab(day_of_month=1, hour=0, minute=0),
                    'schedule': crontab(minute="*/2"),
                    'args': (),
                },
            },
        ),
    )

    app.config.from_prefixed_env()
    celery_init_app(app)
    app.register_blueprint(task_routes.bp)

    app.config.update(
    SECRET_KEY='&wZzC)ihhrt(.{!D6K.UL$twQ5/8;78Gia{!L*ui8u39jkU98U93BT6_k?z=u%C?=AJ?r7y/9(bn,Y4ahn?v_G?Ae_)pMQNj{$$=4$r{Fnk;EaMK',
    SQLALCHEMY_DATABASE_URI='sqlite:///UserDB.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    static_folder='static',
    )

    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = ''
    app.config['MAIL_PASSWORD'] = ''
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    mail = Mail(app) 
    gv.mail = mail


    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    socketio.init_app(app)
    dropzone.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    
    return app, socketio, dropzone
