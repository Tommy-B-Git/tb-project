from flask import Flask, redirect, url_for, abort, request, render_template, json, g, session, flash
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("base.html")

@app.route("/basic")
def basic():
  return render_template("signUp.html")

@app.route('/adduser',methods = ['POST', 'GET'])
def adduser():
  if request.method == 'POST':
    try:
      email = request.form['user_email']
      password = request.form['user_password']

      with sql.connect('myData.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO users (email,password) VALUES (?,?)",(email,password) )
        con.commit()
        msg = "Record successfully added"
    except:
      con.rollback()
      msg = "error in insert operation"
    finally:
      return redirect(url_for('create_profile'))
      con.close()
  else:
    return render_template("signUp.html")

@app.route("/premium")
def premium():
  return "This will be the Premium signup page"

@app.route("/users/new")
def create_profile():
  return render_template('users.html')

#custom 404 Route
@app.errorhandler(404)
def page_not_found(error):
  return render_template('404.html'), 404

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)


