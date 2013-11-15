import os
import sqlite3
from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from pybtex.database.input import bibtex
from string import punctuation, whitespace

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/bib.db'
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
collections = {} # initialize a list of collections, each item of format: (name, file)
db = SQLAlchemy(app) # initialize a database
eng = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True) # for running queries
info4db = [] # initialize a bucket for the parsed data to be inserted into the database

class Article(db.Model):
    """ Article database object, for inserting data """
    __tablename__ = 'article' #@@@@@@ TAG @@@@@@
    id = db.Column(db.Integer, primary_key=True)
    citation_tag = db.Column(db.String(100), unique=True)
    author_list = db.Column(db.String(500), unique=True)
    journal=db.Column(db.String(100),unique=True)
    volume=db.Column(db.Integer,unique=True)
    pages=db.Column(db.String(50),unique=True)
    year=db.Column(db.Integer,unique=True)
    title=db.Column(db.String(200),unique=True)
    collection=db.Column(db.String(50),unique=True)
    def __init__(self, citation_tag,author_list,journal,volume,pages,year,title,collection):
        self.citation_tag=citation_tag
        self.author_list=author_list
        self.journal=journal
        self.volume=volume
        self.pages=pages
        self.year=year
        self.title=title
        self.collection=collection
db.create_all() # create database objects

def add_entries(bib_data,database="/tmp/bib.db"):
    """ Adds the entries in "bib_data" to the database located at path "database" """
    for item in bib_data:
        db.session.add(Article(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7]))
        try:
            db.session.commit()
        except:
            pass

def allowed_file(filename):
    """ Sanitizes filename entry """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_bibtex(filename):
    """ returns True if the file is a bibtex file """
    return filename.rsplit('.', 1)[1].lower() == 'bib'

def parse_bibtex(bib_file_path_local, col_name):
    """ Parses a .bib file """
    parser = bibtex.Parser()
    bib_data = parser.parse_file(bib_file_path_local)
    def author2str(author):
        """ formats a Pybtex Person object into a string represntation """
        return author.last()[0].strip('{}') + ", " + " ".join(author.bibtex_first())
    gunk = punctuation + whitespace
    for tag, entry in bib_data.entries.items():
        try: # authors
           author_list = str(" and ".join([author2str(x) for x in entry.persons['author']]))
        except:
            author_list = "Not Available"
        try: # journal
            journal = str(entry.fields['journal'].strip(gunk))
        except:
            journal = "Not Available"
        try: # volume
            vol = str(entry.fields['volume'].strip(gunk))
        except:
            vol = "Not Available"
        try: # pages
            pages = str(entry.fields['pages'].strip(gunk))
        except:
            pages = "Not Available"
        try: # year
            year = str(entry.fields['year'].strip(gunk))
        except:
            year = "Not Available"
        try: # title
            title = str(entry.fields['title'].strip(gunk))
        except:
            title = "Not Available"
        info4db.append( (str(tag), author_list, journal, vol, pages, year, title, col_name) )
    add_entries(info4db)

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
        parse_bibtex(os.path.join(app.config['UPLOAD_FOLDER'], filename), col_name)
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
def run_query(query, database="/tmp/bib.db"):
    connection = eng.connect()
    sql_cmd="SELECT * FROM article WHERE " + query
    results = connection.execute(sql_cmd)
    for entry in db_info:
        results.append(entry)
    return results

@app.route("/query", methods=['GET', 'POST'])
def query_database():
    """ Query the databse html page manager """
    links_list = [(url_for("home"), 'Back to Home Page')]
    if request.method == 'POST':
        query_raw = request.form['query_str']
        query_results = info4db #run_query(query_raw)  #@@@@@@ TAG @@@@@@
        return render_template('query.html',
                               links=links_list,
                               db_present=(len(collections) > 0),
                               query_preset=query_raw,
                               query_str = query_raw,
                               results = info4db)
    else:
        return render_template('query.html',
                               links=links_list,
                               db_present=(len(collections) > 0))
                               
#--------------------- Main Program ---------------------
if __name__ == "__main__":
    clear_uploads() # Empty out the uploads folder from the previous session
    if os.path.isfile("/tmp/bib.db"):
        os.unlink("/tmp/bib.db") # release previous session's database

    app.run()
