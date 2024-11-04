from os import environ, path
from data import load_data, move_item, add_user, add_item
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

application = bottle.default_app()
data_path = environ["DATA_PATH"]


@hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']


@route('/')
def home():
    session = request.session
    data = load_data(data_path)
    message = session.get("message", "")
    session["message"] = ""
    if session.get("username", "") not in data["users"]:
        session["username"] = ""
    return template("templates/home.html",
                    todos=data["todo"],
                    doing=data["doing"],
                    done=data["done"],
                    user=session.get("username", ""),
                    message=message,
                    users=data["users"])


@post('/move/<id:int>/<direction>')
def move_request(id, direction):
    id = str(id)
    data = load_data(data_path)
    item = (data["todo"].get(id, None)
            or data["doing"].get(id, None)
            or data["done"].get(id, None))
    if not item:
        request.session["message"] = "Item doesn't exist"
        redirect("/")
    if item["owner"] != request.session.get("username", ""):
        request.session["message"] = "Not yours don't touch"
        redirect("/")

    to = move_item(data_path, id, direction == "left")
    response.status = "200 " + to


@post('/login')
def login():
    username = request.forms.get("username")
    password = sha512(request.forms.get("password").encode())
    password = password.hexdigest()

    users = load_data(data_path)["users"]

    if username not in users:
        request.session["message"] = "User does not exist"
        return redirect("/")

    if users[username]["password"] != password:
        request.session["message"] = "Wrong password"
        return redirect("/")

    request.session["username"] = username
    return redirect("/")


@post('/addtask')
def addtask():
    if "username" not in request.session:
        request.session["message"] = "Not logged in"
        return redirect('/')

    text = request.forms.get("description")
    date = request.forms.get("date")
    time = request.forms.get("time")
    add_item(data_path, "todo", text,
             ("/".join(date.split("-")[::-1]) + " " + time),
             request.session["username"])

    return redirect('/')


@post('/signup')
def signup():
    username = request.forms.get("username")
    pfp = request.files.get("pfp")
    password = sha512(request.forms.get("password").encode())
    password = password.hexdigest()

    if not (username and pfp and request.forms.get("password", None)):
        request.session["message"] = "Missing field!"
        return redirect("/")

    users = load_data(data_path)["users"]

    if username in users:
        request.session["message"] = "Username has been taken"
        return redirect("/")
    request.session["username"] = username
    name, ext = path.splitext(pfp.filename)
    add_user(data_path, username, password, ext)
    pfp.save(f"static/images/pfps/{username}{ext}", overwrite=True)
    request.body.close()

    return redirect("/")


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, "./static")


@error(404)
def error404(error):
    return template("templates/error404.html")


if __name__ == "__main__":
    session_opts = {
        "session.type": "cookie",
        "session.auto": True,
        "session.cookie_expires": False,
        "session.validate_key": environ["VALIDATE_KEY"],
        "session.encrypt_key": environ["ENCRYPT_KEY"],
        "session.key": "session",
        "session.crypto_type": "cryptography"
    }

    app = SessionMiddleware(application, session_opts)
    run(app=app,
        host='0.0.0.0',
        port=6900,
        debug=True,
        reloader=True)
