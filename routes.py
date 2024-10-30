from sys import argv
from data import load_data, move_item
from bottle import (Bottle,
                    run,
                    static_file,
                    response,
                    request,
                    redirect,
                    mako_template as template)

app = Bottle()


@app.route('/')
def home():
    data = load_data(data_path)
    return template("templates/home.html",
                    todos=data["todo"],
                    doing=data["doing"],
                    done=data["done"],
                    user="")


@app.post('/move/<id:int>/<direction>')
def move_request(id, direction):
    to = move_item(data_path, str(id), direction == "left")
    response.status = "200 " + to


@app.post('/login')
def login():
    username = request.forms.get("username")
    password = request.forms.get("password")
    print(username, password)
    return redirect("/")


@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, "./static")


@app.error(404)
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
