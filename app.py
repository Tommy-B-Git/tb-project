from flask import Flask, redirect, url_for, abort, request, render_template, json
from werkzeug.utils import secure_filename

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

#custom 404 Route
@app.errorhandler(404)
def page_not_found(error):
  return render_template('404.html'), 404

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)


