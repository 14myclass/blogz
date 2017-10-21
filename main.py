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

#route to handle displaying main page
@app.route('/blog', methods=['POST', 'GET'])
def blog():
    #if request.method == 'POST':
       # blog_header = request.form['blog.title']
        #blog_post = request.form['blog.body']
    #else:
        #blog_number = request.args.get('id')
        #blogs = Blog.query.filter_by(id=blog_number).all()
        #return render_template('single_blog_form.html', blog=blogs)
        
    blogs = Blog.query.all()
    
    if request.args:
        blog_number = request.args.get('id')
        #blogs = Blog.query.get(id='blog_number')
        single_blog = Blog.query.filter_by(id=blog_number).first()
        return render_template('single_blog_form.html', blog=single_blog)
    
    return render_template('blog_listings_form.html', blogs=blogs)
#displays single entry when blog title selected
#@app.route('/blog?id=', methods=['GET'])
#def single_blog():
    #blog_number = int(request.args.get('id'))
    #blogs = Blog.query.filter_by(id=blog_number).all()
    #return render_template('single_blog_form.html', blog=blogs.id)





#handler for adding new blog entry
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    title_error = ""
    blog_error = ""
    if request.method == 'POST':
        blog_header = request.form['blog.title']
        blog_post = request.form['blog.body']
        if blog_header =="" and blog_post !="":
            title_error = "Please type a title."
            return render_template('blog_entry_form.html', title_error=title_error, b_body=blog_post)
        elif blog_post =="" and blog_header !="":
            blog_error = "Enter text please."
            return render_template('blog_entry_form.html', blog_error=blog_error,b_title=blog_header)
        elif blog_header =="" and blog_post =="":
            title_error = "Please type a title."
            blog_error = "Enter text please."
            return render_template('blog_entry_form.html',title_error=title_error,blog_error=blog_error)
        new_post = Blog(blog_header, blog_post)
        db.session.add(new_post)
        db.session.commit()
    blogs = Blog.query.all()
    return render_template('blog_entry_form.html', blogs=blogs)



if __name__ == '__main__':
    app.run()