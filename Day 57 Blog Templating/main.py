from flask import Flask, render_template
import requests
from post import Post

# Get the DATA, make a list of POST objects with the corresponding info
url = 'https://api.npoint.io/c790b4d5cab58020d391'
all_posts_data = requests.get(url=url).json()
posts = []
for post in all_posts_data:
    post_obj = Post(post['id'], post['title'], post['subtitle'], post['body'])
    posts.append(post_obj)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", posts=posts)

@app.route('/post/<int:post_id>')
def get_post(post_id):
    requested_post = None
    for blog_post in posts:
        if blog_post.id == post_id:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True)