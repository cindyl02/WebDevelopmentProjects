from flask import Flask, render_template
import random
import requests
import datetime as dt

app = Flask(__name__)


@app.route("/")
def home():
    random_number = random.randint(1, 10)
    year = dt.datetime.now().year
    return render_template("index.html", num=random_number, year=year)


@app.route("/guess/<name>")
def guess(name):
    data = {
        "name": name
    }
    response = requests.get(url="https://api.agify.io", params=data)
    age = response.json()["age"]
    response = requests.get(url="https://api.genderize.io", params=data)
    gender = response.json()["gender"]

    return render_template("guess.html", name=name, gender=gender, age=age)


@app.route("/blog/<num>")
def get_blog(num):
    print(num)
    blog_url = "https://api.npoint.io/d39c25a6fe7aa8f6c26b"
    response = requests.get(blog_url)
    all_posts = response.json()

    return render_template("blog.html", posts=all_posts)


if __name__ == "__main__":
    app.run(debug=True)
