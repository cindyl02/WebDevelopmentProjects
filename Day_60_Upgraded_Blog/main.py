from flask import Flask, render_template
import requests

app = Flask(__name__)

posts = requests.get(url="https://api.npoint.io/d86a8a53412c167844b3").json()

@app.route("/")
def home_page():
    return render_template("index.html", posts=posts)


@app.route("/about")
def get_about_page():
    return render_template("about.html")


@app.route("/contact")
def get_contact_page():
    return render_template("contact.html")


@app.route("/post/<int:post_id>")
def get_post_page(post_id):
    requested_post = None
    for post in posts:
        if post["id"] == post_id:
            requested_post = post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)
