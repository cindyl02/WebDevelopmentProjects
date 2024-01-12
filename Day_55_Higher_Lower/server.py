from flask import Flask
import random

app = Flask(__name__)
random_number = random.randint(0, 9)
print(random_number)


@app.route("/")
def home_page():
    return ('<h1 style="text-align: center">Guess a number between 0 and 9</h1>'
            '<img src="https://media.giphy.com/media/chzz1FQgqhytWRWbp3/giphy.gif" width=500>')


@app.route("/<int:number>")
def page(number):
    if number < random_number:
        return (f'<h1 style="color: red">Too low, try again!</h1>'
                '<img src="https://media.giphy.com/media/saJYuwjsF8Kfm/giphy.gif" width=500>')
    elif number > random_number:
        return (f'<h1 style="color: blue">Too high, try again!</h1>'
                '<img src="https://media.giphy.com/media/U1LED36Q78kqxiLt0K/giphy.gif" width=500>')
    else:
        return (f'<h1 style="color: green">You found me!</h1>'
                '<img src="https://media.giphy.com/media/6IxTpqbf5WVA4/giphy.gif" width=500>')


if __name__ == '__main__':
    app.run(debug=True)
