import os
from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bib', 'aux'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.debug = True

#--------------------- Home Page ---------------------
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
                           links=links_list,
                           db_present=(len(dbs) > 0),
                           content='Current databases:' + str(dbs) + '\nsize: ' + str(len(dbs)))

#--------------------- File Uploading ---------------------
duplicates = [False, False] # [collection_name_taken, file_name_taken]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#@app.route('/uploads/<filename>')
#def uploaded_file(filename):
#    return send_from_directory(app.config['UPLOAD_FOLDER'],  filename)

def process_file(filename, col_name, the_file):
    """ Verify entries, parse the file, and create a database from it """
    if len(col_name.strip(' ')) == 0: # if no name provided for collection, use file name
        col_name = ''.join(secure_filename(the_file.filename).split('.')[:-1])

    if col_name in dbs.keys(): # if collection name already taken
        duplicates[0] = True
        return redirect(url_for('upload_file'))

    if filename in os.listdir(app.config['UPLOAD_FOLDER']): # if filename name already taken
                duplicates[1] = True
                duplicates[0] = False
                return redirect(url_for('upload_file'))

    duplicates[0] = False
    duplicates[1] = False
    dbs[col_name] = the_file # add to dictionary of databases
    the_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('home'))    

@app.route('/insert_collection', methods=['GET', 'POST'])
def upload_file():
    """ Function for inserting a collection """
    links_list = [url_for("home"),
                  'Back to Home Page']
    if request.method == 'POST':
        bib_file = request.files['col_file']
        bib_name = request.form['col_name']
        if bib_file and allowed_file(bib_file.filename):
            filename = secure_filename(bib_file.filename)
            return process_file(filename, bib_name, bib_file)
    else:
        comment = "Please insert a new collection by uploading a Bibtex file with the form below."
        return render_template('upload_file.html',
                               links=links_list,
                               db_present=(len(dbs) > 0),
                               content=comment + 'col_name_taken is: ' + str(duplicates[0]) + ', file_name_taken is: ' + str(duplicates[1]),
                               dupes=duplicates)

#--------------------- Querying ---------------------
@app.route("/query")
def query_database():
    return "query place-holder page"

#--------------------- Database Management ---------------------
db = SQLAlchemy(app)

dbs = {} # initialize a list of databases, each item of format: (name, database)

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
    
@app.route("/users")
def get_users():
   print " ".join([str(x) for x in User.query.all()])
   return str([x.email for x in User.query.all()])

@app.route("/admin")
def get_admin_email():
   admin = User.query.filter_by(username='admin').first()
   return "<b>Admin Email</b>: %s" % admin.email

#--------------------- Main Program ---------------------
if __name__ == "__main__":
    app.run()
