from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:just4me@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '14angelstar'




class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner
        

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username , password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')
    
@app.route('/login',methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        if user and user.password != password:
            flash('User password incorrect.', 'error')
            return redirect('/login')
        if not user:
            flash('User does not exist.', 'error')
            return redirect('/login')
        
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        if len(username) < 3 or len(password) < 3 or len(verify) < 3  :
            flash("Please enter data greater than 3 characters", 'error')
            return redirect('/signup')
        if len(username) == "" or len(password) == "" or len(verify) == "":
            flash("Enter valid data without spaces", 'error')
            return redirect('/signup')
        
        # validate user's data
        existing_user = User.query.filter_by(username=username).first()


        if not existing_user and password == verify:
            new_user = User(username, password)
           # print('made it here')
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        elif not existing_user and password != verify:
            flash('Password does not match', 'error')
            return redirect('/signup')
        else:
            flash("User already exists", 'error')
            return redirect('/login')
        #
    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

#display all blog users for home page
@app.route('/', methods=['POST', 'GET'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users)
                

#route to handle displaying main page
@app.route('/blog', methods=['POST', 'GET'])
def blog():
        
    blogs = Blog.query.all()
    

    if request.args.get('id'):
        blog_number = request.args.get('id')
        single_blog = Blog.query.filter_by(id=blog_number).first()
        return render_template('single_blog_form.html', blog=single_blog)
    #return render_template('blog_listings_form.html', blogs=blogs)

    
    elif request.args.get('user'):
        user_number = request.args.get('user')
        user = User.query.get(user_number)  
        single_user_blog = Blog.query.filter_by(owner=user).all()
        return render_template('singleUser.html', entries=single_user_blog)
    
    return render_template('blog_listings_form.html', blogs=blogs)

#handler for adding new blog entry
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    title_error = ""
    blog_error = ""

    owner = User.query.filter_by(username=session['username']).first()
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
        new_post = Blog(blog_header, blog_post,owner)
        db.session.add(new_post)
        db.session.commit()   
        return redirect('/blog?id='+str(new_post.id))
    blogs = Blog.query.all()
    return render_template('blog_entry_form.html', blogs=blogs)



if __name__ == '__main__':
    app.run()