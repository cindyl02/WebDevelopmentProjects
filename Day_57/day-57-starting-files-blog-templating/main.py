from flask import Flask, render_template
from post import Post
import requests

app = Flask(__name__)

response = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
all_posts = []
for post in response:
    all_posts.append(Post(id=post["id"], title=post["title"], subtitle=post["subtitle"], body=post["body"]))


@app.route("/")
def home():
    return render_template("index.html", posts=all_posts)


@app.route("/post/<int:blog_id>")
def get_blog_post(blog_id):
    get_post = None
    for post in all_posts:
        if post.id == blog_id:
            get_post = post
    return render_template("post.html", post=get_post)


if __name__ == "__main__":
    app.run(debug=True)
