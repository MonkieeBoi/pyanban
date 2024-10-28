from bottle import Bottle, route, run, error, static_file, post, mako_template as template
from sys import argv
from data import load_data, move_item

app = Bottle()
data_path = ""


@route('/')
def home():
    data = load_data(data_path)
    return template("templates/home.html",
                    todos=data["todo"],
                    doing=data["doing"],
                    done=data["done"])


@post('/move/<id:int>/<direction>')
def move_request(id, direction):
    move_item(data_path, str(id), direction == "left")


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
    run(host='0.0.0.0',
        port=6900,
        debug=True,
        reloader=True)
