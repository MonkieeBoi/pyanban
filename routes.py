from sys import argv
from os import environ
from data import load_data, move_item
from beaker.middleware import SessionMiddleware
from dotenv import load_dotenv
from hashlib import sha512
import bottle
from bottle import (run,
                    static_file,
                    response,
                    request,
                    redirect,
                    route,
                    post,
                    error,
                    hook,
                    mako_template as template)

load_dotenv()

session_opts = {
    "session.type": "cookie",
    "session.auto": True,
    "session.validate_key": environ["VALIDATE_KEY"],
    "session.encrypt_key": environ["ENCRYPT_KEY"],
    "session.key": "session",
    "session.crypto_type": "cryptography"
}

app = SessionMiddleware(bottle.app(), session_opts)


@hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']


@route('/')
def home():
    session = request.session
    data = load_data(data_path)
    message = session.get("message", "")
    session["message"] = ""
    return template("templates/home.html",
                    todos=data["todo"],
                    doing=data["doing"],
                    done=data["done"],
                    user=request.session.get("username", ""),
                    message=message)


@post('/move/<id:int>/<direction>')
def move_request(id, direction):
    to = move_item(data_path, str(id), direction == "left")
    response.status = "200 " + to


@post('/login')
def login():
    username = request.forms.get("username")
    password = sha512(request.forms.get("password").encode())
    password = password.hexdigest()
    print(password)

    users = load_data(data_path)["users"]

    if username not in users:
        request.session["message"] = "User does not exist"
        return redirect("/")

    if users[username]["password"] != password:
        request.session["message"] = "Wrong password"
        return redirect("/")

    request.session["username"] = username
    return redirect("/")


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, "./static")


@error(404)
def error404(error):
    return template("templates/error404.html")


if __name__ == "__main__":
    if (len(argv) < 2):
        print("Missing data path")
        exit()
    data_path = argv[1]
    run(app=app,
        host='0.0.0.0',
        port=6900,
        debug=True,
        reloader=True)
