import bcrypt
from functools import wraps
from flask import Flask, redirect, url_for, abort, request, render_template, json, g, session, flash
from werkzeug.utils import secure_filename
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
########################
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

# INDIVIDUAL PROFILE PAGE#
##########################
@app.route("/members/<email>")
@requires_login
def my_profile(email):
  conn = sqlite3.connect('var/database.db')
  with conn:
    cur = conn.cursor()
    cur.execute('SELECT * FROM profiles WHERE email = (?)', (email,))
    rows = cur.fetchall()
  return render_template('myProfile.html', rows=rows)

# USER LOGIN #
##############
@app.route("/login", methods=['GET', 'POST'])
def login():
  error=None
  success=None
  if request.method == 'POST':
    email = request.form['user_email']
    password = request.form['user_password']
    if validate(email, password) or validate_prem(email, password):
      session['logged_in'] = True
      flash('You have succesfully logged in')
      return redirect(url_for('my_profile', email=email))
    else:
      error = "Wrong details, try again!"
  return render_template("login.html")


@app.route("/basic")
def basic():
  return render_template("signUp.html")


# signUp.html brings you here
@app.route('/adduser',methods = ['POST', 'GET'])
def adduser():
  if request.method == 'POST':
    username = request.form['username']
    email = request.form['user_email']
    password = request.form['user_password']
    # Try to hash and salt password
    #valid_pwhash = bcrypt.hashpw(password, bcrypt.gensalt())

    db = get_db()
    db.cursor().execute("INSERT INTO users (email,password,username) VALUES(?,?,?)", (email,password,username) )
    db.commit()
    return redirect(url_for('login',username=username))
  else:
    return render_template("signUp.html")


# CREATE PROFILE ROUTE
@app.route("/profile/create",methods = ['GET', 'POST'])
def create_profile():
  error = None
  msg = None
  if request.method == 'POST':
    email = request.form['email']
    username = request.form['username']
    location = request.form['location']
    bio = request.form['bio']
    gender = request.form['gender']
    
    ## HANDLE IMAGES ##
    f = request.files['datafile']
    new_file = f.filename
    if new_file == "":
      # Make page for line below if time!!
      return "Please select a file to upload"
    else:
      f.save('static/img/' + new_file)

    db = get_db()
    db.cursor().execute("INSERT INTO profiles(email,username,location,bio,gender,prof_img) VALUES (?,?,?,?,?,?)",(email,username,location,bio,gender,new_file))
    db.commit()
    flash("Profile Created!")
    return redirect(url_for('my_profile', email=email))
  else:
    return render_template('newProfile.html')

# UPDATE PROFILE ROUTE #
@app.route("/profile/update", methods = ['GET', 'POST'])
def update_profile():
  error = None
  msg = None
  if request.method == 'POST':
    email = request.form['email']
    username = request.form['username']
    location = request.form['location']
    bio = request.form['bio']
    gender = request.form['gender']

    f = request.files['datafile']
    new_file = f.filename
    if new_file == "":
      # Make page for line below if time!!
      return "Please select a file to upload"
    else:
      f.save('static/img/' + new_file)

    db = get_db()
    db.cursor().execute("UPDATE profiles SET email=?, username=?,location=?,bio=?, gender=?, prof_img=? WHERE email= ?" ,(email,username,location,bio,gender,new_file,email))
    #cur.execute("UPDATE profiles SET email=?,username=?,location=?,bio=?,gender=?,prof_img=? WHERE email=?",(email,username,location,bio,gender,prof_img))
    db.commit()
    flash("Your profile is updated")
    return redirect(url_for('my_profile', email=email))
  else:
    return render_template('update.html')

# DELETE PROFILE #
@app.route("/profile/delete")
@requires_login
def delete_profile():
  return render_template('deleteProfile.html')

@app.route("/delete", methods = ['POST'])
def delete():
  conn = sqlite3.connect('var/database.db')
  with conn:
    cur = conn.cursor()
    cur.execute('DELETE * FROM profiles WHERE email = (?)', (email,))
    flash('Your profile is deleted')
  return render_template('index.html')


@app.route("/members/view")
def view_members():
 # conn = sqlite3.connect('var/database.db')
 # with conn:
  #  cur = conn.cursor()
  #  cur.execute('SELECT * FROM profiles')
  #  rows = cur.fetchall()
    #for row in rows:
      #dbEmail = row[0]
      #dbPass = row[1]
      #dbPass = row[1]
      #dbPass = row[1]
      #dbPass = row[1]
  return "This will be the View Members page"

@app.route("/premium")
def premium():
  return render_template("premium.html")


@app.route("/addpremium", methods = ['GET', 'POST'])
def add_premium():
  if request.method == 'POST':
    username = request.form['username']
    password =  request.form['password']
    email = request.form['email']
    cc_number = request.form['cc_number']
    sec_code = request.form['sec_code']

    db = get_db()
    db.cursor().execute("INSERT INTO premium (username,password,email,cc_number,sec_code) VALUES (?,?,?,?,?)",(username,password,email,cc_number,sec_code) )
    db.commit()
    return redirect(url_for('login'))
  else:
    return render_template("premium.html")

# Validate login                                                                                            
def validate_prem(email, password):
  conn = sqlite3.connect('var/database.db')
  with conn:
    cur = conn.cursor()
    cur.execute('SELECT * FROM premium WHERE email=(?)', (email,))
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

#custom 404 Route
@app.errorhandler(404)
def page_not_found():
  return render_template('404.html'), 404

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
