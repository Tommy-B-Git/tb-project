import bcrypt
from functools import wraps
from flask import Flask, redirect, url_for, abort, request, render_template, json, g, session, flash
import sqlite3

app = Flask(__name__)
db_location = 'var/database.db'

app.secret_key = 'A0Zr98j/3yXR~XHH!jmN]LWX/,?RT'
valid_pwhash = bcrypt.hashpw('secretpass', bcrypt.gensalt())

# Start of DB stuff
###################
def get_db():
  db = getattr(g, 'db', None)
  if db is None:
    db = sqlite3.connect(db_location)
    g.db = db
  return db

@app.teardown_appcontext
def close_db_connection(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

def init_db():
  with app.app_context():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()

# End of DB stuff
#################


# Validate login
def validate(email, password):
  conn = sqlite3.connect('var/database.db')
  valid_pwhash == bcrypt.hashpw(password.encode('utf-8'), valid_pwhash)
  with conn:
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    for row in rows:
      dbEmail = row[0]
      dbPass = row[1]
      #if  dbEmail == email and dbPass == password:
      if dbEmail == email and dbPass == password:
        return True
      else:
        return False 

def requires_login(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    status = session.get('logged_in', False)
    if not status:
      return redirect(url_for('login'))
    return f(*args, **kwargs)
  return decorated

@app.route("/logout/")
def logout():
  session['logged_in'] = False
  return redirect(url_for('login'))

@app.route("/members")
@requires_login
def members():
  return render_template('users.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
  error=None
  success=None
  if request.method == 'POST':
    email = request.form['user_email']
    password = request.form['user_password']
    if validate(email, password):
      session['logged_in'] = True
      success = 'You have succesfully logged in'
      return redirect(url_for('.members'))
    else:
      error = 'Wrong details. Try again'
  return render_template("login.html", error=error)

@app.route("/")
def index():
 return render_template("base.html")


@app.route("/basic")
def basic():
  return render_template("signUp.html")

@app.route('/adduser',methods = ['POST', 'GET'])
def adduser():
  if request.method == 'POST':
    email = request.form['user_email']
    password = request.form['user_password']
    
    db = get_db()
    db.cursor().execute("INSERT INTO users (email,password) VALUES (?,?)", (email,password) )
    db.commit()
    msg = "Account created, now create your profile"
    return render_template('users.html',msg=msg)
  else:
    return render_template("signUp.html")


@app.route("/premium")
def premium():
  return "This will be the Premium signup page"

@app.route("/users/new")
def create_profile():
  return render_template('newProfile.html')

#custom 404 Route
@app.errorhandler(404)
def page_not_found(error):
  return render_template('404.html'), 404

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)


