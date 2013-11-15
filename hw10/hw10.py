import os
from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from pybtex.database.input import bibtex
from string import punctuation, whitespace

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bib', 'aux'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.debug = True

def clear_uploads():
    """ Delete all files in uploads folder """
    for the_file in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], the_file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
#--------------------- Home Page ---------------------
@app.route("/") # Main page
@app.route("/index.html")
@app.route("/home")
def home():
    """ Home page """
    # Specify links:
    links_list = [(url_for("upload_file"), 'Insert a Collection'),
                  (url_for("query_database"), 'Run a Query')]
    collections_list = collections.keys()
    collections_list.sort()
    return render_template('base.html',
                           window_title='BibTex Viewer | Main Page',
                           page_title='Home Page',
                           links=links_list,
                           db_present=(len(collections) > 0),
                           content='These are your available collections:',
                           html_collections=collections_list)

#--------------------- File Uploading & Parsing ---------------------
duplicates = [False, False] # [collection_name_taken, file_name_taken]
collections = {} # initialize a list of collections, each item of format: (name, database)
info4db = [] # initialize a database

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_bibtex(filename):
    """ returns true if the file is a bibtex file """
    return filename.rsplit('.', 1)[1].lower() == '.bib'

def parse_bibtex(bib_file, col_name):
    """ Parses a .bib file """
    parser = bibtex.Parser()
    bib_data = parser.parse_file(bib_file)
    def author2str(author):
        """ formats a Pybtex Person object into a string represntation """
        return author.last()[0].strip('{}') + ", " + " ".join(author.bibtex_first())
    gunk = punctuation + whitespace
    for tag, entry in bib_data.entries.items():
        try: # authors
            author_list = " and ".join([author2str(x) for x in entry.persons['author']])
        except:
            author_list = "Not Available"
        try: # journal
            journal = entry.fields['journal'].strip(gunk)
        except:
            journal = "Not Available"
        try: # volume
            vol = int(entry.fields['volume'].strip(gunk))
        except:
            vol = -1
        try: # pages
            pages = entry.fields['pages'].strip(gunk)
        except:
            pages = "Not Available"
        try: # year
            year = int(entry.fields['year'].strip(gunk))
        except:
            year = -1
        try: # title
            title = entry.fields['title'].strip(gunk)
        except:
            title = "Not Available"

        info4db.append( (tag, author_list, journal, vol, pages, year, title, col_name) )

def process_file(filename, col_name, the_file):
    """ Verify entries, parse the file, and create / add to a database from it """
    if len(col_name.strip(' ')) == 0: # if no name provided for collection, use file name
        col_name = ''.join(secure_filename(the_file.filename).split('.')[:-1])
    if col_name in collections.keys(): # if collection name already taken
        duplicates[0] = True
        duplicates[1] = False
        return redirect(url_for('upload_file'))
    if filename in os.listdir(app.config['UPLOAD_FOLDER']): # if filename name already taken
                duplicates[1] = True
                duplicates[0] = False
                return redirect(url_for('upload_file'))
    duplicates[0] = False
    duplicates[1] = False
    collections[col_name] = the_file # add to dictionary of databases
    the_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # Parse the file if bibtex
    if is_bibtex(the_file.filename):
        parse_bibtex(the_file, col_name)
    """
    ref_tag, author_list TEXT, journal TEXT, volume INT, pages INT, year DATE, title TEXT, collection TEXT
    """
    return redirect(url_for('home'))    

@app.route('/insert_collection', methods=['GET', 'POST'])
def upload_file():
    """ Function for inserting a collection """
    links_list = [(url_for("home"), 'Back to Home Page')]
    if request.method == 'POST':
        bib_file = request.files['col_file']
        bib_name = request.form['col_name']
        if bib_file and allowed_file(bib_file.filename):
            filename = secure_filename(bib_file.filename)
            return process_file(filename, bib_name, bib_file)  
    else:
        return render_template('upload_file.html',
                               links=links_list,
                               db_present=(len(collections) > 0),
                               dupes=duplicates)

#--------------------- Querying---------------------
@app.route("/query", methods=['GET', 'POST'])
def query_database():
    """ Query the databse """
    links_list = [(url_for("home"), 'Back to Home Page')]
    if request.method == 'POST':
        query_raw = request.form['query_str']
        query = "processed--" + str(query_raw) + "--processed"
        return render_template('query.html',
                               links=links_list,
                               db_present=(len(collections) > 0),
                               query_preset=query_raw,
                               query_str = query,
                               db_info = str(info4db) )
    else:
        return render_template('query.html',
                               links=links_list,
                               db_present=(len(collections) > 0))
                               

#--------------------- Previous Funcs ---------------------
db = SQLAlchemy(app)

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
    clear_uploads()
    app.run()
