import bcrypt
from functools import wraps
from flask import Flask, redirect, url_for, abort, request, render_template, json, g, session, flash
import sqlite3

#Application Object
app = Flask(__name__)
db_location = 'var/database.db'

app.secret_key = 'a_really_secret_key'


@app.route("/")
def index():
 return render_template("base.html")


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
  with conn:
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE email=(?)', (email,))
    rows = cur.fetchall()
    for row in rows:
      dbEmail = row[0]
      dbPass = row[1]
      #print(dbEmail, email, dbPass, password)
      if  dbEmail == email and dbPass == password:
      # CHECK HASHED PW 
      #if (email == dbEmail and password == bcrypt.hashpw(password.encode('utf-8'), password)):
        return True
      else:
        return False

# REQUIRES LOGIN STUFF #
#######################
def requires_login(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      flash('You need to login')
      return redirect(url_for('login'))
  return decorated

@app.route("/logout")
@requires_login
def logout():
  session['logged_in'] = False
  flash("You were logged out")
  return redirect(url_for('index'))

@app.route("/members")
@requires_login
def members():
  if session['logged_in']:
    #return "link from here to create profile Page"
    return render_template("members.html")
  else:
    return redirect(url_for('index'))

# MEMBER PROFILE PAGE#
######################
@app.route("/members/profile")
@requires_login
def my_profile():
  conn = sqlite3.connect('var/database.db')
  with conn:
    cur = conn.cursor()
    cur.execute('SELECT * FROM profiles')
    rows = cur.fetchall()
    for row in rows:
      username = row[0]
      location = row[1]
      bio = row[2]
      gender = row[3]
      prof_img = row[4]
  return "Individual profile pagge here"

# USER LOGIN #
##############
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
      return redirect(url_for('members'))
    else:
      error = "Wrong details, try again!"
  return render_template("login.html", error=error)


@app.route("/basic")
def basic():
  return render_template("signUp.html")


# signUp.html brings you here
@app.route('/adduser',methods = ['POST', 'GET'])
def adduser():
  if request.method == 'POST':
    email = request.form['user_email']
    password = request.form['user_password']
    # Try to hash and salt password
    #valid_pwhash = bcrypt.hashpw(password, bcrypt.gensalt())

    db = get_db()
    db.cursor().execute("INSERT INTO users (email,password) VALUES (?,?)", (email,password) )
    db.commit()
    msg = "Account created, now create your profile"
    return redirect(url_for('login'))
  else:
    return render_template("signUp.html")

# CREATE PROFILE PAGE
@app.route("/user/new",methods = ['GET', 'POST'])
def create_profile():
  if request.method == 'POST':
    username = request.form['username']
    location = request.form['location']
    bio = request.form['bio']
    gender = request.form['gender']
    prof_img = request.form['prof_img']

    db = get_db()
    db.cursor().execute("INSERT INTO profiles (username,location,bio,gender,prof_img) VALUES (?,?,?,?,?)",(username,location,bio,gender,prof_img))
    db.commit()
    msg = "Profile Created!"
    return redirect(url_for('view_members'))
  else:
    return render_template('newProfile.html')


@app.route("/members/view")
def view_members():
  conn = sqlite3.connect('var/database.db')
  with conn:
    cur = conn.cursor()
    cur.execute('SELECT * FROM profiles')
    rows = cur.fetchall()
    #for row in rows:
      #dbEmail = row[0]
      #dbPass = row[1]
      #dbPass = row[1]
      #dbPass = row[1]
      #dbPass = row[1]
  return "This will be the View Members page"

@app.route("/premium")
def premium():
  return "This will be the Premium signup page"


#custom 404 Route
@app.errorhandler(404)
def page_not_found(error):
  return render_template('404.html'), 404

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
