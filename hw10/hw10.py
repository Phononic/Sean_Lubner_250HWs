from flask import Flask, render_template, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

app.debug = True

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __str__(self):
        return 'Yo, my name is %r' % self.username

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    addresses = db.relationship('Address', backref='person',
                                lazy='dynamic')

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))


db.create_all()
admin = User('admin', 'admin@example.com')
guest = User('guest', 'guest@example.com')
db.session.add(admin)
db.session.add(guest)
try:
	db.session.commit()
except:
	pass

@app.route("/") # Main page
@app.route("/index.html")
@app.route("/home")
def home():
    """ Home page """
    # Specify links:
    links_list = [url_for("upload_file"),
                  'Insert a Collection',
                  url_for("query_database"),
                  'Run a Query']
    
    return render_template('base.html',
                           window_title='BibTex Viewer | Main Page',
                           page_title='Home Page',
                           links=links_list)

@app.route("/insert_collection", methods=['GET', 'POST'])
def upload_file():
    """ Function for inserting a collection """
    links_list = [url_for("home"),
                  'Back to Home Page']
    if request.method == 'POST':
        collection = request.form['col_name']
        return "Name of collection to upload is: '{0:s}'".format(collection)
    else:
    	## this is a normal GET request
        return render_template('upload_file.html',
                           links=links_list)    

@app.route("/query")
def query_database():
    return "query place-holder page"

@app.route("/users")
def get_users():
   print " ".join([str(x) for x in User.query.all()])
   return str([x.email for x in User.query.all()])

@app.route("/admin")
def get_admin_email():
   admin = User.query.filter_by(username='admin').first()
   return "<b>Admin Email</b>: %s" % admin.email

if __name__ == "__main__":
    app.run()
