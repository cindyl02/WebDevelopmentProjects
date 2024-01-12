from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return ('<h1 style="text-align: center">Hello, World!</h1>'
            '<p>This is a paragraph</p>'
            '<img src="https://media.giphy.com/media/YRVP7mapl24G6RNkwJ/giphy.gif" width=200>')


def make_bold(function):
    def wrapper_function():
        return f"<b>{function()}</b>"

    return wrapper_function


def make_underline(function):
    def wrapper_function():
        return f"<u>{function()}</u>"

    return wrapper_function


def make_emphasis(function):
    def wrapper_function():
        return f"<em>{function()}</em>"

    return wrapper_function


@app.route("/bye")
@make_bold
@make_underline
@make_emphasis
def bye():
    return "Bye!"


if __name__ == "__main__":
    app.run(debug=True)
