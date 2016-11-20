from flask import Flask, redirect, url_for, abort, request, render_template, json, g
import sqlite3 

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("base.html")

@app.route("/basic")
def basic():
  return render_template("signUp.html")

@app.route("/premium")
def premium():
  return "This will be the Premium signup page"

@app.route("/adduser", methods=['GET', 'POST'])
def adduser():
  if request.method == 'POST':
    try:
      email = request.form['user_email']
      password = request.form['user_password']
         
      with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO users (user_email,user_password) VALUES (?,?)",(email,password))
        con.commit()
        msg = "Record successfully added"
    except:
      con.rollback()
      msg = "error in insert operation"
      
    finally:
      return render_template("createSee.html",msg = msg)
      con.close()

@app.route("/users/new")
def create_profile():
  return "This is the create profile page"

#custom 404 Route
@app.errorhandler(404)
def page_not_found(error):
  return render_template('404.html'), 404

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)


