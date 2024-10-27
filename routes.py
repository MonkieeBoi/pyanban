from bottle import Bottle, route, run, error, static_file, mako_template as template

app = Bottle()


@route('/')
def home():
    return template("templates/home.html")


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, "./static")


@error(404)
def error404(error):
    return template("templates/error404.html")


if __name__ == "__main__":
    run(host='0.0.0.0',
        port=6900,
        debug=True,
        reloader=True)
