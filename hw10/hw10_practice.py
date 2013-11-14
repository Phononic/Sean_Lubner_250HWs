from flask import Flask, redirect, request, url_for

app = Flask(__name__)
app.debug = True

login_form = """
<title> Login Page </title>
<form name="login_info" method="post" action="use_form">
login: <input type="text" name="login_name"> <br>
Password: <input type="password" name="pw"> <br>
<input type="submit" value="Login">
</form>
"""

## we can tell our view functions what HTTP methods it
## is allowed to respond to
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return "performing the log in"
    else:
    	## this is a normal GET request
        return login_form

@app.route('/use_form', methods=['POST'])
def do_stuff():
    response = """
    form used method: {0:s}
    <br> form has variables and structures: {1:s}
    """.format(request.method, request.form.items())
    return response

@app.route("/")
@app.route("/index.html")
@app.route("/home.html")
def home_page():
	## 301 is an HTTP error code
	return redirect("/login",301)

#app.run()
if __name__ == "__main__":
    app.run()
