from flask import Flask, redirect, url_for, abort, request, render_template, json, g, session, flash
import sqlite3

app = Flask(__name__)
db_location = 'var/database.db'

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


