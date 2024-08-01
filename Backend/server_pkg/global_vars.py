# global variables
def init_globals():
    global basePath
    global pluginList
    global cred
    global csrf
    global dropzone
    global smtp
    global app
    global socketio

    basePath = ""
    pluginList = []
    cred = []
    csrf = ""
    dropzone = ""
    smtp = ""
    app = ""
    socketio = ""


if __name__ == "__main__":
    init_globals()
