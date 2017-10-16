from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:14lagimatua@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body


#handler for adding new blog entry
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        blog_header = request.form['blog.title']
        blog_post = request.form['blog.body']
        new_post = Blog(blog_header, blog_post)
        db.session.add(new_post)
        db.session.commit()
    blogs = Blog.query.all()
    return render_template('blog_entry_form.html', blogs=blogs)


if __name__ == '__main__':
    app.run()