from server_pkg.server.app import create_app

app, socketio, dropzone = create_app()
celery_app = app.extensions["celery"]
